# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class for Dafs* modules
"""
import time

from classes.kernel.WSModule import WSModule
from classes.kernel.WSCounter import WSCounter
from classes.jobs.DafsJob import DafsJob
from classes.threads.pools.DafsThreadsPool import DafsThreadsPool


class DafsModules(WSModule):
    """ Common module class form Dafs* modules """
    logger_enable = True
    logger_name = 'dafs'
    logger_have_items = True

    def make_queue(self):
        self.queue = DafsJob()

        loaded = self.load_objects(self.queue)

        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )

        self.counter = WSCounter.factory(loaded['all'] if not loaded['end'] else loaded['end'] - loaded['start']
        )

    def start_pool(self):
        pool = DafsThreadsPool(self.queue, self.counter, self.result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if self.is_critical_stop():
                pool.kill_all()
            time.sleep(1)

    def output(self):
        WSModule.output(self)

        self.logger.log("\n")
        for result_row in self.result:
            self.logger.log("{0} {1}".format(result_row['code'], result_row['url']))
