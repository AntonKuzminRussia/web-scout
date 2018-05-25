# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for CMS module (selenium)
"""
from __future__ import division

import Queue
import time
import re
import pprint

from selenium.common.exceptions import TimeoutException

from libs.common import clear_double_slashes
from classes.Registry import Registry
from classes.threads.SeleniumThread import SeleniumThread


class SCmsThread(SeleniumThread):
    """ Thread class for CMS module (selenium) """
    queue = None
    method = None
    url = None
    counter = None
    last_action = 0

    def __init__(
            self, queue, domain, url, protocol, method, not_found_re,
            delay, ddos_phrase, ddos_human, recreate_re, counter, result
    ):
        super(SCmsThread, self).__init__()
        self.queue = queue
        self.method = method if not (len(not_found_re) and method.lower() == 'head') else 'get'
        self.domain = domain
        self.url = url
        self.result = result
        self.counter = counter
        self.protocol = protocol
        self.not_found_re = False if not len(not_found_re) else re.compile(not_found_re)
        self.done = False
        self.http = Registry().get('http')
        self.delay = int(delay)
        self.ddos_phrase = ddos_phrase
        self.ddos_human = ddos_human
        self.recreate_re = False if not len(recreate_re) else re.compile(recreate_re)
        self.logger = Registry().get('logger')

        Registry().set('url_for_proxy_check', url)

        self.browser_create()

    def run(self):
        """ Run thread """
        while not self.done:
            self.last_action = int(time.time())

            if self.delay:
                time.sleep(self.delay)

            try:
                path = self.queue.get()
                self.counter.up()

                try:
                    url = "{0}://{1}{2}".format(self.protocol, self.domain, clear_double_slashes(self.url + path))
                except UnicodeDecodeError:
                    self.logger.log(
                        "URL build error (UnicodeDecodeError) with path '{0}', skip it".format(pprint.pformat(path)),
                        _print=False
                    )
                    continue

                self.browser.get(url)

                if self.recreate_re and self.recreate_re.findall(self.browser.page_source):
                    self.queue.put(path)
                    self.browser_close()
                    self.browser_create()
                    continue

                positive_item = False
                if not self.not_found_re.findall(self.browser.page_source):
                    item_data = {'path': path, 'code': 0}
                    if Registry().isset('xml'):
                        Registry().get('xml').put_result(item_data)
                    self.result.append(item_data)
                    positive_item = True

                if Registry().isset('tester'):
                    Registry().get('tester').put(
                        path,
                        {
                            'code': 0,
                            'positive': positive_item,
                            'size': len(self.browser.page_source),
                            'content': self.browser.page_source,
                        }
                    )

                self.logger.item(
                    path,
                    self.browser.page_source,
                    True,
                    positive_item
                )

                self.queue.task_done()
            except Queue.Empty:
                self.done = True
                break
            except TimeoutException as e:
                self.queue.put(path)
                self.browser_close()
                self.browser_create()
                continue
            except UnicodeDecodeError as e:
                self.logger.ex(e)
                self.queue.task_done()
            except BaseException as e:
                try:
                    self.queue.put(path)
                    if len(e.args) and e.args[0] == 111:
                        self.browser_close()
                        self.browser_create()
                    elif not str(e).count('Timed out waiting for page load'):
                        self.logger.ex(e)
                except UnicodeDecodeError:
                    pass
                self.queue.task_done()
            self.up_requests_count()

            if Registry().isset('tester') and Registry().get('tester').done():
                self.done = True
                break

        self.browser_close()
