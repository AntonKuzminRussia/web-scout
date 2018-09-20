# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for HostsBrute modules
"""

import threading
import Queue
import time
import copy
import pprint
import re

from requests.exceptions import ChunkedEncodingError, ConnectionError

from libs.common import get_response_size
from classes.Registry import Registry
from classes.threads.HttpThread import HttpThread
from classes.threads.params.HostBruteThreadParams import HostBruteThreadParams


class HostsBruteThread(HttpThread):
    """ Thread class for HostsBrute modules """
    queue = None
    method = None
    url = None
    mask_symbol = None
    counter = None
    retested_words = None
    last_action = 0

    def __init__(self, queue, counter, result, params):
        """

        :type params: HostBruteThreadParams
        """
        threading.Thread.__init__(self)
        self.retested_words = {}

        self.queue = queue
        self.protocol = params.protocol
        self.host = params.host
        self.template = params.template
        self.mask_symbol = params.msymbol
        self.counter = counter
        self.result = result
        self.done = False

        self.false_phrase = params.false_phrase
        self.retest_codes = list(set(params.retest_codes.split(','))) if len(params.retest_codes) else []

        self.delay = int(params.delay)
        self.retest_delay = int(Registry().get('config')['hosts_brute']['retest_delay'])

        self.http = copy.deepcopy(Registry().get('http'))
        self.logger = Registry().get('logger')

        self.method = 'get'

        self.ignore_words_re = False if not len(params.ignore_words_re) else re.compile(params.ignore_words_re)

        self.retest_limit = int(Registry().get('config')['hosts_brute']['retest_limit'])

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
                    self.counter.up()

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
                    resp = req_func(self.protocol + "://" + self.host, headers={'host': hostname})
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
                if resp is not None and not search_scope.count(self.false_phrase):
                    self.result.append(hostname)
                    if Registry().isset('xml'):
                        Registry().get('xml').put_result({'hostname': hostname})
                    positive_item = True

                if Registry().isset('tester'):
                    Registry().get('tester').put(
                        hostname,
                        {
                            'code': resp.status_code,
                            'positive': positive_item,
                            'size': get_response_size(resp, "/", self.method),
                            'content': resp.content,
                        }
                    )

                self.log_item(word, resp, positive_item)

                self.check_positive_limit_stop(self.result)

                need_retest = False
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

            finally:
                pass

            if Registry().isset('tester') and Registry().get('tester').done():
                self.done = True
                break
