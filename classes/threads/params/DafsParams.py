# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class with thread params
"""
import re


class DafsParams:
    template = None
    method = None
    msymbol = None
    not_found_re = None
    found_re = None
    not_found_ex = None
    not_found_size = None
    not_found_codes = None
    retest_codes = None
    delay = None
    browser_wait_re = None
    browser_recreate_re = None
    ignore_words_re = None
    retest_re = None

    def __init__(self, options):
        self.template = options['template'].value
        self.msymbol = options['msymbol'].value
        self.delay = int(options['delay'].value)
        self.not_found_re = False if not len(options['not-found-re'].value) else re.compile(options['not-found-re'].value)
        self.found_re = False if not len(options['found-re'].value) else re.compile(options['found-re'].value)
        self.not_found_ex = False if not len(options['not-found-ex'].value) else options['not-found-ex'].value
        self.not_found_size = int(options['not-found-size'].value)
        self.browser_wait_re = False if not len(options['browser-wait-re'].value) else re.compile(options['browser-wait-re'].value)
        self.browser_recreate_re = False if not len(options['browser-recreate-re'].value) else re.compile(options['browser-recreate-re'].value)
        self.ignore_words_re = False if not len(options['ignore-words-re'].value) else re.compile(options['ignore-words-re'].value)
        self.method = options['method'].value.lower()

        if self.method == 'head' and (self.not_found_re or self.not_found_size != -1):
            self.method = 'get'

        not_found_codes = options['not-found-codes'].value.split(',')
        self.not_found_codes = list(set(not_found_codes))

        self.retest_codes = list(set(options['retest-codes'].value.split(','))) if len(options['retest-codes'].value) else []
        self.retest_re = False if not len(options['retest-re'].value) else re.compile(options['retest-re'].value)
