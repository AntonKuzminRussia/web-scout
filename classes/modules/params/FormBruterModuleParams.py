# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of module for DAFS by Dict+Mask
"""
from classes.modules.params.AbstractModuleParams import AbstractModuleParams


class FormBruterModuleParams(AbstractModuleParams):
    def __init__(self):
        AbstractModuleParams.__init__(self)
        self.add_options(
            [
                'url',
                'false-phrase',
                'true-phrase',
                'false-size',
                "retest-codes",
                "retest-phrase",
                'delay',
                'selenium',
                "ddos-detect-phrase",
                "ddos-human-action",
                "reload-form-page",
                'proxies',
                "confstr",
                "conffile",
                'dict',
                'login',
                "headers-file",
                "pass-min-len",
                "pass-max-len",
                'first-stop',
                'follow-redirects',
            ]
        )
        self.add_option("browser-recreate-re", "browser-recreate-phrase")
