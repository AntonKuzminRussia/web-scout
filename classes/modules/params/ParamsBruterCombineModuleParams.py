# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Module params class
"""

from classes.modules.params.AbstractParamsBruterModule import AbstractParamsBruterModule


class ParamsBruterCombineModuleParams(AbstractParamsBruterModule):
    def __init__(self):
        AbstractParamsBruterModule.__init__(self)
        self.add_options(
            [
                'dict',
                'mask',
                'combine-template',
            ]
        )
