# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for FuzzerUrls module (selenium)
"""
from __future__ import division

import Queue
import time

from selenium.common.exceptions import TimeoutException

from classes.Registry import Registry
from classes.threads.SeleniumThread import SeleniumThread
from libs.common import file_to_list
from classes.threads.params.FuzzerThreadParams import FuzzerThreadParams


class SFuzzerUrlsThread(SeleniumThread):
    """ Thread class for FuzzerUrls module (selenium) """
    queue = None
    method = None
    url = None
    counter = None
    last_action = 0

    def __init__(self, queue, counter, result, params):
        """

        :type params: FuzzerThreadParams
        """
        super(SFuzzerUrlsThread, self).__init__()
        self.queue = queue
        self.method = params.method
        self.domain = params.host
        self.result = result
        self.counter = counter
        self.protocol = params.protocol
        self.done = False
        self.bad_words = params.bad_words
        self.http = Registry().get('http')
        self.delay = params.delay
        self.ddos_phrase = params.ddos_detect_phrase
        self.ddos_human = params.ddos_human_action
        self.recreate_phrase = params.browser_recreate_phrase

        Registry().set('url_for_proxy_check', "{0}://{1}".format(self.protocol, self.domain))

        self.browser_create()

    def run(self):
        """ Run thread """
        if self.delay:
            time.sleep(self.delay)
        while True:
            self.last_action = int(time.time())

            try:
                url = self.queue.get()
                self.browser.get(
                    "{0}://{1}{2}".format(self.protocol, self.domain, url)
                )

                found_words = []
                for bad_word in self.bad_words:
                    if self.browser.page_source.count(bad_word):
                        found_words.append(bad_word)

                if len(found_words):
                    item_data = {"url": url, "words": found_words}
                    if Registry().isset('xml'):
                        Registry().get('xml').put_result(item_data)
                    self.result.append(item_data)

                self.counter.up()
            except Queue.Empty:
                self.done = True
                break
            except TimeoutException as e:
                self.queue.put(url)
                self.browser_close()
                self.browser_create()
                continue
            except BaseException as e:
                if not str(e).count('Timed out waiting for page load'):
                    print url + " " + str(e)
            self.up_requests_count()

        self.browser.close()
