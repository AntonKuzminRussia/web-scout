# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class for common HTTP work
"""

import re
import os
import requests
from classes.Registry import Registry
from classes.kernel.WSException import WSException
from classes.HttpResponseImitation import HttpResponseImitation


class HttpMaxSizeException(BaseException):
    """ Exception class for max-size error """
    pass


class Http(object):
    """ Class for common HTTP work """
    verify = False
    allow_redirects = False
    headers = None
    config = None
    noscan_content_types = []
    scan_content_types = []
    # Common for all class copies dict with errors
    errors = {'maxsize': [], 'noscan_content_types': [], 'scan_content_types': []}
    current_proxy = None
    current_proxy_counter = None
    every_request_new_session = False
    requests_per_session = None
    requests_counter = None

    def __init__(self, verify=False, allow_redirects=False, headers=None):
        self.verify = verify
        self.allow_redirects = allow_redirects
        self.headers = {} if headers is None else headers
        self.session = requests.Session()
        self.session.trust_env = False

        self.requests_counter = 0
        self.requests_per_session = 50
        self.current_proxy_counter = 0

    def up_requests_counter(self):
        self.requests_counter += 1

        # every_request_new_session checks in get()/post()/head(), here we don`t need it,
        # only actions relates with counter
        if not self.every_request_new_session and \
                self.requests_per_session and \
                self.requests_counter >= self.requests_per_session:
            self.requests_counter = 0
            self.session = requests.Session()
            self.change_proxy()

    def load_headers_from_file(self, _file):
        if not os.path.exists(_file):
            raise WSException("File '{0}' not exists".format(_file))

        header_regex = re.compile('([a-zA-Z0-9\-]*): (.*)')
        fh = open(_file, 'r')
        for line in fh:
            try:
                if len(line.strip()):
                    parsed_header = header_regex.findall(line)[0]
                    self.headers[parsed_header[0]] = parsed_header[1]
            except BaseException:
                raise WSException("Wrong header line '{0}'".format(line.strip()))
        fh.close()

    def set_allowed_types(self, types):
        """ Set allowed contnent types """
        self.scan_content_types = types

    def set_denied_types(self, types):
        """ Set denied contnent types """
        self.noscan_content_types = types

    def change_proxy(self):
        self.current_proxy = Registry().get('proxies').get_proxy()

    def get_current_proxy(self):
        """ Check current proxy, get next if need (max requests per proxy made) """
        if Registry().isset('tor'):
            proxy_str = Registry().get('config')['tor']['ip'] + ":" + Registry().get('config')['tor']['port']
            return {
                "http": "socks5h://" + proxy_str,
                "https": "socks5h://" + proxy_str,
            }

        if self.current_proxy_counter >= int(Registry().get('config')['main']['requests_per_proxy']):
            self.current_proxy = None
            self.current_proxy_counter = 0

        if not self.current_proxy:
            self.change_proxy()

        self.current_proxy_counter += 1

        return {
            "http": "http://" + self.current_proxy,
            "https": "http://" + self.current_proxy,
        } if self.current_proxy else None

    def is_response_length_less_than_limit(self, url, resp):
        """ Checking response length by Content-Length header """
        if 'content-length' in resp.headers and \
                        int(resp.headers['content-length']) > int(Registry().get('config')['main']['max_size']):
            self.errors['maxsize'].append(
                "URL {0} has size {1} bytes, but limit in config - {2} bytes".
                format(
                    url,
                    resp.headers['content-length'],
                    Registry().get('config')['main']['max_size']
                )
            )
            return False
        return True

    def get(self, url, verify=None, allow_redirects=None, headers=None, cookies=None, auth=None):
        """ HTTP GET request """
        self.up_requests_counter()

        if self.every_request_new_session:
            self.session = requests.Session()
            self.change_proxy()
        verify = self.verify if verify is None else verify
        allow_redirects = self.allow_redirects if allow_redirects is None else allow_redirects
        headers = self.headers if headers is None else headers

        if 'user-agent' not in map(str.lower, headers.keys()):
            headers['User-Agent'] = Registry().get('ua')

        timeout = int(Registry().get('config')['main']['http_timeout']) if \
            not Registry().isset('tor') else \
            int(Registry().get('config')['tor']['http_timeout'])

        resp = self.session.get(
            url,
            verify=verify,
            allow_redirects=allow_redirects,
            headers=headers,
            stream=True,
            proxies=self.get_current_proxy(),
            timeout=timeout,
            cookies=cookies,
            auth=auth
        )

        if not self.is_response_length_less_than_limit(url, resp):
            resp.close()
            resp = HttpResponseImitation(resp.status_code, resp.headers, "too big for download, see docs or increase config.ini->max_size")

        if resp and 'content-type' in resp.headers and (len(self.scan_content_types) or len(self.noscan_content_types)):
            if len(self.noscan_content_types):
                for _type in self.noscan_content_types:
                    if resp.headers['content-type'].lower().count(_type.lower()):
                        self.errors['noscan_content_types'].append(
                            "URL {0} have denied content type  - {1}".format(url, _type)
                        )
                        resp.close()
                        resp = None
                        break
            if resp and len(self.scan_content_types):
                allowed = False
                for _type in self.scan_content_types:
                    if resp.headers['content-type'].lower().count(_type.lower()):
                        allowed = True
                        break
                if not allowed:
                    self.errors['scan_content_types'].append(
                        "URL {0} have not allowed content type  - {1}".format(url, resp.headers['content-type'])
                    )
                    resp.close()
                    resp = None

        return resp

    def post(self, url, data=None, verify=None, allow_redirects=None, headers=None, cookies=None, files=None):
        """ HTTP POST request """
        self.up_requests_counter()

        if self.every_request_new_session:
            self.session = requests.Session()
        verify = self.verify if verify is None else verify
        allow_redirects = self.allow_redirects if allow_redirects is None else allow_redirects
        headers = self.headers if headers is None else headers

        if 'user-agent' not in map(str.lower, headers.keys()):
            headers['User-Agent'] = Registry().get('ua')
        if files is None and 'Content-Type' not in headers.keys():
            headers['Content-Type'] = "application/x-www-form-urlencoded"

        timeout = int(Registry().get('config')['main']['http_timeout']) if \
            not Registry().isset('tor') else \
            int(Registry().get('config')['tor']['http_timeout'])
        resp = self.session.post(
            url,
            data=data,
            verify=verify,
            allow_redirects=allow_redirects,
            headers=headers,
            stream=True,
            proxies=self.get_current_proxy(),
            timeout=timeout,
            cookies=cookies,
            files=files
        )
        if not self.is_response_length_less_than_limit(url, resp):
            resp.close()
            resp = HttpResponseImitation(resp.status_code, resp.headers, "too big for download, see docs or increase config.ini->max_size")

        return resp

    def head(self, url, verify=None, allow_redirects=None, headers=None):
        """ HTTP HEAD request """
        self.up_requests_counter()

        if self.every_request_new_session:
            self.session = requests.Session()
        verify = self.verify if verify is None else verify
        allow_redirects = self.allow_redirects if allow_redirects is None else allow_redirects
        headers = self.headers if headers is None else headers

        if 'user-agent' not in map(str.lower, headers.keys()):
            headers['User-Agent'] = Registry().get('ua')

        timeout = int(Registry().get('config')['main']['http_timeout']) if \
            not Registry().isset('tor') else \
            int(Registry().get('config')['tor']['http_timeout'])

        resp = self.session.head(
            url,
            verify=verify,
            allow_redirects=allow_redirects,
            headers=headers,
            proxies=self.get_current_proxy(),
            timeout=timeout
        )

        if 'content-length' in resp.headers and \
                        int(resp.headers['content-length']) > int(Registry().get('config')['main']['max_size']):
            self.errors['maxsize'].append(
                "URL {0} has size {1} bytes, but limit in config - {2} bytes".\
                format(
                    url,
                    resp.headers['content-length'],
                    Registry().get('config')['main']['max_size']
                )
            )
            resp.close()
            resp = None
        return resp
