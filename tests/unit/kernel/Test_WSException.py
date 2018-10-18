# -*- coding: utf-8 -*-

from classes.kernel.WSException import WSException


class Test_WSException(object):
    def test_str(self):
        ex = WSException("test")
        assert "ERROR: test" == str(ex)