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

import dns.query
import dns.message

from classes.Registry import Registry

class DnsBruteThread(threading.Thread):
    """ Thread class for DnsBrute* modules """
    done = False

    def __init__(self, queue, domains, template, proto, msymbol, ignore_ip, dns_srv, delay, http_nf_re, http_protocol, http_retest_phrase, ignore_words_re, result, counter):
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

    def run(self):
        """ Run thread """
        ip_re = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
        ns_resp_re = re.compile(r";ANSWER\s(?P<data>(.|\s)*)\s;AUTHORITY", re.M)

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
                    check_name = self.template.replace(self.msymbol, host.decode('utf8', 'ignore')) + '.' + domain
                    query = dns.message.make_query(check_name, 'A')

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

                    response = ns_resp_re.search(result.to_text())
                    if response is not None:
                        for ip in ip_re.findall(response.group('data')):
                            if not len(self.ignore_ip) or ip != self.ignore_ip:
                                if self.http_nf_re is not None:
                                    for i in range(self.retest_limit):
                                        resp = Registry().get('http').get(
                                            "{0}://{1}/".format(self.http_protocol, ip),
                                            headers={'Host': check_name},
                                            allow_redirects=False)

                                        if len(self.http_retest_phrase) and resp.text.count(self.http_retest_phrase):
                                            if i == 4:
                                                self.logger.log("Too many retest actions for {0}".format(check_name))
                                            time.sleep(self.retest_delay)
                                            continue

                                        if not self.http_nf_re.findall(resp.text.replace('\r', '').replace('\n', '')):
                                            self.result.append({'name': check_name, 'ip': ip, 'dns': self.dns_srv})

                                        break
                                else:
                                    self.result.append({'name': check_name, 'ip': ip, 'dns': self.dns_srv})
                            break

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

