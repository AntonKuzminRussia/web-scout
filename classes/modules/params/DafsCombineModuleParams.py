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


class DafsCombineModuleParams:
    options = {
        "test": WSOption(
            "test",
            "Test run with results dump",
            "",
            False,
            ['--test']
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
            "Template of URLs for scan",
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
            "Requests method (default - HEAD)",
            "HEAD",
            False,
            ['--method']
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
        "not-found-re": WSOption(
            "not-found-re",
            "Regex for detect 'Not found' response (404)",
            "",
            False,
            ['--not-found-re']
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
        "headers-file": WSOption(
            "headers-file",
            "File with list of HTTP headers",
            "",
            False,
            ['--headers-file']
        ),
    }

