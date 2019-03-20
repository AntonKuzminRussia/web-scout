# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Threads pool class for Dafs* modules
"""
import random
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
    """ Common module class form Dafs* modules """
    logger_name = 'content_discovery'

    def __init__(self, kernel):
        DafsModules.__init__(self, kernel)
        self.options = ContentDiscoveryModuleParams().get_options()

    def gen_exts_variants(self, basename):
        result = [basename]
        for ext in self.options['discovery-exts'].value.split(","):
            ext = ext.strip()
            result.append(basename + "." + ext)
        return result

    def gen_backups_variants(self, basename, may_be_file):
        results = []
        basenames = [basename]

        if may_be_file and basename.count("."):
            basenames.append(basename[:basename.rfind(".")])

        schemas = file_to_list(Registry().get('wr_path') + "/bases/backup-schemas.txt")
        for basename in basenames:
            for schema in schemas:
                results.append(schema.replace("|name|", basename))
        return results

    def write_bases_variants(self, base_fh):
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
        fh = open(Registry().get('wr_path') + "/bases/content-discovery/tools-and-others.txt")
        while True:
            line = fh.readline()
            if not line:
                break
            line = line.strip()

            base_fh.write(line + "\n")

        fh.close()

    def write_urls_file_variants(self, urls_file, base_fh):
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

                if c == len(parts):  # It`s may be file
                    baseword = part[:part.rfind(".")] if part.count(".") else part
                else:
                    baseword = part

                gens.extend(self.gen_exts_variants(baseword))
                for gen in gens:
                    base_fh.write(gen + "\n")

        urls_fh.close()

    def write_mask_variants(self, mask, base_fh):
        dom = DictOfMask(mask, 0, 0)
        while True:
            line = dom.get()
            if line is None:
                break

            gens = self.gen_exts_variants(line)
            for gen in gens:
                base_fh.write(gen + "\n")
        del dom

    def build_attack_list(self, dict_path):
        base_fh = open(dict_path, 'w')

        self.write_bases_variants(base_fh)
        self.write_tools_variants(base_fh)
        self.write_mask_variants('?l?d,1,2', base_fh)

        if len(self.options['urls-file'].value):  # TODO is it checking for exists?
            self.write_urls_file_variants(self.options['urls-file'].value, base_fh)

        base_fh.close()

    def do_work(self):
        dict_path = "/tmp/web-scout-content-discovery-%d.txt" % random.randint(1000000, 9000000)

        tmp_files = Registry().get('tmp_files')
        tmp_files.append(dict_path)
        Registry().set('tmp_files', tmp_files)

        self.build_attack_list(dict_path)

        self.options['dict'] = WSOption(
            "dict",
            "Dictionary for work",
            "",
            True,
            ['--dict']
        )
        self.options['dict'].value = dict_path

        WSModule.do_work(self)
