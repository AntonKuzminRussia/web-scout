# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of module for DAFS by Dict+Mask
"""

from classes.modules.params.AbstractDafsModuleParams import AbstractDafsModuleParams


class DafsCombineModuleParams(AbstractDafsModuleParams):
    options = {}

    def __init__(self):
        AbstractDafsModuleParams.__init__(self)
        self.add_options(
            [
                'dict',
                'mask',
                'combine-template',
            ]
        )


