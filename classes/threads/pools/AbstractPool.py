# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Abstract class for all pools
"""

import threading
import time

from classes.Registry import Registry


class AbstractPool(threading.Thread):
    daemon = True

    queue = None
    counter = None
    result = None
    options = None
    threads_params = None
    logger = None

    kill_timeout = None
    threads_resurect_max_count = None
    pool = []

    def __init__(self, queue, counter, result, options, logger):
        threading.Thread.__init__(self)

        self.logger = logger
        self.options = options
        self.result = result
        self.counter = counter
        self.queue = queue

        self.kill_timeout = int(Registry().get('config')['main']['kill_thread_after_secs'])
        self.threads_resurect_max_count = int(Registry().get('config')['main']['timeout_threads_resurect_max_count'])
        self.threads_params = self.build_threads_params()

    def build_threads_params(self):
        raise Exception("This method must be declared in child object")

    def born_thread(self):
        raise Exception("This method must be declared in child object")

    def kill_all(self):
        for thrd in self.pool:
            thrd.done = True

    def run(self):
        for _ in range(int(self.options['threads'].value)):
            self.pool.append(self.born_thread())
            time.sleep(1)

        timeout_threads_count = 0

        active = True
        while active:
            active = False

            for thrd in self.pool:
                if not thrd.done and thrd.isAlive():
                    active = True

                if int(time.time()) - thrd.last_action > self.kill_timeout:
                    self.logger.log(
                        "Thread killed by time, resurected {0} times from {1}".format(
                            timeout_threads_count,
                            self.threads_resurect_max_count
                        )
                    )
                    del self.pool[self.pool.index(thrd)]

                    if timeout_threads_count <= self.threads_resurect_max_count:
                        self.pool.append(self.born_thread())

                        timeout_threads_count += 1

            time.sleep(1)