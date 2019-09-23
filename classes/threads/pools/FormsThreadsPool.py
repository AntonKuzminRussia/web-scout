# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class
"""

from classes.threads.FormsRawThread import FormsRawThread
from classes.threads.FormsSeleniumThread import FormsSeleniumThread
from classes.threads.pools.AbstractPool import AbstractPool
from classes.threads.params.FormsThreadParams import FormsThreadParams


class FormsThreadsPool(AbstractPool):
    def __init__(self, queue, counter, result, options, logger):
        AbstractPool.__init__(self, queue, counter, result, options, logger)

    def born_thread(self):
        if self.options['selenium'].value:
            thrd = FormsSeleniumThread(self.queue, self.counter, self.result, self.threads_params)
        else:
            thrd = FormsRawThread(self.queue, self.counter, self.result, self.threads_params)
        thrd.start()
        return thrd

    def build_threads_params(self):
        return FormsThreadParams(self.options)