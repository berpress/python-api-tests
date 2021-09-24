import json
import logging
import pprint
from functools import wraps
from json import JSONDecodeError

logger = logging.getLogger("api")


def logging(message):
    """
    Request Logging
    :return: response
    """

    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            logger.info(message)
            res = function(*args, **kwargs)
            method = res.request.method
            url = res.request.url
            body = res.request.body
            status = res.status_code
            body_sep = " "
            log_request = f"Request method: {method}, url: {url}"
            if body is not None:
                try:
                    json_body = json.dumps(
                        json.loads(body.decode("utf-8")), indent=4, ensure_ascii=False
                    )
                    if len(body) > 20:
                        body_sep = "\n"
                    log_request += (
                        f", body:{body_sep}{json_body or pprint.pformat(body)}"
                    )
                except AttributeError:
                    log_request += f", body:{body}"
            logger.info(log_request)

            log_response = f"Response method: {method}, url: {url}, status: {status}"
            try:
                body = res.json()
                if len(res.content) > 20:
                    body_sep = "\n"
                    bd = json.dumps(body, indent=4, ensure_ascii=False)
                    log_response += f", body:{body_sep}{bd}"
                else:
                    log_response += f", body:{json.dumps(body)}"
                logger.info(log_response)
            except JSONDecodeError:
                if len(res.text) > 120:
                    log_response += f", body: {res.text[:120]}..."
                else:
                    log_response += f", body: {res.text}"
                logger.info(log_response)
            return res

        return inner

    return wrapper
