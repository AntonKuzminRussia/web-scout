# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of Spider module
"""

from classes.threads.pools.AbstractPool import AbstractPool
from classes.threads.SpiderThread import SpiderThread
from classes.threads.SSpiderThread import SSpiderThread
from classes.threads.params.SpiderThreadParams import SpiderThreadParams


class SpiderThreadsPool(AbstractPool):
    src = None

    def __init__(self, queue, counter, src, options, logger):
        AbstractPool.__init__(self, queue, counter, None, options, logger)
        self.src = src

    def build_threads_params(self):
        return SpiderThreadParams(self.options)

    def born_thread(self):
        if self.options['selenium'].value:
            thrd = SSpiderThread(self.queue, self.src, self.counter, self.threads_params)
        else:
            thrd = SpiderThread(self.queue, self.src, self.counter, self.threads_params)
        thrd.start()
        return thrd