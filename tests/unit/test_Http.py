import pytest
import mock
import random
import string

from classes.Http import Http
from classes.Registry import Registry
from classes.kernel.WSException import WSException
from libs.common import file_put_contents


class ResponseMock():
    headers = None

    def __init__(self, headers={}):
        self.headers = headers


class ProxiesMock():
    changed_count = 0
    def get_proxy(self):
        self.changed_count += 1
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


class SessionMock():
    requests = None

    def __init__(self):
        self.requests = []

    def request(self, url, verify, allow_redirects, headers, stream, proxies, timeout, data=None, cookies=None, files=None):
        request = {
                'url': url,
                'verify': verify,
                'allow_redirects': allow_redirects,
                'headers': headers,
                'stream': stream,
                'proxies': proxies,
                'timeout': timeout,
                'cookies': cookies,
                'files': files,
            }
        if data is not None:
            request['data'] = data
        self.requests.append(request)
        return ResponseMock()

    def get(self, url, verify, allow_redirects, headers, stream, proxies, timeout, cookies=None, files=None):
        return self.request(url, verify, allow_redirects, headers, stream, proxies, timeout, cookies=cookies, files=files)

    def post(self, url, verify, allow_redirects, headers, stream, proxies, timeout, data, cookies=None, files=None):
        return self.request(url, verify, allow_redirects, headers, stream, proxies, timeout, data=data, cookies=cookies, files=files)

    def head(self, url, verify, allow_redirects, headers, proxies, timeout, cookies=None, files=None):
        return self.request(url, verify, allow_redirects, headers, False, proxies, timeout, cookies=cookies, files=files)


