from __future__ import print_function, unicode_literals
from base64 import b64encode

__author__ = "danishabdullah"

from requests import Session

from .errors import ValidationError, APIError
from .logger import LOG


class GreenHouseClient(object):

    def __init__(self, api_key: str, per_page=500):
        session = Session()
        session.headers.update({"Authorization": "Basic {}:".format(b64encode(api_key.encode('utf-8')).decode('utf-8'))})
        self._base_url = "https://harvest.greenhouse.io/v1/"
        self._per_page = per_page
        self._session = session
        LOG.info("GreenHouseClient initialized")

    def _request(self, method: str, url: str, params=None, load_all=False):
        assert method in ("GET", "POST", "PUT", "DELETE")
        if not url.startswith('http'):
            url = self._base_url + url
        if not params:
            params = {"per_page": self._per_page}
        if params.get('per_page', None):
            params['per_page'] = self._per_page
        LOG.info("{}: {} with PARAMS={}".format(method, url, params))
        response = self._session.request(method, url, data=params)
        url = response.url
        status_code = response.status_code
        headers = response.request.headers
        if status_code == 200:
            LOG.info("SUCCESS: {}ing to {} with PARAMS={} returned successfully".format(method, url, params))
            data = response.json()
            if response.links.get('next', None) and load_all:
                data.extend(self._request('GET', response.links['next']['url'], load_all=load_all))
            return data
        elif status_code == 422:
            LOG.error("HTTP ERROR {}: {}ing to {} with PARAMS={} returned in a Validation Error".format(status_code,
                                                                                                        method, url,
                                                                                                        params))
            raise ValidationError(url, headers, params, status_code, response.json()['errors'])
        elif status_code == 401:
            msg = "Unauthorized – Invalid Harvest API key. Check to make sure you’re passing it in via the " \
                  "Authorization header (Basic Auth)"
            LOG.error("HTTP ERROR {}: {}ing to {} with PARAMS={} returned in an Authorisation Error".format(
                status_code, method, url, params))
            raise APIError(msg, url, headers, params, status_code, "Authorisation error")
        elif status_code == 403:
            msg = "Forbidden – You do not have access to that record"
            LOG.error("HTTP ERROR {}: Access denied for {}ing to {} with PARAMS={}".format(status_code, method, url,
                                                                                           params))
            raise APIError(msg, url, headers, params, status_code, "Access Denied Error")
        elif status_code == 404:
            msg = "Not Found – Resource not found"
            LOG.error("HTTP ERROR {}: {}ing to {} with PARAMS={} returned in a Not Found Error".format(status_code,
                                                                                                       method,
                                                                                                       url,
                                                                                                       params))
            raise APIError(msg, url, headers, params, status_code, "Not found error")
        elif status_code == 500:
            msg = "Server Error – We had a problem with our server. Try again later or contact: support@greenhouse.io"
            LOG.ERROR("HTTP ERROR {}: {}ing to {} with PARAMS={} returned in a Server Error".format(status_code, method,
                                                                                                    url, params))
            raise APIError(msg, url, headers, params, status_code, "Server error")
        else:
            LOG.error("HTTP ERROR {}: {}ing to {} with PARAMS={} returned in an Unhandled Error".format(status_code,
                                                                                                        method,
                                                                                                        url,
                                                                                                        params))
            raise APIError('', url, headers, params, status_code, "Unhandled state")

    def _get(self, url: str, params=None, load_all=False):
        return self._request("GET", url, params=params, load_all=load_all)

    def _post(self, url: str, params=None, load_all=False):
        return self._request("POST", url, params=params, load_all=load_all)

    def _put(self, url: str, params=None, load_all=False):
        return self._request("PUT", url, params=params, load_all=load_all)

    def _delete(self, url: str, params=None, load_all=False):
        return self._request("DELETE", url, params=params, load_all=load_all)