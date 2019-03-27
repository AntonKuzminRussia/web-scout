# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of module for DAFS by Dict+Mask
"""

from classes.modules.params.AbstractDnsModuleParams import AbstractDnsModuleParams


class DnsBruterDictModuleParams(AbstractDnsModuleParams):
    def __init__(self):
        AbstractDnsModuleParams.__init__(self)
        self.add_option('dict')
