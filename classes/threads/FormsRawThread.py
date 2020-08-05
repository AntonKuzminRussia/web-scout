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
import urllib

from requests.exceptions import ChunkedEncodingError, ConnectionError

from libs.common import get_response_size
from classes.threads.AbstractRawThread import AbstractRawThread
from classes.threads.params.FormsThreadParams import FormsThreadParams
from classes.Registry import Registry
from classes.ErrorsCounter import ErrorsCounter


class FormsRawThread(AbstractRawThread):
    """ Thread class for FormBruter module """
    method = None
    url = None
    mask_symbol = None
    retested_words = None
    method = None
    
    method = None
    def __init__(self, queue, counter, result, params):
        """

        :type params: FormsThreadParams
        """
        AbstractRawThread.__init__(self)
        self.retested_words = {}
        self.queue = queue
        self.url = params.url
        self.false_re = params.false_re
        self.false_size = params.false_size
        self.true_re = params.true_re
        self.delay = params.delay
        self.confstr = params.confstr
        self.first_stop = params.first_stop
        self.login = params.login
        self.counter = counter
        self.result = result
        self.retest_codes = params.retest_codes
        self.retest_re = params.retest_re
        self.method = params.method

        self.http.every_request_new_session = True
        self.pass_min_len = params.pass_min_len
        self.pass_max_len = params.pass_max_len

        self.http.allow_redirects = params.follow_redirects

    def make_conf_from_str(self, confstr):
        """ Build brute config from --conf-str """
        result = {}
        tmp = confstr.split("&")
        for tmp_row in tmp:
            field, value = tmp_row.split("=", 1)
            result[field] = value
        return result

    def fill_conf(self, conf, login, password):
        """ Put login and password on their places in config """
        for field in conf.keys():
            conf[field] = conf[field].replace("^USER^", login).replace("^PASS^", password)
        return conf

    def is_pass_found(self):
        """ Are password found? """
        return Registry().get('pass_found')

    def set_pass_found(self, value):
        """ Set pass_found value """
        return Registry().set('pass_found', value)

    def ignore_word(self, word):
        return self.pass_min_len and len(word) < self.pass_min_len or \
               self.pass_max_len and len(word) > self.pass_max_len

    def is_positive(self, resp):
        if self.false_size is not None and get_response_size(resp) != self.false_size:
            return True
        if self.false_re and not self.false_re.findall(resp.content):
            return True
        if self.true_re and self.true_re.findall(resp.content):
            return True
        return False

    def run(self):
        """ Run thread """
        need_retest = False
        word = False

        conf = self.make_conf_from_str(self.confstr)

        while not self.done and not self.is_pass_found():
            try:
                self.last_action = int(time.time())

                if self.delay:
                    time.sleep(self.delay)

                if not need_retest:
                    word = self.queue.get()

                if self.ignore_word(word):
                    continue

                work_conf = self.fill_conf(dict(conf), self.login, word)
                try:
                    if self.method == 'get':
                        resp = self.http.get(self.url + "?" + urllib.urlencode(work_conf))
                    else:
                        resp = self.http.post(self.url, data=work_conf)
                    ErrorsCounter.flush()
                except ConnectionError:
                    ErrorsCounter.up()
                    need_retest = True
                    self.http.change_proxy()
                    continue

                if self.is_retest_need(word, resp):
                    time.sleep(self.retest_delay)
                    need_retest = True
                    resp.close()
                    continue

                positive_item = False
                if self.is_positive(resp):
                    positive_item = True
                    item_data = {'word': word, 'content': resp.content, 'size': get_response_size(resp)}
                    self.result.append(item_data)
                    self.xml_log(item_data)
                    self.logger.log("F", False)
                    self.log_item(word, resp, positive_item)
                    self.check_positive_limit_stop(self.result)

                self.test_log(word, resp, positive_item)

                if positive_item and int(self.first_stop):
                    self.done = True
                    self.set_pass_found(True)
                    break

                need_retest = False

                self.counter.up()

                resp.close()
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
