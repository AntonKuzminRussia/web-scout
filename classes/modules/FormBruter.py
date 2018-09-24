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

from classes.Registry import Registry
from classes.FileGenerator import FileGenerator
from classes.jobs.FormBruterJob import FormBruterJob
from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.kernel.WSCounter import WSCounter
from classes.threads.pools.FormBruterThreadsPool import FormBruterThreadsPool
from classes.modules.params.FormBruterModuleParams import FormBruterModuleParams


class FormBruter(WSModule):
    """ Class of FormBruter module """
    model = None
    mode = 'dict'
    log_path = '/dev/null'
    logger_enable = True
    logger_name = 'form-bruter'
    logger_have_items = True
    time_count = True
    options = FormBruterModuleParams().get_options()

    def validate_main(self):
        """ Check users params """
        super(FormBruter, self).validate_main()

        if self.options['selenium'].value:
            if not len(self.options['conffile'].value.strip()):
                raise WSException(
                    "You must specify param --conffile"
                )

            if not os.path.exists(self.options['conffile'].value):
                raise WSException(
                    "Config file '{0}' not exists or not readable!"
                    .format(self.options['conffile'].value)
                )

        else:
            if not len(self.options['confstr'].value.strip()):
                raise WSException(
                    "You must specify param --confstr"
                )
            if not self.options['confstr'].value.count("^USER^"):
                raise WSException(
                    "--confstr must have a ^USER^ fragment"
                )

            if not self.options['confstr'].value.count("^PASS^"):
                raise WSException(
                    "--confstr must have a ^PASS^ fragment"
                )

        if not len(self.options['true-phrase'].value) and not len(self.options['false-phrase'].value) and not self.options['false-size'].value:
            raise WSException(
                "You must specify --false-phrase param or --true-phrase param or --false-size param!"
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

    def do_work(self):
        """ Brute action of module """
        self.enable_logger()
        self.validate_main()
        self.pre_start_inf()

        if self.options['proxies'].value:
            Registry().get('proxies').load(self.options['proxies'].value)

        result = []

        queue = FormBruterJob()
        loaded = self.load_objects(queue)

        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )

        counter = WSCounter(5, 300, loaded['all'] if not loaded['end'] else loaded['end']-loaded['start'])

        pass_found = False

        pool = FormBruterThreadsPool(queue, counter, result, pass_found, self.options, self.logger)
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

        self.logger.log("")
        self.logger.log("Passwords found:")
        for row in result:
            self.logger.log('\t' + row['word'])

        self.done = True
