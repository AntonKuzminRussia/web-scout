# -*- coding: utf-8 -*-

import Queue
import time

import pytest

from classes.logger.MongoInserterThread import MongoLoggerThread
from classes.Registry import Registry


class MongoInserterMock:
    working = True

    def isAlive(self):
        return False;


class MongoCollMock():
    inserted_data = []
    indexes_created = False

    def insert(self, data):
        self.inserted_data.append(data)

    def insert_many(self, data):
        for row in data:
            self.insert(row)

    def create_index(self, some, unique=False):
        self.indexes_created = True

    def find(self, some):
        return self

    def count(self):
        return 1


class MongoMock():
    items = MongoCollMock()
    scans = None
    colls = None

    def __init__(self, colls=[]):
        self.scans = MongoCollMock()
        self.colls = colls

    def collection_names(self):
        return self.colls


class Test_MongoLoggerThread(object):
    insert_pool_provider = [
        ([], True),
        (['items'], False),
    ]
    @pytest.mark.parametrize("colls,expected_indexes", insert_pool_provider)
    def test_insert_pool(self, colls, expected_indexes):
        MongoCollMock.inserted_data = []
        test_dataset = ['some', 'test']

        mongo_mock = MongoMock(colls)
        Registry().set("mongo", mongo_mock)
        Registry().set("config", {"main": {"mongo_logger_items_pool_count_limit": 10}})

        mongo_logger_thread = MongoLoggerThread(False)
        mongo_logger_thread.pool = test_dataset

        mongo_mock.items.indexes_created = False

        mongo_logger_thread.insert_pool()

        assert 0 == len(mongo_logger_thread.pool)
        assert test_dataset == mongo_mock.items.inserted_data
        assert expected_indexes == mongo_mock.items.indexes_created

    """
        Case - limit 3 records in pool. Add 2, wait, nothing added. 
                Add two more. Check, 3 added, 1 in pool. Stop thread, last item go in added.
    """
    def test_run(self):
        queue = Queue.Queue();
        queue.put('some')
        queue.put('test')

        mongo_mock = MongoMock()
        mongo_mock.items.inserted_data = []
        Registry().set("mongo", mongo_mock)
        Registry().set("config", {"main": {"mongo_logger_items_pool_count_limit": 2}})

        mongo_logger_thread = MongoLoggerThread(queue)
        mongo_logger_thread.sleep_time_per_step = 0.1
        mongo_logger_thread.start()

        time.sleep(0.1)

        assert 2 == len(mongo_logger_thread.pool)
        assert [] == mongo_mock.items.inserted_data
        assert 0 == queue.qsize()

        queue.put("foo")
        queue.put("bar")
        time.sleep(0.2)

        assert 1 == len(mongo_logger_thread.pool)
        assert ['bar'] == mongo_logger_thread.pool
        assert ['some', 'test', 'foo'] == mongo_mock.items.inserted_data
        assert 0 == queue.qsize()

        mongo_logger_thread.working = False
        while mongo_logger_thread.isAlive():
            time.sleep(0.1)

        assert 0 == len(mongo_logger_thread.pool)
        assert ['some', 'test', 'foo', 'bar'] == mongo_mock.items.inserted_data
        assert 0 == queue.qsize()




