# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for FormBruter module
"""

import Queue
import time

from requests.exceptions import ChunkedEncodingError, ConnectionError

from libs.common import get_response_size
from classes.threads.HttpThread import HttpThread
from classes.threads.params.FormBruterThreadParams import FormBruterThreadParams
from classes.Registry import Registry


class FormBruterThread(HttpThread):
    """ Thread class for FormBruter module """
    method = None
    url = None
    mask_symbol = None
    retested_words = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: FormBruterThreadParams
        """
        HttpThread.__init__(self)
        self.retested_words = {}
        self.queue = queue
        self.url = params.url
        self.false_phrase = params.false_phrase
        self.false_size = params.false_size
        self.true_phrase = params.true_phrase
        self.delay = params.delay
        self.confstr = params.confstr
        self.first_stop = params.first_stop
        self.login = params.login
        self.counter = counter
        self.result = result
        self.retest_codes = params.retest_codes
        self.retest_phrase = params.retest_phrase

        self.http.every_request_new_session = True
        self.pass_min_len = params.pass_min_len
        self.pass_max_len = params.pass_max_len

    def _make_conf_from_str(self, confstr):
        result = {}
        tmp = confstr.split("&")
        for tmp_row in tmp:
            field, value = tmp_row.split("=", 1)
            result[field] = value
        return result

    def _fill_conf(self, conf, login, password):
        for field in conf.keys():
            conf[field] = conf[field].replace("^USER^", login).replace("^PASS^", password)
        return conf

    def pass_found(self):
        return Registry().get('pass_found')

    def set_pass_found(self, value):
        return Registry().set('pass_found', value)

    def run(self):
        """ Run thread """
        need_retest = False
        word = False

        conf = self._make_conf_from_str(self.confstr)

        while not self.done and not self.pass_found():
            try:
                self.last_action = int(time.time())

                if self.delay:
                    time.sleep(self.delay)

                if not need_retest:
                    word = self.queue.get()

                if (self.pass_min_len and len(word) < self.pass_min_len) or \
                        (self.pass_max_len and len(word) > self.pass_max_len):
                    continue

                work_conf = self._fill_conf(dict(conf), self.login, word)
                try:
                    resp = self.http.post(
                        self.url, data=work_conf
                    )
                except ConnectionError:
                    need_retest = True
                    self.http.change_proxy()
                    continue

                if self.is_retest_need(word, resp):
                    time.sleep(self.retest_delay)
                    need_retest = True
                    continue

                positive_item = False

                if (len(self.false_phrase) and
                        not resp.content.count(self.false_phrase)) or \
                        (len(self.true_phrase) and resp.content.count(self.true_phrase) or
                             (self.false_size is not None and get_response_size(resp) != self.false_size)):
                    item_data = {'word': word, 'content': resp.content, 'size': get_response_size(resp)}
                    self.result.append(item_data)
                    self.xml_log(item_data)
                    positive_item = True

                    self.check_positive_limit_stop(self.result)

                self.log_item(word, resp, positive_item)

                self.test_log(word, resp, positive_item)

                if positive_item and int(self.first_stop):
                    self.done = True
                    self.set_pass_found(True)
                    break

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
                        self.logger.log(str(word) + " " + str(e))
                except UnicodeDecodeError:
                    pass
                except UnboundLocalError:
                    self.logger.ex(e)
            finally:
                pass
