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
                '0test0.txt', '0test1.txt', '0test2.txt', '0test3.txt', '0test4.txt', '0test5.txt',
                '0test6.txt', '0test7.txt', '0test8.txt', '0test9.txt', '1test0.txt', '1test1.txt',
                '1test2.txt', '1test3.txt', '1test4.txt', '1test5.txt', '1test6.txt', '1test7.txt',
                '1test8.txt', '1test9.txt', '2test0.txt', '2test1.txt', '2test2.txt', '2test3.txt',
                '2test4.txt', '2test5.txt', '2test6.txt', '2test7.txt', '2test8.txt', '2test9.txt',
                '3test0.txt', '3test1.txt', '3test2.txt', '3test3.txt', '3test4.txt', '3test5.txt',
                '3test6.txt', '3test7.txt', '3test8.txt', '3test9.txt', '4test0.txt', '4test1.txt',
                '4test2.txt', '4test3.txt', '4test4.txt', '4test5.txt', '4test6.txt', '4test7.txt',
                '4test8.txt', '4test9.txt', '5test0.txt', '5test1.txt', '5test2.txt', '5test3.txt',
                '5test4.txt', '5test5.txt', '5test6.txt', '5test7.txt', '5test8.txt', '5test9.txt',
                '6test0.txt', '6test1.txt', '6test2.txt', '6test3.txt', '6test4.txt', '6test5.txt',
                '6test6.txt', '6test7.txt', '6test8.txt', '6test9.txt', '7test0.txt', '7test1.txt',
                '7test2.txt', '7test3.txt', '7test4.txt', '7test5.txt', '7test6.txt', '7test7.txt',
                '7test8.txt', '7test9.txt', '8test0.txt', '8test1.txt', '8test2.txt', '8test3.txt',
                '8test4.txt', '8test5.txt', '8test6.txt', '8test7.txt', '8test8.txt', '8test9.txt',
                '9test0.txt', '9test1.txt', '9test2.txt', '9test3.txt', '9test4.txt', '9test5.txt',
                '9test6.txt', '9test7.txt', '9test8.txt', '9test9.txt'
            ]
        ),
        (
            "1test1",
            True,
            [
                '0test0', '0test1', '0test2', '0test3', '0test4', '0test5',
                '0test6', '0test7', '0test8', '0test9', '1test0', '1test1',
                '1test2', '1test3', '1test4', '1test5', '1test6', '1test7',
                '1test8', '1test9', '2test0', '2test1', '2test2', '2test3',
                '2test4', '2test5', '2test6', '2test7', '2test8', '2test9',
                '3test0', '3test1', '3test2', '3test3', '3test4', '3test5',
                '3test6', '3test7', '3test8', '3test9', '4test0', '4test1',
                '4test2', '4test3', '4test4', '4test5', '4test6', '4test7',
                '4test8', '4test9', '5test0', '5test1', '5test2', '5test3',
                '5test4', '5test5', '5test6', '5test7', '5test8', '5test9',
                '6test0', '6test1', '6test2', '6test3', '6test4', '6test5',
                '6test6', '6test7', '6test8', '6test9', '7test0', '7test1',
                '7test2', '7test3', '7test4', '7test5', '7test6', '7test7',
                '7test8', '7test9', '8test0', '8test1', '8test2', '8test3',
                '8test4', '8test5', '8test6', '8test7', '8test8', '8test9',
                '9test0', '9test1', '9test2', '9test3', '9test4', '9test5',
                '9test6', '9test7', '9test8', '9test9'
            ]
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
            "123test55",
            False,
            [
                '120test50', '120test51', '120test52', '120test53', '120test54',
                '120test55', '120test56', '120test57', '120test58', '120test59',
                '121test50', '121test51', '121test52', '121test53', '121test54',
                '121test55', '121test56', '121test57', '121test58', '121test59',
                '122test50', '122test51', '122test52', '122test53', '122test54',
                '122test55', '122test56', '122test57', '122test58', '122test59',
                '123test50', '123test51', '123test52', '123test53', '123test54',
                '123test55', '123test56', '123test57', '123test58', '123test59',
                '124test50', '124test51', '124test52', '124test53', '124test54',
                '124test55', '124test56', '124test57', '124test58', '124test59',
                '125test50', '125test51', '125test52', '125test53', '125test54',
                '125test55', '125test56', '125test57', '125test58', '125test59',
                '126test50', '126test51', '126test52', '126test53', '126test54',
                '126test55', '126test56', '126test57', '126test58', '126test59',
                '127test50', '127test51', '127test52', '127test53', '127test54',
                '127test55', '127test56', '127test57', '127test58', '127test59',
                '128test50', '128test51', '128test52', '128test53', '128test54',
                '128test55', '128test56', '128test57', '128test58', '128test59',
                '129test50', '129test51', '129test52', '129test53', '129test54',
                '129test55', '129test56', '129test57', '129test58', '129test59',
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

