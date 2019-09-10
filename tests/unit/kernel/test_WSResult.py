# -*- coding: utf-8 -*-

import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from classes.kernel.WSResult import WSResult


class Test_WSResult(object):
    def test_put(self):
        result = WSResult()
        result.put("aaa")
        assert ["aaa"] == result.get_all()

    def test_as_string(self):
        result = WSResult()
        result.put("aaa")
        result.put("bbb")
        result.put("ccc")
        assert "aaa\nbbb\nccc\n" == result.as_string()

    def test_get_all(self):
        result = WSResult()
        result.put("aaa")
        assert ["aaa"] == result.get_all()

    def test_unique(self):
        result = WSResult()
        result.put("aaa")
        result.put("aaa")
        result.put("bbb")
        result.put("ccc")
        result.unique()
        assert result.get_all() == ["aaa", "bbb", "ccc"]