# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Alexey Meshcheryakov <tank1st99@gmail.com>

Kernel class for modules results
"""


class WSResult(object):
    results = None

    def __init__(self):
        self.results = []

    def put(self, item):
        """ Put item to results """
        self.results.append(item)
        return self

    def as_string(self):
        """ Return results as string """
        result = ""
        for row in self.results:
            result += row + "\n"
        return result

    def get_all(self):
        """ Get list of all results """
        return self.results

    def unique(self):
        """ Remove dups from results list """
        self.results = list(set(self.results))
        return self
