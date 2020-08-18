# -*- coding: utf-8 -*-
# author: itimor

import requests
import json

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class FalconClient(object):
    def __init__(self, endpoint=None, user=None, token=None, keys=[], session=None, ssl_verify=True):
        self._endpoint = endpoint
        self._job_prex = 'job/'
        self._url_suffix = 'api/json'
        self._keys = keys
        self._session = session
        self.ssl_verify = ssl_verify

        if not session:
            params = {
                "name": user,
                "password": token
            }
            self._session = requests.Session()
            ret = self.do_request('get', '/', params=params)
            print(ret)
            api_token = {
                "name": user,
                "sig": ret.get("sig")
            }
            self._session.auth = (user, token)
            self._session.headers.update({
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
                'Apitoken': json.dumps(api_token)
            })

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]

        return self.__class__(
            endpoint=self._endpoint,
            keys=self._keys + [key],
            session=self._session,
            ssl_verify=self.ssl_verify)

    def __getitem__(self, key):
        """Look up an option value and perform string substitution."""
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        method = self._keys[-1]
        url = "/".join(self._keys[0:-1])
        url = url.replace("_", "-")
        return self.do_request(method, url, **kwargs)

    def do_request(self, method, url, params=None, data=None):
        url = self._endpoint + url + self._url_suffix
        if data:
            print(data)

        if params is None:
            params = {}

        if method == 'get' or method == 'list':
            response = self._session.get(url, params=params, verify=self.ssl_verify)

        if method == 'post' or method == 'create':
            response = self._session.post(url, params=params, json=data, verify=self.ssl_verify)

        if method == 'put' or method == 'update':
            response = self._session.put(url, json=data, verify=self.ssl_verify)

        if method == 'delete':
            response = self._session.delete(url, params=params, json=data, verify=self.ssl_verify)

        try:
            body = json.loads(response.text)
        except ValueError:
            body = "Get unknow error is [%s]" % response.reason

        return body


if __name__ == '__main__':
    cli = FalconClient(endpoint="http://n9e.xxoo.com", user='admin', token='11871bd159bd19da9ab624d161c569e3c8')
    params = {"idents": ["192.168.0.112"]}
    r = cli.node['2'].endpoint_unbind.post(data=params)
    print(r)
