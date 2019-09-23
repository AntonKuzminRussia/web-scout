# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of module ParamsBruterCombine
"""


from classes.modules.ParamsModules import ParamsModules
from classes.generators.CombineGenerator import CombineGenerator
from classes.modules.params.ParamsCombineModuleParams import ParamsCombineModuleParams


class ParamsCombine(ParamsModules):
    model = None
    mode = 'dict'
    log_path = '/dev/null'
    time_count = True
    options = ParamsCombineModuleParams().get_options()

    def load_objects(self, queue):
        """ Prepare generator for work """
        generator = CombineGenerator(
            self.options['mask'].value,
            self.options['dict'].value,
            int(self.options['parts'].value),
            int(self.options['part'].value),
            self.options['combine-template'].value
        )
        queue.set_generator(generator)
        return {'all': generator.lines_count, 'start': generator.first_border, 'end': generator.second_border}

