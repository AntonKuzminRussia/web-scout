# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of Pre module
"""

import re
import socket

import requests
import dns.message
import dns.query

from libs.common import file_to_list
from classes.kernel.WSModule import WSModule
from classes.Registry import Registry
from classes.modules.params.PreModuleParams import PreModuleParams


class Pre(WSModule):
    """ Class of Pre module """
    model = None
    nf_codes = [404]
    log_path = '/dev/null'
    options = {}
    time_count = True
    root_url = ''
    dns_proto = None
    logger_enable = True
    logger_name = 'pre'
    logger_have_items = False
    options = PreModuleParams().get_options()

    def _get_default_dns_proto(self):
        """ Check default dns protocol """
        if self.dns_proto is None:
            try:
                dns.query.tcp(dns.message.make_query('test.com', 'A'), self.options['dns'].value, timeout=2)
                self.dns_proto = 'tcp'
            except socket.error:
                try:
                    dns.query.udp(dns.message.make_query('test.com', 'A'), self.dns_proto, timeout=2)
                    self.dns_proto = 'udp'
                except socket.error:
                    raise Exception(
                        'Can`t detect DNS-server protocol. Check dns server addr ({0}).'
                        .format(self.options['dns'].value)
                    )
            self.logger.log('DNS protolol detected automaticaly: ' + self.dns_proto)
        return self.dns_proto

    def get_ns_zone_txt_response(self, domain, zone):
        req_func = getattr(dns.query, self._get_default_dns_proto())
        query = dns.message.make_query(domain, zone)
        result = req_func(query, self.options['dns'].value, timeout=2)
        return result.to_text()

    def get_interest_ns(self):
        result = {}
        domain = self.options['host'].value
        zones = ['MX', 'SPF', 'NS', 'PTR', 'SOA']

        for zone in zones:
            result[domain + " " + zone] = self.get_ns_zone_txt_response(domain, zone)
            if zone == 'PTR':
                ip = socket.gethostbyname(domain)
                result[ip + " " + zone] = self.get_ns_zone_txt_response(ip, zone)

        to_return = ""
        for zone_row in result.keys():
            to_return += "\t" + zone_row + ":\n"
            lines = result[zone_row].split("\n")
            for line in lines:
                line = line.strip()
                if not len(line) or re.search('^opcode|^flags |^id |^rcode |^;| IN [A-Z]+$', line):
                    continue
                to_return += "\t\t" + line + "\n"
        return to_return

    def check_ns_always_true(self):
        """ Check always good answer by dns zone """
        domain = self.options['host'].value
        check_list = ['wekjmwei82hjnb2ou82g2', 'wklmehf7e03he3fgb', 'dmvbfyf7393jhfvv']

        req_func = getattr(dns.query, self._get_default_dns_proto())

        for check_name in check_list:
            ipRe = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
            nsRespRe = re.compile(r";ANSWER\s(?P<data>(.|\s)*)\s;AUTHORITY", re.M)

            query = dns.message.make_query(check_name + '.' + domain, 'A')
            result = req_func(query, self.options['dns'].value, timeout=2)
            response = nsRespRe.search(result.to_text())
            if not response or not ipRe.findall(response.group('data')):
                return False

            return True

    def _parse_sitemap_links(self, content, domain):
        """ Parsing sitemap links """
        links = re.findall("<loc>http(?:s|)://" + domain.replace(".", "\\.") + "(.*?)</loc>", content)
        return map(str.strip, map(str, links))

    def check_sitemap(self, robots_txt):
        """ Check is sitemap exists """
        links = []
        sitemap_links = []

        r = requests.get(self.root_url + 'sitemap.xml', allow_redirects=True, verify=False)
        if not self._response_404(r):
            links.append('/sitemap.xml')
            links.extend(self._parse_sitemap_links(r.content, self.options['host'].value))
            sitemap_links.append(self.root_url + 'sitemap.xml')

        if robots_txt:
            r = requests.get(self.root_url + 'robots.txt', allow_redirects=False, verify=False)
            sitemap = re.findall("Sitemap:((?:.*?).xml)(?: |\n|$)", r.content, re.M)
            if len(sitemap):
                sitemap = str(sitemap[0]).strip()
                links.append(sitemap)
                sitemap_links.append(self.root_url + (sitemap if sitemap[0:1] != '/' else sitemap[1:]))

                #while sitemap_url.count("//"):
                #    sitemap_url.replace("//", "/")

                r = requests.get(self.root_url + sitemap, allow_redirects=True, verify=False)
                if not self._response_404(r):
                    links.extend(self._parse_sitemap_links(r.content, self.options['host'].value))

        return {
            'links': map(str.strip, map(str, sitemap_links)),
        }

    def _response_404(self, resp):
        """ Check answers on 404 request """
        nf_phrase = self.options['not-found-re'].value if len(self.options['not-found-re'].value) else False

        return resp.status_code in self.nf_codes or (nf_phrase and resp.content.lower().count(nf_phrase.lower()))

    def check_backups(self):
        """ Simple check backups """
        Http = Registry().get('http')
        check = []
        result = []

        dirs = file_to_list(Registry().get('wr_path') + "/bases/pre-backups-dirs.txt")
        dirs.append(self.options['host'].value)
        files = file_to_list(Registry().get('wr_path') + "/bases/pre-backups-files.txt")
        dirs_exts = file_to_list(Registry().get('wr_path') + "/bases/bf-dirs.txt")
        files_exts = file_to_list(Registry().get('wr_path') + "/bases/bf-files.txt")

        for _dir in dirs:
            for dir_ext in dirs_exts:
                check.append(dir_ext.replace('|name|', _dir))
        for _file in files:
            for file_ext in files_exts:
                check.append(file_ext.replace('|name|', _file))

        for url in check:
            r = Http.get(self.root_url + url)
            if not self._response_404(r):
                result.append({'url': self.root_url + url, 'code': r.status_code})

        return result

    def do_work(self):
        """ Scan action of module """
        self.enable_logger()
        self.validate_main()
        self.pre_start_inf()

        if self.options['proxies'].value:
            Registry().get('proxies').load(self.options['proxies'].value)

        self.root_url = "{0}://{1}/".format(self.options['protocol'].value, self.options['host'].value)

        if len(self.options['not-found-codes'].value):
            for code in self.options['not-found-codes'].value.split(","):
                self.nf_codes.append(int(code.strip()))

        result = {}
        result['ns_always_true'] = str(int(self.check_ns_always_true()))
        result['nf'] = self.check_404()
        result['backups'] = self.check_backups()
        result['ns'] = self.check_ns() if not result['ns_always_true'] else []
        result['interest_ns'] = self.get_interest_ns()
        result['powered_by'] = self.check_powered_by()
        result['robots_txt'] = self.check_robots_txt()
        result['sitemap'] = self.check_sitemap(result['robots_txt'])
        result['dafs_dirs'] = self.check_dafs('dirs') if result['nf']['dirs'] else []
        result['dafs_files'] = self.check_dafs('files') if result['nf']['files'] else []
        result['encodings'] = self._get_encodings()
        result['headers'] = self.check_headers()

        if len(result['ns']):
            self.logger.log("Found {0} hosts: ".format(len(result['ns'])))
            for ns_name in result['ns']:
                self.logger.log("\t{0} ({1})".format(ns_name['name'], ns_name['ip']))

        if len(result['interest_ns']):
            self.logger.log("Interest DNS records: ")
            self.logger.log(result['interest_ns'])

        self.logger.log("Encodings:")
        self.logger.log("\tHTTP: " + result['encodings']['http'])
        self.logger.log("\tHTML: " + result['encodings']['html'])

        if len(result['headers']):
            self.logger.log("Interest headers:\n")
            for header in result['headers']:
                self.logger.log("\t{0}: {1}".format(header['name'], header['value']))

        if result['robots_txt']:
            self.logger.log("Check robots.txt")
            self.logger.log("\t" + self.root_url + "robots.txt")
            urls = self._get_urls_from_robots_txt(
                requests.get(
                    self.root_url + "robots.txt",
                    allow_redirects=False,
                    verify=False
                ).content
            )
            self.logger.log("\tExtracted {0} urls from robots.txt".format(len(urls)))

        if len(result['sitemap']['links']):
            self.logger.log("Found {0} sitemap(s):".format(len(result['sitemap']['links'])))
            for link in result['sitemap']['links']:
                self.logger.log("\t" + link)

        if len(result['backups']):
            self.logger.log("Found {0} backups".format(len(result['backups'])))
            for backup_url in result['backups']:
                self.logger.log("\t{0} {1}".format(backup_url['code'], backup_url['url']))

        self.logger.log("Not Found test:")
        self.logger.log("\tDirs: " + str(result['nf']['dirs']))
        self.logger.log("\tFiles: " + str(result['nf']['files']))

        if len(result['powered_by']):
            self.logger.log("Found 'powered by' signature: {0}".format(result['powered_by']))

        if len(result['ns_always_true']) and int(result['ns_always_true']):
            self.logger.log("DNS server always answer positive on every subdomain of target. Be careful")

        if len(result['dafs_dirs']):
            self.logger.log("DAFS dirs")
            self.logger.log("\t{0} dirs found".format(len(result['dafs_dirs'])))
            for url in result['dafs_dirs']:
                self.logger.log("\t\t{0} {1}".format(url['url'], url['code']))
            self.logger.log(
                "\tFound {0} URLs".format(len(result['dafs_dirs']))
            )

        if len(result['dafs_files']):
            self.logger.log("DAFS files")
            self.logger.log("\t{0} files found".format(len(result['dafs_files'])))
            for url in result['dafs_files']:
                self.logger.log("\t\t{0} {1}".format(url['url'], url['code']))
            self.logger.log(
                "\tFound {0} URLs".format(len(result['dafs_files']))
            )

        self.done = True

    def _get_encodings(self):
        """ Get encoding from headers and pages """
        url = self.root_url
        encs = {}

        r = requests.get(url, allow_redirects=True, verify=False)

        resp = r.content.lower()
        enc = re.findall('<meta charset=(?:\'|"|)([^"\'>]*)(?:\'|"|)', resp, re.I)
        if enc and len(enc):
            encs['html'] = enc[0]
        else:
            enc = re.findall('http-equiv=(?:[^>]*)charset=([^"\'>]*)', resp, re.I)
            if enc and len(enc):
                encs['html'] = enc[0]
            else:
                encs['html'] = ""

        for header in r.headers:
            if header.lower() == 'content-type':
                enc = re.findall("charset=(.*)", r.headers[header].lower())
                if enc and len(enc):
                    encs['http'] = enc[0]
                else:
                    encs['http'] = ""
                break

        return encs

    def _get_urls_from_robots_txt(self, content):
        """ Extract urls from robots.txt """
        content = content.split("\n")
        urls = []
        for line in content:
            if line.count("$") or line.count("*"):
                continue

            if line[:6].lower() == 'allow:' or line[:9].lower() == 'disallow:':
                line = line.strip()
                cut = 6 if line[:6].lower() == 'allow:' else 9
                urls.append(line[cut:].strip())
        return urls

    def check_ns(self):
        """ Simple brute subdomains """
        domain = self.options['host'].value
        result_names = []

        ipRe = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
        nsRespRe = re.compile(r";ANSWER\s(?P<data>(.|\s)*)\s;AUTHORITY", re.M)

        req_func = getattr(dns.query, self._get_default_dns_proto())

        ns_names = file_to_list(Registry().get('wr_path') + "/bases/pre-domain-names.txt")
        for name in ns_names:
            try:
                query = dns.message.make_query(name + '.' + domain, 'A')
                result = req_func(query, self.options['dns'].value, timeout=2)

                response = nsRespRe.search(result.to_text())
                if response is not None and ipRe.findall(response.group('data')):
                    for ip in ipRe.findall(response.group('data')):
                        result_names.append({'name': name + '.' + domain, 'ip': ip})
                        break
            except BaseException as e:
                self.logger.ex(e)

        return result_names

    def check_powered_by(self):
        """ Are page contains a 'Powered by' fragment? """
        r = requests.get(self.root_url, allow_redirects=False, verify=False)
        return re.findall("(powered by (?:.*)</)", r.content, re.I)

    def check_robots_txt(self):
        """ Is robots.txt exists """
        return int(requests.get(self.root_url + "robots.txt", allow_redirects=False, verify=False).status_code != 404)

    def check_404(self):
        """ Check 404 answer for files and dirs """
        result = {
            'files': requests.get(
                self.root_url + "ergergergergegerger.php", allow_redirects=False, verify=False
            ).status_code,
            'dirs':  requests.get(
                self.root_url + "ergergergergeg/", allow_redirects=False, verify=False
            ).status_code
        }
        self.nf_codes.append(result['files'])
        self.nf_codes.append(result['dirs'])
        self.nf_codes = list(set(self.nf_codes))
        return result

    def check_headers(self):
        """ Parse headers from answer """
        result = []
        r = requests.get(self.root_url, allow_redirects=False, verify=False)
        for header in r.headers:
            if header[:2].lower() == "x-" or header.lower() == 'server':
                result.append({'name': header, 'value': r.headers[header]})
        return result

    def check_dafs(self, _type):
        """ Simple dafs search """
        Http = Registry().get('http')
        result = []
        _dict = open(Registry().get('wr_path') + '/bases/pre-dafs-{0}.txt'.format(_type), 'r').read().split("\n")
        for obj in _dict:
            r = Http.get(self.root_url + obj)
            if r is not None and not self._response_404(r):
                result.append({'url': "/" + obj, 'code': r.status_code, 'time': 0})

        return result
