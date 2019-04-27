# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class for logging WS output
"""

import sys
import os
import traceback
import re
import codecs
import random

from libs.common import t
from classes.Registry import Registry


class Logger(object):
    """ Class for logging WS output """
    logs_dir = None
    module_name = None
    log_fh = None
    items_dir = None
    scan_name = None
    scan_hash = None

    def __init__(self, module_name, have_items):
        self.module_name = module_name
        logs_dir = "{0}/logs/{1}".format(Registry().get('wr_path'), module_name)
        curdate = t("%Y-%m-%d")
        curtime = t("%H_%M_%S")

        if not os.path.exists(logs_dir):
            os.mkdir(logs_dir)

        log_date_path = "{0}/{1}".format(logs_dir, curdate)
        if not os.path.exists(log_date_path):
            os.mkdir(log_date_path)

        logs_time_path = "{0}/{1}".format(log_date_path, curtime)
        if not os.path.exists(logs_time_path):
            try:
                os.mkdir(logs_time_path)
            except OSError:
                logs_time_path += "_" + str(random.randint(100, 900))
                os.mkdir(logs_time_path)

        if have_items:
            self.items_dir = "{0}/items".format(logs_time_path)
            if not os.path.exists(self.items_dir):
                os.mkdir(self.items_dir)
            else:
                self.log("!!! Concurrency bug, logs/items content may be shuffled with other ws process !!!")

        self.logs_dir = "{0}/{1}/{2}".format(logs_dir, curdate, curtime)

        self.log_fh = open("{0}/run.log".format(self.logs_dir), "w")

    def log(self, _str, new_str=True, _print=True):
        """ Write string in log and print it if need """
        self.log_fh.write(
            (t("[%H:%M:%S] ") if new_str else '') + str(_str) + ('\n' if new_str else '')
        )
        self.log_fh.flush()
        if _print:
            if new_str:
                print _str
            else:
                print _str,
        sys.stdout.flush()

    def item(self, name, content, binary=False, positive=False):
        """ Write item and it content in file """

        if not positive or not len(name):
            return

        name = name[1:] if name[0] == '/' else name
        name = name.replace(" ", "_")
        name = re.sub(r"[^a-zA-Z0-9_\-\.\|]", "_", name)

        ext = "bin" if binary else "txt"

        fh = codecs.open("{0}/{1}.{2}".format(self.items_dir, name, ext), 'ab', 'utf-8')

        if binary:
            try:
                fh.write(content)
            except UnicodeDecodeError:
                fh.write("BINARY ENCODING ERROR")
        else:
            decoded_content = ""
            for symbol in content:
                try:
                    symbol = codecs.encode(symbol, 'utf8', 'ignore')
                except UnicodeDecodeError:
                    symbol = '?'
                decoded_content += symbol.decode('utf8', 'ignore')
            fh.write(decoded_content)
        fh.close()

    def ex(self, _exception):
        """ Log func for exceptions """
        exc_type, exc_obj, exc_tb = sys.exc_info()
        tb_text = "\n"
        tb_text += "{0:=^20}\n".format("")
        tb_text += "Exception: " + str(exc_obj) + "\n"
        for tb_line in traceback.extract_tb(exc_tb):
            tb_file, tb_strnum, tb_where, tb_call = tb_line
            log_str = "{0}:{1} in '{2}' => {3}\n".format(tb_file, tb_strnum, tb_where, tb_call)
            tb_text += log_str
        tb_text += "{0:=^20}".format("")

        self.log(tb_text, _print=True)

        if Registry().isset('xml'):
            Registry().get('xml').put_error(str(_exception), tb_text)

    def stop(self):
        """ Stop logger """
        if not self.log_fh.closed:
            self.log_fh.close()