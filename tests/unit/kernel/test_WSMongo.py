# -*- coding: utf-8 -*-

from bson import Binary
import pytest

from classes.kernel.WSMongo import WSMongo
from classes.Registry import Registry


class MongoCollMock():
    inserted_data = []
    cnt = 0
    test_hashes = {
        'a': '0cc175b9c0f1b6a831c399e269772661',
        'b': '92eb5ffee6ae2fec3ad71c777531578f',
        'c': '4a8a08f09d37b73795649038408b5f33',
    }

    def find(self, data):
        if data['hash'] == self.test_hashes["a"]:
            self.cnt = 0
        if data['hash'] == self.test_hashes["c"]:
            self.cnt = 1
        return self

    def count(self):
        return self.cnt

    def insert(self, data):
        self.inserted_data.append(data)


class MongoMock():
    responses_content = MongoCollMock()


class Test_WSMongo(object):
    """
        Cases:
            0 - content new, hash not found in db, insert in
            1 - content known, not insert
            2 - content unknown, but found in db and not insert there
    """
    load_mongo_content_hash_provider = [
        ("a", 1, [{'hash': MongoCollMock.test_hashes["a"], 'content': Binary("a")}]),
        ("b", 0, []),
        ("c", 0, [])
    ]

    @pytest.mark.parametrize("content,expected_inserts,expected_inserted_data", load_mongo_content_hash_provider)
    def test_load_mongo_content_hash(self, content, expected_inserts, expected_inserted_data):
        Registry().set("mongo", MongoMock())
        MongoCollMock.inserted_data = []
        WSMongo.content_hashes = set(["92eb5ffee6ae2fec3ad71c777531578f"])
        WSMongo.inserts = 0

        load_result = WSMongo.load_mongo_content_hash(content)

        assert MongoCollMock.test_hashes[content] == load_result
        assert expected_inserts == WSMongo.inserts
        assert expected_inserted_data == MongoCollMock.inserted_data