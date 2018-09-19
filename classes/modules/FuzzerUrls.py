# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of FuzzerUrls module
"""

import time
import os
from urlparse import urlparse

from classes.kernel.WSModule import WSModule
from classes.Registry import Registry
from classes.kernel.WSException import WSException
from classes.kernel.WSCounter import WSCounter
from classes.kernel.WSOption import WSOption
from classes.threads.FuzzerUrlsThread import FuzzerUrlsThread
from classes.jobs.FuzzerUrlsJob import FuzzerUrlsJob
from classes.threads.SFuzzerUrlsThread import SFuzzerUrlsThread
from classes.FileGenerator import FileGenerator


class FuzzerUrls(WSModule):
    """ Class of FuzzerUrls module """
    model = None
    logger_enable = True
    logger_name = 'fuzzer-urls'
    logger_have_items = False
    log_path = '/dev/null'
    options = {}
    time_count = True
    options_sets = {
        "scan": {
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
            "ddos-detect-phrase": WSOption(
                "ddos-detect-phrase",
                "Phrase for detect DDoS protection",
                "",
                False,
                ['--ddos-detect-phrase']
            ),
            "ddos-human-action": WSOption(
                "ddos-human-action",
                "Phrase for detect human action need",
                "",
                False,
                ['--ddos-human-action']
            ),
            "browser-recreate-phrase": WSOption(
                "browser-recreate-phrase",
                "Phrase for recreate browser with new proxy",
                "",
                False,
                ['--browser-recreate-phrase']
            ),
            "selenium": WSOption(
                "selenium",
                "Use Selenium for scanning",
                "",
                False,
                ['--selenium']
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
        },
    }

    def validate_main(self):
        """ Check users params """
        super(FuzzerUrls, self).validate_main()

        if not os.path.exists(self.options['urls-file'].value):
            raise WSException(
                "File with urls '{0}' not exists!".format(self.options['urls-file'].value)
            )


    def _parse_params(self, query):
        """ Parse url params string to dict """
        result = []
        params = query.split("&")
        for param in params:
            param = param.split("=")
            result.append({"name": param[0], "value": "" if len(param) == 1 else param[1]})
        return result

    def _generate_fuzz_urls(self, url):
        """ Parse urls and make a fuzzer urls from it """
        templates = open(Registry().get('wr_path') + "/bases/fuzzer-templates.txt").readlines()
        result = []
        url = urlparse(url)
        if len(url.query):
            params = self._parse_params(url.query.strip())

            for template in templates:
                template = template.strip()

                for n in range(0, len(params)):
                    path = url.path + '?'
                    for param in params:
                        if params.index(param) == n:
                            path += template.replace("|name|", param['name']).replace("|value|", param['value']) + "&"
                        else:
                            path += "{0}={1}&".format(param['name'], param['value'])
                    result.append(path)
        return result

    def scan_action(self):
        """ Scan action of module """
        self.enable_logger()
        self.validate_main()
        self.pre_start_inf()

        if self.options['proxies'].value:
            Registry().get('proxies').load(self.options['proxies'].value)

        result = []

        q = FuzzerUrlsJob()

        generator = FileGenerator(self.options['urls-file'].value)
        q.set_generator(generator)
        self.logger.log("Loaded {0} variants.".format(generator.lines_count))

        counter = WSCounter(1, 60, generator.lines_count)

        w_thrds = []
        for _ in range(int(self.options['threads'].value)):
            if self.options['selenium'].value:
                worker = SFuzzerUrlsThread(
                    q,
                    self.options['host'].value,
                    self.options['protocol'].value.lower(),
                    self.options['method'].value.lower(),
                    self.options['delay'].value,
                    self.options['ddos-detect-phrase'].value,
                    self.options['ddos-human-action'].value,
                    self.options['browser-recreate-phrase'].value,
                    counter,
                    result
                )
            else:
                worker = FuzzerUrlsThread(
                    q,
                    self.options['host'].value,
                    self.options['protocol'].value.lower(),
                    self.options['method'].value.lower(),
                    self.options['delay'].value,
                    counter,
                    result
                )
            worker.setDaemon(True)
            worker.start()
            w_thrds.append(worker)

            time.sleep(1)

        timeout_threads_count = 0
        while len(w_thrds):
            for worker in w_thrds:
                if worker.done or Registry().get('proxy_many_died'):
                    del w_thrds[w_thrds.index(worker)]

                if int(time.time()) - worker.last_action > int(Registry().get('config')['main']['kill_thread_after_secs']):
                    self.logger.log(
                        "Thread killed by time, resurected {0} times from {1}".format(
                            timeout_threads_count,
                            Registry().get('config')['main']['timeout_threads_resurect_max_count']
                        )
                    )
                    del w_thrds[w_thrds.index(worker)]

                    if timeout_threads_count <= int(Registry().get('config')['main']['timeout_threads_resurect_max_count']):
                        if self.options['selenium'].value:
                            worker = SFuzzerUrlsThread(
                                q,
                                self.options['host'].value,
                                self.options['protocol'].value.lower(),
                                self.options['method'].value.lower(),
                                self.options['delay'].value,
                                self.options['ddos-detect-phrase'].value,
                                self.options['ddos-human-action'].value,
                                self.options['browser-recreate-phrase'].value,
                                counter,
                                result
                            )
                        else:
                            worker = FuzzerUrlsThread(
                                q,
                                self.options['host'].value,
                                self.options['protocol'].value.lower(),
                                self.options['method'].value.lower(),
                                self.options['delay'].value,
                                counter,
                                result
                            )
                        worker.setDaemon(True)
                        worker.start()
                        w_thrds.append(worker)

                        timeout_threads_count += 1

            time.sleep(2)

        for fuzz in result:
            self.logger.log("{0} {1}://{2}{3} (Word: {4})".format(
                self.options['method'].value.upper(),
                self.options['protocol'].value.lower(),
                self.options['host'].value,
                fuzz['url'],
                ", ".join(fuzz['words'])
            ))

        self.done = True
