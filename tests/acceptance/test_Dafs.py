import subprocess
import os
import time
import re

runPath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../../')
#TODO tests re as re, not as str only

class Test_Dafs(object):
    dict_path = '/tmp/wstest.dict'
    headers_file_path = '/tmp/wstest.headers_file'

    def get_results_count(self, output):
        return len(re.findall('^(\d+ http)', output, re.M))

    def test_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("simpledicta.php\naaa\nsimpledictb.php\nbbb\nsimpledict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/simpledicta.php") == 1
        assert output.count("/simpledictb.php") == 1
        assert output.count("/simpledict9.php") == 1

    def test_mask(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--template',
            'http://wsat.local/simplemask@.php',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/simplemaska.php") == 1
        assert output.count("/simplemaskb.php") == 1
        assert output.count("/simplemask9.php") == 1

    def test_comb(self):
        fh = open(self.dict_path, 'w')
        fh.write("simpleaaa\nsimplecomb\nsimplebbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/simplecomba.php") == 1
        assert output.count("/simplecombb.php") == 1
        assert output.count("/simplecomb9.php") == 1

    def test_not_found_re_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("nfredicta.php\nnfreaaa\nnfredictb.php\nnfrebbb\nnfredict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--template',
            'http://wsat.local/@',
            '--not-found-re',
            'always 200',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/nfredicta.php") == 1
        assert output.count("/nfredictb.php") == 1
        assert output.count("/nfredict9.php") == 1

    def test_not_found_re_mask(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--template',
            'http://wsat.local/nfremask@.php',
            '--not-found-re',
            'always 200',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/nfremaska.php") == 1
        assert output.count("/nfremaskb.php") == 1
        assert output.count("/nfremask9.php") == 1

    def test_not_found_re_comb(self):
        fh = open(self.dict_path, 'w')
        fh.write("nfreaaa\nnfrecomb\nnfrebbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/nfrecomba.php") == 1
        assert output.count("/nfrecombb.php") == 1
        assert output.count("/nfrecomb9.php") == 1

    def test_found_re_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("fredicta.php\nfreaaa\nfredictb.php\nfrebbb\nfredict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--template',
            'http://wsat.local/@',
            '--found-re',
            'Really',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/fredicta.php") == 1
        assert output.count("/fredictb.php") == 1
        assert output.count("/fredict9.php") == 1

    def test_found_re_mask(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--template',
            'http://wsat.local/fremask@.php',
            '--found-re',
            'Really',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/fremaska.php") == 1
        assert output.count("/fremaskb.php") == 1
        assert output.count("/fremask9.php") == 1

    def test_found_re_comb(self):
        fh = open(self.dict_path, 'w')
        fh.write("freaaa\nfrecomb\nfrebbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/frecomba.php") == 1
        assert output.count("/frecombb.php") == 1
        assert output.count("/frecomb9.php") == 1

    def test_not_found_size_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("nfsizedicta.php\nnfsizeaaa\nnfsizedictb.php\nnfsizebbb\nnfsizedict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--template',
            'http://wsat.local/@',
            '--not-found-size',
            '20',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/nfsizedicta.php") == 1
        assert output.count("/nfsizedictb.php") == 1
        assert output.count("/nfsizedict9.php") == 1

    def test_not_found_size_mask(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--template',
            'http://wsat.local/nfsizemask@.php',
            '--not-found-size',
            '20',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/nfsizemaska.php") == 1
        assert output.count("/nfsizemaskb.php") == 1
        assert output.count("/nfsizemask9.php") == 1

    def test_not_found_size_comb(self):
        fh = open(self.dict_path, 'w')
        fh.write("nfsizeaaa\nnfsizecomb\nnfsizebbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/nfsizecomba.php") == 1
        assert output.count("/nfsizecombb.php") == 1
        assert output.count("/nfsizecomb9.php") == 1

    def test_not_found_codes_dict(self):
        fh = open(self.dict_path, 'w')
        fh.write("nfcodesdicta.php\nnfcodesaaa\nnfcodesdictb.php\nnfcodesbbb\nnfcodesdict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--template',
            'http://wsat.local/@',
            '--not-found-codes',
            '200',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/nfcodesdicta.php") == 1
        assert output.count("/nfcodesdictb.php") == 1
        assert output.count("/nfcodesdict9.php") == 1

    def test_not_found_codes_mask(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--template',
            'http://wsat.local/nfcodesmask@.php',
            '--not-found-codes',
            '200',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/nfcodesmaska.php") == 1
        assert output.count("/nfcodesmaskb.php") == 1
        assert output.count("/nfcodesmask9.php") == 1

    def test_not_found_codes_comb(self):
        fh = open(self.dict_path, 'w')
        fh.write("nfcodesaaa\nnfcodescomb\nnfcodesbbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/nfcodescomba.php") == 1
        assert output.count("/nfcodescombb.php") == 1
        assert output.count("/nfcodescomb9.php") == 1

    def test_dict_ignore_words(self):
        fh = open(self.dict_path, 'w')
        fh.write("simpledicta.php\naaa\nsimpledictb.php\nbbb\nsimpledict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--ignore-words-re',
            'b',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 2
        assert output.count("/simpledicta.php") == 1
        assert output.count("/simpledict9.php") == 1

    def test_mask_ignore_words(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--ignore-words-re',
            'b',
            '--template',
            'http://wsat.local/simplemask@.php',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 2
        assert output.count("/simplemaska.php") == 1
        assert output.count("/simplemask9.php") == 1

    def test_comb_ignore_words(self):
        fh = open(self.dict_path, 'w')
        fh.write("simpleaaa\nsimplecomb\nsimplebbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
            '--ignore-words-re',
            'b',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 2
        assert output.count("/simplecomba.php") == 1
        assert output.count("/simplecomb9.php") == 1

    def test_dict_retest_codes(self):
        fh = open(self.dict_path, 'w')
        fh.write("retestcodesdicta.php\naaa\nretestcodesdictb.php\nbbb\nretestcodesdict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--retest-codes',
            '503',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/retestcodesdicta.php") == 1
        assert output.count("/retestcodesdictb.php") == 1
        assert output.count("/retestcodesdict9.php") == 1

    def test_mask_retest_codes(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--retest-codes',
            '503',
            '--template',
            'http://wsat.local/retestcodesmask@.php',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/retestcodesmaska.php") == 1
        assert output.count("/retestcodesmaskb.php") == 1
        assert output.count("/retestcodesmask9.php") == 1

    def test_comb_retest_codes(self):
        fh = open(self.dict_path, 'w')
        fh.write("retestcodesaaa\nretestcodescomb\nretestcodesbbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/retestcodescomba.php") == 1
        assert output.count("/retestcodescombb.php") == 1
        assert output.count("/retestcodescomb9.php") == 1

    def test_dict_retest_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("retestredicta.php\naaa\nretestredictb.php\nbbb\nretestredict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--retest-re',
            'unavailable',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/retestredicta.php") == 1
        assert output.count("/retestredictb.php") == 1
        assert output.count("/retestredict9.php") == 1

    def test_mask_retest_re(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--retest-re',
            'unavailable',
            '--template',
            'http://wsat.local/retestremask@.php',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/retestremaska.php") == 1
        assert output.count("/retestremaskb.php") == 1
        assert output.count("/retestremask9.php") == 1

    def test_comb_retest_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("retestreaaa\nretestrecomb\nretestrebbb")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/retestrecomba.php") == 1
        assert output.count("/retestrecombb.php") == 1
        assert output.count("/retestrecomb9.php") == 1

    def test_dict_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("simpledicta.php\naaa\nsimpledictb.php\nbbb\nsimpledict9.php\n")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'DafsDict',
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

        assert etime-stime > 10

    def test_mask_delay(self):
        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
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

        assert etime-stime > 10

    def test_comb_delay(self):
        fh = open(self.dict_path, 'w')
        fh.write("test\n")
        fh.close()

        stime = int(time.time())
        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert etime-stime > 10

    def test_dict_selenium(self):
        fh = open(self.dict_path, 'w')
        fh.write("simpledicta.php\nsimpleaaa\nsimpledictb.php\nsimplebbb\nsimpledict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--selenium',
            '1',
            '--not-found-re',
            '<h1>404 Not Found</h1>',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/simpledicta.php") == 1
        assert output.count("/simpledictb.php") == 1
        assert output.count("/simpledict9.php") == 1

    def test_mask_selenium(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--selenium',
            '1',
            '--not-found-re',
            '<h1>404 Not Found</h1>',
            '--template',
            'http://wsat.local/simplemask@.php',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/simplemaska.php") == 1
        assert output.count("/simplemaskb.php") == 1
        assert output.count("/simplemask9.php") == 1

    def test_comb_selenium(self):
        fh = open(self.dict_path, 'w')
        fh.write("simplecomb\nsimpleaaa\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/simplecomba.php") == 1
        assert output.count("/simplecombb.php") == 1
        assert output.count("/simplecomb9.php") == 1

    def test_dict_selenium_not_found_size(self):
        fh = open(self.dict_path, 'w')
        fh.write("simpledicta.php\nsimpleaaa\nsimpledictb.php\nsimplebbb\nsimpledict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--selenium',
            '1',
            '--not-found-size',
            '61',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/simpledicta.php") == 1
        assert output.count("/simpledictb.php") == 1
        assert output.count("/simpledict9.php") == 1

    def test_mask_selenium_not_found_size(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--selenium',
            '1',
            '--not-found-size',
            '61',
            '--template',
            'http://wsat.local/simplemask@.php',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/simplemaska.php") == 1
        assert output.count("/simplemaskb.php") == 1
        assert output.count("/simplemask9.php") == 1

    def test_comb_selenium_not_found_size(self):
        fh = open(self.dict_path, 'w')
        fh.write("simplecomb\nsimpleaaa\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/simplecomba.php") == 1
        assert output.count("/simplecombb.php") == 1
        assert output.count("/simplecomb9.php") == 1

    def test_dict_selenium_wait_re(self):
        fh = open(self.dict_path, 'w')
        fh.write("seleniumwaitdicta.php\naaa\nseleniumwaitdictb.php\nbbb\nseleniumwaitdict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
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

        assert self.get_results_count(output) == 2
        assert output.count("/seleniumwaitdicta.php") == 1
        assert output.count("/seleniumwaitdictb.php") == 1

    def test_mask_selenium_wait_re(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--selenium',
            '1',
            '--not-found-re',
            '404 Not Found',
            '--browser-wait-re',
            'Checking your browser',
            '--template',
            'http://wsat.local/seleniumwaitmask@.php',
            '--mask',
            '?l?d,1,1',
        ])

        assert self.get_results_count(output) == 2
        assert output.count("/seleniumwaitmaska.php") == 1
        assert output.count("/seleniumwaitmaskb.php") == 1

    def test_comb_headers_file(self):
        fh = open(self.dict_path, 'w')
        fh.write("headersdicta.php\nheadersaaa\nheadersdictb.php\nheadersbbb\nheadersdict9.php\n")
        fh.close()

        fh = open(self.headers_file_path, 'w')
        fh.write("Cookie: a=b\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
            '--headers-file',
            self.headers_file_path,
            '--template',
            'http://wsat.local/@',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 2
        assert output.count("/seleniumwaitdicta.php") == 1
        assert output.count("/seleniumwaitdictb.php") == 1

    def test_mask_headers_file(self):
        fh = open(self.headers_file_path, 'w')
        fh.write("Cookie: a=b\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--headers-file',
            self.headers_file_path,
            '--template',
            'http://wsat.local/headersmask@.php',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/headersmaska.php") == 1
        assert output.count("/headersmaskb.php") == 1
        assert output.count("/headersmask9.php") == 1

    def test_comb_headers_file(self):
        fh = open(self.dict_path, 'w')
        fh.write("headersaaa\nheaderscomb\nheadersbbb")
        fh.close()

        fh = open(self.headers_file_path, 'w')
        fh.write("Cookie: a=b\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/headerscomba.php") == 1
        assert output.count("/headerscombb.php") == 1
        assert output.count("/headerscomb9.php") == 1

    def test_dict_method_post(self):
        fh = open(self.dict_path, 'w')
        fh.write("postdicta.php\naaa\npostdictb.php\nbbb\npostdict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--method',
            'POST',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/postdicta.php") == 1
        assert output.count("/postdictb.php") == 1
        assert output.count("/postdict9.php") == 1

    def test_mask_method_post(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--method',
            'POST',
            '--template',
            'http://wsat.local/postmask@.php',
            '--mask',
            '?l?d,1,1',
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/postmaska.php") == 1
        assert output.count("/postmaskb.php") == 1
        assert output.count("/postmask9.php") == 1

    def test_comb_method_post(self):
        fh = open(self.dict_path, 'w')
        fh.write("postcomb\naaa\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/postcomba.php") == 1
        assert output.count("/postcombb.php") == 1
        assert output.count("/postcomb9.php") == 1

    def test_dict_method_head(self):
        fh = open(self.dict_path, 'w')
        fh.write("headdicta.php\naaa\nheaddictb.php\nbbb\nheaddict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--method',
            'HEAD',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/headdicta.php") == 1
        assert output.count("/headdictb.php") == 1
        assert output.count("/headdict9.php") == 1

    def test_mask_method_head(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--method',
            'HEAD',
            '--template',
            'http://wsat.local/headmask@.php',
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/headmaska.php") == 1
        assert output.count("/headmaskb.php") == 1
        assert output.count("/headmask9.php") == 1

    def test_comb_method_head(self):
        fh = open(self.dict_path, 'w')
        fh.write("headcomb\naaa\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
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

        assert self.get_results_count(output) == 3
        assert output.count("/headcomba.php") == 1
        assert output.count("/headcombb.php") == 1
        assert output.count("/headcomb9.php") == 1

    def test_dict_method_get_default(self):
        fh = open(self.dict_path, 'w')
        fh.write("getdicta.php\naaa\ngetdictb.php\nbbb\ngetdict9.php\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsDict',
            '--template',
            'http://wsat.local/@',
            '--dict',
            self.dict_path
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/getdicta.php") == 1
        assert output.count("/getdictb.php") == 1
        assert output.count("/getdict9.php") == 1

    def test_mask_method_get_default(self):
        output = subprocess.check_output([
            './main.py',
            'DafsMask',
            '--template',
            'http://wsat.local/getmask@.php',
            '--mask',
            '?l?d,1,1',
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/getmaska.php") == 1
        assert output.count("/getmaskb.php") == 1
        assert output.count("/getmask9.php") == 1

    def test_comb_method_get_default(self):
        fh = open(self.dict_path, 'w')
        fh.write("getcomb\naaa\n")
        fh.close()

        output = subprocess.check_output([
            './main.py',
            'DafsCombine',
            '--template',
            'http://wsat.local/@.php',
            '--combine-template',
            '%d%%m%',
            '--dict',
            self.dict_path,
            '--mask',
            '?l?d,1,1'
        ])

        assert self.get_results_count(output) == 3
        assert output.count("/getcomba.php") == 1
        assert output.count("/getcombb.php") == 1
        assert output.count("/getcomb9.php") == 1