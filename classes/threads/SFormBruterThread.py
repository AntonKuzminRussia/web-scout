# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for FormBruter module (selenium)
"""
import Queue
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, InvalidElementStateException

from classes.Registry import Registry
from classes.threads.SeleniumThread import SeleniumThread
from classes.threads.params.FormBruterThreadParams import FormBruterThreadParams


class SFormBruterThread(SeleniumThread):
    """ Thread class for FormBruter module (selenium) """
    method = None
    url = None
    mask_symbol = None
    retested_words = None
    first_page_load = False

    def __init__(self, queue, counter, result, params):
        """

        :type params: FormBruterThreadParams
        """
        SeleniumThread.__init__(self)
        self.retested_words = {}

        self.queue = queue
        self.url = params.url
        self.delay = params.delay
        self.browser_wait_re = params.browser_wait_re
        self.browser_recreate_re = params.browser_recreate_phrase
        self.conffile = params.conffile
        self.false_phrase = params.false_phrase
        self.true_phrase = params.true_phrase
        self.first_stop = params.first_stop
        self.login = params.login
        self.reload_form_page = params.reload_form_page
        self.pass_min_len = params.pass_min_len
        self.pass_max_len = params.pass_max_len

        self.browser_create()

        self.counter = counter
        self.result = result

        Registry().set('url_for_proxy_check', params.url)

    def is_pass_found(self):
        """ Is password found? """
        return Registry().get('pass_found')

    def set_pass_found(self, value):
        """ Set pass_found value """
        return Registry().set('pass_found', value)

    def parse_brute_config(self, path):
        """ Parse conf file to dict """
        to_return = {}

        fh = open(path)
        for line in fh.readlines():
            if not len(line.strip()):
                continue

            point, selector = line.strip().split("\t")
            to_return[point] = selector
        return to_return

    def run(self):
        """ Run thread """
        need_retest = False
        word = False

        brute_conf = self.parse_brute_config(self.conffile)

        while not self.is_pass_found() and not self.done:
            try:
                self.last_action = int(time.time())

                if self.delay:
                    time.sleep(self.delay)

                if not need_retest:
                    word = self.queue.get()

                if (self.pass_min_len and len(word) < self.pass_min_len) or \
                        (self.pass_max_len and len(word) > self.pass_max_len):
                    continue

                if self.browser.current_url == 'about:blank' or \
                        self.reload_form_page or \
                       (not self.browser.element_exists(By.CSS_SELECTOR, brute_conf['^USER^']) or
                        not self.browser.element_exists(By.CSS_SELECTOR, brute_conf['^PASS^'])):
                    self.browser.get(self.url)

                # self.browser.get(self.protocol + "://" + self.host + self.url)

                if self.browser_recreate_re and self.browser_recreate_re.findall(self.browser.page_source):
                    need_retest = True
                    self.browser_close()
                    self.browser_create()
                    continue

                timeout_page_load = int(Registry().get('config')['selenium']['timeout_page_load'])
                start_timeout_time = int(time.time())
                while True:
                    try:
                        self.browser.find_element(By.CSS_SELECTOR, brute_conf['^USER^']).clear()
                        self.browser.find_element(By.CSS_SELECTOR, brute_conf['^USER^']).send_keys(self.login)
                        self.browser.find_element(By.CSS_SELECTOR, brute_conf['^PASS^']).clear()
                        self.browser.find_element(By.CSS_SELECTOR, brute_conf['^PASS^']).send_keys(word)
                        self.browser.find_element(By.CSS_SELECTOR, brute_conf['^SUBMIT^']).click()
                        break
                    except InvalidElementStateException as ex:
                        if int(time.time()) < start_timeout_time + timeout_page_load:
                            time.sleep(1)
                        else:
                            raise ex

                time.sleep(1)

                positive_item = False
                if ((len(self.false_phrase) and not self.browser.page_source.count(self.false_phrase)) or
                        (len(self.true_phrase) and self.browser.page_source.count(self.true_phrase))):
                    item_data = {'word': word, 'content': self.browser.page_source}
                    self.result.append(item_data)
                    self.xml_log(item_data)
                    positive_item = True

                    if len(self.result) >= int(Registry().get('config')['main']['positive_limit_stop']):
                        Registry().set('positive_limit_stop', True)

                if Registry().isset('tester'):
                    Registry().get('tester').put(
                        word,
                        {
                            'positive': positive_item,
                            'size': len(self.browser.page_source),
                            'content': self.browser.page_source,
                        }
                    )

                self.logger.item(word, self.browser.page_source, False, positive_item)

                if positive_item:
                    if int(self.first_stop):
                        self.done = True
                        self.set_pass_found(True)
                        break
                    else:
                        # Иначе старая сессия останется и будет куча false-positive
                        self.browser_close()
                        self.browser_create()

                need_retest = False

                self.counter.up()
            except Queue.Empty:
                self.done = True
                break
            except TimeoutException as e:
                need_retest = True
                self.browser_close()
                self.browser_create()
                continue
            except UnicodeDecodeError as e:
                self.logger.ex(e)
                need_retest = False
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
