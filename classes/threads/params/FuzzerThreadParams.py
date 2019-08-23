# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class with thread params
"""
from libs.common import file_to_list
from classes.Registry import Registry


class FuzzerThreadParams:
    method = None
    delay = None
    ddos_human_action = None
    browser_recreate_phrase = None
    bad_words = None
    headers = None

    def __init__(self, options):
        self.method = options['method'].value.lower()
        self.delay = int(options['delay'].value)
        if 'ddos-human-action' in options:
            self.ddos_human_action = options['ddos-human-action'].value
        if 'browser-recreate-phrase' in options:
            self.browser_recreate_phrase = options['browser-recreate-re'].value

        self.bad_words = file_to_list(Registry().get('wr_path') + "/bases/fuzzer/bad-words.txt")
        self.headers = file_to_list(Registry().get('wr_path') + "/bases/fuzzer/headers.txt")
        self.retest_codes = list(set(options['retest-codes'].value.split(','))) if len(options['retest-codes'].value) else []
        self.retest_phrase = options['retest-phrase'].value if len(options['retest-phrase'].value) else None
