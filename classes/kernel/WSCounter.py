# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Alexey Meshcheryakov <tank1st99@gmail.com>

Kernel class of work counter for all modules
"""
from __future__ import division
import sys
import time

from libs.common import secs_to_text, nformat
from classes.Registry import Registry


class WSCounter(object):
    """ Kernel class of work counter for all modules """
    counter = 0
    last_point_time = 0
    last_point_count = 0

    def __init__(self, point, new_str, _all=0):
        self.point = point
        self.new_str = new_str
        self.all = _all
        self.start_time = int(time.time())
        self.last_point_time = int(time.time())

    def up(self):
        """ Up counter, print result if need """
        try:
            self.counter += 1

            if self.counter%self.point == 0:
                sys.stdout.write('.')

            if self.counter%self.new_str == 0:
                if self.all == 0:
                    print "({0})".format(self.counter)
                else:
                    percents = round(self.counter/(self.all/100)) if round(self.counter/(self.all/100)) > 0 else 1
                    # Костыль если 0 секунд прошло, а уже есть что выводить
                    time_now = int(time.time()) - self.start_time if int(time.time()) - self.start_time > 0 else 1
                    time_left = round((100-percents)*(time_now/percents))

                    counter_str = nformat(self.counter)
                    all_str = nformat(self.all)
                    percent = round(self.counter/(self.all/100), 2)
                    time_now_str = secs_to_text(time_now)
                    time_left_str = secs_to_text(time_left)
                    speed = round((self.counter - self.last_point_count) / (int(time.time()) - self.last_point_time), 2)

                    print "({0}/{1}/{2}%) | {3} | {4} | {5} o/s".format(
                        counter_str,
                        all_str,
                        percent,
                        time_now_str,
                        time_left_str,
                        speed
                    )

                    if Registry().isset('xml'):
                        Registry().get('xml').put_progress(
                            counter_str,
                            all_str,
                            percent,
                            time_now_str,
                            time_left_str,
                            speed
                        )

                    self.last_point_count = self.counter
                    self.last_point_time = int(time.time())
        except ZeroDivisionError:
            pass

        sys.stdout.flush()

        return self

