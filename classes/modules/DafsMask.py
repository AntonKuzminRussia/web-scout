# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of module for DAFS by mask
"""

from classes.DictOfMask import DictOfMask
from classes.modules.DafsModules import DafsModules
from classes.modules.params.DafsMaskModuleParams import DafsMaskModuleParams


class DafsMask(DafsModules):
    """ Class of module for DAFS by mask """
    model = None
    mode = 'mask'
    log_path = '/dev/null'
    time_count = True
    options = DafsMaskModuleParams.options

    def load_objects(self, queue):
        """ Prepare generator for work """
        dom = DictOfMask(self.options['mask'].value, int(self.options['parts'].value), int(self.options['part'].value))

        queue.set_generator(dom)
        return {'all': dom.all_objects_count, 'start': dom.first_border, 'end': dom.second_border}
