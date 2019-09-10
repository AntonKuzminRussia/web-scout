import pytest
import mock
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from classes.Proxies import Proxies
from classes.Registry import Registry


class Test_Proxies(object):
    def test_init(self):
        Registry().set('config', {'main': {'proxies_died_limit': 10}})
        proxies = Proxies()
        assert 10 == proxies.died_limit

    def test_count(self):
        Registry().set('config', {'main': {'proxies_died_limit': 10}})
        proxies = Proxies()
        proxies._proxies = ['a', 'b', 'c']
        assert 3 == proxies.count()

    def test_load(self):
        Registry().set('config', {'main': {'proxies_died_limit': 10}})
        proxies = Proxies()
        with mock.patch("classes.Proxies.file_to_list") as ftl_mock:
            ftl_mock.return_value = ['a', 'b', 'c', 'd']
            proxies.load('/test/proxies/path.txt')
            assert 4 == proxies.count()

    def test_get_proxy_has_proxy(self):
        with mock.patch.object(Proxies, 'check_live') as check_alive_mock:
            Registry().set('config', {'main': {'proxies_died_limit': 10}})
            proxies = Proxies()
            test_set = ['a', 'b', 'c']
            proxies._proxies = test_set
            check_alive_mock.return_value = True
            for _ in range(0, 3):
                assert proxies.get_proxy() in test_set

    def test_get_proxy_has_no_proxy(self):
        with mock.patch.object(Proxies, 'check_live') as check_alive_mock:
            Registry().set('config', {'main': {'proxies_died_limit': 10}})
            proxies = Proxies()
            for _ in range(0, 3):
                assert not proxies.get_proxy()

    def test_check_alive_default_url(self):
        def get_mock_function(url, timeout=0, allow_redirects=False, proxies=None, verify=False):
            assert url == 'http://google.com'

        with mock.patch('requests.get', side_effect=get_mock_function):
            Registry().set('config', {'main': {'proxies_died_limit': 10}})
            proxies = Proxies()
            assert proxies.check_live("aaa")

    def test_check_alive_custom_url(self):
        def get_mock_function(url, timeout=0, allow_redirects=False, proxies=None, verify=False):
            assert url == 'http://www.ru'

        with mock.patch('requests.get', side_effect=get_mock_function):
            Registry().set('config', {'main': {'proxies_died_limit': 10}})
            Registry().set('url_for_proxy_check', 'http://www.ru')
            proxies = Proxies()
            assert proxies.check_live("aaa")

    def test_check_alive_proxy_dead(self):
        def get_mock_function(url, timeout=0, allow_redirects=False, proxies=None):
            raise Exception("test")

        with mock.patch('requests.get', side_effect=get_mock_function):
            Registry().set('config', {'main': {'proxies_died_limit': 10}})
            Registry().set('url_for_proxy_check', 'http://www.ru')
            proxies = Proxies()
            assert not proxies.check_live("aaa")