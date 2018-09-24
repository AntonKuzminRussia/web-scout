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
from classes.jobs.FuzzerUrlsJob import FuzzerUrlsJob
from classes.FileGenerator import FileGenerator
from classes.threads.pools.FuzzerUrlsThreadPool import FuzzerUrlsThreadsPool
from classes.modules.params.FuzzerUrlsModuleParams import FuzzerUrlsModuleParams


class FuzzerUrls(WSModule):
    """ Class of FuzzerUrls module """
    model = None
    logger_enable = True
    logger_name = 'fuzzer-urls'
    logger_have_items = False
    log_path = '/dev/null'
    time_count = True
    options = FuzzerUrlsModuleParams().get_options()

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
                    result.append("{0}://{1}{2}".format(url.scheme, url.netloc, path))
        return result

    def do_work(self):
        """ Scan action of module """
        self.enable_logger()
        self.validate_main()
        self.pre_start_inf()

        if self.options['proxies'].value:
            Registry().get('proxies').load(self.options['proxies'].value)

        result = []

        fh_base = open(self.options['urls-file'].value, 'r')
        fh_work = open('/tmp/fuzzer-urls.txt', 'w')
        while True:
            line = fh_base.readline()
            if len(line) == 0:
                break
            urls_to_work = self._generate_fuzz_urls(line.strip())
            for url_to_work in urls_to_work:
                fh_work.write(url_to_work + "\n")
        fh_work.close()
        fh_base.close()

        queue = FuzzerUrlsJob()

        generator = FileGenerator('/tmp/fuzzer-urls.txt')
        queue.set_generator(generator)
        self.logger.log("Loaded {0} variants.".format(generator.lines_count))

        counter = WSCounter(1, 60, generator.lines_count)

        pool = FuzzerUrlsThreadsPool(queue, counter, result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if Registry().get('positive_limit_stop'):
                pool.kill_all()
            time.sleep(1)

        if Registry().get('proxy_many_died'):
            self.logger.log("Proxy many died, stop scan")

        self.logger.log("\n")
        for fuzz in result:
            self.logger.log("{0} (Word(s): {1})".format(
                fuzz['url'],
                ", ".join(fuzz['words'])
            ))

        self.done = True
