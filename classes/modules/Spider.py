# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of Spider module
"""
import os
import re
import time
from urlparse import urlparse

from libs.common import parse_split_conf
from classes.Registry import Registry
from classes.spider.SpiderCommon import SpiderCommon
from classes.spider.SpiderResult import SpiderResult
from classes.spider.SpiderRequestsCounter import SpiderRequestsCounter
from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.kernel.WSCounter import WSCounter
from classes.jobs.SpiderJob import SpiderJob
from classes.threads.pools.SpiderThreadsPool import SpiderThreadsPool
from classes.modules.params.SpiderModuleParams import SpiderModuleParams


class Spider(WSModule):
    """ Class of Spider module """
    model = None
    log_path = '/dev/null'
    time_count = True
    logger_enable = True
    logger_name = 'spider'
    logger_have_items = False
    options = SpiderModuleParams().get_options()
    src = None
    logger_scan_name_option = 'url'

    def validate_main(self):
        """ Check users params """
        super(Spider, self).validate_main()

        if not len(self.options['urls-file'].value) and not len(self.options['url'].value):
            raise WSException("You must specify 'url' or 'urls-file' param")

        if len(self.options['urls-file'].value) > 0 and not os.path.exists(self.options['urls-file'].value):
            raise WSException(
                "File with urls '{0}' not exists!".format(self.options['urls-file'].value)
            )

    def options_to_registry(self):
        if self.options['ignore'].value:
            Registry().set('ignore_regexp', re.compile(self.options['ignore'].value))

        expr = ''
        for ext in Registry().get('config')['spider']['allow_exts'].split(','):
            expr += r'\.' + ext.strip() + '$|'
        expr = expr.rstrip('|')
        Registry().set('allow_regexp', re.compile(expr, re.I))

        if self.options['only-one'].value:
            tmp = self.options['only-one'].value.split("||")
            if len(tmp):
                only_one = []
                for regex in tmp:
                    only_one.append({'regex': regex, 'block': False})
                Registry().set('only_one', only_one)

        denied_schemes = parse_split_conf(Registry().get('config')['spider']['denied_schemes'])
        Registry().set('denied_schemes', denied_schemes)
        Registry().get('http').set_allowed_types(
            parse_split_conf(Registry().get('config')['spider']['scan_content_types'])
        )
        Registry().get('http').set_denied_types(
            parse_split_conf(Registry().get('config')['spider']['noscan_content_types'])
        )

    def start_pool(self):
        pool = SpiderThreadsPool(self.queue, self.counter, self.src, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if Registry().get('positive_limit_stop'):
                pool.kill_all()
            time.sleep(1)

    def make_queue(self):
        self.queue = SpiderJob()
        self.counter = WSCounter.factory()

    def build_queue_source_file(self):
        if len(self.options['urls-file'].value):
            start_urls_file = self.options['urls-file'].value
            start_urls = map(str.strip, open(start_urls_file).readlines())
        else:
            start_urls = [self.options['url'].value]

        target_host = urlparse(start_urls[0]).netloc
        SpiderCommon.clear_old_data(target_host)

        SpiderCommon.prepare_first_pages(start_urls)

        if not os.path.exists(Registry().get('data_path') + target_host):
            os.mkdir(Registry().get('data_path') + target_host)
            os.chmod(Registry().get('data_path') + target_host, 0o777)

    def do_work(self):
        """ Scan action of module """
        self.result = SpiderResult()
        self.options_to_registry()
        self.build_queue_source_file()
        self.src = SpiderRequestsCounter(int(Registry().get('config')['spider']['requests_limit']))

        WSModule.do_work(self)

    def output(self):
        WSModule.output(self)

        self.logger.log("\nTotal links count: " + str(Registry().get('mongo').spider_urls.count()))
        self.logger.log(str(self.result))

    def help(self):
        """ Help func """
        return "Module Spider ver 1.0"

    def finished(self):
        """ Is module finished? """
        return self.kernel.finished()

