# -*- coding: utf-8 -*-

import os

import pytest
import mock

from classes.kernel.WSException import WSException
from classes.logger.Logger import Logger
from classes.Registry import Registry
from libs.common import t, file_get_contents




class Test_Logger(object):
    def test_plug(self):
        assert 1 == 1
