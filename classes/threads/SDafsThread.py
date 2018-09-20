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
import re
import pprint

from selenium.common.exceptions import TimeoutException

from classes.Registry import Registry
from classes.threads.SeleniumThread import SeleniumThread
from classes.threads.params.DafsThreadParams import DafsThreadParams

class SDafsThread(SeleniumThread):
    """ Thread class for Dafs modules (selenium) """
    queue = None
    method = None
    template = None
    mask_symbol = None
    counter = None
    last_action = 0

    def __init__(self, queue, counter, result, params):
        """

        :type params: DafsThreadParams
        """
        super(SDafsThread, self).__init__()
        self.queue = queue
        self.protocol = params.protocol
        self.host = params.host
        self.method = params.method if not (len(params.not_found_re) and params.method.lower() == 'head') else 'get'
        self.template = params.template
        self.mask_symbol = params.mask_symbol
        self.counter = counter
        self.result = result
        self.done = False
        self.not_found_re = False if not len(params.not_found_re) else re.compile(params.not_found_re)
        self.recreate_re = False if not len(params.browser_recreate_re) else re.compile(params.browser_recreate_re)
        self.http = Registry().get('http')
        self.delay = int(params.delay)
        self.ddos_phrase = params.ddos_detect_phrase
        self.ddos_human = params.ddos_human_action
        self.ignore_words_re = False if not len(params.ignore_words_re) else re.compile(params.ignore_words_re)

        Registry().set('url_for_proxy_check', "{0}://{1}".format(self.protocol, self.host))

        self.browser_create()

        self.logger = Registry().get('logger')

    def run(self):
        """ Run thread """
        need_retest = False
        word = None
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
                self.browser.get(self.protocol + "://" + self.host + url)

                if self.recreate_re and self.recreate_re.findall(self.browser.page_source):
                    need_retest = True
                    self.browser_close()
                    self.browser_create()
                    continue

                positive_item = False
                if not self.not_found_re.findall(self.browser.page_source):
                    item_data = {'url': url, 'code': 0, 'time': int(time.time()) - rtime}
                    if Registry().isset('xml'):
                        Registry().get('xml').put_result(item_data)
                    self.result.append(item_data)
                    positive_item = True

                if Registry().isset('tester'):
                    Registry().get('tester').put(
                        url,
                        {
                            'code': 0,
                            'positive': positive_item,
                            'size': len(self.browser.page_source),
                            'content': self.browser.page_source,
                        }
                    )

                self.logger.item(word, self.browser.page_source, False, positive_item)

                if len(self.result) >= int(Registry().get('config')['main']['positive_limit_stop']):
                    Registry().set('positive_limit_stop', True)

                need_retest = False
            except Queue.Empty:
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
