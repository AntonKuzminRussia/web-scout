# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Module params class
"""

from classes.modules.params.AbstractFuzzerModuleParams import AbstractFuzzerModuleParams


class FuzzerUrlsModuleParams(AbstractFuzzerModuleParams):
    def __init__(self):
        AbstractFuzzerModuleParams.__init__(self)
        self.add_options(
            [
                "ddos-detect-phrase",
                "ddos-human-action",
                "selenium",
            ]
        )
        self.add_option("browser-recreate-re")
