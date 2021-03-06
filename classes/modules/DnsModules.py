# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Common class for DnsBrute modules
"""

import time
import re

from classes.kernel.WSCounter import WSCounter
from classes.kernel.WSException import WSException
from classes.kernel.WSModule import WSModule
from classes.jobs.DnsBruteJob import DnsBruteJob
from classes.threads.pools.DnsThreadsPool import DnsThreadsPool


class DnsBruterModules(WSModule):
    """ Common class for DnsBrute modules """
    logger_enable = True
    logger_name = 'dns'
    logger_have_items = True

    def validate_main(self):
        """ Check users params """
        super(DnsBruterModules, self).validate_main()

        if not self.options['template'].value.count("."):
            raise WSException(
                "Bad template structure, dot not found"
            )

        if self.options['template'].value.endswith(".onion"):
            raise WSException(
                "DNS bruteforce for .onion is pointless"
            )

        if re.search('[^a-zA-Z0-9\-\.]', self.options['template'].value.replace(self.options['msymbol'].value, '')):
            raise WSException(
                "Template contains bad symbols, check it. Allowed only a-zA-Z0-9, -, ., " +
                self.options['msymbol'].value
            )

    def start_pool(self):
        """
        Start threads pool and check it alive
        :return:
        """
        pool = DnsThreadsPool(self.queue, self.counter, self.result, self.options, self.logger)
        pool.start()

        while pool.isAlive():
            if self.is_critical_stop():
                pool.kill_all()
            time.sleep(1)

    def make_queue(self):
        """
        Make queue for work
        :return:
        """
        self.queue = DnsBruteJob()

        loaded = self.load_objects(self.queue)
        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )
        self.counter = WSCounter.factory(loaded['all'] if not loaded['end'] else loaded['end'] - loaded['start'])

    def output(self):
        """
        Write output in the end of work
        :return:
        """
        WSModule.output(self)

        self.logger.log("\nFound hosts (full):")
        for host in self.result:
            self.logger.log("\t{0} {1} (DNS: {2})".format(host['name'], host['ip'], host['dns']))

        self.logger.log("\nFound hosts names:")
        for host in self.result:
            self.logger.log("\t{0}".format(host['name']))

        self.logger.log("Found IPs:")

        uniq_hosts = []
        for host in self.result:
            uniq_hosts.append(host['ip'])
        uniq_hosts = list(set(uniq_hosts))

        for host in uniq_hosts:
            self.logger.log("\t" + host)

        self.logger.log("\nFound {0} hosts.".format(len(self.result)))
