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


class PreModuleParams(AbstractModuleParams):
    def __init__(self):
        AbstractModuleParams.__init__(self)
        self.add_options(
            [
                'host',
                'url',
                "not-found-codes",
                'proxies',
                "headers-file",
                'dns',
            ]
        )
        self.add_option('http-protocol')
        self.add_option("not-found-re")
