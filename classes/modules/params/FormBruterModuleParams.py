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


class FormBruterModuleParams:
    options = {
        "xml-report": WSOption(
            "xml-report",
            "XML report file",
            "",
            False,
            ['--xml-report']
        ),
        "test": WSOption(
            "test",
            "Test run with results dump",
            "",
            False,
            ['--test']
        ),
        "threads": WSOption(
            "threads",
            "Threads count, default 10",
            int(Registry().get('config')['main']['default_threads']),
            False,
            ['--threads']
        ),
        "url": WSOption(
            "url",
            "Traget url for brute",
            "",
            True,
            ['--url']
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
        "retest-codes": WSOption(
            "retest-codes",
            "Custom codes for re-test object after 5 sec",
            "",
            False,
            ['--retest-codes']
        ),
        "true-phrase": WSOption(
            "true-phrase",
            "Phrase for detect true answer (auth is good)",
            "",
            False,
            ['--true-phrase']
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
        "reload-form-page": WSOption(
            "reload-form-page",
            "Reload page with form before every auth request",
            "1",
            False,
            ['--reload-form-page']
        ),
        "browser-recreate-phrase": WSOption(
            "browser-recreate-phrase",
            "Phrase for recreate browser with new proxy",
            "",
            False,
            ['--browser-recreate-phrase']
        ),
        "proxies": WSOption(
            "proxies",
            "File with list of proxies",
            "",
            False,
            ['--proxies']
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
        "dict": WSOption(
            "dict",
            "Dictionary for work",
            "",
            True,
            ['--dict']
        ),
        "login": WSOption(
            "login",
            "Target login",
            "",
            True,
            ['--login']
        ),
        "headers-file": WSOption(
            "headers-file",
            "File with list of HTTP headers",
            "",
            False,
            ['--headers-file']
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
    }