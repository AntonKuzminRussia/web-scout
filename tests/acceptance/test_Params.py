import subprocess
import os
import time
import re

runPath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../../')

#TODO 2 params
class Test_Params(object):
    dict_path = '/tmp/wstest.dict'
    headers_file_path = '/tmp/wstest.headers_file'
    conf_file_path = "/tmp/wstest.conf_file"

    def get_results_count(self, output):
        return len(re.findall('^(\t.+)', output, re.M))

    def test_get_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-get.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-size',
            '3'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\taa=1") == 1

    def test_get_mask(self):
        output = subprocess.check_output([
            './main.py',
            'ParamsMask',
            '--url',
            'http://wsat.local/params-bruter-mask-get.php',
            '--mask',
            '?l,1,1',
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-size',
            '3'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\tg=1") == 1

    def test_post_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-post.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '1000',
            '--params-method',
            'POST',
            '--not-found-size',
            '3'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\taa=1") == 1

    def test_post_mask(self):
        output = subprocess.check_output([
            './main.py',
            'ParamsMask',
            '--url',
            'http://wsat.local/params-bruter-mask-post.php',
            '--mask',
            '?l,1,1',
            '--max-params-length',
            '1000',
            '--params-method',
            'POST',
            '--not-found-size',
            '3'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\tg=1") == 1

    def test_cookie_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-cookie.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '10',
            '--params-method',
            'COOKIES',
            '--not-found-size',
            '3'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\taa=1") == 1 #TODO different, in all places and tests

    def test_cookie_mask(self):
        output = subprocess.check_output([
            './main.py',
            'ParamsMask',
            '--url',
            'http://wsat.local/params-bruter-mask-cookie.php',
            '--mask',
            '?l,1,1',
            '--max-params-length',
            '10',
            '--params-method',
            'COOKIES',
            '--not-found-size',
            '3'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\tg=1") == 1

    def test_files_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-files.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '10',
            '--params-method',
            'FILES',
            '--not-found-size',
            '3'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\taa=1") == 1

    def test_files_mask(self):
        output = subprocess.check_output([
            './main.py',
            'ParamsMask',
            '--url',
            'http://wsat.local/params-bruter-mask-files.php',
            '--mask',
            '?l,1,1',
            '--max-params-length',
            '10',
            '--params-method',
            'FILES',
            '--not-found-size',
            '3'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\tg=1") == 1

    def test_get_dict_value(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-get-value.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-size',
            '3',
            '--value',
            '2',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\taa=2") == 1

    def test_get_mask_value(self):
        output = subprocess.check_output([
            './main.py',
            'ParamsMask',
            '--url',
            'http://wsat.local/params-bruter-mask-get-value.php',
            '--mask',
            '?l,1,1',
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-size',
            '3',
            '--value',
            '2',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\tg=2") == 1

    def test_get_dict_not_found_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-not-found-re.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-re',
            'NOT'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\taa=1") == 1

    def test_get_dict_not_found_codes(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-not-found-codes.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-codes',
            '404'
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\taa=1") == 1

    def test_get_dict_ignore_words_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-get.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-size',
            '3',
            '--ignore-words-re',
            'aa'
        ])
        print(output)
        assert self.get_results_count(output) == 0
        assert output.count("Params found:\n\taa=1") == 0

    def test_get_dict_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\n")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-get.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-size',
            '3',
            '--delay',
            '3',
            '--threads',
            '1',
        ])
        etime = int(time.time())
        print(output)
        assert etime - stime > 9

    def test_get_dict_retest_codes(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-retest-codes.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-size',
            '3',
            '--retest-codes',
            '503',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\taa=1") == 1

    def test_get_dict_retest_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-retest-re.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-size',
            '3',
            '--retest-re',
            'Too big load',
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\taa=1") == 1

    def test_get_dict_heders_file(self):
        fh = open(self.dict_path, 'w')
        fh.write("aa\nbb\ncc\ndd\nee\nff\ngg\nhh\nii\n")
        fh.close()

        fh = open(self.headers_file_path, 'w')
        fh.write("Cookie: a=b\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'ParamsDict',
            '--url',
            'http://wsat.local/params-bruter-dict-headers-file.php',
            '--dict',
            self.dict_path,
            '--max-params-length',
            '1000',
            '--params-method',
            'GET',
            '--not-found-size',
            '3',
            '--retest-re',
            'Too big load',
            '--headers-file',
            self.headers_file_path
        ])
        print(output)
        assert self.get_results_count(output) == 1
        assert output.count("Params found:\n\taa=1") == 1
