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

        R = Registry()
        R.set('config', config)
        R.set('wr_path', os.getcwd())
        R.set('data_path', os.getcwd() + '/data/')
        R.set('http', Http())
        R.set('ua', random_ua())
        R.set('proxies', Proxies())
        R.set('tmp_files', [])
        R.set(
            'fuzzer_evil_value',
            file_get_contents(Registry().get('wr_path') + "/bases/fuzzer/evil-value.txt").strip()
        )
        R.set('proxy_many_died', False)
        R.set('positive_limit_stop', False)

        if " ".join(sys.argv).count('selenium') and int(config['selenium']['virtual_display']):
            display = Display(visible=0, size=(800, 600))
            display.start()
            R.set('display', display)

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
