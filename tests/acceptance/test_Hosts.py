import subprocess
import os
import time
import re

runPath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../../')


class Test_Hosts(object):
    dict_path = '/tmp/wstest.dict'
    headers_file_path = '/tmp/wstest.headers_file'
    conf_file_path = "/tmp/wstest.conf_file"

    def get_results_count(self, output):
        return len(re.findall('^(\t.+)', output, re.M))

    def test_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\nfoobar\nadmin\ndev")
        fh.close()

        output = subprocess.check_output([
            './ws.py',
            'HostsDict',
            '--template',
            '@.wildcard-web.polygon.web-scout.online',
            '--ip',
            '82.146.56.21',
            '--false-re',
            'Apache2 Ubuntu Default Page',
            '--dict',
            self.dict_path,
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("admin.wildcard-web.polygon.web-scout.online") == 1

    def test_mask(self):
        output = subprocess.check_output([
            './ws.py',
            'HostsMask',
            '--template',
            'admi@.wildcard-web.polygon.web-scout.online',
            '--ip',
            '82.146.56.21',
            '--false-re',
            'Apache2 Ubuntu Default Page',
            '--mask',
            '?l,1,1',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("admin.wildcard-web.polygon.web-scout.online") == 1

    def test_combine(self):
        fh = open(self.dict_path, 'w')
        fh.write("\nadmi\nde")
        fh.close()

        output = subprocess.check_output([
            './ws.py',
            'HostsCombine',
            '--combine-template',
            '%d%%m%',
            '--template',
            'admi@.wildcard-web.polygon.web-scout.online',
            '--ip',
            '82.146.56.21',
            '--false-re',
            'Apache2 Ubuntu Default Page',
            '--mask',
            '?l,1,1',
            '--dict',
            self.dict_path,
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("admin.wildcard-web.polygon.web-scout.online") == 1

    def test_false_size(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\nfoobar\nadmin\ndev")
        fh.close()

        output = subprocess.check_output([
            './ws.py',
            'HostsDict',
            '--template',
            '@.wildcard-web.polygon.web-scout.online',
            '--ip',
            '82.146.56.21',
            '--false-size',
            '10918',
            '--dict',
            self.dict_path,
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("admin.wildcard-web.polygon.web-scout.online") == 1

    def test_msymbol(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\nfoobar\nadmin\ndev")
        fh.close()

        output = subprocess.check_output([
            './ws.py',
            'HostsDict',
            '--template',
            '%.wildcard-web.polygon.web-scout.online',
            '--msymbol',
            '%',
            '--ip',
            '82.146.56.21',
            '--false-re',
            'Apache2 Ubuntu Default Page',
            '--dict',
            self.dict_path,
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("admin.wildcard-web.polygon.web-scout.online") == 1

    def test_ignore_words_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\nfoobar\nadmin\ndev")
        fh.close()

        output = subprocess.check_output([
            './ws.py',
            'HostsDict',
            '--template',
            '@.wildcard-web.polygon.web-scout.online',
            '--ip',
            '82.146.56.21',
            '--false-re',
            'Apache2 Ubuntu Default Page',
            '--dict',
            self.dict_path,
            '--ignore-words-re',
            'admin'
        ])
        print(output)
        assert self.get_results_count(output) == 0
        assert output.count("admin.wildcard-web.polygon.web-scout.online") == 0

    def test_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\nfoobar\nadmin\ndev")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './ws.py',
            'HostsDict',
            '--template',
            '@.wildcard-web.polygon.web-scout.online',
            '--ip',
            '82.146.56.21',
            '--false-re',
            'Apache2 Ubuntu Default Page',
            '--dict',
            self.dict_path,
            '--threads',
            '1',
            '--delay',
            '2',
        ])
        print(output)
        etime = int(time.time())
        assert etime - stime > 8
