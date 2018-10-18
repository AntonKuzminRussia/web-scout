# -*- coding: utf-8 -*-

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