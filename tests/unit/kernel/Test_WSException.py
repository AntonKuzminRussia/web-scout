# -*- coding: utf-8 -*-
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from classes.kernel.WSException import WSException


class Test_WSException(object):
    def test_str(self):
        ex = WSException("test")
        assert "ERROR: test" == str(ex)