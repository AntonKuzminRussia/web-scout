# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common module class form Dafs* modules
"""


class DafsThreadParams:
    protocol = None
    host = None
    template = None
    method = None
    msymbol = None
    not_found_re = None
    not_found_ex = None
    not_found_size = None
    not_found_codes = None
    retest_codes = None
    delay = None
    ddos_detect_phrase = None
    ddos_human_action = None
    browser_recreate_re = None
    ignore_words_re = None

    def __init__(self, options):
        self.protocol = options['protocol'].value.lower()
        self.host = options['host'].value
        self.template = options['template'].value
        self.method = options['method'].value.lower()
        self.msymbol = options['msymbol'].value
        self.delay = options['delay'].value
        self.not_found_re = options['not-found-re'].value
        self.not_found_ex = options['not-found-ex'].value
        self.not_found_size = options['not-found-size'].value
        self.not_found_codes = options['not-found-codes'].value
        self.ddos_detect_phrase = options['ddos-detect-phrase'].value
        self.ddos_human_action = options['ddos-human-action'].value
        self.browser_recreate_re = options['browser-recreate-re'].value
        self.ignore_words_re = options['ignore-words-re'].value
        self.retest_codes = options['retest-codes'].value
