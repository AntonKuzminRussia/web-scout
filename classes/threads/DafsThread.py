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

from libs.common import get_response_size
from classes.Registry import Registry
from classes.threads.HttpThread import HttpThread
from classes.threads.params.DafsThreadParams import DafsThreadParams


class DafsThread(HttpThread):
    """ Thread class for Dafs modules """
    method = None
    mask_symbol = None
    retested_words = None
    ignore_words_re = None
    template = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: DafsThreadParams
        """
        HttpThread.__init__(self)
        self.retested_words = {}

        self.queue = queue
        self.template = params.template
        self.mask_symbol = params.msymbol
        self.counter = counter
        self.result = result
        self.ignore_words_re = params.ignore_words_re
        self.not_found_re = params.not_found_re
        self.not_found_ex = params.not_found_ex
        self.not_found_size = int(params.not_found_size)
        self.method = params.method
        self.not_found_codes = params.not_found_codes
        self.retest_codes = params.retest_codes
        self.delay = params.delay

        self.retest_delay = int(Registry().get('config')['dafs']['retest_delay'])
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
                    resp = req_func(url)
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
