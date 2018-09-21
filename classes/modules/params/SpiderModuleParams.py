# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of module for DAFS by Dict+Mask
"""

from classes.kernel.WSOption import WSOption
from classes.Registry import Registry


class SpiderModuleParams:
    options = {
        "threads": WSOption(
            "threads",
            "Threads count, default 10",
            int(Registry().get('config')['main']['default_threads']),
            False,
            ['--threads']
        ),
        "ignore": WSOption(
            "ignore",
            "ignore regexp",
            "",
            False,
            ['--ignore-re']
        ),
        "only_one": WSOption(
            "only_one",
            "only one",
            "",
            False,
            ['--only-one']
        ),
        "host": WSOption(
            "host",
            "Traget host for scan",
            "",
            True,
            ['--host']
        ),
        "not-found-re": WSOption(
            "not-found-re",
            "Regex for detect 'Not found' response (404)",
            "",
            False,
            ['--not-found-re']
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
        "proxies": WSOption(
            "proxies",
            "File with list of proxies",
            "",
            False,
            ['--proxies']
        ),
        "headers-file": WSOption(
            "headers-file",
            "File with list of HTTP headers",
            "",
            False,
            ['--headers-file']
        ),
        "protocol": WSOption(
            "protocol",
            "Protocol http or https (default - http)",
            "http",
            False,
            ['--protocol']
        ),
        "urls-file": WSOption(
            "urls-file",
            "File with list of URLs (if not, Spider started from /)",
            "",
            False,
            ['--urls-file']
        ),
    }