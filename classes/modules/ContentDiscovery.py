# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

ContentDiscovery module class
"""
import re
import random
import subprocess
import datetime
from urlparse import urlparse

from classes.modules.DafsDict import DafsDict
from classes.modules.DafsModules import DafsModules
from classes.modules.params.ContentDiscoveryModuleParams import ContentDiscoveryModuleParams
from classes.kernel.WSModule import WSModule
from classes.Registry import Registry
from libs.common import file_to_list
from classes.kernel.WSOption import WSOption
from classes.generators.DictOfMask import DictOfMask


class ContentDiscovery(DafsDict):
    """ ContentDiscovery module class """
    logger_name = 'content_discovery'

    def __init__(self, kernel):
        DafsModules.__init__(self, kernel)
        self.options = ContentDiscoveryModuleParams().get_options()

    def gen_exts_variants(self, basename):
        """
        Return target exts list parsed from config
        :param basename:
        :return:
        """
        result = [basename]
        for ext in self.options['discovery-exts'].value.split(","):
            ext = ext.strip()
            result.append(basename + "." + ext)
        return result

    def gen_backups_variants(self, basename, may_be_file):
        """
        Generate backups variants by schames
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

    def gen_numbers_variants(self, basename, may_be_file):
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
        return results

    def write_bases_variants(self, base_fh):
        """
        Write in file basese variants for search.
        Using for write one big dictionary.
        :param base_fh:
        :return:
        """
        fh = open(Registry().get('wr_path') + "/bases/content-discovery/base.txt")
        while True:
            line = fh.readline()
            if not line:
                break
            line = line.strip()

            gens = self.gen_exts_variants(line)
            for gen in gens:
                base_fh.write(gen + "\n")

        fh.close()

    def write_tools_variants(self, base_fh):
        """
        Write in file variants from tools dict.
        Using for write one big dictionary.
        :param base_fh:
        :return:
        """
        fh = open(Registry().get('wr_path') + "/bases/content-discovery/tools-and-others.txt")
        while True:
            line = fh.readline()
            if not line:
                break
            line = line.strip()

            base_fh.write(line + "\n")

        fh.close()

    def write_urls_file_variants(self, urls_file, base_fh):
        """
        Write in file mutation variants of already known urls
        :param urls_file:
        :param base_fh:
        :return:
        """
        urls_fh = open(urls_file)
        while True:
            line = urls_fh.readline()
            if not line:
                break
            line = line.strip()

            parsed_url = urlparse(line)
            if not len(parsed_url.path) or parsed_url.path == '/':
                continue

            path = parsed_url.path[1:]  # Cut start /
            if path[-1] == "/":  # Cut end /
                path = path[:-1]

            c = 0
            parts = path.split("/")
            for part in parts:
                gens = []
                c += 1

                gens.extend(self.gen_backups_variants(part, c == len(parts)))
                if c == len(parts): # It`s may be file
                    gens.extend(self.gen_numbers_variants(part, True))
                gens.extend(self.gen_numbers_variants(part, False))

                if c == len(parts):  # It`s may be file
                    baseword = part[:part.rfind(".")] if part.count(".") else part
                else:
                    baseword = part

                gens.extend(self.gen_exts_variants(baseword))
                for gen in gens:
                    base_fh.write(gen + "\n")

        urls_fh.close()

    def write_mask_variants(self, mask, base_fh):
        """
        Write in file variants names generated by mask
        :param mask:
        :param base_fh:
        :return:
        """
        dom = DictOfMask(mask, 0, 0)
        while True:
            line = dom.get()
            if line is None:
                break

            gens = self.gen_exts_variants(line)
            for gen in gens:
                base_fh.write(gen + "\n")
        del dom

    def write_years(self, base_fh):
        """
        Write in file years variants, from 2010 to current
        :param base_fh:
        :return:
        """
        now = datetime.datetime.now()
        for year in range(2010, now.year+1):
            base_fh.write(str(year) + "\n")

    def build_attack_list(self, dict_path):
        """
        Building big monolit dict for attack
        :param dict_path:
        :return:
        """
        base_fh = open(dict_path, 'w')

        self.write_years(base_fh)
        self.write_bases_variants(base_fh)
        self.write_tools_variants(base_fh)
        self.write_mask_variants('?l?d,1,2', base_fh)

        if len(self.options['urls-file'].value):  # TODO is it checking for exists?
            self.write_urls_file_variants(self.options['urls-file'].value, base_fh)

        base_fh.close()

    def do_work(self):
        """ Start working """
        dict_path = "/tmp/web-scout-content-discovery-%d.txt" % random.randint(1000000, 9000000)

        self.build_attack_list(dict_path)

        dict_path_uniq = dict_path + "-uniq"
        subprocess.check_output("sort -u {0} > {1}".format(dict_path, dict_path_uniq), shell=True)

        tmp_files = Registry().get('tmp_files')
        tmp_files.append(dict_path)
        tmp_files.append(dict_path_uniq)
        Registry().set('tmp_files', tmp_files)

        self.options['dict'] = WSOption(
            "dict",
            "Dictionary for work",
            "",
            True,
            ['--dict']
        )
        self.options['dict'].value = dict_path_uniq

        WSModule.do_work(self)
