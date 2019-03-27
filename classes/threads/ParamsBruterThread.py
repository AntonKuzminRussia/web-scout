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
import os

from requests.exceptions import ChunkedEncodingError, ConnectionError
from classes.threads.HttpThread import HttpThread
from classes.threads.params.ParamsBruterThreadParams import ParamsBruterThreadParams

from libs.common import file_put_contents


class ParamsBruterThread(HttpThread):
    """ Thread class for ParamsBrute modules """
    method = None
    template = None
    mask_symbol = None
    retested_words = None
    ignore_words_re = None
    queue_is_empty = False
    last_word = ""
    tmp_filepath = "/tmp/tmpfileforparamswork.txt"
    files_params_fh = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: ParamsBruterThreadParams
        """
        HttpThread.__init__(self)
        self.retested_words = {}

        self.queue = queue
        self.url = params.url
        self.mask_symbol = params.msymbol
        self.counter = counter
        self.result = result
        self.value = params.value
        self.max_params_length = params.max_params_length
        self.ignore_words_re = params.ignore_words_re
        self.not_found_re = params.not_found_re
        self.not_found_size = params.not_found_size
        self.method = params.method
        self.not_found_codes = params.not_found_codes
        self.retest_codes = params.retest_codes
        self.retest_phrase = params.retest_phrase
        self.delay = params.delay

        if not os.path.exists(self.tmp_filepath):
            file_put_contents(self.tmp_filepath, "test")

        self.files_params_fh = open(self.tmp_filepath, "rb")

    def build_params_str(self):
        if self.method in ['get', 'post']:
            params_str = "" if not len(self.last_word) else "{0}={1}&".format(self.last_word, self.value)
            self.last_word = ""
            while len(params_str) < self.max_params_length:
                try:
                    word = self.queue.get()
                except Queue.Empty:
                    self.queue_is_empty = True
                    if params_str == "":
                        raise Queue.Empty
                    break

                if not len(word.strip()) or (self.ignore_words_re and self.ignore_words_re.findall(word)):
                    continue

                params_str += "{0}={1}&".format(word, self.value)

                self.last_word = word

                if self.is_test():
                    break

            return params_str[:-(len(self.last_word) + 3)]
        elif self.method == 'cookies':
            cookies = {self.last_word: self.value} if len(self.last_word) else {}

            self.last_word = ""
            while len(cookies) < self.max_params_length:
                try:
                    word = self.queue.get()
                except Queue.Empty:
                    self.queue_is_empty = True
                    if len(cookies) == 0:
                        raise Queue.Empty
                    break

                if not len(word.strip()) or (self.ignore_words_re and self.ignore_words_re.findall(word)):
                    continue

                cookies[word] = self.value

                self.last_word = word

            return cookies
        elif self.method == 'files':
            files = {self.last_word: self.files_params_fh} if len(self.last_word) else {}

            self.last_word = ""
            while len(files) < self.max_params_length:
                try:
                    word = self.queue.get()
                except Queue.Empty:
                    self.queue_is_empty = True
                    if len(files) == 0:
                        raise Queue.Empty
                    break

                if not len(word.strip()) or (self.ignore_words_re and self.ignore_words_re.findall(word)):
                    continue

                files[word] = self.files_params_fh

                self.last_word = word
            return files
        else:
            raise BaseException("Unknown work type - {0}".format(self.method))

    def request_params(self, params):
        if self.method == 'get':
            return self.http.get(self.url + "?" + params)
        elif self.method == 'post':
            return self.http.post(self.url, data=params)
        elif self.method == 'cookies':
            return self.http.get(self.url, cookies=params)
        elif self.method == 'files':
            return self.http.post(self.url, files=params, data={'a': 'b'})
        else:
            raise BaseException("Unknown work type - {0}".format(self.method))

    def split_params(self, params):
        if self.method in ['get', 'post']:
            return params.split("&")
        elif self.method in ['cookies', 'files']:
            to_return = []
            for k in params:
                to_return.append({k: params[k]})
            return to_return
        else:
            raise BaseException("Unknown work type - {0}".format(self.method))

    def param_str_repr(self, param):
        if self.method in ['get', 'post']:
            return param
        elif self.method in ['cookies', 'files']:
            to_return = ""
            for k in param:
                to_return += "{0}".format(k)
            return to_return
        else:
            raise BaseException("Unknown work type - {0}".format(self.method))

    def run(self):
        """ Run thread """
        need_retest = False

        while not self.done:
            self.last_action = int(time.time())

            if self.delay:
                time.sleep(self.delay)

            try:
                if not need_retest:
                    params_str = self.build_params_str()

                try:
                    resp = self.request_params(params_str)
                except ConnectionError:
                    need_retest = True
                    self.http.change_proxy()
                    continue

                if self.is_retest_need(params_str, resp):
                    time.sleep(self.retest_delay)
                    need_retest = True
                    continue

                positive_item = False
                if self.is_response_right(resp):
                    param_found = False
                    for one_param in self.split_params(params_str):
                        try:
                            resp = self.request_params(one_param)
                        except ConnectionError:
                            need_retest = True
                            self.http.change_proxy()
                            continue

                        if self.is_response_right(resp):
                            self.result.append(self.param_str_repr(one_param))
                            self.xml_log({'param': self.param_str_repr(one_param)})
                            param_found = True
                            found_item = self.param_str_repr(one_param)

                    if param_found is False:
                        self.xml_log({'param': self.param_str_repr(params_str)})
                        self.result.append(self.param_str_repr(params_str))
                        found_item = self.param_str_repr(params_str)

                    positive_item = True

                    self.log_item(found_item, resp, positive_item)

                self.test_log(params_str, resp, positive_item)

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
