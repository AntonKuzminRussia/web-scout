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


class HostsThreadParams:
    protocol = None
    ip = None
    template = None
    msymbol = None
    false_re = None
    retest_codes = None
    delay = None
    ignore_words_re = None
    retest_re = None
    false_size = None

    def __init__(self, options):
        self.protocol = options['http-protocol'].value
        self.ip = options['ip'].value
        self.template = options['template'].value
        self.msymbol = options['msymbol'].value
        self.false_re = False if not len(options['false-re'].value) else re.compile(options['false-re'].value)
        self.retest_codes = list(set(options['retest-codes'].value.lower().split(','))) if len(options['retest-codes'].value.lower()) else []
        self.delay = int(options['delay'].value)
        self.ignore_words_re = False if not len(options['ignore-words-re'].value) else re.compile(options['ignore-words-re'].value)
        self.retest_re = False if not len(options['retest-re'].value) else re.compile(options['retest-re'].value)
        self.false_size = int(options['false-size'].value) if options['false-size'].value is not None else None
