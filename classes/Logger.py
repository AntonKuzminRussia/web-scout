# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class for logging WS output
"""

import Queue
import sys
import os
import traceback
import random
import time

from libs.common import t, md5
from classes.Registry import Registry
from classes.kernel.WSException import WSException
from bson import Binary
from classes.logger.MongoInserterThread import MongoLoggerThread


class Logger(object):
    """ Class for logging WS output """
    logs_dir = None
    module_name = None
    log_fh = None
    items_dir = None
    scan_name = None
    scan_hash = None
    mdb = None
    mongo_inserter = None
    mongo_inserter_queue = None

    def __init__(self, module_name):
        self.mdb = Registry().get('mongo')

        self.mongo_inserter_queue = Queue.Queue()
        self.mongo_inserter = MongoLoggerThread(self.mongo_inserter_queue)
        self.mongo_inserter.start()

        self.module_name = module_name
        logs_dir = "{0}/logs/{1}".format(Registry().get('wr_path'), module_name)
        curdate = t("%Y-%m-%d")
        curtime = t("%H_%M_%S")

        if not os.path.exists(logs_dir):
            raise WSException("LOGGER ERROR: Path {0} for module {1} not exists!".format(logs_dir, module_name))

        if not os.path.exists("{0}/{1}".format(logs_dir, curdate)):
            os.mkdir("{0}/{1}".format(logs_dir, curdate))

        if not os.path.exists("{0}/{1}/{2}".format(logs_dir, curdate, curtime)):
            os.mkdir("{0}/{1}/{2}".format(logs_dir, curdate, curtime))

        self.logs_dir = "{0}/{1}/{2}".format(logs_dir, curdate, curtime)

        self.log_fh = open("{0}/run.log".format(self.logs_dir), "w")

    def set_scan_name(self, scan_name):
        self.scan_name = scan_name

        need_create_indexes = 'scans' not in self.mdb.collection_names()
        coll = self.mdb.scans

        curdate = t("%Y-%m-%d")
        curtime = t("%H_%M_%S")
        self.scan_hash = md5("{0}|{1}|{2}|{3}|{4}".format(self.module_name, self.scan_name, curdate, curtime, random.randint(0, 9999999)))
        scan_data = {
            'module': self.module_name,
            'name': scan_name,
            'date': t("%Y-%m-%d"),
            'time': t("%H:%M:%S"),
            'hash': self.scan_hash
        }
        coll.insert(scan_data)

        if need_create_indexes:
            coll.create_index([('hash', 1)], unique=True)
            coll.create_index([('module', 1), ('name', 1)])


    def log(self, _str, new_str=True, _print=True):
        """ Write string in log and print it if need """
        self.log_fh.write(
            (t("[%H:%M:%S] ") if new_str else '') + _str + ('\n' if new_str else '')
        )
        self.log_fh.flush()
        if _print:
            if new_str:
                print _str
            else:
                print _str,
        sys.stdout.flush()

    def item(self, name, content, binary=False, positive=False):
        """ Write item and it content in txt-file """
        if self.scan_name is None:
            raise WSException("Scan name must be specified before logging")

        item_data = {
            'name': name,
            'len': len(content),
            'binary': binary,
            'content': Binary(content),
            'positive': positive,
            'scan_hash': self.scan_hash,
            'hash': md5(content)
        }

        self.mongo_inserter_queue.put(item_data)

    def ex(self, _exception):
        """ Log func for exceptions """
        exc_type, exc_obj, exc_tb = sys.exc_info()
        tb_text = ""
        tb_text += "{0:=^20}".format("")
        for tb_line in traceback.extract_tb(exc_tb):
            tb_file, tb_strnum, tb_where, tb_call = tb_line
            log_str = "{0}:{1} in '{2}' => {3}\n".format(tb_file, tb_strnum, tb_where, tb_call)
            tb_text += log_str
        tb_text += "{0:=^20}".format("")

        self.log(log_str, _print=True)

        if Registry().isset('xml'):
            Registry().get('xml').put_error(str(_exception), tb_text)

    def stop(self):
        self.mongo_inserter.working = False
        while self.mongo_inserter.isAlive():
            time.sleep(0.1)