# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class
"""

from classes.threads.DafsThread import DafsThread
from classes.threads.SDafsThread import SDafsThread
from classes.threads.params.DafsThreadParams import DafsThreadParams
from classes.threads.pools.AbstractPool import AbstractPool


class DafsThreadsPool(AbstractPool):
    def build_threads_params(self):
        return DafsThreadParams(self.options)

    def born_thread(self):
        if self.options['selenium'].value:
            thrd = SDafsThread(self.queue, self.counter, self.result, self.threads_params)
        else:
            thrd = DafsThread(self.queue, self.counter, self.result, self.threads_params)
        thrd.start()
        return thrd

