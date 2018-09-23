# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for Dafs modules (selenium)
"""

import Queue
import time

from selenium.common.exceptions import TimeoutException
from classes.threads.params.ParamsBruterThreadParams import ParamsBruterThreadParams
from classes.Registry import Registry
from classes.threads.SeleniumThread import SeleniumThread


class SParamsBruterThread(SeleniumThread):
    """ Thread class for Dafs modules (selenium) """
    method = None
    template = None
    mask_symbol = None
    queue_is_empty = False
    last_word = ""

    def __init__(self, queue, counter, result, params):
        """

        :type params: ParamsBruterThreadParams
        """
        SeleniumThread.__init__(self)
        self.queue = queue
        self.protocol = params.protocol
        self.host = params.host
        self.method = 'get'
        self.url = params.url
        self.max_params_length = params.max_params_length
        self.mask_symbol = params.msymbol
        self.counter = counter
        self.result = result
        self.value = params.value
        self.not_found_re = params.not_found_re
        self.recreate_re = params.browser_recreate_re
        self.delay = params.delay
        self.ddos_phrase = params.ddos_detect_phrase
        self.ddos_human = params.ddos_human_action
        self.ignore_words_re = params.ignore_words_re

        Registry().set('url_for_proxy_check', "{0}://{1}".format(self.protocol, self.host))

        self.browser_create()

    def build_params_str(self):
        params_str = "" if not len(self.last_word) else "{0}={1}&".format(self.last_word, self.value)
        self.last_word = ""
        while len(params_str) < self.max_params_length:
            try:
                word = self.queue.get()
            except Queue.Empty:
                self.queue_is_empty = True
                break

            if not len(word.strip()) or (self.ignore_words_re and self.ignore_words_re.findall(word)):
                continue

            self.counter.up()

            params_str += "{0}={1}&".format(word, self.value)

            self.last_word = word

        return params_str[:-(len(self.last_word) + 3)]

    def run(self):
        """ Run thread """
        need_retest = False

        while not self.done:
            self.last_action = int(time.time())

            if self.delay:
                time.sleep(self.delay)

            try:
                if not need_retest:
                    params_str = params_str = self.build_params_str()

                self.browser.get(self.protocol + "://" + self.host + self.url + params_str)

                if self.recreate_re and self.recreate_re.findall(self.browser.page_source):
                    need_retest = True
                    self.browser_close()
                    self.browser_create()
                    continue

                positive_item = False
                if not self.not_found_re.findall(self.browser.page_source):
                    param_found = False
                    for one_param in params_str.split("&"):
                        self.browser.get(self.protocol + "://" + self.host + self.url + one_param)

                        if not self.not_found_re.findall(self.browser.page_source):
                            self.result.append(one_param)
                            if Registry().isset('xml'):
                                Registry().get('xml').put_result({'param': one_param})
                            param_found = True
                            found_item = one_param

                    if param_found is False:
                        if Registry().isset('xml'):
                            Registry().get('xml').put_result({'param': params_str})
                        self.result.append(params_str)
                        found_item = params_str

                    positive_item = True

                self.logger.item(found_item, self.browser.page_source, True, positive=positive_item)

                if Registry().isset('tester'):
                    Registry().get('tester').put(
                        params_str,
                        {
                            'positive': positive_item,
                            'size': len(self.browser.page_source),
                            'content': self.browser.page_source,
                        }
                    )

                if len(self.result) >= int(Registry().get('config')['main']['positive_limit_stop']):
                    Registry().set('positive_limit_stop', True)

                need_retest = False

                if self.queue_is_empty:
                    self.done = True
                    break
            except UnicodeDecodeError as e:
                self.logger.ex(e)
                need_retest = False
            except TimeoutException as e:
                need_retest = True
                self.browser_close()
                self.browser_create()
                continue
            except BaseException as e:
                try:
                    need_retest = True
                    if len(e.args) and e.args[0] == 111:
                        self.browser_close()
                        self.browser_create()
                    elif not str(e).count('Timed out waiting for page load'):
                        self.logger.ex(e)
                except UnicodeDecodeError:
                    need_retest = False
            self.up_requests_count()

            if Registry().isset('tester') and Registry().get('tester').done():
                self.done = True
                break

        self.browser_close()
