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
from classes.threads.DnsBruteThread import DnsBruteThread
from classes.threads.params.DnsBruteThreadParams import DnsBruteThreadParams


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

    def main_action(self):
        """ Action brute of module """
        self.enable_logger()
        self.validate_main()
        self.pre_start_inf()

        if self.options['http-proxies'].value:
            Registry().get('proxies').load(self.options['http-proxies'].value)

        q = DnsBruteJob()

        loaded = self.load_objects(q)
        self.logger.log(
            "Loaded {0} words ({1}-{2}) from all {3}.".format(
                (loaded['end'] - loaded['start']), loaded['start'], loaded['end'], loaded['all'])
            if (int(self.options['parts'].value) and int(self.options['part'].value)) else
            "Loaded {0} words from source.".format(loaded['all'])
        )
        counter = WSCounter(5, 300, loaded['all'] if not loaded['end'] else loaded['end']-loaded['start'])

        result = []

        w_thrds = []
        DnsRoller = Roller()
        DnsRoller.load_file(Registry().get('wr_path') + '/bases/dns-servers.txt')
        for _ in range(int(self.options['threads'].value)):
            we_need_server = True
            while we_need_server:
                we_need_server = False
                try:
                    next_server = DnsRoller.get()
                    #print "Next DNS " + next_server
                    if self.options['protocol'].value == 'auto':
                        try:
                            dns.query.tcp(dns.message.make_query('test.com', 'A'), next_server, timeout=5)
                            protocol = 'tcp'
                        except socket.error:
                            try:
                                dns.query.udp(dns.message.make_query('test.com', 'A'), next_server, timeout=5)
                                protocol = 'udp'
                            except socket.error:
                                #raise Exception('Can`t detect DNS-server protocol. Check addr.')
                                we_need_server = True
                        #print 'DNS protolol detected automaticaly: ' + protocol
                    else:
                        protocol = self.options['protocol'].value
                except dns.exception.Timeout:
                    self.logger.log("Check server {0}. Don`t work.".format(next_server))
                    we_need_server = True

            hosts = []
            hosts.append(self.options['host'].value)
            params = DnsBruteThreadParams(self.options)
            worker = DnsBruteThread(q, hosts, protocol, next_server, result, counter, params)
            worker.start()
            w_thrds.append(worker)

            time.sleep(1)

        while len(w_thrds):
            for worker in w_thrds:
                if worker.done or Registry().get('positive_limit_stop'):
                    del w_thrds[w_thrds.index(worker)]
            time.sleep(2)

        if self.options['host'].value == 'all':
            self._output_zones(result)
        else:
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

    def _output_zones(self, result):
        zones = {}
        for host in result:
            zone = ".".join(host['name'].split(".")[-2:])
            if zone not in zones.keys():
                zones[zone] = []
            zones[zone].append(host)
            zones[zone].sort()

        self.logger.log("\nFound hosts (full):")
        for zone in zones:
            self.logger.log("\tZone {0}:".format(zone))

            for host in zones[zone]:
                self.logger.log("\t\t{0} {1} (DNS: {2})".format(host['name'], host['ip'], host['dns']))

        self.logger.log("\nFound hosts names:")
        for zone in zones:
            self.logger.log("\tZone {0}:".format(zone))
            for host in zones[zone]:
                self.logger.log("\t\t{0}".format(host['name']))

        self.logger.log("Found IPs by zones:")
        for zone in zones:
            self.logger.log("\tZone {0}:".format(zone))

            uniq_hosts = []
            for host in zones[zone]:
                uniq_hosts.append(host['ip'])
            uniq_hosts = list(set(uniq_hosts))

            for host in uniq_hosts:
                self.logger.log("\t\t" + host)

        self.logger.log("Found IPs (all):")

        uniq_hosts = []
        for zone in zones:
            for host in zones[zone]:
                uniq_hosts.append(host['ip'])
        uniq_hosts = list(set(uniq_hosts))

        for host in uniq_hosts:
            self.logger.log("\t" + host)

        if Registry().get('positive_limit_stop'):
            self.logger.log("\nMany positive detections. Please, look items logs")
            self.logger.log("Last items:")
            for i in range(1, 5):
                print result[-i]
            exit(1)
