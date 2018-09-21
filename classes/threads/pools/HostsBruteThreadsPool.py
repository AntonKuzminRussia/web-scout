# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common module class form Dafs* modules
"""

from classes.threads.pools.AbstractPool import AbstractPool
from classes.threads.params.HostBruteThreadParams import HostBruteThreadParams
from classes.threads.HostsBruteThread import HostsBruteThread


class HostsBruteThreadsPool(AbstractPool):
    def build_threads_params(self):
        return HostBruteThreadParams(self.options)

    def born_thread(self):
        thrd = HostsBruteThread(self.queue, self.counter, self.result, self.threads_params)
        thrd.start()
        return thrd