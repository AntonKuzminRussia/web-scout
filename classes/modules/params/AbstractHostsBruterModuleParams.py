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


class AbstractHostsBruterModuleParams(AbstractModuleParams):
    def __init__(self):
        AbstractModuleParams.__init__(self)
        self.add_options(
            [
                'proxies',
                'delay',
                'template',
                'headers-file',
                "ignore-words-re",
                "retest-codes",
                "retest-phrase",
                'false-phrase',
                'false-size',
                'ip',
                'msymbol',
                'http-protocol',
            ]
        )
