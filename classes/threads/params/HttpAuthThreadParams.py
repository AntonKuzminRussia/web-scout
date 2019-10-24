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


class HttpAuthThreadParams:
    url = None
    delay = None
    login = None
    pass_min_len = None
    pass_max_len = None
    retest_codes = None
    retest_re = None

    def __init__(self, options):
        self.url = options['url'].value
        self.delay = int(options['delay'].value)
        self.first_stop = options['first-stop'].value.lower()
        self.login = options['login'].value
        self.pass_min_len = int(options['pass-min-len'].value)
        self.pass_max_len = int(options['pass-max-len'].value)
        self.retest_codes = list(set(options['retest-codes'].value.split(','))) if len(options['retest-codes'].value) else []
        self.retest_re = False if not len(options['retest-re'].value) else re.compile(options['retest-re'].value)

