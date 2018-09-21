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

from classes.Registry import Registry
from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.kernel.WSCounter import WSCounter
from classes.jobs.DafsJob import DafsJob
from classes.threads.pools.DafsThreadsPool import DafsThreadsPool


class DafsModules(WSModule):
    """ Common module class form Dafs* modules """
    logger_enable = True
    logger_name = 'dafs'
    logger_have_items = True

    def load_objects(self, queue):
        """ Method for prepare check objects, here abstract """
        pass

    def validate_main(self):
        """ Check users params """
        super(DafsModules, self).validate_main()

        if self.options['template'].value[0] != '/':
            raise WSException("Template must start from the root ('/') !")

    def do_work(self):
        """ Scan action of module """
        self.enable_logger()
        self.validate_main()
        self.pre_start_inf()

        if self.options['proxies'].value:
            Registry().get('proxies').load(self.options['proxies'].value)

        if self.options['template'].value.find(self.options['msymbol'].value) == -1:
            raise WSException(
                "Symbol of object position ({0}) not found in URL ({1}) ".
                format(self.options['msymbol'].value, self.options['template'].value)
            )

        result = []

        queue = DafsJob()

        loaded = self.load_objects(queue)

        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )

        counter = WSCounter(5, 300, loaded['all'] if not loaded['end'] else loaded['end']-loaded['start'])

        pool = DafsThreadsPool(queue, counter, result, self.options, self.logger)
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

        self.logger.log("\n")
        for result_row in result:
            self.logger.log("{0} {1}".format(result_row['code'], result_row['url']))

        self.done = True
