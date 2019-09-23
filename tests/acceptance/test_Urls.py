import subprocess
import os
import time
import re

runPath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../../')
#TODO tests re as re, not as str only

class Test_Urls(object):
    dict_path = '/tmp/wstest.dict'
    headers_file_path = '/tmp/wstest.headers_file'

    def get_results_count(self, output):
        return len(re.findall('^(\d+ http)', output, re.M))

    def test_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-simple-dict-a.php\naaa\ndafs-simple-dict-b.php\nbbb\ndafs-simple-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-simple-dict-a.php") == 1
        assert output.count("/dafs-simple-dict-b.php") == 1
        assert output.count("/dafs-simple-dict-9.php") == 1

    def test_mask(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--template',
            'http://wsat.local/dafs-simple-mask-@.php',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-simple-mask-a.php") == 1
        assert output.count("/dafs-simple-mask-b.php") == 1
        assert output.count("/dafs-simple-mask-9.php") == 1

    def test_comb(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-simpleaaa-\ndafs-simple-comb-\ndafs-simplebbb-")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-simple-comb-a.php") == 1
        assert output.count("/dafs-simple-comb-b.php") == 1
        assert output.count("/dafs-simple-comb-9.php") == 1

    def test_not_found_re_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-not-found-re-dict-a.php\ndafs-not-found-reaaa\ndafs-not-found-re-dict-b.php\ndafs-not-found-rebbb\ndafs-not-found-re-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--template',
            'http://wsat.local/@',
            '--not-found-re',
            'always 200',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-not-found-re-dict-a.php") == 1
        assert output.count("/dafs-not-found-re-dict-b.php") == 1
        assert output.count("/dafs-not-found-re-dict-9.php") == 1

    def test_not_found_re_mask(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--template',
            'http://wsat.local/dafs-not-found-re-mask-@.php',
            '--not-found-re',
            'always 200',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-not-found-re-mask-a.php") == 1
        assert output.count("/dafs-not-found-re-mask-b.php") == 1
        assert output.count("/dafs-not-found-re-mask-9.php") == 1

    def test_not_found_re_comb(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-not-found-re-aaa\ndafs-not-found-re-comb-\ndafs-not-found-re-bbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--template',
            'http://wsat.local/@.php',
            '--not-found-re',
            'always 200',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-not-found-re-comb-a.php") == 1
        assert output.count("/dafs-not-found-re-comb-b.php") == 1
        assert output.count("/dafs-not-found-re-comb-9.php") == 1

    def test_found_re_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-found-re-dict-a.php\nfreaaa\ndafs-found-re-dict-b.php\nfrebbb\ndafs-found-re-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--template',
            'http://wsat.local/@',
            '--found-re',
            'Really',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/dafs-found-re-dict-a.php") == 1
        assert output.count("/dafs-found-re-dict-b.php") == 1
        assert output.count("/dafs-found-re-dict-9.php") == 1

    def test_found_re_mask(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--template',
            'http://wsat.local/dafs-found-re-mask-@.php',
            '--found-re',
            'Really',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-found-re-mask-a.php") == 1
        assert output.count("/dafs-found-re-mask-b.php") == 1
        assert output.count("/dafs-found-re-mask-9.php") == 1

    def test_found_re_comb(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-found-re-aaa\ndafs-found-re-comb-\ndafs-found-re-bbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--template',
            'http://wsat.local/@.php',
            '--found-re',
            'Really',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-found-re-comb-a.php") == 1
        assert output.count("/dafs-found-re-comb-b.php") == 1
        assert output.count("/dafs-found-re-comb-9.php") == 1

    def test_not_found_size_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-not-found-size-dict-a.php\ndafs-not-found-sizeaaa\ndafs-not-found-size-dict-b.php\ndafs-not-found-sizebbb\ndafs-not-found-size-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--template',
            'http://wsat.local/@',
            '--not-found-size',
            '20',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-not-found-size-dict-a.php") == 1
        assert output.count("/dafs-not-found-size-dict-b.php") == 1
        assert output.count("/dafs-not-found-size-dict-9.php") == 1

    def test_not_found_size_mask(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--template',
            'http://wsat.local/dafs-not-found-size-mask-@.php',
            '--not-found-size',
            '20',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-not-found-size-mask-a.php") == 1
        assert output.count("/dafs-not-found-size-mask-b.php") == 1
        assert output.count("/dafs-not-found-size-mask-9.php") == 1

    def test_not_found_size_comb(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-not-found-sizeaaa\ndafs-not-found-size-comb-\ndafs-not-found-sizebbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--template',
            'http://wsat.local/@.php',
            '--not-found-size',
            '20',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-not-found-size-comb-a.php") == 1
        assert output.count("/dafs-not-found-size-comb-b.php") == 1
        assert output.count("/dafs-not-found-size-comb-9.php") == 1

    def test_not_found_codes_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-not-found-codes-dict-a.php\ndafs-not-found-codesaaa\ndafs-not-found-codes-dict-b.php\ndafs-not-found-codesbbb\ndafs-not-found-codes-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--template',
            'http://wsat.local/@',
            '--not-found-codes',
            '200',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-not-found-codes-dict-a.php") == 1
        assert output.count("/dafs-not-found-codes-dict-b.php") == 1
        assert output.count("/dafs-not-found-codes-dict-9.php") == 1

    def test_not_found_codes_mask(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--template',
            'http://wsat.local/dafs-not-found-codes-mask-@.php',
            '--not-found-codes',
            '200',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-not-found-codes-mask-a.php") == 1
        assert output.count("/dafs-not-found-codes-mask-b.php") == 1
        assert output.count("/dafs-not-found-codes-mask-9.php") == 1

    def test_not_found_codes_comb(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-not-found-codes-aaa\ndafs-not-found-codes-comb-\ndafs-not-found-codes-bbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--template',
            'http://wsat.local/@.php',
            '--not-found-codes',
            '200',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-not-found-codes-comb-a.php") == 1
        assert output.count("/dafs-not-found-codes-comb-b.php") == 1
        assert output.count("/dafs-not-found-codes-comb-9.php") == 1

    def test_dict_ignore_words(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-simple-dict-a.php\naaa\ndafs-simple-dict-b.php\nbbb\ndafs-simple-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--ignore-words-re',
            'b',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 2
        assert output.count("/dafs-simple-dict-a.php") == 1
        assert output.count("/dafs-simple-dict-9.php") == 1

    def test_mask_ignore_words(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--ignore-words-re',
            'b',
            '--template',
            'http://wsat.local/dafs-simple-mask-@.php',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 2
        assert output.count("/dafs-simple-mask-a.php") == 1
        assert output.count("/dafs-simple-mask-9.php") == 1

    def test_comb_ignore_words(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-simpleaaa\ndafs-simple-comb-\ndafs-simplebbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--ignore-words-re',
            'b', #TODO fix here
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 2
        assert output.count("/dafs-simple-comb-a.php") == 1
        assert output.count("/dafs-simple-comb-9.php") == 1

    def test_dict_retest_codes(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-retest-codes-dict-a.php\naaa\ndafs-retest-codes-dict-b.php\nbbb\ndafs-retest-codes-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--retest-codes',
            '503',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-retest-codes-dict-a.php") == 1
        assert output.count("/dafs-retest-codes-dict-b.php") == 1
        assert output.count("/dafs-retest-codes-dict-9.php") == 1

    def test_mask_retest_codes(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--retest-codes',
            '503',
            '--template',
            'http://wsat.local/dafs-retest-codes-mask-@.php',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-retest-codes-mask-a.php") == 1
        assert output.count("/dafs-retest-codes-mask-b.php") == 1
        assert output.count("/dafs-retest-codes-mask-9.php") == 1

    def test_comb_retest_codes(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-retest-codesaaa\ndafs-retest-codes-comb-\ndafs-retest-codesbbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--retest-codes',
            '503',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-retest-codes-comb-a.php") == 1
        assert output.count("/dafs-retest-codes-comb-b.php") == 1
        assert output.count("/dafs-retest-codes-comb-9.php") == 1

    def test_dict_retest_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-retest-re-dict-a.php\naaa\ndafs-retest-re-dict-b.php\nbbb\ndafs-retest-re-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--retest-re',
            'unavailable',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-retest-re-dict-a.php") == 1
        assert output.count("/dafs-retest-re-dict-b.php") == 1
        assert output.count("/dafs-retest-re-dict-9.php") == 1

    def test_mask_retest_re(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--retest-re',
            'unavailable',
            '--template',
            'http://wsat.local/dafs-retest-re-mask-@.php',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-retest-re-mask-a.php") == 1
        assert output.count("/dafs-retest-re-mask-b.php") == 1
        assert output.count("/dafs-retest-re-mask-9.php") == 1

    def test_comb_retest_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-retest-re-aaa\ndafs-retest-re-comb-\ndafs-retest-re-bbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--retest-re',
            'unavailable',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-retest-re-comb-a.php") == 1
        assert output.count("/dafs-retest-re-comb-b.php") == 1
        assert output.count("/dafs-retest-re-comb-9.php") == 1

    def test_dict_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-simple-dict-a.php\naaa\ndafs-simple-dict-b.php\nbbb\ndafs-simple-dict-9.php\n")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--threads',
            '1',
            '--delay',
            '2',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        etime = int(time.time())
        print(output)
        assert etime-stime > 10

    def test_mask_delay(self):
        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--threads',
            '1',
            '--delay',
            '1',
            '--template',
            'http://wsat.local/@',
            '--mask',
            '?d,1,1',
        ])
        etime = int(time.time())
        print(output)
        assert etime-stime > 10

    def test_comb_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\n")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--threads',
            '1',
            '--delay',
            '1',
            '--template',
            'http://wsat.local/@',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        etime = int(time.time())
        print(output)
        assert etime-stime > 10

    def test_dict_selenium(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-simple-dict-a.php\ndafs-simpleaaa\ndafs-simple-dict-b.php\nsimplebbb\ndafs-simple-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--selenium',
            '1',
            '--not-found-re',
            '<h1>404 Not Found</h1>',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-simple-dict-a.php") == 1
        assert output.count("/dafs-simple-dict-b.php") == 1
        assert output.count("/dafs-simple-dict-9.php") == 1

    def test_mask_selenium(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--selenium',
            '1',
            '--not-found-re',
            '<h1>404 Not Found</h1>',
            '--template',
            'http://wsat.local/dafs-simple-mask-@.php',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-simple-mask-a.php") == 1
        assert output.count("/dafs-simple-mask-b.php") == 1
        assert output.count("/dafs-simple-mask-9.php") == 1

    def test_comb_selenium(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-simple-comb-\ndafs-simple-aaa\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--selenium',
            '1',
            '--not-found-re',
            '<h1>404 Not Found</h1>',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-simple-comb-a.php") == 1
        assert output.count("/dafs-simple-comb-b.php") == 1
        assert output.count("/dafs-simple-comb-9.php") == 1

    def test_dict_selenium_not_found_size(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-simple-dict-a.php\nsimpleaaa\ndafs-simple-dict-b.php\nsimplebbb\ndafs-simple-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--selenium',
            '1',
            '--not-found-size',
            '61',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-simple-dict-a.php") == 1
        assert output.count("/dafs-simple-dict-b.php") == 1
        assert output.count("/dafs-simple-dict-9.php") == 1

    def test_mask_selenium_not_found_size(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--selenium',
            '1',
            '--not-found-size',
            '61',
            '--template',
            'http://wsat.local/dafs-simple-mask-@.php',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-simple-mask-a.php") == 1
        assert output.count("/dafs-simple-mask-b.php") == 1
        assert output.count("/dafs-simple-mask-9.php") == 1

    def test_comb_selenium_not_found_size(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-simple-comb-\nsimpleaaa\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--selenium',
            '1',
            '--not-found-size',
            '61',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-simple-comb-a.php") == 1
        assert output.count("/dafs-simple-comb-b.php") == 1
        assert output.count("/dafs-simple-comb-9.php") == 1

    def test_dict_selenium_wait_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-selenium-browser-wait-re-dict-a.php\naaa\ndafs-selenium-browser-wait-re-dict-b.php\nbbb\ndafs-selenium-browser-wait-re-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--selenium',
            '1',
            '--not-found-re',
            '404 Not Found',
            '--browser-wait-re',
            'Checking your browser',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 2
        assert output.count("/dafs-selenium-browser-wait-re-dict-a.php") == 1
        assert output.count("/dafs-selenium-browser-wait-re-dict-b.php") == 1

    def test_mask_selenium_wait_re(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--selenium',
            '1',
            '--not-found-re',
            '404 Not Found',
            '--browser-wait-re',
            'Checking your browser',
            '--template',
            'http://wsat.local/dafs-selenium-browser-wait-re-mask-@.php',
            '--mask',
            '?l?d,1,1',
        ])
        print(output)
        assert self.get_results_count(output) == 2
        assert output.count("/dafs-selenium-browser-wait-re-mask-a.php") == 1
        assert output.count("/dafs-selenium-browser-wait-re-mask-b.php") == 1

    def test_comb_selenium_wait_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-selenium-browser-wait-re-dict-\naaa")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--combine-template',
            '%d%%m%',
            '--selenium',
            '1',
            '--not-found-re',
            '404 Not Found',
            '--browser-wait-re',
            'Checking your browser',
            '--template',
            'http://wsat.local/@.php',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 2
        assert output.count("/dafs-selenium-browser-wait-re-dict-a.php") == 1
        assert output.count("/dafs-selenium-browser-wait-re-dict-b.php") == 1

    def test_dict_headers_file(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-headers-file-dict-a.php\nheadersaaa\ndafs-headers-file-dict-b.php\nheadersbbb\ndafs-headers-file-dict-9.php\n")
        fh.close()

        fh = open(self.headers_file_path, 'w')
        fh.write("Cookie: a=b\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--headers-file',
            self.headers_file_path,
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path,
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-headers-file-dict-a.php") == 1
        assert output.count("/dafs-headers-file-dict-b.php") == 1
        assert output.count("/dafs-headers-file-dict-9.php") == 1

    def test_mask_headers_file(self):
        fh = open(self.headers_file_path, 'w')
        fh.write("Cookie: a=b\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--headers-file',
            self.headers_file_path,
            '--template',
            'http://wsat.local/dafs-headers-file-mask-@.php',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-headers-file-mask-a.php") == 1
        assert output.count("/dafs-headers-file-mask-b.php") == 1
        assert output.count("/dafs-headers-file-mask-9.php") == 1

    def test_comb_headers_file(self):
        fh = open(self.dict_path, 'w')
        fh.write("headersaaa\ndafs-headers-file-comb-\nheadersbbb")
        fh.close()

        fh = open(self.headers_file_path, 'w')
        fh.write("Cookie: a=b\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--headers-file',
            self.headers_file_path,
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-headers-file-comb-a.php") == 1
        assert output.count("/dafs-headers-file-comb-b.php") == 1
        assert output.count("/dafs-headers-file-comb-9.php") == 1

    def test_dict_method_post(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-post-dict-a.php\naaa\ndafs-post-dict-b.php\nbbb\ndafs-post-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--method',
            'POST',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-post-dict-a.php") == 1
        assert output.count("/dafs-post-dict-b.php") == 1
        assert output.count("/dafs-post-dict-9.php") == 1

    def test_mask_method_post(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--method',
            'POST',
            '--template',
            'http://wsat.local/dafs-post-mask-@.php',
            '--mask',
            '?l?d,1,1',
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-post-mask-a.php") == 1
        assert output.count("/dafs-post-mask-b.php") == 1
        assert output.count("/dafs-post-mask-9.php") == 1

    def test_comb_method_post(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-post-comb-\naaa\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--method',
            'POST',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-post-comb-a.php") == 1
        assert output.count("/dafs-post-comb-b.php") == 1
        assert output.count("/dafs-post-comb-9.php") == 1

    def test_dict_method_head(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-head-dict-a.php\naaa\ndafs-head-dict-b.php\nbbb\ndafs-head-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--method',
            'HEAD',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-head-dict-a.php") == 1
        assert output.count("/dafs-head-dict-b.php") == 1
        assert output.count("/dafs-head-dict-9.php") == 1

    def test_mask_method_head(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--method',
            'HEAD',
            '--template',
            'http://wsat.local/dafs-head-mask-@.php',
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-head-mask-a.php") == 1
        assert output.count("/dafs-head-mask-b.php") == 1
        assert output.count("/dafs-head-mask-9.php") == 1

    def test_comb_method_head(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-head-comb-\naaa\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--method',
            'HEAD',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-head-comb-a.php") == 1
        assert output.count("/dafs-head-comb-b.php") == 1
        assert output.count("/dafs-head-comb-9.php") == 1

    def test_dict_method_get_default(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-get-dict-a.php\naaa\ndafs-get-dict-b.php\nbbb\ndafs-get-dict-9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsDict',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-get-dict-a.php") == 1
        assert output.count("/dafs-get-dict-b.php") == 1
        assert output.count("/dafs-get-dict-9.php") == 1

    def test_mask_method_get_default(self):
        output = subprocess.check_output([
            './main.py',
            'UrlsMask',
            '--template',
            'http://wsat.local/dafs-get-mask-@.php',
            '--mask',
            '?l?d,1,1',
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-get-mask-a.php") == 1
        assert output.count("/dafs-get-mask-b.php") == 1
        assert output.count("/dafs-get-mask-9.php") == 1

    def test_comb_method_get_default(self):
        fh = open(self.dict_path, 'w')
        fh.write("dafs-get-comb-\naaa\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'UrlsCombine',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])
        print(output)
        assert self.get_results_count(output) == 3
        assert output.count("/dafs-get-comb-a.php") == 1
        assert output.count("/dafs-get-comb-b.php") == 1
        assert output.count("/dafs-get-comb-9.php") == 1