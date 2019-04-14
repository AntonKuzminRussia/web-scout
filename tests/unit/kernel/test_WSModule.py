# -*- coding: utf-8 -*-

import pytest

from classes.kernel.WSException import WSException
from classes.kernel.WSModule import WSModule
from classes.kernel.WSOption import WSOption
from classes.Registry import Registry

from libs.common import file_put_contents


class ModuleMock(WSModule):
    log_path = "/tmp"
    result = ['atest', 'btest', 'ctest', 'dtest']

    def work_end_error(self):
        pass


class LoggerMock():
    result = ""
    logs_dir = "/tmp"

    def log(self, s):
        self.result += s


class ProxiesMock():
    loaded_path = ""

    def load(self, path):
        self.loaded_path = path


class Test_WSModule(object):
    def validate_main_exceptions_provider_generator(self, test_name):
        if test_name == "dict1":
            option_dict = WSOption("dict", "Dictionary for work", "", True, ['--dict'])
            option_dict.value = "/tmp/1777.txt"
            return {"dict": option_dict}, "not exists or not readable"
        elif test_name == "selenium1":
            option_selenium = WSOption("selenium", "Use Selenium for scanning", "", False, ['--selenium'])
            option_selenium.value = 1

            option_nf = WSOption("not-found-re", "Regex for detect 'Not found' response (404)", "", False, ['--not-found-re'])
            option_nf.value = ""

            option_threads = WSOption("threads", "Threads count, default 10", 10, False, ['--threads'])
            option_threads.value = 1

            Registry().set('config', {'selenium': {'max_threads': 5}})

            return {"selenium": option_selenium, "not-found-re": option_nf, "threads": option_threads}, "module need a not found phrase"
        elif test_name == "selenium2":
            option_selenium = WSOption("selenium", "Use Selenium for scanning", "", False, ['--selenium'])
            option_selenium.value = 1

            option_threads = WSOption("threads", "Threads count, default 10", 10, False, ['--threads'])
            option_threads.value = 10

            option_nf = WSOption("not-found-re", "Regex for detect 'Not found' response (404)", "", False, ['--not-found-re'])
            option_nf.value = "x"

            Registry().set('config', {'selenium': {'max_threads': 1}})

            return {"selenium": option_selenium, "threads": option_threads, "not-found-re": option_nf}, "very many threads value"
        elif test_name == "http-protocol1":
            option_proto = WSOption("http-protocol", "Protocol http or https (default - http)", "http", False, ['--http-protocol'])
            option_proto.value = "x"
            return {"protocol": option_proto}, "Protocol param must be"
        elif test_name == "method1":
            option_method = WSOption("method", "Requests method (default - GET)", "GET", False, ['--method'])
            option_method.value = "x"
            return {"method": option_method}, "Method param must be only"
        elif test_name == "not-found-codes-1":
            option_nf = WSOption("not-found-codes", "Custom codes for detect 'Not found' response (404)", "404", False, ['--not-found-codes'])
            option_nf.value = "404,a"
            return {"not-found-codes": option_nf}, "Not-found code must be digital"
        elif test_name == "retest-codes-1":
            option_retest = WSOption("retest-codes", "Custom codes for re-test object after 5 sec", "", False, ['--retest-codes'])
            option_retest.value = "404,a"
            return {"retest-codes": option_retest}, "must be digital"
        elif test_name == "proxies1":
            option_proxies = WSOption("proxies", "File with list of proxies", "", False, ['--proxies'])
            option_proxies.value = "/tmp/1777.txt"
            return {"proxies": option_proxies}, "Proxy list not found"
        elif test_name == "proxies2":
            option_proxies = WSOption("http-proxies", "File with list of proxies", "", False, ['--http-proxies'])
            option_proxies.value = "/tmp/1777.txt"
            return {"http-proxies": option_proxies}, "Proxy list not found"
        elif test_name == "not-found-re-1":
            option_nf = WSOption("not-found-re", "Regex for detect 'Not found' response (404)", "", False, ['--not-found-re'])
            option_nf.value = "(("
            return {"not-found-re": option_nf}, "Invalid regex"
        elif test_name == "browser-recreate-re-1":
            option_re = WSOption("browser-recreate-re", "Regex for recreate browser with new proxy", "", False, ['--browser-recreate-re'])
            option_re.value = "(("
            return {"browser-recreate-re": option_re}, "Invalid regex"
        elif test_name == "delay1":
            option_delay = WSOption("delay", "Deley for every thread between requests (secs)", "0", False, ['--delay'])
            option_delay.value = "a"
            return {"delay": option_delay}, "param must be digital"
        elif test_name == "parts1":
            option_parts = WSOption("parts", "How many parts will be create from current source (dict/mask)", "0", False, ['--parts'])
            option_parts.value = "a"
            return {"parts": option_parts}, "param must be digital"
        elif test_name == "parts2":
            option_parts = WSOption("parts", "How many parts will be create from current source (dict/mask)", "0", False, ['--parts'])
            option_parts.value = "2"
            return {"parts": option_parts}, "you must specify"
        elif test_name == "parts3":
            option_parts = WSOption("parts", "How many parts will be create from current source (dict/mask)", "0", False, ['--parts'])
            option_parts.value = "2"
            option_part = WSOption("part", "Number of part for use from --parts", "0", False, ['--part'])
            option_part.value = "5"
            return {"parts": option_parts, "part": option_part}, "more than"
        elif test_name == "part1":
            option_part = WSOption("part", "Number of part for use from --parts", "0", False, ['--part'])
            option_part.value = "a"
            return {"part": option_part}, "param must be digital"
        elif test_name == "part2":
            option_part = WSOption("part", "Number of part for use from --parts", "0", False, ['--part'])
            option_part.value = "2"
            return {"part": option_part}, "you must specify"
        elif test_name == "template1":
            option_template = WSOption("template", "Template for scan", "", True, ['--template'])
            option_template.value = "123"
            option_msymbol = WSOption( "msymbol", "Symbol of mask position in target URL", '@', False, ['--msymbol'])
            option_msymbol.value = "@"
            return {"template": option_template, "msymbol": option_msymbol}, "not found in template"
        elif test_name == "zone1":
            option_zone = WSOption("zone", "DNS zone", "", True, ['--zone'])
            option_zone.value = "123"
            return {"zone": option_zone}, "Wrong DNS zone"
        elif test_name == "dns-protocol-1":
            option_proto = WSOption("dns-protocol", "DNS proto", "", True, ['--dns-protocol'])
            option_proto.value = "123"
            return {"dns-protocol": option_proto}, "DNS Protocol mast be"
        else:
            raise Exception("Unknown test case")

    """
        Cases:
            0 - dict not found
            1 - selenium enabled, not-found-re not setted
            2 - selenium enabled, threads limit very big 
            3 - http protocol wrong (not http or https)
            4 - worng HTTP method 
            5 - literal in not-found-codes param
            6 - literal in retest-codes param
            7 - proxy-list not found
            8 - not-found-re has wrong regex
            9 - browser-recreate-re has wrong regex
            10 - letter in delay param
            11 - letter in parts param
            12 - letter in part param
            13 - parts param set, but not part
            14 - part param more than parts param
            15 - part param set, but not parts param
            16 - mark symbol not found in template
            17 - wrong dns zone
            18 - wrong dns protocol
    """
    validate_main_exceptions_provider = [
        # ("dict1"),
        ("selenium1"),
        # ("selenium2"),
        # ("http-protocol1"),
        # ("method1"),
        # ("not-found-codes-1"),
        # ("retest-codes-1"),
        # ("proxies1"),
        # ("proxies2"),
        # ("not-found-re-1"),
        # ("browser-recreate-re-1"),
        # ("delay1"),
        # ("parts1"),
        # ("part1"),
        # ("parts2"),
        # ("parts3"),
        # ("part2"),
        # ("template1"),
        # ("zone1"),
        # ("dns-protocol-1"),
    ]

    @pytest.mark.parametrize("test_case", validate_main_exceptions_provider)
    def test_validate_main_exceptions(self, test_case):
        options, ex_str = self.validate_main_exceptions_provider_generator(test_case)
        with pytest.raises(WSException) as ex:
            module = ModuleMock(False)
            module.options = options
            module.validate_main()

        assert ex_str in str(ex)

    def test_init_log_path_check(self):
        with pytest.raises(WSException) as ex:
            WSModule(False)
        assert "must have log path" in str(ex)

    def test_output(self):
        logger = LoggerMock()
        module = ModuleMock(False)
        module.logger = logger

        Registry().set('proxy_many_died', True)
        Registry().set('positive_limit_stop', True)
        Registry().set('config', {"main": {"errors_limit": 10}})

        module.output()

        assert "Proxy many died" in logger.result
        assert "Many positive detections" in logger.result
        for s in module.result:
            assert s in logger.result

    load_proxies_provider = [
        ("proxies"),
        ("http-proxies"),
    ]
    @pytest.mark.parametrize("param_name", load_proxies_provider)
    def test_load_proxies(self, param_name):
        file_put_contents("/tmp/test.txt", "")

        proxies_mock = ProxiesMock()
        Registry().set('proxies', proxies_mock)
        module = ModuleMock(False)
        module.options = {param_name: WSOption("proxies", "File with list of proxies", "", False, ['--proxies'])}
        module.options[param_name].value = "/tmp/test.txt"
        module.load_proxies()

        assert "/tmp/test.txt" in proxies_mock.loaded_path

    def test_pre_start_inf(self):
        logger = LoggerMock()

        module = ModuleMock(False)
        module.logger = logger
        module.options = {
            "test1name": WSOption("test1name", "test1", "", False, ['--test1name']),
            "test2name": WSOption("test2name", "test2", "", False, ['--test2name']),
        }
        module.options["test1name"].value = "test1value"
        module.options["test2name"].value = "test2value"

        Registry().set('config', {"main": {"confirm": False}})

        module.pre_start_inf()

        assert "test1name" in logger.result
        assert "test2name" in logger.result
        assert "test1value" in logger.result
        assert "test2value" in logger.result
