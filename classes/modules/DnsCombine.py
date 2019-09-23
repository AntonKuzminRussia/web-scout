# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of WS Module for DNS Brute by dict+mask
"""

from classes.modules.DnsModules import DnsBruterModules
from classes.generators.CombineGenerator import CombineGenerator
from classes.modules.params.DnsCombineModuleParams import DnsCombineModuleParams


class DnsCombine(DnsBruterModules):
    """ Class of WS Module for DNS Brute by dict+mask """
    model = None
    mode = 'dict'
    log_path = '/dev/null'
    time_count = True
    options = DnsCombineModuleParams().get_options()

    def load_objects(self, queue):
        """ Make generator with objects to check """
        generator = CombineGenerator(
            self.options['mask'].value,
            self.options['dict'].value,
            int(self.options['parts'].value),
            int(self.options['part'].value),
            self.options['combine-template'].value
        )
        queue.set_generator(generator)
        return {'all': generator.lines_count, 'start': generator.first_border, 'end': generator.second_border}
