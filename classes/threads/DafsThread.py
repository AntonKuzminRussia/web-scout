# -*- coding: utf-8 -*-
""" Thread class for Dafs modules """

import threading
import Queue
import time
import copy
import re
import pprint

from requests.exceptions import ChunkedEncodingError, ConnectionError

from classes.Registry import Registry
from libs.common import is_binary_content_type


class DafsThread(threading.Thread):
    """ Thread class for Dafs modules """
    queue = None
    method = None
    url = None
    mask_symbol = None
    counter = None
    retested_words = None
    last_action = 0
    retest_limit = int(Registry().get('config')['dafs']['retest_limit'])

    def __init__(
            self, queue, protocol, host, url, method, mask_symbol, not_found_re,
            not_found_codes, retest_codes, delay, counter, result):
        threading.Thread.__init__(self)
        self.retested_words = {}
        
        self.queue = queue
        self.protocol = protocol.lower()
        self.host = host
        self.method = method if not (len(not_found_re) and method.lower() == 'head') else 'get'
        self.url = url
        self.mask_symbol = mask_symbol
        self.counter = counter
        self.result = result
        self.done = False
        self.not_found_re = False if not len(not_found_re) else re.compile(not_found_re)

        not_found_codes = not_found_codes.split(',')
        not_found_codes.append('404')
        self.not_found_codes = list(set(not_found_codes))
        self.retest_codes = list(set(retest_codes.split(','))) if len(retest_codes) else []

        self.delay = int(delay)

        self.http = copy.deepcopy(Registry().get('http'))
        self.logger = Registry().get('logger')

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
                    self.counter.up()

                try:
                    url = self.url.replace(self.mask_symbol, word)
                except UnicodeDecodeError:
                    self.logger.log(
                        "URL build error (UnicodeDecodeError) with word '{0}', skip it".format(pprint.pformat(word)),
                        _print=False
                    )
                    continue
                rtime = int(time.time())

                try:
                    resp = req_func(self.protocol + "://" + self.host + url)
                except ConnectionError:
                    need_retest = True
                    self.http.change_proxy()
                    continue

                binary_content = resp is not None \
                                 and 'content-type' in resp.headers \
                                 and is_binary_content_type(resp.headers['content-type'])

                if resp is not None and len(self.retest_codes) and str(resp.status_code) in self.retest_codes:
                    if word not in self.retested_words.keys():
                        self.retested_words[word] = 0
                    self.retested_words[word] += 1

                    if self.retested_words[word] <= self.retest_limit:
                        need_retest = True
                        time.sleep(int(Registry().get('config')['dafs']['retest_delay']))
                        continue

                if resp is not None \
                    and str(resp.status_code) not in self.not_found_codes \
                    and not (not binary_content and self.not_found_re and self.not_found_re.findall(resp.content)):
                    self.result.append({
                        'url': url,
                        'code': resp.status_code,
                        'time': int(time.time()) - rtime
                    })

                self.logger.item(word, resp.content if not resp is None else "", binary_content)

                if len(self.result) >= int(Registry().get('config')['main']['positive_limit_stop']):
                    Registry().set('positive_limit_stop', True)

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
