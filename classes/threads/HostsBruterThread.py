# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for HostsBrute modules
"""

import Queue
import time
import pprint

from requests.exceptions import ChunkedEncodingError, ConnectionError

from libs.common import get_response_size
from classes.threads.HttpThread import HttpThread
from classes.threads.params.HostsBruterThreadParams import HostsBruterThreadParams


class HostsBruterThread(HttpThread):
    """ Thread class for HostsBrute modules """
    method = None
    url = None
    mask_symbol = None
    retested_words = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: HostsBruterThreadParams
        """
        HttpThread.__init__(self)

        self.retested_words = {}

        self.queue = queue
        self.protocol = params.protocol
        self.ip = params.ip
        self.template = params.template
        self.mask_symbol = params.msymbol
        self.counter = counter
        self.result = result
        self.false_phrase = params.false_phrase
        self.false_size = params.false_size
        self.retest_codes = params.retest_codes
        self.retest_phrase = params.retest_phrase
        self.delay = params.delay
        self.method = 'get'
        self.ignore_words_re = params.ignore_words_re

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
                    hostname = self.template.replace(self.mask_symbol, word)
                except UnicodeDecodeError:
                    self.logger.log(
                        "URL build error (UnicodeDecodeError) with word '{0}', skip it".format(pprint.pformat(word)),
                        _print=False
                    )
                    continue

                try:
                    resp = req_func(self.protocol + "://" + self.ip, headers={'host': hostname})
                except ConnectionError:
                    need_retest = True
                    self.http.change_proxy()
                    continue

                if self.is_retest_need(word, resp):
                    time.sleep(self.retest_delay)
                    need_retest = True
                    continue

                search_scope = ""
                for header in resp.headers:
                    search_scope += "{0}: {1}\r\n".format(header.title(), resp.headers[header])
                search_scope += '\r\n\r\n' + resp.text

                positive_item = False
                if resp is not None and (not search_scope.count(self.false_phrase) or (self.false_size is not None and get_response_size(resp) != self.false_size)):
                    self.result.append(hostname)
                    self.xml_log({'hostname': hostname})
                    positive_item = True

                self.test_log(hostname, resp, positive_item)

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
