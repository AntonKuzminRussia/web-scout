#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)
          (c) Alexey Meshcheryakov <tank1st99@gmail.com>

Main run file
"""

import sys
import argparse
import time
import logging

from libs.common import secs_to_text, main_help

from classes.kernel.WSBase import WSBase
from classes.Registry import Registry
from classes.kernel.WSException import WSException
from classes.Logger import Logger
from classes.Tester import Tester
from classes.XmlOutput import XmlOutput

if len(sys.argv) < 2:
    main_help()

module_name = sys.argv[1]

base = WSBase()

logging.captureWarnings(True)

try:
    module = base.load_module(module_name)
except WSException as e:
    print(e)
    print " ERROR: Module '{0}' not exists!".format(module_name)
    exit(0)

if module.logger_enable:
    Registry().set('logger', Logger(module.logger_name, module.logger_have_items))

if module.time_count:
    print "Started module work at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    start_time = int(time.time())

Registry().set('module', module)

parser = argparse.ArgumentParser(
    description=module.help(),
    prog="{0} {1}".format(sys.argv[0], sys.argv[1])
)
for option in module.options:
    parser.add_argument(
        *module.options[option].flags,
        required=module.options[option].required,
        help=module.options[option].description,
        dest=module.options[option].name
    )

args = vars(parser.parse_args(sys.argv[2:]))
for option in args.keys():
    if args[option] is not None:
        module.options[option].value = args[option].strip()

        if option == 'xml-report' and args[option].strip():
            Registry().set('xml', XmlOutput(args[option].strip()))

        if option == 'test' and args[option].strip():
            Registry().set('tester', Tester())
            module.options["threads"].value = "1"

        if option == 'headers-file':
            try:
                Registry().get('http').load_headers_from_file(args[option].strip())
            except WSException as e:
                print "{0}".format(str(e))
                exit(0)

try:
    module.do_work()

    while not module.finished():
        try:
            sys.stdout.flush()
        except BaseException:
            time.sleep(1)

except WSException as e:
    print " " + str(e)

Http = Registry().get('http')
for k in Http.errors:
    for err_str in Http.errors[k]:
        print err_str

if Registry().isset('display'):
    Registry().get('display').stop()

if Registry().isset('tester'):
    Registry().get('tester').dump()
elif module.time_count:
    print "\nEnded module work at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print "Common work time: {0}".format(secs_to_text(int(time.time()) - start_time))
