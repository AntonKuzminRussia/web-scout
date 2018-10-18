# -*- coding: utf-8 -*-
import pytest
import mock
import copy


from classes.spider.SpiderCommon import SpiderCommon
from classes.Registry import Registry
from urlparse import urlparse, ParseResult


class MongoCollMock():
    updated_data = None
    insreted_data = None
    droped = None
    find_one_data = None
    indexes_created = None

    def __init__(self):
        self.updated_data = []
        self.insreted_data = []
        self.droped = False
        self.find_one_data = {
            "y": "x"
        }
        self.indexes_created = False

    def create_index(self, some, unique=False, dropDups=False):
        self.indexes_created = True

    def update(self, data1, data2):
        self.updated_data.append([data1, data2])

    def insert(self, data):
        self.insreted_data.append(data)

    def drop(self):
        self.droped = True

    def find_one(self, data):
        return self.find_one_data[data['hash']]


class MongoMock():
    spider_urls = MongoCollMock()

    def __init__(self, colls=[]):
        self.scans = MongoCollMock()
        self.colls = colls

    def collection_names(self):
        return self.colls


class Test_SpiderCommon(object):
    def test_clear_link_obj(self):
        expected_link_obj = {
            'hash': 'a',
            'path': 'b',
            'query': 'c',
            'time': 0,
            'code': 200,
            'checked': 0,
            'referer': '',
            'founder': '',
            'size': 0,
            'getted': 0,
        }
        test_data = dict(expected_link_obj)
        test_data['trash'] = 'some'
        assert expected_link_obj == SpiderCommon._clear_link_obj(test_data)

    def test_links_checked(self):
        mongo_mock = MongoMock()
        Registry().set('mongo', mongo_mock)

        links_test_data = [
            {'path': 'a', 'hash': 'x'},
            {'path': 'b', 'hash': 'y'},
        ]
        SpiderCommon.links_checked(links_test_data)

        expected_updated_data = [
            [{'hash': 'x'}, {'$set': {'path': 'a', 'hash': 'x', 'checked': 1}}],
            [{'hash': 'y'}, {'$set': {'path': 'b', 'hash': 'y', 'checked': 1}}]
        ]
        assert expected_updated_data == mongo_mock.spider_urls.updated_data

    gen_url_provider = [
        ({'protocol': 'http', 'host': 'site.com', 'path': '/', 'query': ''}, 'http://site.com/'),
        ({'protocol': 'http', 'host': 'site.com', 'path': '/', 'query': 'a=b'}, 'http://site.com/?a=b')
    ]

    @pytest.mark.parametrize("link,expected", gen_url_provider)
    def test_gen_url(self, link, expected):
        assert expected == SpiderCommon.gen_url(link)

    del_file_from_path_provider = [
        ('a', ''),
        ('/', '/'),
        ('/index.php', '/'),
        ('/a/index.php', '/a/'),
        ('/a/index', '/a/'),
        ('/a/index/', '/a/index/'),
    ]

    @pytest.mark.parametrize("path,expected", del_file_from_path_provider)
    def test_del_file_from_path(self, path, expected):
        assert expected == SpiderCommon.del_file_from_path(path)

    """
        Cases:
            0 - 3 simple links
            1 - 1 simple link, 1 relative
            2 - 1 simple link on external host    
    """
    prepare_links_to_insert_provider = [
        (
            ["http://www.ru/", "http://www.ru/a/index.php", "http://www.ru/a/index.php"],
            [
                ParseResult(scheme='http', netloc='www.ru', path='/', params='', query='', fragment=''),
                ParseResult(scheme='http', netloc='www.ru', path='/a/index.php', params='', query='', fragment=''),
                ParseResult(scheme='http', netloc='www.ru', path='/a/', params='', query='', fragment=''),
            ],
            []
        ),
        (
            ["http://www.ru/", "a/index.php"],
            [
                ParseResult(scheme='http', netloc='www.ru', path='/', params='', query='', fragment=''),
                ParseResult(scheme='', netloc='', path='/some/', params='', query='', fragment=''),
                ParseResult(scheme='', netloc='', path='/some/a/index.php', params='', query='', fragment=''),
                ParseResult(scheme='', netloc='', path='/some/a/', params='', query='', fragment=''),
                ParseResult(scheme='', netloc='', path='/', params='', query='', fragment=''),
            ],
            []
        ),
        (
            ["http://google.com/"],
            [],
            ['google.com']
        ),
    ]
    @pytest.mark.parametrize("links,links_expected,external_hosts_expected", prepare_links_to_insert_provider)
    def test_prepare_links_to_insert(self, links, links_expected, external_hosts_expected):
        Registry().set('config', {'spider': {'allow_exts': 'php, js'}})
        links = SpiderCommon.prepare_links_for_insert(links, urlparse("/some/"), "www.ru")
        assert links_expected.sort() == links.sort()
        assert external_hosts_expected == SpiderCommon._external_hosts

    def test_get_denied_schemas(self):
        Registry().set('config', {'spider': {'denied_schemes': 'aaa, bbb, ccc'}})
        assert SpiderCommon.get_denied_schemas() == ["aaa", "bbb", "ccc"]

    def test_get_url_hash(self):
        assert "89dd117deb3e754a132c43f1e8d310e7" == SpiderCommon.get_url_hash("/", "a=b")

    insert_links_provider = [
        (
            ["http://www.ru/", "http://www.ru/a/index.php", "http://www.ru/a/index.php"],
            [
                {'code': 0, 'hash': '6666cd76f96956469e7be39d750cc7d9', 'getted': 0, 'founder': 'spider',
                 'host': 'www.ru',
                 'referer': '/', 'path': '/', 'query': '', 'size': 0, 'checked': 0, 'protocol': 'http', 'time': 0},
                {'code': 0, 'hash': 'e8b55aa25c8ac152f62673bbcacdbddf', 'getted': 0, 'founder': 'spider',
                 'host': 'www.ru',
                 'referer': '/', 'path': '/a/index.php', 'query': '', 'size': 0, 'checked': 0, 'protocol': 'http',
                 'time': 0},
                {'code': 0, 'hash': 'a2c180452d0aaaff54812a20c88c23fa', 'getted': 0, 'founder': 'spider',
                 'host': 'www.ru',
                 'referer': '/', 'path': '/a/', 'query': '', 'size': 0, 'checked': 0, 'protocol': 'http', 'time': 0}
            ]
        ),
        (
            ["http://www.ru/", "http://google.com"],
            [
                {'code': 0, 'hash': '6666cd76f96956469e7be39d750cc7d9', 'getted': 0, 'founder': 'spider',
                 'host': 'www.ru',
                 'referer': '/', 'path': '/', 'query': '', 'size': 0, 'checked': 0, 'protocol': 'http', 'time': 0},
            ]
        ),
    ]

    @pytest.mark.parametrize("links,expected_inserts", insert_links_provider)
    def test_insert_links(self, links, expected_inserts):
        mongo_mock = MongoMock()
        Registry().set('mongo', mongo_mock)
        Registry().set('config', {'spider': {'denied_schemes': 'aaa, bbb, ccc', 'allow_exts': 'php, js'}})
        mongo_mock.spider_urls.insreted_data = []
        SpiderCommon.insert_links(links, "/", 'www.ru')

        assert expected_inserts == mongo_mock.spider_urls.insreted_data

    link_allowed_provider = [
        ("/a.php", True),
        ("/a.jpg", False),
        ("/ajpg", True),
        ("/a.jpg/a.php", True),
    ]
    @pytest.mark.parametrize("link,expeted", link_allowed_provider)
    def test_link_allowed(self, link, expeted):
        Registry().set('config', {'spider': {'allow_exts': 'php, js'}})
        assert expeted == bool(SpiderCommon._link_allowed(urlparse(link)))

    build_path_provider = [
        ("/a.php", "/some/", "/a.php"),
        ("a.php", "/some/", "/some/a.php"),
    ]
    @pytest.mark.parametrize("link, path, expected", build_path_provider)
    def test_build_path(self, link, path, expected):
        assert urlparse(expected) == SpiderCommon.build_path(urlparse(link), path)

    def test_clear_link(self):
        assert urlparse("/a/b.php?a=1&b=1") == SpiderCommon.clear_link(urlparse("/x/.././a//b.php?a=1&amp;b=1"))

    def test_get_link_data_by_hash(self):
        mongo_mock = MongoMock()
        Registry().set('mongo', mongo_mock)
        assert "x" == SpiderCommon().get_link_data_by_hash("y")

    def test_clear_old_data(self):
        Registry().set('data_path', '/tmp/test/')

        mongo_mock = MongoMock()
        Registry().set('mongo', mongo_mock)

        with mock.patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            with mock.patch('shutil.rmtree') as mock_rmtree:
                SpiderCommon.clear_old_data("site.com")

                assert mongo_mock.spider_urls.droped
                mock_exists.assert_called_once_with("/tmp/test/site.com")
                mock_rmtree.assert_called_once_with("/tmp/test/site.com")

    def test_get_pages_list(self):
        Registry().set('data_path', '/tmp/test/')
        with mock.patch('os.listdir') as mock_listdir:
            mock_listdir.return_value = ['eeae4c14428ebabcacb740214b3ae403', '.', 'index.html', 'zzze4c14428ebabcacb740214b3ae403']
            assert ['eeae4c14428ebabcacb740214b3ae403', 'zzze4c14428ebabcacb740214b3ae403'] == SpiderCommon()._get_pages_list("site.com")

    def test_prepare_first_pages(self):
        mongo_mock = MongoMock()
        Registry().set('mongo', mongo_mock)
        mongo_mock.spider_urls.insreted_data = []
        SpiderCommon.prepare_first_pages(["http://site.com/index.php?a=b"])
        assert mongo_mock.spider_urls.insreted_data[0]['host'] == 'site.com'
        assert mongo_mock.spider_urls.insreted_data[0]['path'] == '/index.php'
        assert mongo_mock.spider_urls.insreted_data[0]['query'] == 'a=b'
        assert mongo_mock.spider_urls.droped
        assert mongo_mock.spider_urls.indexes_created
