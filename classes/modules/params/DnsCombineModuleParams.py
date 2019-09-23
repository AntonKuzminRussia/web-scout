# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Module params class
"""

from classes.modules.params.AbstractDnsModuleParams import AbstractDnsModuleParams


class DnsCombineModuleParams(AbstractDnsModuleParams):
    def __init__(self):
        AbstractDnsModuleParams.__init__(self)
        self.add_options(
            [
                'mask',
                'dict',
                'combine-template'
            ]
        )
