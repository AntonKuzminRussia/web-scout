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
from classes.threads.params.FuzzerThreadParams import FuzzerThreadParams


class SFuzzerUrlsThread(SeleniumThread):
    """ Thread class for FuzzerUrls module (selenium) """
    method = None
    url = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: FuzzerThreadParams
        """
        SeleniumThread.__init__(self)
        self.queue = queue
        self.method = params.method
        self.result = result
        self.counter = counter
        self.bad_words = params.bad_words
        self.delay = params.delay
        self.ddos_phrase = params.ddos_detect_phrase
        self.ddos_human = params.ddos_human_action
        self.recreate_phrase = params.browser_recreate_phrase

        Registry().set('url_for_proxy_check', "https://google.com")

        self.browser_create()

    def run(self):
        """ Run thread """
        if self.delay:
            time.sleep(self.delay)
        while True:
            self.last_action = int(time.time())

            try:
                url = self.queue.get()
                self.browser.get(url)

                found_words = []
                for bad_word in self.bad_words:
                    if self.browser.page_source.count(bad_word):
                        found_words.append(bad_word)

                if len(found_words):
                    item_data = {"url": url, "words": found_words}
                    self.xml_log(item_data)
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
