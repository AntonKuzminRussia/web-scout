import subprocess
import os
import time
import re

runPath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../../')


class Test_FuzzerUrls(object):
    dict_path = '/tmp/wstest.dict'
    headers_file_path = '/tmp/wstest.headers_file'
    conf_file_path = "/tmp/wstest.conf_file"

    def get_results_count(self, output):
        return len(re.findall('^(\t.+)', output, re.M))

    def test_run(self):
        fh = open(self.dict_path, 'w')
        fh.write("http://wsat.local/fuzzer-urls.php?a=1")
        fh.close()

        output = subprocess.check_output([
            './ws.py',
            'FuzzerUrls',
            '--urls-file',
            self.dict_path,
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("http://wsat.local/fuzzer-urls.php?a") == 3
