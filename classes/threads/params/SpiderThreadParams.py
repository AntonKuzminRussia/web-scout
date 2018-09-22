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


class SpiderThreadParams:
    host = None
    protocol = None
    not_found_re = None
    delay = None
    ddos_detect_phrase = None
    ddos_human_action = None
    browser_recreate_re = None

    def __init__(self, options):
        self.host = options['host'].value
        self.protocol = options['protocol'].value
        self.not_found_re = False if not len(options['not-found-re'].value) else re.compile(options['not-found-re'].value)
        self.delay = int(options['delay'].value)
        self.ddos_human_action = options['ddos-human-action'].value
        self.ddos_detect_phrase = options['ddos-detect-phrase'].value
        self.browser_recreate_re = False if not len(options['browser-recreate-re'].value) else re.compile(options['browser-recreate-re'].value)
