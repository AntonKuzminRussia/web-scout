import subprocess
import os
import time
import re

runPath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../../')
#TODO test found 2 passwords
#TODO print out everythere
class Test_FormBruter(object):
    dict_path = '/tmp/wstest.dict'
    headers_file_path = '/tmp/wstest.headers_file'
    conf_file_path = "/tmp/wstest.conf_file"

    def get_results_count(self, output):
        return len(re.findall('^(\t.+)', output, re.M))

    def test_raw_brute_false_re(self): #TODO all names to raw|selenium
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--url',
            'http://wsat.local/fbfalseandtruere.php',
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--false-re',
            'false'
        ])

        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_raw_brute_true_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--url',
            'http://wsat.local/fbfalseandtruere.php',
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--true-re',
            'true'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_raw_brute_false_size(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--url',
            'http://wsat.local/fbfalsesize.php', #TODO - everythere
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--false-size',
            '5'
        ])

        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_selenium_brute_false_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--selenium',
            '1',
            '--url',
            'http://wsat.local/fbseleniumfalseandtruere.php',
            '--dict',
            self.dict_path,
            '--login',
            'admin',
            '--false-re',
            'Submit',
            '--conf-file',
            self.conf_file_path,
        ])
        print (output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_selenium_brute_true_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--selenium',
            '1',
            '--url',
            'http://wsat.local/fbseleniumfalseandtruere.php',
            '--dict',
            self.dict_path,
            '--login',
            'admin',
            '--true-re',
            'true',
            '--conf-file',
            self.conf_file_path,
        ])
        print (output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_selenium_brute_false_size(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nadmin\ntest\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--selenium',
            '1',
            '--url',
            'http://wsat.local/fbseleniumfalsesize.php',
            '--dict',
            self.dict_path,
            '--login',
            'admin',
            '--false-size',
            '332',
            '--conf-file',
            self.conf_file_path,
        ])
        print (output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_raw_brute_retest_codes(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--url',
            'http://wsat.local/fbretestcodes.php',
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--false-re',
            'false',
            '--retest-codes',
            '503',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_raw_brute_retest_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--url',
            'http://wsat.local/fbretestre.php',
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--false-re',
            'false',
            '--retest-re',
            'too big',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_raw_brute_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--url',
            'http://wsat.local/fbretestre.php',
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--false-re',
            'false',
            '--delay',
            '2',
            '--threads',
            '1'
        ])
        etime = int(time.time())
        print(output)
        assert etime - stime > 10

    def test_selenium_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--selenium',
            '1',
            '--url',
            'http://wsat.local/fbseleniumfalseandtruere.php',
            '--dict',
            self.dict_path,
            '--login',
            'admin',
            '--false-re',
            'Submit',
            '--conf-file',
            self.conf_file_path,
            '--delay',
            '2'
        ])
        etime = int(time.time())
        print (output)
        assert etime - stime > 10

    def test_selenium_brute_false_re_browser_wait_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--selenium',
            '1',
            '--url',
            'http://wsat.local/fbseleniumbrowserwaitre.php',
            '--dict',
            self.dict_path,
            '--login',
            'admin',
            '--false-re',
            'Submit',
            '--conf-file',
            self.conf_file_path,
            '--browser-wait-re',
            'Checking your browser',
        ])
        print (output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_selenium_brute_true_browser_wait_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--selenium',
            '1',
            '--url',
            'http://wsat.local/fbseleniumbrowserwaitre.php',
            '--dict',
            self.dict_path,
            '--login',
            'admin',
            '--true-re',
            'true',
            '--conf-file',
            self.conf_file_path,
            '--browser-wait-re',
            'Checking your browser',
        ])
        print (output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_selenium_brute_false_size_browser_wait_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nadmin\ntest\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'FormBruter',
            '--selenium',
            '1',
            '--url',
            'http://wsat.local/fbseleniumbrowserwaitre.php',
            '--dict',
            self.dict_path,
            '--login',
            'admin',
            '--false-size',
            '597',
            '--conf-file',
            self.conf_file_path,
            '--browser-wait-re',
            'Checking your browser',
        ])
        print (output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1