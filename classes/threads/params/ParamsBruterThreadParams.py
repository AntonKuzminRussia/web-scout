# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common module class form Dafs* modules
"""


class ParamsBruterThreadParams:
    protocol = None
    host = None
    url = None
    max_params_length = None
    value = None
    method = None
    msymbol = None
    not_found_re = None
    not_found_size = None
    not_found_codes = None
    delay = None
    ddos_detect_phrase = None
    ddos_human_action = None
    browser_recreate_re = None
    ignore_words_re = None
    retest_codes = None

    def __init__(self, options):
        self.protocol = options['protocol'].value
        self.host = options['host'].value
        self.url = options['url'].value
        self.max_params_length = options['max-params-length'].value
        self.value = options['value'].value
        self.method = options['method'].value.lower()
        self.msymbol = options['msymbol'].value
        self.not_found_re = options['not-found-re'].value
        self.delay = options['delay'].value
        self.ddos_detect_phrase = options['ddos-detect-phrase'].value
        self.ddos_human_action = options['ddos-human-action'].value
        self.browser_recreate_re = options['browser-recreate-re'].value
        self.ignore_words_re = options['ignore-words-re'].value
        self.not_found_re = options['not-found-re'].value
        self.not_found_size = options['not-found-size'].value
        self.not_found_codes = options['not-found-codes'].value.lower()
        self.retest_codes = options['retest-codes'].value.lower()
