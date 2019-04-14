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
import copy

import requests
import dns.query
import dns.message
import dns.resolver

from classes.Registry import Registry
from libs.common import is_binary_content_type
from classes.kernel.WSException import WSException
from classes.threads.params.DnsBruterThreadParams import DnsBruterThreadParams
from classes.threads.AbstractThread import AbstractThread
from classes.ErrorsCounter import ErrorsCounter


class DnsBruterThread(AbstractThread):
    """ Thread class for DnsBrute* modules """
    current_response_text = None

    re = {
        'ip': re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"),
        'ns_resp': re.compile(r";ANSWER\s(?P<data>(.|\s)*)\s;AUTHORITY", re.M),
        'cname': re.compile("IN CNAME (.*?)\.$", re.MULTILINE)
    }

    proxyErrors = [
        "Cannot connect to proxy.",
        "Connection aborted",
        "Max retries exceeded with url",
    ]

    def __init__(self, queue, proto, dns_srv, result, counter, params):
        """

        :type params: DnsBruterThreadParams
        """
        AbstractThread.__init__(self)

        self.queue = queue
        self.proto = proto
        self.dns_srv = dns_srv
        self.counter = counter
        self.result = result

        self.msymbol = params.msymbol
        self.template = params.template
        self.delay = params.delay
        self.ignore_ip = params.ignore_ip
        self.http_nf_re = params.http_not_found_re
        self.ignore_words_re = params.ignore_words_re
        self.http_protocol = params.http_protocol
        self.http_retest_phrase = params.http_retest_phrase
        self.zone = params.zone

        self.check_name = ""

        self.http = copy.deepcopy(Registry().get('http'))
        self.http.every_request_new_session = True

    def run(self):
        """ Run thread """
        req_func = getattr(dns.query, self.proto.lower())

        need_retest = False

        while not self.done:
            self.last_action = int(time.time())

            if self.delay:
                time.sleep(self.delay)

            try:
                if not need_retest:
                    check_host = self.queue.get()
                    if not len(check_host.strip()) or (self.ignore_words_re and self.ignore_words_re.findall(check_host)):
                        continue

                self.check_name = self.template.replace(self.msymbol, check_host.decode('utf8', 'ignore'))
                query = dns.message.make_query(self.check_name, self.zone)

                try:
                    result = req_func(query, self.dns_srv, timeout=5)
                    ErrorsCounter.flush()
                except EOFError:
                    ErrorsCounter.up()
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

                self.current_response_text = str(result.to_text())
                response = self.re['ns_resp'].search(result.to_text())
                if response is not None:
                    if self.zone == 'A':
                        self.parse_zone_a(response)
                    elif self.zone == 'CNAME':
                        self.parse_zone_cname(result)
                    else:
                        raise WSException("Wrong dns zone '{0}'".format(self.zone))
                self.test_log('', False)

                if len(self.result) >= int(Registry().get('config')['main']['positive_limit_stop']):
                    Registry().set('positive_limit_stop', True)

                need_retest = False

                self.counter.up()
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

    def test_log(self, answer, positive_item):
        if self.is_test():
            self.test_put(
                self.check_name,
                {
                    'ip': str(answer),
                    'dns': self.dns_srv,
                    'positive': positive_item
                }
            )

    def parse_zone_cname(self, dns_result):
        """ Parsing CNAME zone answer """
        answers = self.re['cname'].findall(dns_result.to_text())
        positive_item = False
        for answer in answers:
            positive_item = True
            item_data = {'name': self.check_name, 'ip': answer, 'dns': self.dns_srv}
            self.result.append(item_data)
            self.logger.item(
                self.check_name,
                self.current_response_text,
                False,
                positive=True
            )
            self.xml_log(item_data)

        self.test_log(answers, positive_item)

    def additional_hostname_validation(self, name):
        dns_server = Registry().get('config')['dns']['additional_domains_check_dns']
        myResolver = dns.resolver.Resolver()
        myResolver.nameservers = [dns_server]

        result = False
        for i in range(0, 3):
            time.sleep(3)

            try:
                myResolver.query(name, 'A')
                result = True
            except dns.resolver.NXDOMAIN:
                result = False
                break

        return result

    def parse_zone_a(self, response):
        """ Parsing A zone answer """
        positive_item = False
        additional_validation_passed = False
        for ip in self.re['ip'].findall(response.group('data')):
            if Registry().get('config')['dns']['additional_domains_check'] == '1' and not additional_validation_passed:
                if self.additional_hostname_validation(self.check_name):
                    additional_validation_passed = True
                else:
                    self.logger.log("Domain {0} with ip {1} not pass additional validation, skip it".format(self.check_name, ip))
                    return

            if self.http_nf_re is None and (not len(self.ignore_ip) or ip != self.ignore_ip):
                positive_item = True
                item_data = {'name': self.check_name, 'ip': ip, 'dns': self.dns_srv}
                self.result.append(item_data)
                self.logger.item(
                    self.check_name,
                    self.current_response_text,
                    False,
                    positive=True
                )
                self.xml_log(item_data)
                self.test_log('', positive_item)
                continue

            if self.http_nf_re is not None:
                self.http_test(ip)

    def http_test(self, ip):
        """ Make HTTP(S) test for found ip """
        for i in range(self.retest_limit):
            try:
                resp = self.http.get(
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

                positive_item = False
                if not self.http_nf_re.findall(
                        text_for_search.replace('\r', '').replace('\n', '')):
                    positive_item = True
                    item_data = {'name': self.check_name, 'ip': ip, 'dns': self.dns_srv}
                    self.result.append(item_data)
                    self.xml_log(item_data)
                    self.logger.item(
                        self.check_name,
                        text_for_search,
                        self.is_response_content_binary(resp),
                        positive=positive_item
                    )
                self.test_log(ip, positive_item)
                break
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.ChunkedEncodingError) as e:

                if Registry().get('proxies').count() > 0:
                    is_proxy_error = False
                    for proxyError in self.proxyErrors:
                        if str(e).count(proxyError):
                            is_proxy_error = True
                    if is_proxy_error:
                        self.http.change_proxy()
                        continue

                item_data = {'name': self.check_name, 'ip': ip, 'dns': self.dns_srv}
                self.result.append(item_data)
                self.xml_log(item_data)
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