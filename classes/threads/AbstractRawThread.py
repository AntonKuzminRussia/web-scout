# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common parent for all threads working with raw http (not by selenium)
"""

import copy

from libs.common import is_binary_content_type
from classes.Registry import Registry
from classes.threads.AbstractThread import AbstractThread
from libs.common import get_response_size


class AbstractRawThread(AbstractThread):
    """ Common parent for all threads working with raw http (not by selenium) """
    http = None

    def __init__(self):
        AbstractThread.__init__(self)
        self.http = copy.deepcopy(Registry().get('http'))

    def get_response_full_text(self,  resp):
        """ Return headers and body of response """
        proto_version = "1.1" if resp.raw.version == 11 else "1.0"
        first_str = "HTTP/{0} {1} {2}".format(proto_version, resp.status_code, resp.raw.reason)
        return first_str + "\r\n" + self.get_headers_text(resp) + "\r\n" + resp.text

    def test_log(self, target_obj, resp, positive_item):
        """
        Log data for test mode
        :param target_obj: checked obj (params str, dir name, url, files set, ...)
        :param resp:
        :param positive_item:
        :return:
        """
        if not self.is_test():
            return
        if isinstance(target_obj, dict):
            target_obj = ",".join(target_obj.keys())

        self.test_put(
            target_obj,
            {
                'code': resp.status_code if resp is not None else 0,
                'positive': positive_item,
                'size': get_response_size(resp) if resp is not None else 0,
                'content': resp.text if resp is not None else '',
            }
        )

    def is_response_content_binary(self, resp):
        """

        :param resp:
        :return:
        """
        return resp is not None \
            and 'content-type' in resp.headers \
            and is_binary_content_type(resp.headers['content-type'])

    def get_headers_text(self, resp):
        """
        Join all headers from Response object in one string (http represenation with \r\n)
        :param resp:
        :return:
        """
        response_headers_text = ''
        for header in resp.headers:
            response_headers_text += '{0}: {1}\r\n'.format(header, resp.headers[header])
        return response_headers_text

    def is_response_right(self, resp):
        """
        Return true if response has not false or not-found respose attribute(s)
        :param resp:
        :return:
        """
        if resp is None:
            return False

        if self.not_found_size != -1:
            return self.not_found_size != len(resp.content)

        if self.not_found_re and not self.is_response_content_binary(resp):
            return not self.not_found_re.findall(self.get_response_full_text(resp))

        if str(resp.status_code) not in self.not_found_codes:
            return True

        return False

    def log_item(self, item_str, resp, is_positive):
        """
        Logging checked item
        :param item_str:
        :param resp:
        :param is_positive:
        :return:
        """
        if isinstance(resp, str):
            log_content = resp
        else:
            if resp is None:
                log_content = ""
            else:
                log_content = resp.content if self.is_response_content_binary(resp) else resp.text

        Registry().get('logger').item(
            item_str,
            log_content,
            self.is_response_content_binary(resp) if not isinstance(resp, str) else False,
            positive=is_positive
        )

    def check_positive_limit_stop(self, result, rate=1):
        """
        Does we have too many positive results now?
        :param result:
        :param rate:
        :return:
        """
        if len(result) >= (int(Registry().get('config')['main']['positive_limit_stop']) * rate):
            Registry().set('positive_limit_stop', True)

    def is_retest_need(self, word, resp):
        """
        Return true if response has attributes of retest need
        :param word:
        :param resp:
        :return:
        """
        try:
            if resp is not None:
                if (len(self.retest_codes) and str(resp.status_code) in self.retest_codes) or \
                        (self.retest_re and self.retest_re.findall(resp.text)):
                    if word not in self.retested_words.keys():
                        self.retested_words[word] = 0
                    self.retested_words[word] += 1

                    return self.retested_words[word] <= self.retest_limit
        except BaseException as e:
            print(e)
        return False