class Test_Http(object):
    get_params_provider = [
        ("get", "testurl1", True, {}, True, None, None, {'url': 'testurl1', 'verify': True, 'headers': {'User-Agent': 'TestUA'}, 'allow_redirects': True, 'cookies': None, 'files': None}),
        ("get", "testurl2", True, {'A': 'B'}, True, None, None, {'url': 'testurl2', 'verify': True, 'headers': {'A': 'B', 'User-Agent': 'TestUA'}, 'allow_redirects': True, 'cookies': None, 'cookies': None, 'files': None}),
        ("get", "testurl3", False, {}, False, None, None, {'url': 'testurl3', 'verify': False, 'headers': {'User-Agent': 'TestUA'}, 'allow_redirects': False, 'cookies': None, 'cookies': None, 'files': None}),
        ("get", "testurl3", False, {}, False, 'xcookie', None, {'url': 'testurl3', 'verify': False, 'headers': {'User-Agent': 'TestUA'}, 'allow_redirects': False, 'cookies': 'xcookie', 'files': None}),
        ("post", "testurl1", True, {}, True, None, None, {'url': 'testurl1', 'verify': True, 'headers': {'User-Agent': 'TestUA', 'Content-Type': "application/x-www-form-urlencoded"}, 'allow_redirects': True, 'data': {'postparam': 'postvalue'}, 'cookies': None, 'cookies': None, 'files': None}),
        ("post", "testurl2", True, {'A': 'B'}, True, None, None, {'url': 'testurl2', 'verify': True, 'headers': {'A': 'B', 'User-Agent': 'TestUA', 'Content-Type': "application/x-www-form-urlencoded"}, 'allow_redirects': True, 'data': {'postparam': 'postvalue'}, 'cookies': None, 'cookies': None, 'files': None}),
        ("post", "testurl3", False, {}, False, None, None, {'url': 'testurl3', 'verify': False, 'headers': {'User-Agent': 'TestUA', 'Content-Type': "application/x-www-form-urlencoded"}, 'allow_redirects': False, 'data': {'postparam': 'postvalue'}, 'cookies': None, 'cookies': None, 'files': None}),
        ("post", "testurl1", True, {}, True, 'xcookies', 'xfiles', {'url': 'testurl1', 'verify': True, 'headers': {'User-Agent': 'TestUA'}, 'allow_redirects': True, 'data': {'postparam': 'postvalue'}, 'cookies': 'xcookies', 'files': 'xfiles'}),
        ("head", "testurl1", True, {}, True, None, None, {'url': 'testurl1', 'verify': True, 'headers': {'User-Agent': 'TestUA'}, 'allow_redirects': True, 'cookies': None, 'cookies': None, 'files': None}),
        ("head", "testurl2", True, {'A': 'B'}, True, None, None, {'url': 'testurl2', 'verify': True, 'headers': {'A': 'B', 'User-Agent': 'TestUA'}, 'allow_redirects': True, 'cookies': None, 'cookies': None, 'files': None}),
        ("head", "testurl3", False, {}, False, None, None, {'url': 'testurl3', 'verify': False, 'headers': {'User-Agent': 'TestUA'}, 'allow_redirects': False, 'cookies': None, 'cookies': None, 'files': None}),
    ]

    @pytest.mark.parametrize("reqtype,url,verify,headers,allow_redirects,cookies,files,expected", get_params_provider)
    def test_get_params(self, reqtype, url, verify, headers, allow_redirects, cookies, files, expected):
        Registry().set('proxies', ProxiesMock())
        Registry().set('ua', 'TestUA')
        Registry().set('config', {'main': {'http_timeout': 5, 'requests_per_proxy': 1}})

        with mock.patch("requests.Session") as sess_creation_mock:
            session_mock = SessionMock()
            sess_creation_mock.return_value = session_mock
            http = Http()
            if reqtype == "get":
                http.get(url, verify=verify, headers=headers, allow_redirects=allow_redirects, cookies=cookies)
            elif reqtype == "head":
                http.head(url, verify=verify, headers=headers, allow_redirects=allow_redirects)
            elif reqtype == "post":
                http.post(url, verify=verify, headers=headers, allow_redirects=allow_redirects, data={'postparam': 'postvalue'}, cookies=cookies, files=files)

            test_data = session_mock.requests[0]
            del test_data['proxies']
            del test_data['timeout']
            del test_data['stream']

            assert expected == test_data

    def test_up_requests_counter(self):
        Registry().set('proxies', ProxiesMock())

        http = Http()
        sess1 = http.session

        http.up_requests_counter()
        assert 1 == http.requests_counter
        assert sess1 == http.session

        http.requests_per_session = 2
        http.up_requests_counter()
        assert 0 == http.requests_counter
        assert sess1 != http.session

    def test_up_requests_counter_with_every_request_new_session(self):
        Registry().set('proxies', ProxiesMock())

        http = Http()
        http.every_request_new_session = True
        sess1 = http.session
        http.requests_per_session = 1
        http.up_requests_counter()
        http.up_requests_counter()
        assert 2 == http.requests_counter
        assert sess1 == http.session

    def test_load_headers_from_file(self):
        file_put_contents("/tmp/test.txt", "A: B\nC: D")
        http = Http()
        http.load_headers_from_file("/tmp/test.txt")
        assert {'A': 'B', 'C': 'D'} == http.headers

    def test_load_headers_from_file_error(self):
        file_put_contents("/tmp/test.txt", "A: B\nC")
        http = Http()
        with pytest.raises(WSException) as ex:
            http.load_headers_from_file("/tmp/test.txt")
            assert "Wrong header line" in str(ex)

    def test_change_proxy(self):
        proxies_mock = ProxiesMock()
        Registry().set('proxies', proxies_mock)

        http = Http()
        http.change_proxy()
        assert 1 == proxies_mock.changed_count
        http.change_proxy()
        assert 2 == proxies_mock.changed_count

    def test_get_current_proxy(self):
        proxies_mock = ProxiesMock()
        Registry().set('proxies', proxies_mock)
        Registry().set('config', {'main': {'requests_per_proxy': 3}})

        http = Http()
        http.get_current_proxy()
        assert 1 == proxies_mock.changed_count
        assert 1 == http.current_proxy_counter

        http.get_current_proxy()
        assert 1 == proxies_mock.changed_count
        assert 2 == http.current_proxy_counter

        http.get_current_proxy()
        http.get_current_proxy()
        assert 2 == proxies_mock.changed_count
        assert 1 == http.current_proxy_counter

    is_response_length_less_than_limit_provider = [
        (
            {},
            True
        ),
        (
            {'content-length': '5'},
            True
        ),
        (
            {'content-length': '11'},
            False
        ),
    ]
    @pytest.mark.parametrize("headers, expected", is_response_length_less_than_limit_provider)
    def test_is_response_length_less_than_limit(self, headers, expected):
        Registry().set('config', {'main': {'max_size': 10}})
        response_mock = ResponseMock(headers)
        assert expected == Http().is_response_length_less_than_limit("test", response_mock)
