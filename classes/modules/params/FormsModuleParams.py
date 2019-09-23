# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Module params class
"""

from classes.modules.params.AbstractModuleParams import AbstractModuleParams


class FormsModuleParams(AbstractModuleParams):
    def __init__(self):
        AbstractModuleParams.__init__(self)
        self.add_options(
            [
                'url',
                'false-re',
                'true-re',
                'false-size',
                "retest-codes",
                "retest-re",
                'delay',
                'selenium',
                "browser-wait-re",
                "reload-form-page",
                'proxies',
                "conf-str",
                "conf-file",
                'dict',
                'login',
                "headers-file",
                "pass-min-len",
                "pass-max-len",
                'first-stop',
                'follow-redirects',
            ]
        )
        self.add_option("browser-recreate-re")
