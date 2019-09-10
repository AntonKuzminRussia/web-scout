# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Unit tests for FileGenetator
"""
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from classes.generators.FileGenerator import FileGenerator
from libs.common import file_put_contents


class Test_FileGenerator(object):
    """Unit tests for CombineGenetator"""
    def test_no_parts(self):
        file_put_contents('/tmp/test.txt', 'aaa\nbbb\nccc')
        gen = FileGenerator('/tmp/test.txt', parts=0, part=0)

        assert gen.get() == "aaa"
        assert gen.get() == "bbb"
        assert gen.get() == "ccc"
        assert gen.get() is None

    def test_part(self):
        file_put_contents('/tmp/test.txt', 'aaa\nbbb\nccc\nddd')
        gen = FileGenerator('/tmp/test.txt', parts=2, part=1)

        assert gen.get() == "aaa"
        assert gen.get() == "bbb"
        assert gen.get() is None