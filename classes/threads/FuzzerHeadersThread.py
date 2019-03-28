# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for FuzzerHeaders module
"""
from __future__ import division

import Queue
import time

from requests.exceptions import ConnectionError

from classes.Registry import Registry
from classes.threads.params.FuzzerThreadParams import FuzzerThreadParams
from classes.threads.HttpThread import HttpThread


class FuzzerHeadersThread(HttpThread):
    """ Thread class for FuzzerHeaders module """
    method = None
    url = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: FuzzerThreadParams
        """
        HttpThread.__init__(self)
        self.queue = queue
        self.method = params.method.lower()
        self.result = result
        self.counter = counter
        self.bad_words = params.bad_words
        self.headers = params.headers
        self.delay = params.delay

    def run(self):
        """ Run thread """
        req_func = getattr(self.http, self.method)
        need_retest = False

        while not self.done:
            self.last_action = int(time.time())

            if self.delay:
                time.sleep(self.delay)
            try:
                if not need_retest:
                    url = self.queue.get()

                for header in self.headers:
                    try:
                        resp = req_func(
                            url,
                            headers={header.lower(): Registry().get('fuzzer_evil_value')},
                        )
                    except ConnectionError:
                        need_retest = True
                        self.http.change_proxy()
                        continue

                    if self.is_retest_need(url, resp):
                        time.sleep(self.retest_delay)
                        need_retest = True
                        continue

                    if resp is None:
                        continue

                    if 499 < resp.status_code < 600:
                        item_data = {"url": url, "words": ["{0} Status code".format(resp.status_code)], "header": header}
                        self.result.append(item_data)
                        self.xml_log(item_data)
                        continue

                    found_words = []
                    for bad_word in self.bad_words:
                        if resp.content.lower().count(bad_word):
                            found_words.append(bad_word)

                    self.test_log(url + " " + header, resp, len(found_words) > 0)

                    if len(found_words):
                        item_data = {"url": url, "words": found_words, "header": header}
                        self.result.append({"url": url, "words": found_words, "header": header})
                        self.xml_log(item_data)

                #self.log_item(str(found_words), resp, len(found_words) > 0)

                self.counter.up()

                self.check_positive_limit_stop(self.result)

                need_retest = False
            except Queue.Empty:
                self.done = True
                break
            except BaseException as e:
                print url + " " + str(e)
