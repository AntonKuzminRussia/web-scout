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
import os
from urlparse import urlparse

from classes.Registry import Registry
from classes.generators.FileGenerator import FileGenerator
from classes.jobs.FormBruterJob import FormBruterJob
from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.kernel.WSCounter import WSCounter
from classes.threads.pools.FormsThreadsPool import FormsThreadsPool
from classes.modules.params.FormsModuleParams import FormsModuleParams


class Forms(WSModule):
    """ Class of FormBruter module """
    model = None
    mode = 'dict'
    log_path = '/dev/null'
    logger_enable = True
    logger_name = 'form-bruter'
    logger_have_items = True
    time_count = True
    options = FormsModuleParams().get_options()

    def validate_main(self):
        """ Check users params """
        super(Forms, self).validate_main()

        parsed_url = urlparse(self.options['url'].value)
        if not len(parsed_url.scheme) or not len(parsed_url.netloc):
            raise WSException("Target URL not valid")

        if self.options['selenium'].value:
            if not len(self.options['conf-file'].value.strip()):
                raise WSException(
                    "You must specify param --conf-file"
                )

            if not os.path.exists(self.options['conf-file'].value):
                raise WSException(
                    "Config file '{0}' not exists or not readable!"
                    .format(self.options['conf-file'].value)
                )

        else:
            if not len(self.options['conf-str'].value.strip()):
                raise WSException(
                    "You must specify param --conf-str"
                )
            if not self.options['conf-str'].value.count("^USER^"):
                raise WSException(
                    "--conf-str must have a ^USER^ fragment"
                )

            if not self.options['conf-str'].value.count("^PASS^"):
                raise WSException(
                    "--conf-str must have a ^PASS^ fragment"
                )

        if not len(self.options['true-re'].value) and not len(self.options['false-re'].value) and not self.options['false-size'].value:
            raise WSException(
                "You must specify --false-re param or --true-re param or --false-size param!"
            )

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
        self.queue = FormBruterJob()
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
        pool = FormsThreadsPool(self.queue, self.counter, self.result, self.options, self.logger)
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
