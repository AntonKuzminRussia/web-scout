import subprocess
import os
import time
import re

runPath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../../')
#TODO test found 2 passwords
#TODO - in filenames, refactoring

class Test_HttpAuth(object):
    dict_path = '/tmp/wstest.dict'
    headers_file_path = '/tmp/wstest.headers_file'
    conf_file_path = "/tmp/wstest.conf_file"

    def get_results_count(self, output):
        return len(re.findall('^(\t.+)', output, re.M))


    def test_run(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\npassword\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './ws.py',
            'HttpAuth',
            '--url',
            'http://wsat.local/http-auth.php',
            '--dict',
            self.dict_path,
            '--login',
            'user'
        ])
        print(output)
        output = output.decode('utf8')
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\tpassword") == 1


    def test_run_retest_codes(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\npassword\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './ws.py',
            'HttpAuth',
            '--url',
            'http://wsat.local/http-auth-retest-codes.php',
            '--dict',
            self.dict_path,
            '--login',
            'user',
            '--retest-codes',
            '503'
        ])
        print(output)
        output = output.decode('utf8')
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\tpassword") == 1

    def test_run_retest_phrase(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\npassword\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './ws.py',
            'HttpAuth',
            '--url',
            'http://wsat.local/http-auth-retest-phrase.php',
            '--dict',
            self.dict_path,
            '--login',
            'user',
            '--retest-re',
            'Too big'
        ])
        print(output)
        output = output.decode('utf8')
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\tpassword") == 1

    def test_run_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './ws.py',
            'HttpAuth',
            '--url',
            'http://wsat.local/http-auth.php',
            '--dict',
            self.dict_path,
            '--login',
            'user',
            '--delay',
            '2',
            '--threads',
            '1',
        ])
        etime = int(time.time())
        print(output)
        output = output.decode('utf8')
        assert etime - stime > 10
