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
from classes.threads.pools.HostsBruteThreadsPool import HostsBruteThreadsPool


class HostsBruteModules(WSModule):
    """ Common module class form HostsBrute* modules """
    logger_enable = True
    logger_name = 'hosts'
    logger_have_items = True

    def load_objects(self, queue):
        """ Method for prepare check objects, here abstract """
        pass

    def validate_main(self):
        """ Check users params """
        super(HostsBruteModules, self).validate_main()

        if not self.options['template'].value.count(self.options['msymbol'].value):
            raise WSException(
                "Template '{0}' not contains msymbol ({1})".format(
                    self.options['template'].value,
                    self.options['msymbol'].value
                )
            )

    def do_work(self):
        """ Brute action of module """
        self.enable_logger()
        self.validate_main()
        self.pre_start_inf()

        if self.options['proxies'].value:
            Registry().get('proxies').load(self.options['proxies'].value)

        result = []

        queue = HostsBruteJob()

        loaded = self.load_objects(queue)

        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )

        counter = WSCounter(5, 300, loaded['all'] if not loaded['end'] else loaded['end']-loaded['start'])

        pool = HostsBruteThreadsPool(queue, counter, result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if Registry().get('positive_limit_stop'):
                pool.kill_all()
            time.sleep(1)

        if Registry().get('proxy_many_died'):
            self.logger.log("Proxy many died, stop scan")

        if Registry().get('positive_limit_stop'):
            self.logger.log("\nMany positive detections. Please, look items logs")
            self.logger.log("Last items:")
            for i in range(1, 5):
                print result[-i]
            exit(1)

        self.logger.log("\nFound {0} hosts:".format(len(result)))
        for host in result:
            self.logger.log("\t" + host)

        self.done = True
