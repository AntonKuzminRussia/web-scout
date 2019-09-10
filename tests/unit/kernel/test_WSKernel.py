# -*- coding: utf-8 -*-
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from classes.kernel.WSKernel import WSKernel


class ThreadMock():
    started = False
    running = True

    def start(self):
        self.started = True


class Test_WSKernel(object):
    def test_create_threads(self):
        thread1 = ThreadMock()
        thread2 = ThreadMock()
        thread3 = ThreadMock()

        kernel = WSKernel()
        kernel.create_threads([thread1, thread2, thread3])

        assert 3 == len(kernel.pool)

        assert thread1.started
        assert thread2.started
        assert thread3.started

    def test_finished(self):
        thread1 = ThreadMock()
        thread2 = ThreadMock()
        thread3 = ThreadMock()

        kernel = WSKernel()
        kernel.create_threads([thread1, thread2, thread3])

        assert not kernel.finished()

        thread1.running = False
        thread2.running = False
        thread3.running = False

        assert kernel.finished()