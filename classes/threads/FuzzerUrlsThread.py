# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for FuzzerUrls module
"""

import queue
import time

from requests.exceptions import ConnectionError

from classes.threads.params.FuzzerThreadParams import FuzzerThreadParams
from classes.threads.AbstractFuzzerRawThread import AbstractFuzzerRawThread
from classes.ErrorsCounter import ErrorsCounter


class FuzzerUrlsThread(AbstractFuzzerRawThread):
    """ Thread class for FuzzerUrls module """
    method = None
    url = None
    counter = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: FuzzerThreadParams
        """
        AbstractFuzzerRawThread.__init__(self)

        self.queue = queue
        self.method = params.method
        self.retest_codes = params.retest_codes
        self.retest_re = params.retest_re
        self.result = result
        self.counter = counter
        self.bad_words = params.bad_words
        self.delay = params.delay

    def build_positive_log_str(self, url, found_words, resp):
        return "URL: {0}\nWords: {1}\nResponse: {2}\n\n".format(url, ",".join(found_words), resp.text)

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

                try:
                    resp = req_func(url)
                    ErrorsCounter.flush()
                except ConnectionError:
                    ErrorsCounter.up()
                    need_retest = True
                    self.http.change_proxy()
                    continue

                if self.is_retest_need(url, resp):
                    time.sleep(self.retest_delay)
                    need_retest = True
                    resp.close()
                    continue

                if resp is None:
                    continue

                if 499 < resp.status_code < 600:
                    item_data = {"url": url, "words": ["{0} Status code".format(resp.status_code)]}
                    self.result.append(item_data)
                    self.xml_log(item_data)
                    resp.close()
                    continue

                found_words = []
                for bad_word in self.bad_words:
                    if resp.text.lower().count(bad_word):
                        found_words.append(bad_word)

                self.test_log(url, resp, len(found_words) > 0)

                if len(found_words):
                    item_data = {"url": url, "words": found_words}
                    self.result.append(item_data)
                    self.xml_log(item_data)

                self.log_item(
                    "_".join(found_words),
                    self.build_positive_log_str(url, found_words, resp),
                    len(found_words) > 0
                )

                self.counter.up()

                self.check_positive_limit_stop(self.result)

                resp.close()

                need_retest = False
            except queue.Empty:
                self.done = True
                break
            except BaseException as e:
                print(url + " " + str(e))
