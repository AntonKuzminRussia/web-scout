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
from urllib.parse import urlparse

import requests

from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.kernel.WSCounter import WSCounter
from classes.jobs.ParamsBruterJob import ParamsBruterJob
from classes.threads.pools.ParamsThreadsPool import ParamsThreadsPool
from classes.Registry import Registry


class ParamsModules(WSModule):
    """ Common module class form Params* modules """
    logger_enable = True
    logger_name = 'params-bruter'
    logger_have_items = True

    def validate_main(self):
        """ Check users params """
        super(ParamsModules, self).validate_main()

        try:
            resp = Registry().get('http').get(self.options['url'].value)
        except requests.exceptions.ConnectionError:
            raise WSException("Target web-site not available")

        parsed_url = urlparse(self.options['url'].value)
        if not len(parsed_url.scheme) or not len(parsed_url.netloc):
            raise WSException("Target URL not valid")

        if self.options['params-method'].value.lower() not in ['get', 'post'] and int(self.options['max-params-length'].value) > 100:
            raise WSException(
                "Attention! Too big --max-params-length. Big value here allowed only in GET and POST modes"
            )

        if not len(self.options['not-found-re'].value) and self.options['not-found-size'].value == "-1":
            raise WSException(
                "You must set one or more params for detect negative server respose: not-found-re, not-found-size"
            )

    def make_queue(self):
        """
        Make work queue
        :return:
        """
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
        """ Start threads pool and control it live """
        pool = ParamsThreadsPool(self.queue, self.counter, self.result, self.options, self.logger)
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
        self.logger.log("Params found:")
        for result_row in self.result:
            self.logger.log("\t" + result_row)