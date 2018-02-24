# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Thread class for DnsBrute* modules
"""
import time
import Queue
import re
import threading

import requests
import dns.query
import dns.message

from classes.Registry import Registry
from libs.common import is_binary_content_type
from classes.kernel.WSException import WSException

class DnsBruteThread(threading.Thread):
    """ Thread class for DnsBrute* modules """
    done = False

    def __init__(self, queue, domains, template, proto, msymbol, ignore_ip, dns_srv, delay, http_nf_re, http_protocol,
                 http_retest_phrase, ignore_words_re, zone, result, counter):
        threading.Thread.__init__(self)
        self.queue = queue
        self.domains = domains
        self.proto = proto
        self.dns_srv = dns_srv
        self.counter = counter
        self.msymbol = msymbol
        self.template = template
        self.result = result
        self.delay = int(delay)
        self.done = False
        self.logger = Registry().get('logger')
        self.ignore_ip = ignore_ip
        self.http_nf_re = re.compile(http_nf_re) if len(http_nf_re) else None
        self.ignore_words_re = False if not len(ignore_words_re) else re.compile(ignore_words_re)
        self.http_protocol = http_protocol
        self.http_retest_phrase = http_retest_phrase

        self.retest_delay = int(Registry().get('config')['dns']['retest_delay'])
        self.retest_limit = int(Registry().get('config')['dns']['retest_limit'])

        self.zone = zone.upper()

        self.re = {
            'ip': re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"),
            'ns_resp': re.compile(r";ANSWER\s(?P<data>(.|\s)*)\s;AUTHORITY", re.M),
            'cname': re.compile("IN CNAME (.*?)\.$", re.MULTILINE)
        }

        self.check_name = ""

    def run(self):
        """ Run thread """
        req_func = getattr(dns.query, self.proto.lower())

        need_retest = False

        while True:
            if self.delay:
                time.sleep(self.delay)
            try:
                if not need_retest:
                    host = self.queue.get()
                    if not len(host.strip()) or (self.ignore_words_re and self.ignore_words_re.findall(host)):
                        continue

                    self.counter.up()

                for domain in self.domains:
                    self.check_name = self.template.replace(self.msymbol, host.decode('utf8', 'ignore')) + '.' + domain
                    query = dns.message.make_query(self.check_name, self.zone)

                    try:
                        result = req_func(query, self.dns_srv, timeout=5)
                    except EOFError:
                        time.sleep(3)
                        need_retest = True
                        break
                    except BaseException as e:
                        if str(e).count("Connection refused") or\
                                str(e).count("Connection reset by peer") or\
                                str(e).count("[Errno 104]"):
                            time.sleep(3)
                            need_retest = True
                            break
                        else:
                            raise e

                    response = self.re['ns_resp'].search(result.to_text())
                    if response is not None:
                        if self.zone == 'A':
                            self.parse_zone_a(response)
                        elif self.zone == 'CNAME':
                            self.parse_zone_cname(result)
                        else:
                            raise WSException("Wrong dns zone '{0}'".format(self.zone))

                if len(self.result) >= int(Registry().get('config')['main']['positive_limit_stop']):
                    Registry().set('positive_limit_stop', True)

                need_retest = False
            except Queue.Empty:
                self.done = True
                break
            except dns.exception.Timeout:
                need_retest = True
                time.sleep(1)
            except BaseException as e:
                self.logger.ex(e)
                self.logger.log("Exception with {0}".format(self.dns_srv))
                time.sleep(5)

    def parse_zone_cname(self, dns_result):
        """ Parsing CNAME zone answer """
        answers = self.re['cname'].findall(dns_result.to_text())
        for answer in answers:
            self.result.append({'name': self.check_name, 'ip': answer, 'dns': self.dns_srv})

    def parse_zone_a(self, response):
        """ Parsing A zone answer """
        for ip in self.re['ip'].findall(response.group('data')):
            if not len(self.ignore_ip) or ip != self.ignore_ip:
                if self.http_nf_re is not None:
                    self.http_test(ip)
                else:
                    self.result.append({'name': self.check_name, 'ip': ip, 'dns': self.dns_srv})
            break

    def http_test(self, ip):
        """ Make HTTP(S) test for found ip """
        for i in range(self.retest_limit):
            try:
                resp = Registry().get('http').get(
                    "{0}://{1}/".format(self.http_protocol, ip),
                    headers={'Host': self.check_name},
                    allow_redirects=False)

                text_for_search = ""
                for header in resp.headers:
                    text_for_search += "{0}: {1}\r\n".format(header, resp.headers[header])
                text_for_search += "\r\n"
                text_for_search += resp.text

                if len(self.http_retest_phrase) and \
                        text_for_search.replace('\r', '').replace('\n', '') \
                                .count(self.http_retest_phrase):
                    if i == self.retest_limit - 1:
                        self.logger.log(
                            "Too many retest actions for {0}".format(self.check_name))
                    time.sleep(self.retest_delay)
                    continue

                if not self.http_nf_re.findall(
                        text_for_search.replace('\r', '').replace('\n', '')):
                    self.result.append({'name': self.check_name, 'ip': ip, 'dns': self.dns_srv})
                    self.logger.item(
                        self.check_name,
                        text_for_search,
                        self.is_response_content_binary(resp),
                        positive=True
                    )
                break
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.ChunkedEncodingError) as e:
                self.result.append({'name': self.check_name, 'ip': ip, 'dns': self.dns_srv})
                self.logger.item(
                    self.check_name,
                    'ERROR: ' + str(e),
                    False,
                    positive=True
                )
                break

    def is_response_content_binary(self, resp):
        """ Is it bynary http content? """
        return resp is not None \
            and 'content-type' in resp.headers \
            and is_binary_content_type(resp.headers['content-type'])