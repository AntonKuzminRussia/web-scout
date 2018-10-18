# -*- coding: utf-8 -*-
import time

from classes.kernel.WSCounter import WSCounter
from classes.Registry import Registry


class Test_WSCounter(object):
    def test_factory(self):
        Registry().set('config', {'main': {'counter_step': '1', 'counter_steps_for_new_string': '2'}})

        counter = WSCounter.factory(3)

        assert 1 == counter.point
        assert 2 == counter.new_str
        assert 3 == counter.all

        assert int(time.time()) == counter.start_time
        assert int(time.time()) == counter.last_point_time
