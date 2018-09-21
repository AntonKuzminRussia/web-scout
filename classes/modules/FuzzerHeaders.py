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
from classes.kernel.WSOption import WSOption
from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.threads.pools.FuzzerHeadersThreadPool import FuzzerHeadersThreadsPool


class FuzzerHeaders(WSModule):
    """ Class of FuzzerHeaders module """
    model = None
    log_path = '/dev/null'
    time_count = True
    logger_enable = True
    logger_name = 'fuzzer-headers'
    logger_have_items = False
    options = {
        "threads": WSOption(
            "threads",
            "Threads count, default 10",
            int(Registry().get('config')['main']['default_threads']),
            False,
            ['--threads']
        ),
        "host": WSOption(
            "host",
            "Traget host for scan",
            "",
            True,
            ['--host']
        ),
        "method": WSOption(
            "method",
            "Requests method (default - GET)",
            "GET",
            False,
            ['--method']
        ),
        "protocol": WSOption(
            "protocol",
            "Protocol http or https (default - http)",
            "http",
            False,
            ['--protocol']
        ),
        "delay": WSOption(
            "delay",
            "Deley for every thread between requests (secs)",
            "0",
            False,
            ['--delay']
        ),
        "proxies": WSOption(
            "proxies",
            "File with list of proxies",
            "",
            False,
            ['--proxies']
        ),
        "headers-file": WSOption(
            "headers-file",
            "File with list of HTTP headers",
            "",
            False,
            ['--headers-file']
        ),
        "urls-file": WSOption(
            "urls-file",
            "File with list of URLs",
            "",
            True,
            ['--urls-file']
        ),
    }

    def validate_main(self):
        """ Check users params """
        super(FuzzerHeaders, self).validate_main()

        if not os.path.exists(self.options['urls-file'].value):
            raise WSException(
                "File with urls '{0}' not exists!".format(self.options['urls-file'].value)
            )

    def do_work(self):
        """ Scan action of module """
        self.enable_logger()
        self.validate_main()
        self.pre_start_inf()

        if self.options['proxies'].value:
            Registry().get('proxies').load(self.options['proxies'].value)

        result = []

        to_scan = map(str.strip, open(self.options['urls-file'].value).readlines())

        queue = FuzzerHeadersJob()
        queue.load_dict(to_scan)

        self.logger.log("Loaded {0} variants.".format(len(to_scan)))

        counter = WSCounter(1, 60, len(to_scan))

        pool = FuzzerHeadersThreadsPool(queue, counter, result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if Registry().get('positive_limit_stop'):
                pool.kill_all()
            time.sleep(1)

        if Registry().get('proxy_many_died'):
            self.logger.log("Proxy many died, stop scan")

        for fuzz in result:
            self.logger.log("{0} {1}://{2}{3} (Word: {4}, Header: {5})".format(
                self.options['method'].value.upper(),
                self.options['protocol'].value.lower(),
                self.options['host'].value,
                fuzz['url'],
                ", ".join(fuzz['words']),
                fuzz['header']
            ))

        self.done = True
