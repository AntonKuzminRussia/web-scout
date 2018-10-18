# -*- coding: utf-8 -*-

import os

import pytest
import mock

from classes.kernel.WSException import WSException
from classes.logger.Logger import Logger
from classes.Registry import Registry
from libs.common import t, file_get_contents


class MongoInserterMock:
    working = True

    def isAlive(self):
        return False;


class MongoCollMock():
    inserted_data = []
    indexes_created = False

    def insert(self, data):
        self.inserted_data.append(data)

    def create_index(self, some, unique=False):
        self.indexes_created = True

    def find(self, some):
        return self

    def count(self):
        return 1


class MongoMock():
    responses_content = MongoCollMock()
    scans = None
    colls = None

    def __init__(self, colls=[]):
        self.scans = MongoCollMock()
        self.colls = colls

    def collection_names(self):
        return self.colls


class Test_Logger(object):
    def test_init_module_logpath_exists_error(self):
        with mock.patch('classes.logger.Logger.MongoLoggerThread'):
            Registry().set("mongo", False)
            Registry().set("wr_path", "/tmp/")
            Registry().set("config", {"main": {"mongo_logger_items_pool_count_limit": 1}})
            with pytest.raises(WSException) as ex:
                Logger("test")
            assert "LOGGER ERROR: Path" in str(ex)

    def test_init_logs_dir_creation_date(self):
        def exists_mock_function(path):
            if path == "/tmp/logs/test":
                return True
            return False

        with mock.patch('os.path.exists', side_effect=exists_mock_function):
            with mock.patch('os.mkdir') as mkdir_mock:
                with mock.patch('classes.logger.Logger.open') as open_mock:
                    Registry().set("mongo", False)
                    Registry().set("wr_path", "/tmp")
                    Registry().set("config", {"main": {"mongo_logger_items_pool_count_limit": 1}})

                    Logger("test")
                    mkdir_mock.assert_has_calls(
                        [
                            mock.call("/tmp/logs/test/" + t("%Y-%m-%d")),
                            mock.call("/tmp/logs/test/" + t("%Y-%m-%d") + "/" + t("%H_%M_%S"))
                        ]
                    )

                    open_mock.assert_called_once_with("/tmp/logs/test/" + t("%Y-%m-%d") + "/" + t("%H_%M_%S") + "/run.log", "w")

    set_scan_name_provider = [
        ([], True),
        (["scans"], False),
    ]
    @pytest.mark.parametrize("colls,expected_indexes", set_scan_name_provider)
    def test_set_scan_name(self, colls, expected_indexes):
        MongoCollMock.inserted_data = []

        with mock.patch('classes.logger.Logger.MongoLoggerThread'):
            with mock.patch('os.path.exists') as exists_mock:
                with mock.patch('classes.logger.Logger.open'):
                    exists_mock.return_value = True

                    Registry().set("mongo", MongoMock(colls))
                    Registry().set("wr_path", "/tmp")
                    Registry().set("config", {"main": {"mongo_logger_items_pool_count_limit": 1}})

                    expected_scan_data = {
                        'module': "test",
                        'name': "foobar",
                        'date': t("%Y-%m-%d"),
                        'time': t("%H:%M:%S"),
                    }

                    Logger("test").set_scan_name("foobar")
                    test_data = MongoCollMock.inserted_data[0]
                    assert 32 == len(test_data['hash'])
                    del test_data['hash']
                    assert expected_scan_data == test_data

                    assert expected_indexes == Registry().get("mongo").scans.indexes_created


    def test_item_no_scan_name_exception(self):
        with mock.patch('classes.logger.Logger.MongoLoggerThread'):
            with mock.patch('os.path.exists') as exists_mock:
                with mock.patch('classes.logger.Logger.open'):
                    exists_mock.return_value = True

                    Registry().set("mongo", MongoMock())
                    Registry().set("wr_path", "/tmp")
                    Registry().set("config", {"main": {"mongo_logger_items_pool_count_limit": 1}})

                    logger = Logger("test")
                    with pytest.raises(WSException) as ex:
                        logger.item("name", "")
                    assert "Scan name must be specified" in str(ex)

    def test_item(self):
        with mock.patch('classes.logger.Logger.MongoLoggerThread'):
            with mock.patch('os.path.exists') as exists_mock:
                with mock.patch('classes.logger.Logger.open'):
                    exists_mock.return_value = True

                    Registry().set("mongo", MongoMock())
                    Registry().set("wr_path", "/tmp")
                    Registry().set("config", {"main": {"mongo_logger_items_pool_count_limit": 1}})

                    logger = Logger("test")
                    logger.set_scan_name("test")
                    logger.item("testname", "testcontent")

                    assert "testname" == logger.mongo_inserter_queue.get(False)['name']

    def test_ex(self):
        if os.path.exists("/tmp/test.txt"):
            os.remove("/tmp/test.txt")

        try:
            raise BaseException("Test message")
        except BaseException as ex:
            with mock.patch('classes.logger.Logger.MongoLoggerThread'):
                with mock.patch('os.path.exists') as exists_mock:
                    with mock.patch('classes.logger.Logger.open'):
                        exists_mock.return_value = True

                        Registry().set("mongo", MongoMock())
                        Registry().set("wr_path", "/tmp")
                        Registry().set("config", {"main": {"mongo_logger_items_pool_count_limit": 1}})

                        logger = Logger("test")
                        logger.log_fh = open("/tmp/test.txt", "w")
                        logger.set_scan_name("test")
                        logger.ex(ex)

                        assert "Test message" in file_get_contents("/tmp/test.txt")

    def test_stop(self):
        with mock.patch('classes.logger.Logger.MongoLoggerThread'):
            with mock.patch('os.path.exists') as exists_mock:
                with mock.patch('classes.logger.Logger.open'):
                    exists_mock.return_value = True

                    Registry().set("mongo", MongoMock())
                    Registry().set("wr_path", "/tmp")
                    Registry().set("config", {"main": {"mongo_logger_items_pool_count_limit": 1}})

                    inserter_mock = MongoInserterMock()

                    logger = Logger("test")
                    logger.mongo_inserter = inserter_mock
                    logger.stop()

                    assert not inserter_mock.working
