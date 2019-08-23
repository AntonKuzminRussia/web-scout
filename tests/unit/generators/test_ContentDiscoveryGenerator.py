# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Unit tests for ContentDiscoveryGenerator
"""
import sys
import os

import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../../')

from classes.generators.ContentDiscoveryNameGenerator import ContentDiscoveryNameGenerator
from classes.Registry import Registry

class Test_ContentDiscoveryNameGenerator(object):
    """Unit tests for ContentDiscoveryNameGenerator"""
    model = None

    def test_gen_exts_variants(self):
        basename = "test"
        assert ["test", "test.log", "test.txt"] == \
               ContentDiscoveryNameGenerator.gen_exts_variants(basename, ['txt', 'log'])

    def gen_expected_letters_variants(self, basename, ext):
        wait = []
        wait.extend([chr(n) + basename[1:] + ("." + ext if len(ext) else "") for n in range(97, 123)])
        wait.extend([basename[:-1] + chr(n) + ("." + ext if len(ext) else "") for n in range(97, 123)])
        wait.sort()
        return wait

    gen_letters_variants_provider = [
        ("test", "txt"),
        ("test", ""),
    ]

    @pytest.mark.parametrize("name,ext", gen_letters_variants_provider)
    def test_gen_letters_variants(self, name, ext):
        basename = name + ("." + ext if len(ext) else "")
        expected = self.gen_expected_letters_variants(name, ext)

        assert expected == ContentDiscoveryNameGenerator.gen_letters_variants(basename, True)

    gen_numbers_variants_provider = [
        (
            "test.txt",
            True,
            [
                "0test.txt", "1test.txt", "2test.txt", "3test.txt", "4test.txt",
                "5test.txt", "6test.txt", "7test.txt", "8test.txt", "9test.txt",
                "test0.txt", "test1.txt", "test2.txt", "test3.txt", "test4.txt",
                "test5.txt", "test6.txt", "test7.txt", "test8.txt", "test9.txt",
            ]
        ),
        (
            "test",
            False,
            [
                "0test", "1test", "2test", "3test", "4test",
                "5test", "6test", "7test", "8test", "9test",
                "test0", "test1", "test2", "test3", "test4",
                "test5", "test6", "test7", "test8", "test9",
            ]
        ),
        (
            "1test.txt",
            True,
            [
                "0test.txt", "1test.txt", "2test.txt", "3test.txt", "4test.txt",
                "5test.txt", "6test.txt", "7test.txt", "8test.txt", "9test.txt",
            ]
        ),
        (
            "test1.txt",
            True,
            [
                "test0.txt", "test1.txt", "test2.txt", "test3.txt", "test4.txt",
                "test5.txt", "test6.txt", "test7.txt", "test8.txt", "test9.txt",
            ]
        ),
        (
            "1test",
            False,
            [
                "0test", "1test", "2test", "3test", "4test",
                "5test", "6test", "7test", "8test", "9test",
            ]
        ),
        (
            "test1",
            False,
            [
                "test0", "test1", "test2", "test3", "test4",
                "test5", "test6", "test7", "test8", "test9",
            ]
        ),
        (
            "1test1.txt",
            True,
            [
                "0test0.txt",
                "0test1.txt", "1test1.txt", "2test1.txt", "3test1.txt", "4test1.txt",
                "5test1.txt", "6test1.txt", "7test1.txt", "8test1.txt", "9test1.txt",
                "1test0.txt", "1test2.txt", "1test3.txt", "1test4.txt",
                "1test5.txt", "1test6.txt", "1test7.txt", "1test8.txt", "1test9.txt",
                "1test1.txt", "2test2.txt", "3test3.txt", "4test4.txt", "5test5.txt",
                "6test6.txt", "7test7.txt", "8test8.txt", "9test9.txt",
            ]
        ),
        (
            "1test1",
            True,
            [
                "0test0",
                "0test1", "1test1", "2test1", "3test1", "4test1",
                "5test1", "6test1", "7test1", "8test1", "9test1",
                "1test0", "1test2", "1test3", "1test4",
                "1test5", "1test6", "1test7", "1test8", "1test9",
                "1test1", "2test2", "3test3", "4test4", "5test5",
                "6test6", "7test7", "8test8", "9test9",
            ]
        ),
    ]

    @pytest.mark.parametrize("basename,is_file,expect", gen_numbers_variants_provider)
    def test_gen_numbers_variants(self, basename, is_file, expect):
        expect = list(set(expect))
        expect.sort()
        assert expect == ContentDiscoveryNameGenerator.gen_numbers_variants(basename, is_file)

    gen_backups_variants_provider = [
        ("test.txt", ["test.txt.zip", "test.txt.OLD", "test.OLD"]),
        ("test", ["test.zip", "test.OLD"]),
    ]

    @pytest.mark.parametrize("basename,expects", gen_backups_variants_provider)
    def test_gen_backups_variants(self, basename, expects):
        Registry().set('wr_path', os.path.dirname(os.path.realpath(__file__)) + "/../../../")
        results = ContentDiscoveryNameGenerator.gen_backups_variants(basename, basename.count(".") > 0)
        for expect in expects:
            assert expect in results

