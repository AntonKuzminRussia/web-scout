# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common module class form Dafs* modules
"""
import re


class HostBruteThreadParams:
    protocol = None
    ip = None
    template = None
    msymbol = None
    false_phrase = None
    retest_codes = None
    delay = None
    ignore_words_re = None
    retest_phrase = None
    false_size = None

    def __init__(self, options):
        self.protocol = options['protocol'].value
        self.ip = options['ip'].value
        self.template = options['template'].value
        self.msymbol = options['msymbol'].value
        self.false_phrase = options['false-phrase'].value
        self.retest_codes = list(set(options['retest-codes'].value.lower().split(','))) if len(options['retest-codes'].value.lower()) else []
        self.delay = int(options['delay'].value)
        self.ignore_words_re = False if not len(options['ignore-words-re'].value) else re.compile(options['ignore-words-re'].value)
        self.retest_phrase = options['retest-phrase'].value if len(options['retest-phrase'].value) else None
        self.false_size = int(options['false-size'].value) if options['false-size'].value is not None else None
