import subprocess
import os
import time
import re

runPath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../../')


class Test_Dns(object):
    dict_path = '/tmp/wstest.dict'
    headers_file_path = '/tmp/wstest.headers_file'
    conf_file_path = "/tmp/wstest.conf_file"

    def get_results_count(self, output):
        return len(re.findall('^(\t.+DNS:.+)', output, re.M))

    def test_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\nfoobar\ncc\nhh\nii\ndev")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DnsDict',
            '--template',
            '@.standart-zone.polygon.web-scout.online',
            '--dict',
            self.dict_path,
        ])
        print(output)
        assert self.get_results_count(output) == 2
        assert output.count("test.standart-zone.polygon.web-scout.online") == 2
        assert output.count("dev.standart-zone.polygon.web-scout.online") == 2

    def test_msymbol(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\nfoobar\ncc\nhh\nii\ndev")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DnsDict',
            '--template',
            '%.standart-zone.polygon.web-scout.online',
            '--dict',
            self.dict_path,
            '--msymbol',
            '%',
        ])
        print(output)
        assert self.get_results_count(output) == 2
        assert output.count("test.standart-zone.polygon.web-scout.online") == 2
        assert output.count("dev.standart-zone.polygon.web-scout.online") == 2

    def test_dict_ignore_words_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\nfoobar\ncc\nhh\nii\ndev")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DnsDict',
            '--template',
            '@.standart-zone.polygon.web-scout.online',
            '--dict',
            self.dict_path,
            '--ignore-words-re',
            'test'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("test.standart-zone.polygon.web-scout.online") == 0
        assert output.count("dev.standart-zone.polygon.web-scout.online") == 2

    def test_mask(self):
        output = subprocess.check_output([
            './main.py',
            'DnsMask',
            '--template',
            'tes@.standart-zone.polygon.web-scout.online',
            '--mask',
            '?l,1,1',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("test.standart-zone.polygon.web-scout.online") == 2

    def test_ignore_ip(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\ndev\ncc\nhh\nii")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DnsDict',
            '--template',
            '@.wildcard-ip.polygon.web-scout.online',
            '--ignore-ip',
            '8.8.8.8',
            '--dict',
            self.dict_path,
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("dev.wildcard-ip.polygon.web-scout.online") == 2

    def test_http_not_found(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\ndev\ncc\nadmin\nii")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DnsDict',
            '--template',
            '@.wildcard-web.polygon.web-scout.online',
            '--http-not-found-re',
            'Apache2 Ubuntu Default Page',
            '--dict',
            self.dict_path,
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("admin.wildcard-web.polygon.web-scout.online") == 2

    def test_combine(self):
        fh = open(self.dict_path, 'w')
        fh.write("tes\nfoobar")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DnsCombine',
            '--template',
            '@.standart-zone.polygon.web-scout.online',
            '--combine-template',
            '%d%%m%',
            '--mask',
            '?l,1,1',
            '--dict',
            self.dict_path,
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("test.standart-zone.polygon.web-scout.online") == 2

    def test_dict_zone_cname(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\nadmin\nfoobar")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DnsDict',
            '--template',
            '@.standart-zone.polygon.web-scout.online',
            '--dict',
            self.dict_path,
            '--zone',
            'CNAME',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("admin.standart-zone.polygon.web-scout.online") == 2

    def test_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\nfoobar\ncc\nhh\nii\ndev")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'DnsDict',
            '--template',
            '@.standart-zone.polygon.web-scout.online',
            '--dict',
            self.dict_path,
            '--delay',
            '1',
            '--threads',
            '1',
        ])
        print(output)
        etime = int(time.time())

        assert etime - stime > 12