# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of WS Module for DNS Brute by dict
"""

import os

from classes.kernel.WSException import WSException
from classes.modules.DnsBruteModules import DnsBruteModules
from classes.generators.FileGenerator import FileGenerator
from classes.modules.params.DnsBruteDictModuleParams import DnsBruteDictModuleParams


class DnsBruteDict(DnsBruteModules):
    """ Class of WS Module for DNS Brute by dict """
    model = None
    mode = 'dict'
    log_path = '/dev/null'
    time_count = True
    options = DnsBruteDictModuleParams().get_options()

    def load_objects(self, queue):
        """ Make generator with objects to check """
        generator = FileGenerator(
            self.options['dict'].value,
            int(self.options['parts'].value),
            int(self.options['part'].value)
        )
        queue.set_generator(generator)
        return {'all': generator.lines_count, 'start': generator.first_border, 'end': generator.second_border}
