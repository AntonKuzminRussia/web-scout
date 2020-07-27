# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of FuzzerHeaders module
"""

import time

from classes.modules.FuzzerModules import FuzzerModules
from classes.jobs.FuzzerHeadersJob import FuzzerHeadersJob
from classes.kernel.WSCounter import WSCounter
from classes.kernel.WSModule import WSModule
from classes.threads.pools.FuzzerHeadersThreadPool import FuzzerHeadersThreadsPool
from classes.modules.params.FuzzerHeadersModuleParams import FuzzerHeadersModuleParams
from classes.generators.FileGenerator import FileGenerator


class FuzzerHeaders(FuzzerModules):
    """ Class of FuzzerHeaders module """
    model = None
    log_path = '/dev/null'
    time_count = True
    logger_enable = True
    logger_name = 'fuzzer-headers'
    logger_have_items = True
    options = FuzzerHeadersModuleParams().get_options()

    def make_queue(self):
        """
        Make work queue
        :return:
        """
        self.queue = FuzzerHeadersJob()
        generator = FileGenerator(self.options['urls-file'].value)

        self.queue.set_generator(generator)
        self.logger.log("Loaded {0} variants.".format(generator.lines_count))

        self.counter = WSCounter.factory(generator.lines_count)

    def start_pool(self):
        """ Start threads pool and control it live """
        pool = FuzzerHeadersThreadsPool(self.queue, self.counter, self.result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if self.is_critical_stop():
                pool.kill_all()
            time.sleep(1)

    def output(self):
        """
        Output in the end of work
        :return:
        """
        WSModule.output(self)

        self.logger.log("")
        for fuzz in self.result:
            self.logger.log("\t{0} (Word(s): {1}, Header: {2})".format(
                fuzz['url'],
                ", ".join(fuzz['words']),
                fuzz['header']
            ))
