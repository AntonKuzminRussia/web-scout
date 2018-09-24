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


class HostsBruteCombineModuleParams:
    options = {
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
        "ip": WSOption(
            "ip",
            "Traget IP",
            "",
            True,
            ['--ip']
        ),
        "msymbol": WSOption(
            "msymbol",
            "Symbol of mask position in target URL (default {0})"
                .format(Registry().get('config')['main']['standart_msymbol']),
            Registry().get('config')['main']['standart_msymbol'],
            False,
            ['--msymbol']
        ),
        "protocol": WSOption(
            "protocol",
            "Protocol http or https (default - http)",
            "http",
            False,
            ['--protocol']
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
        "false-phrase": WSOption(
            "false-phrase",
            "Phrase for detect 'Host not found' response",
            "",
            True,
            ['--false-phrase']
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
        "template": WSOption(
            "template",
            "Template for brute",
            "",
            True,
            ['--template']
        ),
        "combine-template": WSOption(
            "combine-template",
            "Combine template ",
            "",
            True,
            ['--combine-template']
        ),
        "headers-file": WSOption(
            "headers-file",
            "File with list of HTTP headers",
            "",
            False,
            ['--headers-file']
        ),
        "ignore-words-re": WSOption(
            "ignore-words-re",
            "Regex for ignore some words from dict or mask",
            "",
            False,
            ['--ignore-words-re']
        ),
    }