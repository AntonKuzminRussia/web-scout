# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common class for DnsBrute modules
"""

import os
import time
import socket

import dns.query
import dns.message

from classes.Roller import Roller
from classes.Registry import Registry
from classes.kernel.WSCounter import WSCounter
from classes.kernel.WSModule import WSModule
from classes.kernel.WSException import WSException
from classes.jobs.DnsBruteJob import DnsBruteJob
from classes.threads.pools.DnsBruteThreadsPool import DnsBruteThreadsPool


class DnsBruteModules(WSModule):
    """ Common class for DnsBrute modules """
    logger_enable = True
    logger_name = 'dns'
    logger_have_items = True

    ZONE_CNAME = 'CNAME'
    ZONE_A = 'A'
    POSSIBLE_ZONES = [ZONE_A, ZONE_CNAME]

    def validate_main(self):
        """ Check users params """
        if self.options['protocol'].value not in ['tcp', 'udp', 'auto']:
            raise WSException(
                "Protocol mast be 'tcp', 'udp' or 'auto', but it is '{0}'"
                .format(self.options['protocol'].value)
            )

        if self.options['http-protocol'].value not in ['http', 'https']:
            raise WSException(
                "HTTP Protocol mast be 'http' or 'https', but it is '{0}'"
                .format(self.options['http-protocol'].value)
            )

        if not self.options['template'].value.count(self.options['msymbol'].value):
            raise WSException(
                "Brute template must contains msymbol ({0}), but it not ({1})"
                .format(self.options['msymbol'].value, self.options['template'].value)
            )

        if self.options['zone'].value.upper() not in self.POSSIBLE_ZONES:
            raise WSException(
                "Wrong DNS zone - '{0}', allowed: {1}"
                .format(self.options['zone'].value, ", ".join(self.POSSIBLE_ZONES))
            )

        if 'http-proxies' in self.options.keys() and len(self.options['http-proxies'].value) and \
                not os.path.exists(self.options['http-proxies'].value):
            raise WSException(
                "Proxy list not found: '{0}'".
                format(self.options['http-proxies'].value)
            )

    def load_objects(self, queue):
        """ Method for prepare test objects, here abstract """
        pass

    def do_work(self):
        """ Action brute of module """
        self.enable_logger()
        self.validate_main()
        self.pre_start_inf()

        if self.options['http-proxies'].value:
            Registry().get('proxies').load(self.options['http-proxies'].value)

        queue = DnsBruteJob()

        loaded = self.load_objects(queue)
        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )
        counter = WSCounter(5, 300, loaded['all'] if not loaded['end'] else loaded['end']-loaded['start'])

        result = []

        pool = DnsBruteThreadsPool(queue, counter, result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if Registry().get('proxy_many_died') or Registry().get('positive_limit_stop'):
                pool.kill_all()
            time.sleep(1)

        self._output(result)

        self.done = True

    def _output(self, result):
        self.logger.log("\nFound hosts (full):")
        for host in result:
            self.logger.log("\t{0} {1} (DNS: {2})".format(host['name'], host['ip'], host['dns']))

        self.logger.log("\nFound hosts names:")
        for host in result:
            self.logger.log("\t{0}".format(host['name']))

        self.logger.log("Found IPs:")

        uniq_hosts = []
        for host in result:
            uniq_hosts.append(host['ip'])
        uniq_hosts = list(set(uniq_hosts))

        for host in uniq_hosts:
            self.logger.log("\t" + host)

        self.logger.log("\nFound {0} hosts.".format(len(result)))
