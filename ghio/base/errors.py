from __future__ import print_function, unicode_literals

__author__ = "danishabdullah"


class APIError(Exception):

    def __init__(self, msg: str, url: str, headers: dict, params: dict, http_code: int, error_type: str, *args):
        if not msg:
            msg = "{} - {}".format(http_code, error_type)
        self.url = url
        self.params = params
        self.http_code = http_code
        self.error_type = error_type
        self.headers = headers
        super(APIError, self).__init__(msg, *args)


class ValidationError(APIError):

    def __init__(self, url: str, headers: dict, params: dict, http_code: int, failures: dict, *args):
        self.failures = failures
        msg = "{} - Validation error:\n{}".format(http_code, failures)
        super(ValidationError, self).__init__(msg, url, headers, params, http_code, "Validation error", *args)

