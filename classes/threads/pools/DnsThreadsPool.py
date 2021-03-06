# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class
"""

import socket

import dns.query
import dns.message

from classes.threads.DnsRawThread import DnsRawThread
from classes.threads.params.DnsThreadParams import DnsThreadParams
from classes.Roller import Roller
from classes.Registry import Registry
from classes.threads.pools.AbstractPool import AbstractPool


class DnsThreadsPool(AbstractPool):
    servers_roller = None

    def __init__(self, queue, counter, result, options, logger):
        AbstractPool.__init__(self, queue, counter, result, options, logger)

        self.servers_roller = Roller(Registry().get('wr_path') + '/bases/dns/servers.txt')

    def build_threads_params(self):
        return DnsThreadParams(self.options)

    def born_thread(self):
        dns_server, protocol = self.get_next_server()
        thrd = DnsRawThread(self.queue, protocol, dns_server, self.result, self.counter, self.threads_params)
        thrd.start()
        return thrd

    def get_next_server(self):
        """ Get next DNS server from list, checking it protocol and return both """
        we_need_server = True
        while we_need_server:
            we_need_server = False

            try:
                dns_server = self.servers_roller.get()
                if self.options['dns-protocol'].value == 'auto':
                    try:
                        dns.query.tcp(dns.message.make_query('test.com', 'A'), dns_server, timeout=5)
                        protocol = 'tcp'
                    except socket.error:
                        try:
                            dns.query.udp(dns.message.make_query('test.com', 'A'), dns_server, timeout=5)
                            protocol = 'udp'
                        except socket.error:
                            we_need_server = True
                else:
                    protocol = self.options['dns-protocol'].value
            except dns.exception.Timeout:
                self.logger.log("Check server {0}. Don`t work.".format(dns_server))
                we_need_server = True
        return dns_server, protocol
