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


class PreModuleParams:
    options = {
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
        "protocol": WSOption(
            "protocol",
            "Protocol http or https (default - http)",
            "http",
            False,
            ['--protocol']
        ),
        "not-found-phrase": WSOption(
            "not-found-phrase",
            "Phrase for detect 'Not found' response (404)",
            "",
            False,
            ['--not-found-phrase']
        ),
        "not-found-codes": WSOption(
            "not-found-codes",
            "Custom codes for detect 'Not found' response (404)",
            "",
            False,
            ['--not-found-codes']
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
    }