# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class for test run
"""

from classes.Registry import Registry

class Tester:
    """ Class for test run """
    items = None
    display_items_content = None
    requests_count = None

    def __init__(self):
        self.display_items_content = bool(int(Registry().get('config')['test']['display_items_content']))
        self.requests_count = int(Registry().get('config')['test']['requests_count'])
        self.items = {}

    def done(self):
        """ Is test done? """
        return len(self.items) >= self.requests_count

    def put(self, name, props):
        """ Put new data for item """
        if not self.done():
            if name in self.items.keys():
                self.items[name].update(props)
            else:
                self.items[name] = props

    def dump(self):
        """ Dump all collected data to stdout """
        for item in self.items.keys():
            if not self.display_items_content and "content" in self.items[item].keys():
                del self.items[item]["content"]

            print "{0} => {1}".format(item, self.items[item])