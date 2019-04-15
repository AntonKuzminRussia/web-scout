# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common module class form HostsBrute* modules
"""
import time

from classes.Registry import Registry
from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.kernel.WSCounter import WSCounter
from classes.jobs.HostsBruteJob import HostsBruteJob
from classes.threads.pools.HostsBruterThreadsPool import HostsBruterThreadsPool
from classes.ErrorsCounter import ErrorsCounter


class HostsBruterModules(WSModule):
    """ Common module class form HostsBrute* modules """
    logger_enable = True
    logger_name = 'hosts'
    logger_have_items = True
    logger_scan_name_option = 'template'

    def validate_main(self):
        """ Check users params """
        super(HostsBruterModules, self).validate_main()

        if (not self.options['false-phrase'].value or not len(self.options['false-phrase'].value)) and (not self.options['false-size'].value or not len(self.options['false-size'].value)):
            raise WSException(
                "You must specify --false-phrase param or --false-size param!"
            )

    def make_queue(self):
        self.queue = HostsBruteJob()

        loaded = self.load_objects(self.queue)

        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )

        self.counter = WSCounter.factory(loaded['all'] if not loaded['end'] else loaded['end']-loaded['start'])

    def start_pool(self):
        pool = HostsBruterThreadsPool(self.queue, self.counter, self.result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if self.is_critical_stop():
                pool.kill_all()
            time.sleep(1)

    def output(self):
        WSModule.output(self)

        self.logger.log("\nFound {0} hosts:".format(len(self.result)))
        for host in self.result:
            self.logger.log("\t" + host)

