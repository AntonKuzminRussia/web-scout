# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of roller list (get last element - next first element)
"""
import os


class Roller(object):
    """ Class of roller list (get last element - next first element) """
    fh = None
    first_line_flag = False
    file_name = None

    def __init__(self, file_name):
        self.file_name = file_name
        self.fh = open(file_name)
        if not os.path.exists(file_name):
            raise BaseException("File not found: " + file_name)

    def get(self):
        """ Method get next list item """
        line = self.fh.readline()
        if not line:
            if not self.first_line_flag:
                raise BaseException("File %s has not lines" % self.file_name)

            self.fh.seek(0)
            return self.get()

        self.first_line_flag = True
        return line
