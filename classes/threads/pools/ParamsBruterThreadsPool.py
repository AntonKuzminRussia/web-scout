# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class
"""

from classes.threads.ParamsBruterThread import ParamsBruterThread
from classes.threads.SParamsBruterThread import SParamsBruterThread
from classes.threads.params.ParamsBruterThreadParams import ParamsBruterThreadParams
from classes.threads.pools.AbstractPool import AbstractPool


class ParamsBruterThreadsPool(AbstractPool):
    def build_threads_params(self):
        return ParamsBruterThreadParams(self.options)

    def born_thread(self):
        thrd = ParamsBruterThread(self.queue, self.counter, self.result, self.threads_params)
        # if self.options['selenium'].value:
        #     thrd = SParamsBruterThread(self.queue, self.counter, self.result, self.threads_params)
        # else:
        #     thrd = ParamsBruterThread(self.queue, self.counter, self.result, self.threads_params)
        thrd.start()
        return thrd