# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for HostsBrute modules
"""

import queue
import time
import pprint

from requests.exceptions import ChunkedEncodingError, ConnectionError

from libs.common import get_response_size, get_full_response_text
from classes.threads.AbstractRawThread import AbstractRawThread
from classes.threads.params.HostsThreadParams import HostsThreadParams
from classes.ErrorsCounter import ErrorsCounter


class HostsRawThread(AbstractRawThread):
    """ Thread class for HostsBrute modules """
    method = None
    url = None
    mask_symbol = None
    retested_words = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: HostsThreadParams
        """
        AbstractRawThread.__init__(self)

        self.retested_words = {}

        self.queue = queue
        self.protocol = params.protocol
        self.ip = params.ip
        self.template = params.template
        self.mask_symbol = params.msymbol
        self.counter = counter
        self.result = result
        self.false_re = params.false_re
        self.false_size = params.false_size
        self.retest_codes = params.retest_codes
        self.retest_re = params.retest_re
        self.delay = params.delay
        self.method = 'get'
        self.ignore_words_re = params.ignore_words_re

    def is_poitive_item(self, resp):
        if resp is None:
            return False

        if self.false_size is not None and get_response_size(resp) != self.false_size:
            return True

        search_scope = get_full_response_text(resp)
        if not self.false_re.findall(search_scope):
            return True

        return False

    def ignore_word(self, word):
        return not len(word.strip()) or (self.ignore_words_re and self.ignore_words_re.findall(word))

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

                if self.ignore_word(word):
                    continue

                try:
                    hostname = self.template.replace(self.mask_symbol, word)
                except UnicodeDecodeError:
                    self.logger.log(
                        "URL build error (UnicodeDecodeError) with word '{0}', skip it".format(pprint.pformat(word)),
                        _print=False
                    )
                    continue

                try:
                    resp = req_func(self.protocol + "://" + self.ip, headers={'host': hostname})
                    ErrorsCounter.flush()
                except ConnectionError:
                    ErrorsCounter.up()

                    if not self.is_test():
                        need_retest = True
                        self.http.change_proxy()
                        continue

                    self.test_log(hostname, None, False)
                    continue

                if self.is_retest_need(word, resp):
                    time.sleep(self.retest_delay)
                    need_retest = True
                    resp.close()
                    continue

                positive_item = False
                if self.is_poitive_item(resp):
                    positive_item = True
                    self.result.append(hostname)
                    self.xml_log({'hostname': hostname})
                    self.log_item(word, resp, True)
                self.test_log(hostname, resp, positive_item)

                self.check_positive_limit_stop(self.result)

                need_retest = False

                self.counter.up()

                resp.close()
            except queue.Empty:
                self.done = True
                break

            except ChunkedEncodingError as e:
                self.logger.ex(e)
            except BaseException as e:
                import traceback
                traceback.format_exc()
                print(e)
                try:
                    if str(e).count('Cannot connect to proxy'):
                        need_retest = True
                    else:
                        self.logger.ex(e)
                except UnicodeDecodeError:
                    pass
                except UnboundLocalError:
                    self.logger.ex(e)
