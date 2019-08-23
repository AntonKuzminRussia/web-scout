# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class for generate words for ContentDiscovery module
"""
import re

from libs.common import file_to_list
from classes.Registry import Registry


class ContentDiscoveryNameGenerator(object):
    @staticmethod
    def gen_exts_variants(basename, exts):
        """
        Return target exts list parsed from config
        :param basename:
        :return:
        """
        result = [basename]
        for ext in exts:
            ext = ext.strip()
            result.append(basename + "." + ext)
        result.sort()
        return result

    @staticmethod
    def gen_letters_variants(basename, may_be_file):
        """
        Generate list of letters variants for files names with letters in start/end of name
        aaa.php => baa.php, caa.php, ...
        aaa.php => aab.php, aac.php, ...
        AAA.php => BAA.php, CAA.php, ...
        AAA.php => AAB.php, AAC.php, ...
        :param basename:
        :param may_be_file:
        :return:
        """
        letters_lower_case = [chr(n) for n in range(97, 123)]
        letters_upper_case = [chr(n) for n in range(65, 91)]

        result = ContentDiscoveryNameGenerator._gen_letters_variants(basename, may_be_file, '[a-z]', letters_lower_case) + \
                 ContentDiscoveryNameGenerator._gen_letters_variants(basename, may_be_file, '[A-Z]', letters_upper_case)
        result.sort()
        return result

    @staticmethod
    def _gen_letters_variants(basename, may_be_file, letters_regexp, letters_charset):
        """
        Generate list of letters variants for files names with letters in start/end of name
        aaa.php => baa.php, caa.php, ...
        aaa.php => aab.php, aac.php, ...
        :param basename:
        :param may_be_file:
        :return:
        """
        results = []
        basenames = [basename]

        ext = ""
        if may_be_file and basename.count("."):
            basenames = []
            ext = basename[basename.rfind("."):]
            basenames.append(basename[:basename.rfind(".")])

        for basename in basenames:
            basename = basename.strip()
            if not len(basename):
                continue

            if re.match(letters_regexp, basename[-1]):
                for i in letters_charset:
                    results.append(basename[:-1] + str(i) + ext)
            if re.match(letters_regexp, basename[0]):
                for i in letters_charset:
                    results.append(str(i) + basename[1:] + ext)
        results.sort()
        return results

    @staticmethod
    def gen_numbers_variants(basename, may_be_file):
        """
        Generate list of numbers variants for files names with digit in start/end of name + both variants in same time
        aaa1.php => aaa2.php, aaa3.php, ...
        1aaa.php => 2aaa.php, 3aaa.php, ...
        1aaa1.php => 2aaa2.php, 3aaa3.php, ...
        :param basename:
        :param may_be_file:
        :return:
        """
        results = []
        basenames = [basename]

        ext = ""
        if may_be_file and basename.count("."):
            basenames = []
            ext = basename[basename.rfind("."):]
            basenames.append(basename[:basename.rfind(".")])

        for basename in basenames:
            basename = basename.strip()
            if not len(basename):
                continue

            if re.match("\d", basename[-1]):
                for i in range(0, 10):
                    results.append(basename[:-1] + str(i) + ext)
            if re.match("\d", basename[0]):
                for i in range(0, 10):
                    results.append(str(i) + basename[1:] + ext)
            if re.match("\d", basename[-1]) and re.match("\d", basename[0]):
                for i in range(0, 10):
                    results.append(str(i) + basename[1:-1] + str(i) + ext)
            if not re.match("\d", basename[-1]) and not re.match("\d", basename[0]):
                for i in range(0, 10):
                    results.append(basename + str(i) + ext)
                    results.append(str(i) + basename + ext)
        results = list(set(results))
        results.sort()

        return results

    @staticmethod
    def gen_backups_variants(basename, may_be_file):
        """
        Generate backups variants by schemas
        :param basename:
        :param may_be_file:
        :return:
        """
        results = []
        basenames = [basename]

        if may_be_file and basename.count("."):
            basenames.append(basename[:basename.rfind(".")])

        schemas = file_to_list(Registry().get('wr_path') + "/bases/content-discovery/backup-schemas.txt")
        for basename in basenames:
            for schema in schemas:
                results.append(schema.replace("|name|", basename))
        return results