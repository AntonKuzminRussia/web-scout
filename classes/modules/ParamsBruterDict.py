# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of module for DAFS by Dict
"""

from classes.modules.ParamsBruterModules import ParamsBruterModules
from classes.generators.FileGenerator import FileGenerator
from classes.modules.params.ParamsBruterDictModuleParams import ParamsBruterDictModuleParams


class ParamsBruterDict(ParamsBruterModules):
    """ Class of module for DAFS by Dict """
    model = None
    mode = 'dict'
    log_path = '/dev/null'
    time_count = True
    options = ParamsBruterDictModuleParams().get_options()

    def load_objects(self, queue):
        """ Prepare generator for work """
        generator = FileGenerator(
            self.options['dict'].value,
            int(self.options['parts'].value),
            int(self.options['part'].value)
        )
        queue.set_generator(generator)
        return {'all': generator.lines_count, 'start': generator.first_border, 'end': generator.second_border}
