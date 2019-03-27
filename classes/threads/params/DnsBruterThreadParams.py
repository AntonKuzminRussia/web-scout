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


class DnsBruterThreadParams:
    template = None
    protocol = None
    msymbol = None
    ignore_ip = None
    delay = None
    http_not_found_re = None
    http_protocol = None
    http_retest_phrase = None
    ignore_words_re = None
    zone = None

    def __init__(self, options):
        self.template = options['template'].value
        self.msymbol = options['msymbol'].value
        self.ignore_ip = options['ignore-ip'].value
        self.delay = int(options['delay'].value)
        self.http_not_found_re = re.compile(options['http-not-found-re'].value) if len(options['http-not-found-re'].value) else None
        self.http_protocol = options['http-protocol'].value
        self.http_retest_phrase = options['http-retest-phrase'].value
        self.ignore_words_re = False if not len(options['ignore-words-re'].value) else re.compile(options['ignore-words-re'].value)
        self.zone = options['zone'].value.upper()
