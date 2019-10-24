# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class
"""

from classes.threads.HttpAuthThread import HttpAuthThread
from classes.threads.pools.AbstractPool import AbstractPool
from classes.threads.params.HttpAuthThreadParams import HttpAuthThreadParams


class HttpAuthThreadsPool(AbstractPool):
    def __init__(self, queue, counter, result, options, logger):
        AbstractPool.__init__(self, queue, counter, result, options, logger)

    def born_thread(self):
        thrd = HttpAuthThread(self.queue, self.counter, self.result, self.threads_params)
        thrd.start()
        return thrd

    def build_threads_params(self):
        return HttpAuthThreadParams(self.options)