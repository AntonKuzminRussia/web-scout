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
from urlparse import urlparse

import requests

from classes.kernel.WSModule import WSModule
from classes.kernel.WSCounter import WSCounter
from classes.kernel.WSException import WSException
from classes.jobs.DafsJob import DafsJob
from classes.threads.pools.UrlsThreadsPool import UrlsThreadsPool
from classes.Registry import Registry


class UrlsModules(WSModule):
    """ Common module class form Dafs* modules """
    logger_enable = True
    logger_name = 'urls'
    logger_have_items = True

    def validate_main(self):
        """ Check users params """
        super(UrlsModules, self).validate_main()

        skip_listings = Registry().get('config')['main']['skip_listings']
        standart_msymbol = Registry().get('config')['main']['standart_msymbol']
        source_url = self.options['template'].value.replace(standart_msymbol, "")
        try:
            resp = Registry().get('http').get(source_url)
            if ("<title>Index of" in resp.text or "<h1>Index of" in resp.text) and skip_listings == "1":
                raise WSException("Source URL is listing, check it. Or change 'skip_listings' param in config")
        except requests.exceptions.ConnectionError:
            raise WSException("Target web-site not available")

        parsed_url = urlparse(self.options['template'].value)
        if not len(parsed_url.scheme) or not len(parsed_url.netloc):
            raise WSException("Target URL not valid")

        if self.options['not-found-size'].value != "-1" and self.options['method'].value.lower() == 'head':
            raise WSException(
                "You can`t use HEAD method with --false-size param"
            )


    def make_queue(self):
        self.queue = DafsJob()

        loaded = self.load_objects(self.queue)

        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )

        self.counter = WSCounter.factory(loaded['all'] if not loaded['end'] else loaded['end'] - loaded['start']
        )

    def start_pool(self):
        pool = UrlsThreadsPool(self.queue, self.counter, self.result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if self.is_critical_stop():
                pool.kill_all()
            time.sleep(1)

    def output(self):
        WSModule.output(self)

        self.logger.log("\n")
        for result_row in self.result:
            self.logger.log("{0} {1}".format(result_row['code'], result_row['url']))
