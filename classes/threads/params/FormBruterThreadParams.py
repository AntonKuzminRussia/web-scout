# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common module class form Dafs* modules
"""


class FormBruterThreadParams:
    protocol = None
    host = None
    url = None
    false_phrase = None
    true_phrase = None
    delay = None
    ddos_detect_phrase = None
    ddos_human_action = None
    browser_recreate_phrase = None
    conffile = None
    first_stop = None
    login = None
    reload_form_page = None
    pass_min_len = None
    pass_max_len = None
    confstr = None
    false_size = None
    retest_codes = None

    def __init__(self, options):
        self.protocol = options['protocol'].value
        self.host = options['host'].value
        self.url = options['url'].value
        self.false_phrase = options['false-phrase'].value
        self.true_phrase = options['true-phrase'].value
        self.delay = options['delay'].value
        self.ddos_human_action = options['ddos-human-action'].value
        self.ddos_detect_phrase = options['ddos-detect-phrase'].value
        self.browser_recreate_phrase = options['browser-recreate-phrase'].value
        self.conffile = options['conffile'].value
        self.first_stop = options['first-stop'].value.lower()
        self.login = options['login'].value
        self.reload_form_page = options['reload-form-page'].value
        self.pass_min_len = options['pass-min-len'].value
        self.pass_max_len = options['pass-max-len'].value
        self.confstr = options['confstr'].value
        self.false_size = options['false-size'].value
        self.retest_codes = options['retest-codes'].value
