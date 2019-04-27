# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class
"""

from classes.threads.params.FuzzerThreadParams import FuzzerThreadParams
from classes.threads.pools.AbstractPool import AbstractPool
from classes.threads.SFuzzerUrlsThread import SFuzzerUrlsThread
from classes.threads.FuzzerUrlsThread import FuzzerUrlsThread


class FuzzerUrlsThreadsPool(AbstractPool):
    def build_threads_params(self):
        return FuzzerThreadParams(self.options)

    def born_thread(self):
        if self.options['selenium'].value:
            thrd = SFuzzerUrlsThread(self.queue, self.counter, self.result, self.threads_params)
        else:
            thrd = FuzzerUrlsThread(self.queue, self.counter, self.result, self.threads_params)
        thrd.start()
        return thrd

