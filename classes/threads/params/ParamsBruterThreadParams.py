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


class ParamsBruterThreadParams:
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
    retest_phrase = None

    def __init__(self, options):
        self.url = options['url'].value
        self.max_params_length = int(options['max-params-length'].value)
        self.value = options['value'].value
        self.method = options['params-method'].value.lower()
        self.not_found_re = options['not-found-re'].value
        self.delay = int(options['delay'].value)
        self.ddos_detect_phrase = options['ddos-detect-phrase'].value
        self.ddos_human_action = options['ddos-human-action'].value
        self.browser_recreate_re = options['browser-recreate-re'].value
        self.ignore_words_re = False if not len(options['ignore-words-re'].value) else re.compile(options['ignore-words-re'].value)
        self.not_found_re = False if not len(options['not-found-re'].value) else re.compile(options['not-found-re'].value)
        self.not_found_size = int(options['not-found-size'].value)

        not_found_codes = options['not-found-codes'].value.split(',')
        not_found_codes.append('404')
        self.not_found_codes = list(set(not_found_codes))

        self.retest_codes = list(set(options['retest-codes'].value.split(','))) if len(options['retest-codes'].value) else []
        self.retest_phrase = options['retest-phrase'].value if len(options['retest-phrase'].value) else None
