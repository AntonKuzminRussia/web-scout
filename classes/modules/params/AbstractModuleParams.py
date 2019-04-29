# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Abstract module params class, contains all possible params description
"""

from classes.kernel.WSOption import WSOption
from classes.kernel.WSException import WSException
from classes.Registry import Registry


class AbstractModuleParams:
    options = {}

    all_options = {
        "test": WSOption(
            "test",
            "Test run with results dump",
            "",
            False,
            ['--test']
        ),
        "follow-redirects": WSOption(
            "follow-redirects",
            "Follow redirects from server response",
            "0",
            False,
            ['--follow-redirects']
        ),
        "xml-report": WSOption(
            "xml-report",
            "XML report file",
            "",
            False,
            ['--xml-report']
        ),
        "threads": WSOption(
            "threads",
            "Threads count, default 10",
            int(Registry().get('config')['main']['default_threads']),
            False,
            ['--threads']
        ),
        "template": WSOption(
            "template",
            "Template for scan ({0} as mark symbol)".format(Registry().get('config')['main']['standart_msymbol']),
            "",
            True,
            ['--template']
        ),
        "msymbol": WSOption(
            "msymbol",
            "Symbol of mask position in target URL (default {0})"
                .format(Registry().get('config')['main']['standart_msymbol']),
            Registry().get('config')['main']['standart_msymbol'],
            False,
            ['--msymbol']
        ),
        "method": WSOption(
            "method",
            "Requests method (default - GET)",
            "GET",
            False,
            ['--method']
        ),
        "params-method": WSOption(
            "params-method",
            "Requests method (default - GET)",
            "GET",
            False,
            ['--params-method']
        ),
        "dict": WSOption(
            "dict",
            "Dictionary for work",
            "",
            True,
            ['--dict']
        ),
        "mask": WSOption(
            "mask",
            "Mask for work",
            "",
            True,
            ['--mask']
        ),
        "combine-template": WSOption(
            "combine-template",
            "Template for combine",
            "",
            True,
            ['--combine-template']
        ),
        "found-re": WSOption(
            "found-re",
            "Regex for detect 'Found' response (200)",
            "",
            False,
            ['--found-re']
        ),
        "not-found-re": WSOption(
            "not-found-re",
            "Regex for detect 'Not found' response (404)",
            "",
            False,
            ['--not-found-re']
        ),
        "http-not-found-re": WSOption(
            "http-not-found-re",
            "Regex for detect 'Not found' response (404)",
            "",
            False,
            ['--http-not-found-re']
        ),
        "not-found-ex": WSOption(
            "not-found-ex",
            "Phrase for detect 'Not found' exception (perceived as 404)",
            "",
            False,
            ['--not-found-ex']
        ),
        "not-found-size": WSOption(
            "not-found-size",
            "Size in bytes for detect 'Not found' response (404)",
            "-1",
            False,
            ['--not-found-size']
        ),
        "not-found-codes": WSOption(
            "not-found-codes",
            "Custom codes for detect 'Not found' response (404)",
            "404",
            False,
            ['--not-found-codes']
        ),
        "ignore-words-re": WSOption(
            "ignore-words-re",
            "Regex for ignore some words from dict or mask",
            "",
            False,
            ['--ignore-words-re']
        ),
        "retest-codes": WSOption(
            "retest-codes",
            "Custom codes for re-test object after 5 sec",
            "",
            False,
            ['--retest-codes']
        ),
        "delay": WSOption(
            "delay",
            "Deley for every thread between requests (secs)",
            "0",
            False,
            ['--delay']
        ),
        "selenium": WSOption(
            "selenium",
            "Use Selenium for scanning",
            "",
            False,
            ['--selenium']
        ),
        "ddos-detect-phrase": WSOption(
            "ddos-detect-phrase",
            "Phrase for detect DDoS protection",
            "",
            False,
            ['--ddos-detect-phrase']
        ),
        "ddos-human-action": WSOption(
            "ddos-human-action",
            "Phrase for detect human action need",
            "",
            False,
            ['--ddos-human-action']
        ),
        "browser-recreate-re": WSOption(
            "browser-recreate-re",
            "Regex for recreate browser with new proxy",
            "",
            False,
            ['--browser-recreate-re']
        ),
        "parts": WSOption(
            "parts",
            "How many parts will be create from current source (dict/mask)",
            "0",
            False,
            ['--parts']
        ),
        "part": WSOption(
            "part",
            "Number of part for use from --parts",
            "0",
            False,
            ['--part']
        ),
        "proxies": WSOption(
            "proxies",
            "File with list of proxies",
            "",
            False,
            ['--proxies']
        ),
        "http-proxies": WSOption(
            "http-proxies",
            "File with list of proxies",
            "",
            False,
            ['--http-proxies']
        ),
        "headers-file": WSOption(
            "headers-file",
            "File with list of HTTP headers",
            "",
            False,
            ['--headers-file']
        ),
        "dns-protocol": WSOption(
            "dns-protocol",
            "TCP or UDP connection to DNS server (default - auto)",
            "auto",
            False,
            ['--dns-protocol']
        ),
        "http-protocol": WSOption(
            "http-protocol",
            "Protocol http or https (default - http)",
            "http",
            False,
            ['--http-protocol']
        ),
        "retest-phrase": WSOption(
            "retest-phrase",
            "Phrase in response for retest",
            "",
            False,
            ['--retest-phrase']
        ),
        "http-retest-phrase": WSOption(
            "http-retest-phrase",
            "Phrase in response for retest",
            "",
            False,
            ['--http-retest-phrase']
        ),
        "zone": WSOption(
            "zone",
            "Zone for check (A/CNAME)",
            "A",
            False,
            ['--zone']
        ),
        "ignore-ip": WSOption(
            "ignore-ip",
            "This IP-address must be ignore in positive detections",
            "",
            False,
            ['--ignore-ip']
        ),
        "only-one": WSOption(
            "only_one",
            "only one",
            "",
            False,
            ['--only-one']
        ),
        "url": WSOption(
            "url",
            "URL for work",
            "",
            True,
            ['--url']
        ),
        "urls-file": WSOption(
            "urls-file",
            "File with list of URLs",
            "",
            False,
            ['--urls-file']
        ),
        "ignore": WSOption(
            "ignore",
            "ignore regexp",
            "",
            False,
            ['--ignore']
        ),
        "host": WSOption(
            "host",
            "Traget host for scan",
            "",
            True,
            ['--host']
        ),
        "dns": WSOption(
            "dns",
            "DNS server for domains search",
            "8.8.8.8",
            False,
            ['--dns']
        ),
        "false-phrase": WSOption(
            "false-phrase",
            "Phrase for detect false answer (auth is wrong)",
            "",
            False,
            ['--false-phrase']
        ),
        "false-size": WSOption(
            "false-size",
            "Response size for detect false answer (auth is wrong)",
            None,
            False,
            ['--false-size']
        ),
        "true-phrase": WSOption(
            "true-phrase",
            "Phrase for detect true answer (auth is good)",
            "",
            False,
            ['--true-phrase']
        ),
        "reload-form-page": WSOption(
            "reload-form-page",
            "Reload page with form before every auth request",
            "1",
            False,
            ['--reload-form-page']
        ),
        "confstr": WSOption(
            "confstr",
            "String with bruter config",
            "",
            False,
            ['--confstr']
        ),
        "conffile": WSOption(
            "conffile",
            "File with bruter config (selenium)",
            "",
            False,
            ['--conffile']
        ),
        "first-stop": WSOption(
            "first-stop",
            "Stop after first password found",
            "0",
            False,
            ['--first-stop']
        ),
        "login": WSOption(
            "login",
            "Target login",
            "",
            True,
            ['--login']
        ),
        "pass-min-len": WSOption(
            "pass-min-len",
            "Password min length",
            "0",
            False,
            ['--pass-min-len']
        ),
        "pass-max-len": WSOption(
            "pass-max-len",
            "Password max length",
            "0",
            False,
            ['--pass-max-len']
        ),
        "ip": WSOption(
            "ip",
            "Traget IP",
            "",
            True,
            ['--ip']
        ),
        "max-params-length": WSOption(
            "max-params-length",
            "Maximum string of params length",
            "",
            True,
            ['--max-params-length']
        ),
        "value": WSOption(
            "value",
            "Value for params, default 1",
            "1",
            False,
            ['--value']
        ),
        "discovery-exts": WSOption(
            "discovery-exts",
            "Exts, comma separated, for generate discovery filenames",
            "php,html,js,log,txt",
            False,
            ['--discovery-exts']
        ),
    }

    def __init__(self):
        self.add_options(
            [
                'test',
                'xml-report',
                'threads',
                'parts',
                'part',
             ]
        )

    def get_options(self):
        return self.options

    def add_options(self, names_list):
        for name in names_list:
            self.add_option(name)

    def add_option(self, internal_name, external_name=None):
        if internal_name not in self.all_options:
            raise WSException("Option '{0}' not exists".format(internal_name))

        if external_name is not None:
            option = self.all_options[internal_name]
            option.flags = ['--' + external_name]
            self.options[external_name] = option
        else:
            self.options[internal_name] = self.all_options[internal_name]
