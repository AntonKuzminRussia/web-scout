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
import os
import urllib3
from urlparse import urlparse

from libs.common import secs_to_text, main_help, t

from classes.kernel.WSBase import WSBase
from classes.Registry import Registry
from classes.kernel.WSException import WSException
from classes.logger.Logger import Logger
from classes.Tester import Tester
from classes.XmlOutput import XmlOutput

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if len(sys.argv) < 2:
    main_help()

module_name = sys.argv[1]

base = WSBase()

logging.captureWarnings(True)

try:
    module = base.load_module(module_name)
except WSException as e:
    if len(str(e)):
        print(e)
    else:
        print "ERROR: Module '{0}' not exists!".format(module_name)
        print "Possible modules:"
        modules_list = []
        for tmp in os.listdir(Registry().get('wr_path') + "/classes/modules/"):
            if tmp.count("Modules") or tmp.count(".pyc") or tmp.count("__init__") or tmp == "params":
                continue
            modules_list.append(tmp.replace(".py", ""))
        modules_list.sort()
        for module_name in modules_list:
            print "\t" + module_name
    exit(1)

if module.logger_enable:
    Registry().set('logger', Logger(module.logger_name, module.logger_have_items))

if module.time_count:
    print "Started module work at " + t("%Y-%m-%d %H:%M:%S")
    start_time = int(time.time())

Registry().set('module', module)

parser = argparse.ArgumentParser(
    description="",
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

        if option == 'tor' and args[option].strip():
            Registry().set('tor', True)

        if (option == 'url' and args[option].strip()) or \
                (option == 'template' and args[option].strip()):
            value = args[option].strip()
            if urlparse(value).netloc.endswith('.onion'):
                Registry().set('tor', True)

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

if module.logger_enable:
    Registry().get('logger').stop()

if Registry().isset('display'):
    Registry().get('display').stop()

if Registry().isset('tester'):
    Registry().get('tester').dump()

if len(Registry().get('tmp_files')):
    for tmp_file in Registry().get('tmp_files'):
        os.remove(tmp_file)

elif module.time_count:
    print "\nEnded module work at " + t("%Y-%m-%d %H:%M:%S")
    print "Common work time: {0}".format(secs_to_text(int(time.time()) - start_time))
