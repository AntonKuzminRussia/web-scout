# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Abstract class for worker threads
"""

import threading

from classes.Registry import Registry


class AbstractThread(threading.Thread):
    daemon = True

    last_action = 0
    logger = None
    queue = None
    counter = None
    result = None

    done = False

    retest_delay = None
    retest_limit = None

    def __init__(self):
        threading.Thread.__init__(self)

        self.logger = Registry().get('logger')

        self.retest_limit = int(Registry().get('config')['main']['retest_limit'])
        self.retest_delay = int(Registry().get('config')['main']['retest_delay'])

    def xml_log(self, data):
        """ Put data to xml log """
        if Registry().isset('xml'):
            Registry().get('xml').put_result(data)

    def is_test(self):
        """ Is test mode enabled? """
        return Registry().isset('tester')

    def is_test_done(self):
        """ Is test mode done? """
        return Registry().get('tester').done()

    def test_put(self, item, data):
        """ Put data in tester (in test mode) """
        Registry().get('tester').put(item, data)
        if self.is_test_done():
            self.done = True
