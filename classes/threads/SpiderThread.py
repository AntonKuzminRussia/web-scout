# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for Spider module
"""
import Queue
import time

from classes.Registry import Registry
from classes.spider.SpiderCommon import SpiderCommon
from classes.spider.SpiderLinksParser import SpiderLinksParser
from libs.common import file_put_contents, md5
from classes.threads.params.SpiderThreadParams import SpiderThreadParams
from classes.threads.HttpThread import HttpThread


class SpiderThread(HttpThread):
    """ Thread class for Spider module """
    url = None
    job = None
    links_parser = None
    src = None
    delay = None
    counter = None
    _db = None
    running = None

    def __init__(self, job, src, counter, params):
        """

        :type params: SpiderThreadParams
        """
        HttpThread.__init__(self)
        self.job = job
        self.url = params.url
        self.links_parser = SpiderLinksParser()
        self.src = src
        self.delay = params.delay
        self.counter = counter
        self._db = Registry().get('mongo')
        self.running = True

    def run(self):
        """ Run thread """
        while self.src.allowed() and not self.done:
            self.counter.all = self.job.qsize()
            try:
                links = self.job.get_many()
                self.scan_links(links)
            except Queue.Empty:
                break
        self.running = False

    def _checked(self, link):
        """ Mark link as checked """
        del link['_id']
        self._db.spider_urls.update({'hash': link['hash']}, {'$set': link})

    def scan_links(self, links):
        """ Scan links """
        req_func = getattr(self.http, 'get')

        for link in links:
            self.last_action = int(time.time())

            url = SpiderCommon.gen_url(link)

            start_time = int(round(time.time() * 1000))

            if self.delay:
                time.sleep(self.delay)

            response = req_func(url)
            self.src.up()
            if response is not None:
                result_time = int(round(time.time() * 1000)) - start_time
                if 'content-type' in response.headers:
                    content_type = response.headers['content-type'].split(";")[0] \
                                   if (response.headers['content-type'].find(";") != -1) \
                                   else response.headers['content-type']
                else:
                    content_type = 'unknown/unknown'

                if 299 < response.status_code < 400:
                    SpiderCommon.insert_links([response.headers['Location']], url, link['host'])
                else:
                    new_links = self.links_parser.parse_links(content_type, str(response.content), link)
                    SpiderCommon.insert_links(new_links, url, link['host'])

                self.logger.item(url, response.content, self.is_response_content_binary(response), response.status_code is not 404)

            link['size'] = len(response.content) if response is not None else 0
            link['code'] = response.status_code if response is not None else 0
            link['time'] = result_time if response is not None else 0

            self.counter.up()

        SpiderCommon.links_checked(links)


