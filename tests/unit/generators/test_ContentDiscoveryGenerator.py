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
            ("{0}test{1}.txt".format(i, j) for i in range(10) for j in range(10))
        ),
        (
            "1test1",
            True,
            ("{0}test{1}".format(i, j) for i in range(10) for j in range(10))
        ),
        (
            "123test",
            False,
            [
                "120test", "121test", "122test", "123test", "124test",
                "125test", "126test", "127test", "128test", "129test",
            ]
        ),
        (
            "123test55", # => 120test50 => 129test59
            False,
            ("{0}test{1}".format(i, j) for i in range(120, 130) for j in range(50, 60))
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

