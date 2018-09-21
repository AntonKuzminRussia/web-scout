# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class for FormBruter module
"""

from classes.threads.FormBruterThread import FormBruterThread
from classes.threads.SFormBruterThread import SFormBruterThread
from classes.threads.pools.AbstractPool import AbstractPool
from classes.threads.params.FormBruterThreadParams import FormBruterThreadParams


class FormBruterThreadsPool(AbstractPool):
    def __init__(self, queue, counter, result, pass_found, options, logger):
        AbstractPool.__init__(self, queue, counter, result, options, logger)
        self.pass_found = pass_found

    def born_thread(self):
        if self.options['selenium'].value:
            thrd = SFormBruterThread(self.queue, self.pass_found, self.counter, self.result, self.threads_params)
        else:
            thrd = FormBruterThread(self.queue, self.pass_found, self.counter, self.result, self.threads_params)
        thrd.start()
        return thrd

    def build_threads_params(self):
        return FormBruterThreadParams(self.options)