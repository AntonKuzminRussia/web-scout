# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class with thread params
"""


class FormBruterThreadParams:
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
    retest_phrase = None
    follow_redirects = False

    def __init__(self, options):
        self.url = options['url'].value
        self.false_phrase = options['false-phrase'].value
        self.true_phrase = options['true-phrase'].value
        self.delay = int(options['delay'].value)
        self.ddos_human_action = options['ddos-human-action'].value
        self.ddos_detect_phrase = options['ddos-detect-phrase'].value
        self.browser_recreate_phrase = options['browser-recreate-re'].value
        self.conffile = options['conf-file'].value
        self.first_stop = options['first-stop'].value.lower()
        self.login = options['login'].value
        self.reload_form_page = int(options['reload-form-page'].value)
        self.pass_min_len = int(options['pass-min-len'].value)
        self.pass_max_len = int(options['pass-max-len'].value)
        self.confstr = options['conf-str'].value
        self.false_size = int(options['false-size'].value) if options['false-size'].value is not None else None
        self.retest_codes = list(set(options['retest-codes'].value.split(','))) if len(options['retest-codes'].value) else []
        self.retest_phrase = options['retest-phrase'].value if len(options['retest-phrase'].value) else None
        self.follow_redirects = (options['follow-redirects'].value != "0")
