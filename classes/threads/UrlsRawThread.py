# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for Dafs modules
"""

import Queue
import time
import pprint

from requests.exceptions import ChunkedEncodingError, ConnectionError

from classes.threads.AbstractRawThread import AbstractRawThread
from classes.threads.params.DafsParams import DafsParams
from classes.ErrorsCounter import ErrorsCounter


class UrlsRawThread(AbstractRawThread):
    """ Thread class for Dafs modules """
    method = None
    mask_symbol = None
    retested_words = None
    ignore_words_re = None
    template = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: DafsParams
        """
        AbstractRawThread.__init__(self)
        self.retested_words = {}

        self.queue = queue
        self.template = params.template
        self.mask_symbol = params.msymbol
        self.counter = counter
        self.result = result
        self.ignore_words_re = params.ignore_words_re
        self.not_found_re = params.not_found_re
        self.found_re = params.found_re
        self.not_found_ex = params.not_found_ex
        self.not_found_size = int(params.not_found_size)
        self.method = params.method
        self.not_found_codes = params.not_found_codes
        self.retest_codes = params.retest_codes
        self.retest_re = params.retest_re
        self.delay = params.delay

    def is_response_right(self, resp):
        """
        Return true if response has not false or not-found respose attribute(s)
        :param resp:
        :return:
        """
        if resp is None:
            return False

        if self.found_re and not self.is_response_content_binary(resp):
            return self.found_re.findall(self.get_response_full_text(resp))

        return AbstractRawThread.is_response_right(self, resp)

    def run(self):
        """ Run thread """
        req_func = getattr(self.http, self.method)
        need_retest = False
        word = False

        while not self.done:
            self.last_action = int(time.time())

            if self.delay:
                time.sleep(self.delay)

            try:
                if not need_retest:
                    word = self.queue.get()
                    if not len(word.strip()) or (self.ignore_words_re and self.ignore_words_re.findall(word)):
                        continue

                try:
                    url = self.template.replace(self.mask_symbol, word)
                except UnicodeDecodeError:
                    self.logger.log(
                        "URL build error (UnicodeDecodeError) with word '{0}', skip it".format(pprint.pformat(word)),
                        _print=False
                    )
                    continue
                rtime = int(time.time())

                positive_item = False
                try:
                    resp = req_func(url)

                    ErrorsCounter.flush()
                except ConnectionError as ex:
                    ErrorsCounter.up()

                    if self.not_found_ex is not False and str(ex).count(self.not_found_ex):
                        positive_item = False
                        self.log_item(word, str(ex), positive_item)
                    elif not self.is_test():
                        need_retest = True
                        self.http.change_proxy()
                    self.test_log(url, None, False)

                    continue

                if self.is_retest_need(word, resp):
                    time.sleep(self.retest_delay)
                    need_retest = True
                    continue

                if self.is_response_right(resp):
                    item_data = {
                        'url': url,
                        'code': resp.status_code,
                        'time': int(time.time()) - rtime
                    }
                    self.result.append(item_data)
                    self.xml_log(item_data)
                    positive_item = True

                self.test_log(url, resp, positive_item)

                self.log_item(word, resp, positive_item)

                self.check_positive_limit_stop(self.result)

                need_retest = False

                self.counter.up()
            except Queue.Empty:
                self.done = True
                break

            except ChunkedEncodingError as e:
                self.logger.ex(e)
            except BaseException as e:
                try:
                    if str(e).count('Cannot connect to proxy'):
                        need_retest = True
                    else:
                        self.logger.ex(e)
                except UnicodeDecodeError:
                    pass
                except UnboundLocalError:
                    self.logger.ex(e)
