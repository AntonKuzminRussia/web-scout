# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for Dafs modules (selenium)
"""

import queue
import time
import pprint

from selenium.common.exceptions import TimeoutException

from classes.Registry import Registry
from classes.threads.AbstractSeleniumThread import AbstractSeleniumThread
from classes.threads.params.DafsParams import DafsParams


class UrlsSeleniumThread(AbstractSeleniumThread):
    """ Thread class for Dafs modules (selenium) """
    method = None
    mask_symbol = None
    template = None

    def __init__(self, queue, counter, result, params):
        """

        :type params: DafsParams
        """
        super(UrlsSeleniumThread, self).__init__()
        self.queue = queue
        self.template = params.template
        self.method = params.method
        self.mask_symbol = params.msymbol
        self.counter = counter
        self.result = result
        self.not_found_re = params.not_found_re
        self.found_re = params.found_re
        self.not_found_size = params.not_found_size
        self.browser_recreate_re = params.browser_recreate_re
        self.delay = params.delay
        self.browser_wait_re = params.browser_wait_re
        self.ignore_words_re = params.ignore_words_re

        Registry().set('url_for_proxy_check', self.template)

        self.browser_create()

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

                try:
                    url = self.template.replace(self.mask_symbol, word)
                except UnicodeDecodeError:
                    self.logger.log(
                        "URL build error (UnicodeDecodeError) with word '{0}', skip it".format(pprint.pformat(word)),
                        _print=False
                    )
                    continue

                rtime = int(time.time())
                self.browser.get(url)

                if self.browser_recreate_re and self.browser_recreate_re.findall(self.browser.page_source):
                    need_retest = True
                    self.browser_close()
                    self.browser_create()
                    continue

                positive_item = False
                if (self.not_found_re and not self.not_found_re.findall(self.browser.page_source)) or \
                        (self.not_found_size != -1 and len(self.browser.page_source) != self.not_found_size) or \
                        (self.found_re and self.not_found_re.findall(self.browser.page_source)):
                    item_data = {'url': url, 'code': 0, 'time': int(time.time()) - rtime}
                    self.xml_log(item_data)
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

                self.counter.up()
            except queue.Empty:
                self.done = True
                break

            except UnicodeDecodeError as e:
                self.logger.ex(e)
                need_retest = False
            except TimeoutException as e:
                item_data = {'url': url, 'code': 0, 'time': int(time.time()) - rtime}
                self.xml_log(item_data)
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

                # need_retest = True
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
