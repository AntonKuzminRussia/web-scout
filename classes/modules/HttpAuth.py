# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of FormBruter module
"""

import time
from urlparse import urlparse

from classes.Registry import Registry
from classes.generators.FileGenerator import FileGenerator
from classes.jobs.HttpAuthBruterJob import HttpAuthBruterJob
from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.kernel.WSCounter import WSCounter
from classes.threads.pools.HttpAuthThreadsPool import HttpAuthThreadsPool
from classes.modules.params.HttpAuthModuleParams import HttpAuthModuleParams


class HttpAuth(WSModule):
    """ Class of FormBruter module """
    model = None
    mode = 'dict'
    log_path = '/dev/null'
    logger_enable = True
    logger_name = 'http-auth'
    logger_have_items = True
    time_count = True
    options = HttpAuthModuleParams().get_options()

    def validate_main(self):
        """ Check users params """
        super(HttpAuth, self).validate_main()

        parsed_url = urlparse(self.options['url'].value)
        if not len(parsed_url.scheme) or not len(parsed_url.netloc):
            raise WSException("Target URL not valid")


    def load_objects(self, queue):
        """ Prepare work objects """
        generator = FileGenerator(
            self.options['dict'].value,
            int(self.options['parts'].value),
            int(self.options['part'].value)
        )
        queue.set_generator(generator)
        return {'all': generator.lines_count, 'start': generator.first_border, 'end': generator.second_border}

    def make_queue(self):
        """
        Make work queue
        :return:
        """
        self.queue = HttpAuthBruterJob()
        loaded = self.load_objects(self.queue)

        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )

        self.counter = WSCounter.factory(loaded['all'] if not loaded['end'] else loaded['end'] - loaded['start'])

    def start_pool(self):
        """ Start threads pool and control it live """
        Registry().set('pass_found', False)
        pool = HttpAuthThreadsPool(self.queue, self.counter, self.result, self.options, self.logger)
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
        self.logger.log("Passwords found:")
        for row in self.result:
            self.logger.log('\t' + row['word'])
