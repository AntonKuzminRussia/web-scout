# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class
"""

from classes.threads.pools.AbstractPool import AbstractPool
from classes.threads.params.HostsThreadParams import HostsThreadParams
from classes.threads.HostsRawThread import HostsRawThread


class HostsThreadsPool(AbstractPool):
    def build_threads_params(self):
        return HostsThreadParams(self.options)

    def born_thread(self):
        thrd = HostsRawThread(self.queue, self.counter, self.result, self.threads_params)
        thrd.start()
        return thrd