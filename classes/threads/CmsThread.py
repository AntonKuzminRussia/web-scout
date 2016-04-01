# -*- coding: utf-8 -*-
""" Thread class for CMS module """
from __future__ import division

import threading
import Queue
import time
import re
import pprint

from requests.exceptions import ChunkedEncodingError, ConnectionError

from classes.Registry import Registry
from libs.common import clear_double_slashes, is_binary_content_type

class CmsThread(threading.Thread):
    """ Thread class for CMS module """
    queue = None
    method = None
    url = None
    counter = None
    last_action = 0

    def __init__(self, queue, domain, url, protocol, method, not_found_re, not_found_codes, delay, counter, result):
        threading.Thread.__init__(self)
        self.queue = queue
        self.method = method if not (len(not_found_re) and method.lower() == 'head') else 'get'
        self.domain = domain
        self.url = url
        self.result = result
        self.counter = counter
        self.protocol = protocol
        self.not_found_re = False if not len(not_found_re) else re.compile(not_found_re)

        not_found_codes = not_found_codes.split(',')
        not_found_codes.append('404')
        self.not_found_codes = list(set(not_found_codes))

        self.delay = int(delay)

        self.done = False
        self.http = Registry().get('http')
        self.logger = Registry().get('logger')

    def run(self):
        """ Run thread """
        req_func = getattr(self.http, self.method)
        need_retest = False

        while not self.done:
            self.last_action = int(time.time())

            if self.delay:
                time.sleep(self.delay)

            try:
                if not need_retest:
                    path = self.queue.get()

                try:
                    url = "{0}://{1}{2}".format(self.protocol, self.domain, clear_double_slashes(self.url + path))
                except UnicodeDecodeError:
                    self.logger.log(
                        "URL build error (UnicodeDecodeError) with path '{0}', skip it".format(pprint.pformat(path)),
                        _print=False
                    )
                    continue
                except UnicodeEncodeError:
                    self.logger.log(
                        "URL build error (UnicodeEncodeError) with path '{0}', skip it".format(pprint.pformat(path)),
                        _print=False
                    )
                    continue

                try:
                    resp = req_func(url)
                except ConnectionError:
                    need_retest = True
                    self.http.change_proxy()
                    continue
                binary_content = resp is not None and is_binary_content_type(resp.headers['content-type'])

                if resp is not None \
                    and str(resp.status_code) not in(self.not_found_codes) \
                    and not (not binary_content and self.not_found_re and self.not_found_re.findall(resp.content)):
                    self.result.append({
                        'path': path,
                        'code': resp.status_code,
                    })

                self.logger.item(
                    path,
                    resp.content if not resp is None else "",
                    binary_content
                )

                self.counter.up()

                self.queue.task_done()
                need_retest = False
            except Queue.Empty:
                self.done = True
                break
            except ChunkedEncodingError as e:
                self.logger.ex(e)
            except UnicodeDecodeError as e:
                self.logger.ex(e)
                self.queue.task_done()
            except BaseException as e:
                try:
                    self.queue.put(path)
                    if not str(e).count('Timed out waiting for page load'):
                        self.logger.ex(e)
                except UnicodeDecodeError:
                    pass
                self.queue.task_done()
