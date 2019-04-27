# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Alexey Meshcheryakov <tank1st99@gmail.com>

Kernel base class. Prepare work, load config, connect db, etc
"""

from classes.Registry import Registry


class ErrorsCounter:
    counter = 0
    reported = False

    @staticmethod
    def up():
        ErrorsCounter.counter += 1
        if not ErrorsCounter.reported and ErrorsCounter.counter/(int(Registry().get('config')['main']['errors_limit'])/100) > 70:
            Registry().get("logger").log("\nAttention! Too many errors, 70% of limit!")
            ErrorsCounter.reported = True

    @staticmethod
    def is_limit():
        """ Is we get errors count limit? """
        return ErrorsCounter.counter > int(Registry().get('config')['main']['errors_limit'])

    @staticmethod
    def flush():
        ErrorsCounter.counter = 0
        ErrorsCounter.reported = False
