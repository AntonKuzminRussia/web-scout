import subprocess
import os
import time
import re

runPath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../../')
#TODO test found 2 passwords
#TODO - in filenames, refactoring

class Test_Forms(object):
    dict_path = '/tmp/wstest.dict'
    headers_file_path = '/tmp/wstest.headers_file'
    conf_file_path = "/tmp/wstest.conf_file"

    def get_results_count(self, output):
        return len(re.findall('^(\t.+)', output, re.M))

    def test_raw_false_re(self): #TODO all names to raw|selenium
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_raw_true_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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

    def test_raw_false_size(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_selenium_false_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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

    def test_selenium_true_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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

    def test_selenium_false_size(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nadmin\ntest\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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

    def test_raw_retest_codes(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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

    def test_raw_retest_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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

    def test_raw_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'Forms',
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
            'Forms',
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

    def test_selenium_false_re_browser_wait_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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

    def test_selenium_true_browser_wait_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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

    def test_selenium_false_size_browser_wait_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nadmin\ntest\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
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

    def test_selenium_reload_form_page(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        fh = open(self.conf_file_path, 'w')
        fh.write("^USER^\t#login\n^PASS^\t#pass\n^SUBMIT^\t#submit\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
            '--selenium',
            '1',
            '--url',
            'http://wsat.local/fbseleniumreloadformpage.php',
            '--dict',
            self.dict_path,
            '--login',
            'admin',
            '--false-re',
            'false',
            '--conf-file',
            self.conf_file_path,
            '--reload-form-page',
            '1',
        ])
        print (output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_raw_headers_file(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        fh = open(self.headers_file_path, 'w')
        fh.write("Cookie: a=b\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
            '--url',
            'http://wsat.local/fbheadersfile.php',
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--false-re',
            'false',
            '--headers-file',
            self.headers_file_path,
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_raw_pass_min_len(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
            '--url',
            'http://wsat.local/fbpassminlen.php',
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--false-re',
            'false',
            '--pass-min-len',
            '4',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_raw_pass_max_len(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
            '--url',
            'http://wsat.local/fbpassmaxlen.php',
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--false-re',
            'false',
            '--pass-max-len',
            '4',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1

    def test_raw_first_stop(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
            '--url',
            'http://wsat.local/fbfirststop.php',
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--false-re',
            'false',
            '--first-stop',
            '1',
            '--threads',
            '1',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\tadmin") == 1

    def test_raw_follow_redirects(self):
        fh = open(self.dict_path, 'w')
        fh.write("aaa\nbb\nccc\nddd\neee\nff\nadmin\ntest\nwegweg\negwdg\nssss\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'Forms',
            '--url',
            'http://wsat.local/fbfollowredirects.php',
            '--dict',
            self.dict_path,
            '--conf-str',
            'login=^USER^&password=^PASS^',
            '--login',
            'admin',
            '--false-re',
            'false',
            '--follow-redirects',
            '1',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Passwords found:\n\ttest") == 1