# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for Dafs modules
"""

import threading
import Queue
import time
import copy
import re
import pprint

from requests.exceptions import ChunkedEncodingError, ConnectionError

from libs.common import get_response_size
from classes.Registry import Registry
from classes.threads.HttpThread import HttpThread
from classes.threads.params.DafsThreadParams import DafsThreadParams


class DafsThread(HttpThread):
    """ Thread class for Dafs modules """
    queue = None
    method = None
    template = None
    mask_symbol = None
    counter = None
    retested_words = None
    last_action = 0
    ignore_words_re = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: DafsThreadParams
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
        self.ignore_words_re = False if not len(params.ignore_words_re) else re.compile(params.ignore_words_re)
        self.not_found_re = False if not len(params.not_found_re) else re.compile(params.not_found_re)
        self.not_found_ex = False if not len(params.not_found_ex) else params.not_found_ex
        self.not_found_size = int(params.not_found_size)
        self.method = params.method
        if self.method == 'head' and (len(params.not_found_re) or self.not_found_size != -1):
            self.method = 'get'

        not_found_codes = params.not_found_codes.split(',')
        not_found_codes.append('404')
        self.not_found_codes = list(set(not_found_codes))
        self.retest_codes = list(set(params.retest_codes.split(','))) if len(params.retest_codes) else []

        self.delay = int(params.delay)
        self.retest_delay = int(Registry().get('config')['dafs']['retest_delay'])

        self.http = copy.deepcopy(Registry().get('http'))
        self.logger = Registry().get('logger')

        self.retest_limit = int(Registry().get('config')['dafs']['retest_limit'])

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
                    self.counter.up()

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
                    resp = req_func(self.protocol + "://" + self.host + url)
                except ConnectionError as ex:
                    if self.not_found_ex is not False and str(ex).count(self.not_found_ex):
                        positive_item = False
                        self.log_item(word, str(ex), positive_item)
                    elif not Registry().isset('tester'):
                        need_retest = True
                        self.http.change_proxy()

                    if Registry().isset('tester'):
                        Registry().get('tester').put(
                            url,
                            {
                                'code': 0,
                                'positive': positive_item,
                                'size': 0,
                                'content': '',
                                'exception': str(ex),
                            }
                        )

                        if Registry().isset('tester') and Registry().get('tester').done():
                            self.done = True
                            break

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
                    if Registry().isset('xml'):
                        Registry().get('xml').put_result(item_data)
                    positive_item = True

                if Registry().isset('tester'):
                    Registry().get('tester').put(
                        url,
                        {
                            'code': resp.status_code,
                            'positive': positive_item,
                            'size': get_response_size(resp, url, self.method),
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
