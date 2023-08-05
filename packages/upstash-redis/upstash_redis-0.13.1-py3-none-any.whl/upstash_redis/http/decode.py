from upstash_redis.schema.http import RESTResult
from upstash_redis.utils.base import base64_to_string
from upstash_redis.exception import UpstashException
from typing import List


def decode(raw: RESTResult, encoding: str) -> RESTResult:
    """
    Decode the response received from the REST API.
    """

    if encoding == "base64":
        if isinstance(raw, str):
            return "OK" if raw == "OK" else base64_to_string(raw)

        elif isinstance(raw, int) or raw is None:
            return raw

        elif isinstance(raw, List):
            return [
                # Decode recursively.
                decode(element, encoding)
                for element in raw
            ]
        else:
            raise UpstashException(
                f"Error decoding data for result type {str(type(raw))}"
            )
