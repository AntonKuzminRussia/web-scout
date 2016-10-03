# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class for generate and work with masks
"""

import os

from classes.DictOfMask import DictOfMask
from classes.FileGenerator import FileGenerator
from classes.kernel.WSException import WSException


class CombineGenerator(object):
    """ Class for generate and work with masks """
    mask = None
    template = None
    mask_generator = None
    dict_generator = None
    first_border = 0
    second_border = 0
    lines_count = 0
    current_counter = 0
    current_dict_line = None

    def __init__(self, mask, dict_file, parts, part, template):
        if not template.count("%m%"):
            raise WSException("Template '{0}' not contains %m% (mask) marker ".format(template))
        if not template.count("%d%"):
            raise WSException("Template '{0}' not contains %d% (dict) marker ".format(template))

        if not os.path.exists(dict_file):
            raise WSException("Dict '{0}' not exists ".format(dict_file))

        self.template = template

        self.dict_generator = FileGenerator(dict_file)
        self.next_dict_line()

        self.mask = mask
        self.mask_generator = DictOfMask(mask)

        self.lines_count = self.dict_generator.lines_count * self.mask_generator.all_objects_count

        if parts and part:
            one_part_count = int(self.lines_count/parts)
            self.first_border = one_part_count * (part - 1)
            self.second_border = one_part_count * part

    def _get(self):
        mask = self.get_next_mask()
        if mask is None:
            self.next_dict_line()
            if self.current_dict_line is None:
                return None

            self.mask_generator = DictOfMask(self.mask)
            mask = self.get_next_mask()

        return self.template.replace("%m%", mask).replace("%d%", self.current_dict_line)

    def get(self):
        self.current_counter += 1
        to_return = self._get()

        if self.second_border:
            if self.current_counter <= self.first_border:
                return self.get()
            if self.current_counter > self.second_border:
                return None

        return to_return


    def get_next_mask(self):
        return self.mask_generator.get()

    def next_dict_line(self):
        self.current_dict_line = self.dict_generator.get()

    def get_dict_current_line(self):
        if not len(self.current_dict_line):
             self.next_dict_line()
        return self.current_dict_line