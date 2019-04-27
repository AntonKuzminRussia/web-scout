# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class
"""

from classes.threads.FuzzerHeadersThread import FuzzerHeadersThread
from classes.threads.params.FuzzerThreadParams import FuzzerThreadParams
from classes.threads.pools.AbstractPool import AbstractPool


class FuzzerHeadersThreadsPool(AbstractPool):
    def build_threads_params(self):
        return FuzzerThreadParams(self.options)

    def born_thread(self):
        thrd = FuzzerHeadersThread(self.queue, self.counter, self.result, self.threads_params)
        thrd.start()
        return thrd

