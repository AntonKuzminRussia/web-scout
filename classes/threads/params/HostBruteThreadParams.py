# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common module class form Dafs* modules
"""


class HostBruteThreadParams:
    protocol = None
    host = None
    template = None
    msymbol = None
    false_phrase = None
    retest_codes = None
    delay = None
    ignore_words_re = None

    def __init__(self, options):
        self.protocol = options['protocol'].value
        self.host = options['host'].value
        self.template = options['template'].value
        self.msymbol = options['msymbol'].value
        self.false_phrase = options['false-phrase'].value
        self.retest_codes = options['retest-codes'].value.lower()
        self.delay = options['delay'].value
        self.ignore_words_re = options['ignore-words-re'].value
