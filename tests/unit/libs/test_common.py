# -*- coding: utf-8 -*-
import datetime
import mock

import pytest

from libs.common import *
from classes.Registry import Registry


class Test_common(object):
    file_to_list_provider = [
        (False, ['aaa', 'bbb', 'ccc', 'ccc']),
        (True, ['aaa', 'bbb', 'ccc']),
    ]

    @pytest.mark.parametrize("unique,expected", file_to_list_provider)
    def test_file_to_list(self, unique, expected):
        file_put_contents('/tmp/test.txt', 'aaa\nbbb\nccc\nccc');
        assert expected == file_to_list('/tmp/test.txt', unique)

    def test_nformat(self):
        Registry().set('config', {'main': {'locale': 'en_US.UTF-8'}})
        assert "1,000,000" == nformat(1000000)

    secs_to_text_provider = [
        (6, "6s"),
        (66, "1m 6s"),
        (3666, "1h 1m 6s"),
        (3600 * 24 + 3666, "1d 1h 1m 6s"),
        (3600 * 24 + 3660, "1d 1h 1m"),
        (3600 * 24 + 3600, "1d 1h"),
        (3600 * 24, "1d"),
    ]

    @pytest.mark.parametrize("secs,expected", secs_to_text_provider)
    def test_secs_to_text(self, secs, expected):
        assert expected == secs_to_text(secs)

    validate_ip_provider = [
        ('1.1.1.1', True),
        ('1.1.1.1a', False),
        ('a1.1.1.1', False),
        ('a', False),
    ]

    @pytest.mark.parametrize("ip,expected", validate_ip_provider)
    def test_validate_ip_provider(self, ip, expected):
        assert expected == validate_ip(ip)

    validate_host_provider = [
        ('site.com', True),
        ('sit-e.com', True),
        ('abc.site.com', True),
        ('abc.abc.site.com', True),
        ('site.com:80', True),
        ('com', False),
        ('com:80', False),
        ('.com', False),
        ('.com:80', False),
        ('si!te.com', False),
        ('http://site.com', False),
    ]

    @pytest.mark.parametrize("host,expected", validate_host_provider)
    def test_validate_ip_provider(self, host, expected):
        assert expected == validate_host(host)

    validate_uri_start_provider = [
        ('http://aaa.com', True),
        ('https://aaa.com:80', True),
        ('aaa.com', False),
        ('ftp://aaa.com', False),
    ]

    @pytest.mark.parametrize("uri,expected", validate_uri_start_provider)
    def test_validate_uri_start(self, uri, expected):
        assert expected == validate_uri_start(uri)

    validate_md5_provider = [
        ('1', 'c4ca4238a0b923820dcc509a6f75849b'),
        ('абв', '9817de3f4bd1d1d149fc366d46e5e134'),
        # Controversial result. Other cases give different hashes in this case,
        # but we need check only no exceptions here
        ('абв'.decode('utf8').encode('cp1251'), 'd41d8cd98f00b204e9800998ecf8427e'),
    ]

    @pytest.mark.parametrize("s,expected", validate_md5_provider)
    def test_md5(self, s, expected):
        assert expected == md5(s)

    parse_split_conf_provider = [
        ('a,b,c', ['a', 'b', 'c']),
        ('a ,b ,c', ['a', 'b', 'c']),
        ('1,2,c', ['1', '2', 'c']),
    ]
    @pytest.mark.parametrize("s,expected", parse_split_conf_provider)
    def test_parse_split_conf(self, s, expected):
        assert expected == parse_split_conf(s)

    def test_file_put_contents(self):
        file_put_contents("/tmp/test.txt", "aaa\nbbb")
        fh = open('/tmp/test.txt')
        assert fh.read() == "aaa\nbbb"
        fh.close()

    def test_file_get_contents(self):
        file_put_contents("/tmp/test.txt", "aaa\nbbb")
        assert file_get_contents('/tmp/test.txt') == "aaa\nbbb"

    def test_t(self):
        assert t("%Y-%m-%d %H:%M:%S") in str(datetime.datetime.now())

    def test_mongo_result_to_list(self):
        assert ['a', 'b', 'c'] == mongo_result_to_list(['a', 'b', 'c'])

    def test_clear_double_slashes(self):
        assert "/a/b/c/" == clear_double_slashes("//a//b/c/")

    always_not_404_provider = [
        (200, True),
        (404, False),
    ]
    @pytest.mark.parametrize("code,expected", always_not_404_provider)
    def test_always_not_404(self, code, expected):
        with mock.patch('requests.get') as req_mock:
            req_mock.return_value = type('', (object,), {"status_code": code})()

            assert expected == always_not_404("http", "localhost")

    is_binary_content_type_provider = [
        ("text/html", False),
        ("application/javascript", False),
        ("image/gif", True),
        ("application/pdf", True),
    ]

    @pytest.mark.parametrize("content_type,expected", is_binary_content_type_provider)
    def test_is_binary_content_type(self, content_type, expected):
        assert is_binary_content_type(content_type) == expected

    def test_md5sum(self):
        file_put_contents("/tmp/test.txt", "aaa\nbbb")
        assert md5sum("/tmp/test.txt") == "f4288da1c441491df98df891e8406cd1"

    def test_get_response_size(self):
        assert 3 == get_response_size(type('', (object,), {"content": "abc"})())

    def test_random_ua(self):
        Registry().set('wr_path', os.path.dirname(os.path.realpath(__file__)) + "/../../../")

        ua1 = random_ua()
        ua2 = random_ua()
        ua3 = random_ua()

        assert len(ua1) and len(ua2) and len(ua3) and ua1 != ua2 != ua3