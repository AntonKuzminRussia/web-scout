# -*- coding: utf-8 -*-
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from classes.kernel.WSOption import WSOption


class Test_WSOption(object):
    def test_init(self):
        option = WSOption("name", "description", "value", "required", "flags", "module")

        assert "name" == option.name
        assert "description" == option.description
        assert "value" == option.value
        assert "required" == option.required
        assert "flags" == option.flags
        assert "module" == option.module