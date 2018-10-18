# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Alexey Meshcheryakov <tank1st99@gmail.com>

Kernel base class. Prepare work, load config, connect db, etc
"""

import sys
import os

import configparser
from pymongo import MongoClient
import pymongo.errors
from pyvirtualdisplay import Display

from libs.common import file_get_contents, md5, random_ua
from classes.Http import Http
from classes.Proxies import Proxies
from classes.kernel.WSKernel import WSKernel
from classes.kernel.WSException import WSException
from classes.Registry import Registry


class WSBase(object):
    """ Kernel base class. Prepare work, load config, connect db, etc """
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.getcwd() + '/' + 'config.ini')

        try:
            mongo_host = config['mongo']['host'] if 'WEBSCOUT_MONGO_HOST' not in os.environ else os.environ['WEBSCOUT_MONGO_HOST']
            mongo_port = config['mongo']['port'] if 'WEBSCOUT_MONGO_PORT' not in os.environ else os.environ['WEBSCOUT_MONGO_PORT']

            mc = MongoClient(host=mongo_host, port=int(mongo_port))
            mongo_collection = getattr(mc, config['mongo']['collection']) #TODO it`s not collection, it`s db

            print("MongoDB: {0}:{1}".format(mongo_host, mongo_port))
        except pymongo.errors.ConnectionFailure as e:
            print " ERROR: Can`t connect to MongoDB server! ({0})".format(str(e))
            exit(0)

        R = Registry()
        R.set('config', config)
        R.set('mongo', mongo_collection)
        R.set('wr_path', os.getcwd())
        R.set('data_path', os.getcwd() + '/data/')
        R.set('http', Http())
        R.set('ua', random_ua())
        R.set('proxies', Proxies())
        R.set(
            'fuzzer_evil_value',
            file_get_contents(Registry().get('wr_path') + "/bases/fuzzer-evil-value.txt").strip()
        )
        R.set('proxy_many_died', False)
        R.set('positive_limit_stop', False)

        if " ".join(sys.argv).count('selenium') and int(config['selenium']['virtual_display']):
            display = Display(visible=0, size=(800, 600))
            display.start()
            R.set('display', display)

        coll = Registry().get('mongo').responses_content
        if coll.count() == 0:
            data = {
                'hash': md5(''),
                'content': '',
            }
            coll.insert(data)

            coll.create_index([('hash', 1)], unique=True)

    def __my_import(self, name):
        """ Load need WS module """
        if not os.path.exists('classes/modules/' + name + '.py'):
            raise WSException

        sys.path.append('classes/modules/')
        mod = __import__(name)
        the_class = getattr(mod, name)
        return the_class

    def load_module(self, modulename):
        """ Public method for load module """
        module = self.__my_import(modulename)
        kernel = WSKernel()
        moduleclass = module(kernel)
        return moduleclass

    def get_modules_list(self):
        """ Return list of available modules """
        return list(map(lambda x: os.path.splitext(x)[0], filter(lambda x: x.endswith('py'), os.listdir('modules/'))))
