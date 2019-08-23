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


class AbstractDafsModuleParams(AbstractModuleParams):
    def __init__(self):
        AbstractModuleParams.__init__(self)
        self.add_options(
            [
                'msymbol',
                'not-found-re',
                'found-re',
                'not-found-ex',
                'not-found-size',
                'not-found-codes',
                'ignore-words-re',
                'retest-codes',
                'retest-phrase',
                'delay',
                'selenium',
                'browser-wait-re',
                'browser-recreate-re',
                'proxies',
                'headers-file',
                'template',
                'method',
            ]
        )
