# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Alexey Meshcheryakov <tank1st99@gmail.com>

Kernel class of modules
"""

import re
import os

from classes.kernel.WSException import WSException
from classes.Registry import Registry
from classes.ErrorsCounter import ErrorsCounter


class WSModule(object):
    """ Kernel class of modules """
    log_path = None
    log_width = 60
    description = "module description"
    done = False
    options = []
    time_count = False
    logger = None
    logger_enable = False
    options_sets = {}

    counter = None
    queue = None
    result = []

    logger_scan_name_option = None

    DNS_ZONE_CNAME = 'CNAME'
    DNS_ZONE_A = 'A'
    POSSIBLE_DNS_ZONES = [DNS_ZONE_A, DNS_ZONE_CNAME]

    def __init__(self, kernel):
        self.kernel = kernel
        if self.log_path is None:
            raise WSException('Module must have log path!')

    def prepare(self):
        self.enable_logger()
        self.validate_main()
        self.pre_start_inf()
        self.load_proxies()

    def work_end_error(self):
        exit(1)

    def output(self):
        if Registry().get('proxy_many_died'):
            self.logger.log("Proxy many died, stop scan")
            self.work_end_error()

        if Registry().get('positive_limit_stop'):
            self.logger.log("\nMany positive detections. Please, look items logs")
            self.logger.log("Last items:")
            for i in range(1, 5):
                self.logger.log(self.result[-i])
            self.work_end_error()

        if ErrorsCounter.is_limit():
            self.logger.log("\nToo many errors")
            self.work_end_error()

    def load_proxies(self):
        for option_key in ['proxies', 'http-proxies']:
            if option_key in self.options.keys() and self.options[option_key].value:
                Registry().get('proxies').load(self.options[option_key].value)

    def load_objects(self, queue):
        """ Method for prepare test objects, here abstract """
        raise WSException("This method must be described in child-class")

    def make_queue(self):
        raise WSException("This method must be described in child-class")

    def start_pool(self):
        raise WSException("This method must be decsribed in child-class")

    def enable_logger(self):
        """ Turn on logger """
        self.logger = Registry().get('logger')

        if self.logger_scan_name_option is not None:
            self.logger.set_scan_name(self.options[self.logger_scan_name_option].value)

    def pre_start_inf(self):
        """ Show options values before work start """
        log_str = ""
        log_str += "---------------------------------\n"
        for option in self.options:
            log_str += "Option '{0}': {1}\n".format(option, self.options[option].value)
        log_str += "Logs dir: {0}\n".format(self.logger.logs_dir)
        log_str += "---------------------------------"
        self.logger.log(log_str)

        if int(Registry().get('config')['main']['confirm']):
            tmp = raw_input("Do you have continue? [Y/n]")
            if len(tmp.strip()) and tmp.lower() != 'y':
                self.logger.log("Aborted...")
                self.work_end_error()

    def finished(self):
        """ Is module finished? """
        return self.done

    def do_work(self):
        """ Scan action of module """
        self.prepare()

        self.make_queue()

        self.start_pool()

        self.output()

        self.done = True

    def validate_main(self):
        """ Common user params validate functions """
        if 'selenium' in self.options.keys() and self.options['selenium'].value:
            if 'not-found-re' in self.options.keys() and not self.options['not-found-re'].value:
                raise WSException("Selenium enabled, module need a not found phrase (--not-found-re) for work!")

            if int(self.options['threads'].value) > int(Registry().get('config')['selenium']['max_threads']):
                raise WSException(
                    "Selenium enabled, very many threads value ({0}), see docs.".format(self.options['threads'].value)
                )

        if 'protocol' in self.options.keys() and self.options['protocol'].value.lower() not in ['http', 'https']:
            raise WSException(
                "Protocol param must be 'http' or 'https', but have value '{0}' !".
                format(self.options['protocol'].value)
            )

        if 'method' in self.options.keys() and self.options['method'].value.lower() not in ['head', 'get', 'post', 'cookies', 'files']:
            raise WSException(
                "Method param must be only 'head', 'get' or 'post', but have value '{0}' !".
                format(self.options['method'].value)
            )

        if 'not-found-codes' in self.options.keys() and len(self.options['not-found-codes'].value):
            for code in self.options['not-found-codes'].value.strip().split(","):
                if len(code.strip()) and not re.match(r'^(\d+)$', code.strip()):
                    raise WSException(
                        "Not-found code must be digital, but it is '{0}'".
                        format(code.strip())
                    )

        if 'retest-codes' in self.options.keys() and len(self.options['retest-codes'].value):
            for code in self.options['retest-codes'].value.strip().split(","):
                if len(code.strip()) and not re.match(r'^(\d+)$', code.strip()):
                    raise WSException(
                        "Retest code must be digital, but it is '{0}'".
                        format(code.strip())
                    )

        for proxies_params in ['proxies', 'http-proxies']:
            if proxies_params in self.options.keys() and len(self.options[proxies_params].value) and \
                    not os.path.exists(self.options[proxies_params].value):
                raise WSException(
                    "Proxy list not found: '{0}'".
                    format(self.options[proxies_params].value)
                )

        if 'not-found-re' in self.options.keys() and len(self.options['not-found-re'].value):
            try:
                re.compile(self.options['not-found-re'].value)
            except re.error:
                raise WSException(
                    "Invalid regex: '{0}'".
                    format(self.options['not-found-re'].value)
                )

        if 'browser-recreate-re' in self.options.keys() and len(self.options['browser-recreate-re'].value):
            try:
                re.compile(self.options['browser-recreate-re'].value)
            except re.error:
                raise WSException(
                    "Invalid regex: '{0}'".
                    format(self.options['browser-recreate-re'].value)
                )

        if 'dict' in self.options.keys() and not os.path.exists(self.options['dict'].value):
            raise WSException("Dictionary '{0}' not exists or not readable!".format(self.options['dict'].value))

        if 'delay' in self.options.keys() and self.options['delay'].value != '0':
            if not re.match(r'^(\d+)$', self.options['delay'].value):
                raise WSException(
                    "Delay param must be digital, but it is '{0}'".
                    format(self.options['delay'].value.strip())
                )

        if 'parts' in self.options.keys() and self.options['parts'].value != '0':
            if not re.match(r'^(\d+)$', self.options['parts'].value):
                raise WSException(
                    "Parts param must be digital, but it is '{0}'".
                    format(self.options['parts'].value.strip())
                )

        if 'part' in self.options.keys() and self.options['part'].value != '0':
            if not re.match(r'^(\d+)$', self.options['part'].value):
                raise WSException(
                    "Part param must be digital, but it is '{0}'".
                    format(self.options['part'].value.strip())
                )

        if 'parts' in self.options.keys() and self.options['parts'].value != '0':
            if 'part' not in self.options.keys() or self.options['part'].value == '0':
                raise WSException(
                    "If you use '--parts' param, you must specify '--part'"
                )
            if int(self.options['part'].value) > int(self.options['parts'].value):
                raise WSException(
                    "Number of part ({0}) more than parts count ({1})".
                    format(self.options['part'].value.strip(), self.options['parts'].value.strip())
                )

        if 'part' in self.options.keys() and self.options['part'].value != '0':
            if 'parts' not in self.options.keys() or self.options['parts'].value == '0':
                raise WSException(
                    "If you use '--part' param, you must specify '--parts'"
                )

        if 'template' in self.options.keys() and 'msymbol' in self.options.keys():
            if self.options['template'].value.find(self.options['msymbol'].value) == -1:
                raise WSException(
                    "Symbol of object position ({0}) not found in template ({1}) ".
                    format(self.options['msymbol'].value, self.options['template'].value)
                )

        if 'zone' in self.options.keys() and self.options['zone'].value.upper() not in self.POSSIBLE_DNS_ZONES:
            raise WSException(
                "Wrong DNS zone - '{0}', allowed: {1}"
                .format(self.options['zone'].value, ", ".join(self.POSSIBLE_DNS_ZONES))
            )

        if 'dns-protocol' in self.options.keys() and self.options['dns-protocol'].value not in ['tcp', 'udp', 'auto']:
            raise WSException(
                "DNS Protocol mast be 'tcp', 'udp' or 'auto', but it is '{0}'"
                .format(self.options['dns-protocol'].value)
            )