# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of WS Module for DNS Brute by mask
"""

from classes.generators.DictOfMask import DictOfMask
from classes.modules.DnsBruteModules import DnsBruteModules
from classes.modules.params.DnsBruteMaskModuleParams import DnsBruteMaskModuleParams


class DnsBruteMask(DnsBruteModules):
    """ Class of WS Module for DNS Brute by mask """
    model = None
    mode = 'dict'
    log_path = '/dev/null'
    time_count = True
    options = DnsBruteMaskModuleParams().get_options()

    def load_objects(self, queue):
        """ Make generator with objects to check """
        dom = DictOfMask(self.options['mask'].value, int(self.options['parts'].value), int(self.options['part'].value))
        queue.set_generator(dom)
        return {'all': dom.all_objects_count, 'start': dom.first_border, 'end': dom.second_border}


