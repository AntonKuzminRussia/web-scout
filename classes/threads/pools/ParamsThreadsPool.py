# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class
"""

from classes.threads.ParamsRawThread import ParamsRawThread
from classes.threads.ParamsSeleniumThread import ParamsSeleniumThread
from classes.threads.params.ParamsThreadParams import ParamsThreadParams
from classes.threads.pools.AbstractPool import AbstractPool


class ParamsThreadsPool(AbstractPool):
    def build_threads_params(self):
        return ParamsThreadParams(self.options)

    def born_thread(self):
        thrd = ParamsRawThread(self.queue, self.counter, self.result, self.threads_params)
        # if self.options['selenium'].value:
        #     thrd = SParamsBruterThread(self.queue, self.counter, self.result, self.threads_params)
        # else:
        #     thrd = ParamsBruterThread(self.queue, self.counter, self.result, self.threads_params)
        thrd.start()
        return thrd