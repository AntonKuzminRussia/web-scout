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
from libs.common import is_binary_content_type, get_full_response_text
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

    dns_retest_exceptions = [
        "Connection refused",
        "Connection reset by peer",
        "[Errno 104]",
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
        self.http_retest_re = params.http_retest_re
        self.zone = params.zone

        self.check_name = ""

        self.http = copy.deepcopy(Registry().get('http'))
        self.http.every_request_new_session = True

    def is_valid_hostname(self, hostname):
        if not len(hostname.strip()):
            return False
        if self.ignore_words_re and self.ignore_words_re.findall(hostname):
            return False
        return True

    def is_dns_retest_need(self, ex_str):
        for retest_text in self.dns_retest_exceptions:
            if ex_str.count(retest_text):
                return True
        return False

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
                    if not self.is_valid_hostname(check_host):
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
                    if self.is_dns_retest_need(str(e)):
                        time.sleep(3)
                        need_retest = True
                        continue
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
        for answer in answers:
            self.positive_item(answer, self.current_response_text)
            self.test_log(answer, True)

    def additional_hostname_validation(self, name):
        """ If we found hostname, be better if we re-check it some times """
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

    def positive_item(self, ip, response_data):
        item_data = {'name': self.check_name, 'ip': ip, 'dns': self.dns_srv}
        self.result.append(item_data)
        self.logger.item(self.check_name, response_data, False, positive=True)
        self.xml_log(item_data)
        self.test_log(ip, True)

    def ignore_this_ip(self, ip):
        return len(self.ignore_ip) and ip == self.ignore_ip

    def validate_additional(self):
        if Registry().get('config')['dns']['additional_domains_check'] != '1':
            return True

        if self.additional_hostname_validation(self.check_name):
            return True

        self.logger.log("Domain {0} not pass additional validation, skip it".format(self.check_name))
        return False

    def parse_zone_a(self, response):
        """ Parsing A zone answer """
        if not self.validate_additional():
            return

        for ip in self.re['ip'].findall(response.group('data')):
            if self.ignore_this_ip(ip):
                self.test_log(ip, False)
                continue

            if self.http_nf_re is None:
                self.positive_item(ip, self.current_response_text)
                break

            http_result, http_response = self.http_test(ip)
            if http_result:
                self.positive_item(ip, self.current_response_text + "\n" + http_response)
                break

            self.test_log(ip, False)

    def http_proxy_error(self, ex_str):
        if Registry().get('proxies').count() > 0:
            for proxyError in self.proxyErrors:
                if ex_str.count(proxyError):
                    return True
        return False

    def http_test(self, ip):
        """ Make HTTP(S) test for found ip """
        for i in range(self.retest_limit):
            try:
                resp = self.http.get(
                    "{0}://{1}/".format(self.http_protocol, ip),
                    headers={'Host': self.check_name},
                    allow_redirects=False
                )

                text_for_search = get_full_response_text(resp)

                if self.http_retest_re and self.http_retest_re.findall(text_for_search):
                    if i == self.retest_limit - 1:
                        self.logger.log("Too many retest actions for {0}".format(self.check_name))
                    time.sleep(self.retest_delay)
                    continue

                if not self.http_nf_re.findall(text_for_search):
                    return True, text_for_search

                break
            except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                if self.http_proxy_error(str(e)):
                    self.http.change_proxy()
                    continue
                return True, 'ERROR: ' + str(e),

        return False, ""

    def is_response_content_binary(self, resp):
        """ Is it binary http content? """
        return resp is not None \
            and 'content-type' in resp.headers \
            and is_binary_content_type(resp.headers['content-type'])