# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common module class form Dafs* modules
"""
import time

from classes.Registry import Registry
from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.kernel.WSCounter import WSCounter
from classes.jobs.ParamsBruterJob import ParamsBruterJob
from classes.threads.pools.ParamsBruterThreadsPool import ParamsBruterThreadsPool
from classes.ErrorsCounter import ErrorsCounter


class ParamsBruterModules(WSModule):
    """ Common module class form Dafs* modules """
    logger_enable = True
    logger_name = 'params-bruter'
    logger_have_items = True

    def validate_main(self):
        """ Check users params """
        super(ParamsBruterModules, self).validate_main()

        if self.options['params-method'].value.lower() not in ['get', 'post'] and int(self.options['max-params-length'].value) > 100:
            raise WSException(
                "Attention! Too big --max-params-length. Big value here allowed only in GET and POST modes"
            )

    def make_queue(self):
        self.queue = ParamsBruterJob()

        loaded = self.load_objects(self.queue)

        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )

        self.counter = WSCounter.factory(loaded['all'] if not loaded['end'] else loaded['end']-loaded['start'])
        self.counter.point *= 10
        self.counter.new_str *= 10

    def start_pool(self):
        pool = ParamsBruterThreadsPool(self.queue, self.counter, self.result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if self.is_critical_stop():
                pool.kill_all()
            time.sleep(1)

    def output(self):
        WSModule.output(self)

        self.logger.log("\n")
        for result_row in self.result:
            self.logger.log(result_row)