"""
Wrapper for trongrid's response JSON data.
"""
import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Union

import requests
from requests_toolbelt.utils import dump
from rich.pretty import pprint
from tenacity import after_log, retry, stop_after_attempt, wait_exponential

from trongrid_extractor.config import log
from trongrid_extractor.request_params import RequestParams
from trongrid_extractor.helpers.csv_helper import *
from trongrid_extractor.helpers.string_constants import *
from trongrid_extractor.helpers.time_helpers import *

# If the distance between min and max_timestamp is less than this don't consider a 0 row
# result a failure.
OK_DURATION_FOR_ZERO_TXNS_MS = 10000
JSON_HEADERS = {'Accept': 'application/json'}


@dataclass
class Response:
    raw_response: requests.models.Response
    params: Dict[str, Any]

    def __post_init__(self):
        log.debug(dump.dump_all(self.raw_response).decode('utf-8'))
        self.response = self.raw_response.json()

    @classmethod
    @retry(wait=wait_exponential(multiplier=1, min=15, max=300), stop=stop_after_attempt(5), after=after_log(log, logging.DEBUG))
    def get_response(cls, url: str, params: Optional[Dict[str, Union[str, int, float]]] = None) -> 'Response':
        """Alternate constructor that calls the API with retries."""
        params = params or {}

        # If an API call yields too many rows to fit in one response a 'next URL' is given and
        # our requests use that URL without params.
        is_new_query = MIN_TIMESTAMP in params and MAX_TIMESTAMP in params

        # Min/Max timestamps are INCLUSIVE.
        if is_new_query:
            msg = f"New query requesting data from {ms_to_datetime(params[MIN_TIMESTAMP])} to {ms_to_datetime(params[MAX_TIMESTAMP])}."
            log.info(msg)

        log.debug(f"Request URL: {url}\nParams: {params}")
        raw_response = requests.get(url, headers=JSON_HEADERS, params=params)
        response = cls(raw_response, deepcopy(params))

        # Sometimes TronGrid will return 0 rows for no apparent reason. Retrying usually fixes it
        # so we throw an exception to get a tenacity retry.
        if response.is_false_complete_response():
            log.info("Empty response that perhaps should not be empty...")

            if is_new_query:
                duration_queried_ms = params[MAX_TIMESTAMP] - params[MIN_TIMESTAMP]
                log.info(f"{duration_queried_ms}ms duration from min to max_timestamp in query")

                if duration_queried_ms <= OK_DURATION_FOR_ZERO_TXNS_MS:
                    log.warning(f"Looks like a bad false empty response but only {duration_queried_ms}ms in range so OK.")
                    return response

            msg = f"Seems like an actual error - this should probably not be empty. Response:\n{response.response}"
            log.error(msg)
            response.pretty_print()
            raise ValueError(msg)

        return response

    def is_continuable_response(self) -> bool:
        return self.next_url() is not None

    def is_paging_complete(self) -> bool:
        page_size = self.page_size() or 0
        return self.was_successful() and page_size > 0 and self.next_url() is None

    def is_false_complete_response(self) -> bool:
        """Sometimes for no reason TronGrid just returns 0 rows to a query that would otherwise return rows."""
        return self.was_successful() and self.page_size() == 0 and DATA and self.next_url() is None

    def was_successful(self) -> bool:
        if SUCCESS not in self.response:
            log.warning(f"No '{SUCCESS}' key found in response!\n{self.response}")
            return False

        success = self.response[SUCCESS]

        if not isinstance(success, bool):
            raise ValueError(f"{success} is of type {type(success)} instead of bool!")

        return success

    def next_url(self) -> Optional[str]:
        if META in self.response and LINKS in self.response[META] and NEXT in self.response[META][LINKS]:
            return self.response[META][LINKS][NEXT]

    def page_size(self) -> Optional[int]:
        if META in self.response and PAGE_SIZE in self.response[META]:
            return self.response[META][PAGE_SIZE]

    def without_data(self) -> Dict[str, Any]:
        """Return the response JSON just without the 'data' field."""
        abbreviated_response = deepcopy(self.response)
        abbreviated_response['data'] = f"[Skipping {len(self.response['data'])} elements of 'data' array]"
        return abbreviated_response

    def pretty_print(self) -> None:
        log.info(f"RAW RESPONSE:")
        log.info(dump.dump_all(self.raw_response).decode('utf-8') + "\n")
        log.info(f"Response formatted with Rich:")
        pprint(self, expand_all=True)
        pprint(self.response, expand_all=True)

    def print_abbreviated(self) -> None:
        pprint(self.without_data(), expand_all=True)
