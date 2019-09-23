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


class FormsThreadParams:
    url = None
    false_re = None
    true_re = None
    delay = None
    browser_wait_re = None
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
    retest_re = None
    follow_redirects = False

    def __init__(self, options):
        self.url = options['url'].value
        self.false_re = False if not len(options['false-re'].value) else re.compile(options['false-re'].value)
        self.true_re = False if not len(options['true-re'].value) else re.compile(options['true-re'].value)
        self.delay = int(options['delay'].value)
        self.browser_wait_re = False if not len(options['browser-wait-re'].value) else re.compile(
            options['browser-wait-re'].value)
        self.browser_recreate_re = False if not len(options['browser-recreate-re'].value) else re.compile(
            options['browser-recreate-re'].value)
        self.conffile = options['conf-file'].value
        self.first_stop = options['first-stop'].value.lower()
        self.login = options['login'].value
        self.reload_form_page = int(options['reload-form-page'].value)
        self.pass_min_len = int(options['pass-min-len'].value)
        self.pass_max_len = int(options['pass-max-len'].value)
        self.confstr = options['conf-str'].value
        self.false_size = int(options['false-size'].value) if options['false-size'].value is not None else None #TODO make one, -1 or None
        self.retest_codes = list(set(options['retest-codes'].value.split(','))) if len(options['retest-codes'].value) else []
        self.retest_re = False if not len(options['retest-re'].value) else re.compile(options['retest-re'].value)
        self.follow_redirects = (options['follow-redirects'].value != "0")
