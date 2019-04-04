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
import os

from classes.Registry import Registry
from classes.jobs.FuzzerHeadersJob import FuzzerHeadersJob
from classes.kernel.WSCounter import WSCounter
from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.threads.pools.FuzzerHeadersThreadPool import FuzzerHeadersThreadsPool
from classes.modules.params.FuzzerHeadersModuleParams import FuzzerHeadersModuleParams
from classes.generators.FileGenerator import FileGenerator
from libs.common import file_put_contents
from classes.ErrorsCounter import ErrorsCounter


class FuzzerHeaders(WSModule):
    """ Class of FuzzerHeaders module """
    model = None
    log_path = '/dev/null'
    time_count = True
    logger_enable = True
    logger_name = 'fuzzer-headers'
    logger_have_items = False
    options = FuzzerHeadersModuleParams().get_options()

    def validate_main(self):
        """ Check users params """
        super(FuzzerHeaders, self).validate_main()

        if not len(self.options['urls-file'].value) and not len(self.options['url'].value):
            raise WSException("You must specify 'url' or 'urls-file' param")

        if len(self.options['urls-file'].value) and not os.path.exists(self.options['urls-file'].value):
            raise WSException(
                "File with urls '{0}' not exists!".format(self.options['urls-file'].value)
            )

    def make_queue(self):
        self.queue = FuzzerHeadersJob()
        if len(self.options['urls-file'].value):
            generator = FileGenerator(self.options['urls-file'].value)
        else:
            file_put_contents('/tmp/fuzzer-urls.txt', self.options['url'].value)
            generator = FileGenerator('/tmp/fuzzer-urls.txt')

        self.queue.set_generator(generator)
        self.logger.log("Loaded {0} variants.".format(generator.lines_count))

        self.counter = WSCounter.factory(generator.lines_count)

    def start_pool(self):
        pool = FuzzerHeadersThreadsPool(self.queue, self.counter, self.result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if Registry().get('proxy_many_died') or Registry().get('positive_limit_stop') or ErrorsCounter.is_limit():
                pool.kill_all()
            time.sleep(1)

    def output(self):
        WSModule.output(self)

        self.logger.log("\n")
        for fuzz in self.result:
            self.logger.log("{0} (Word(s): {1}, Header: {2})".format(
                fuzz['url'],
                ", ".join(fuzz['words']),
                fuzz['header']
            ))
