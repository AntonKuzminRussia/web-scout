from classes.Roller import Roller

import mock


class Test_Roller(object):
    def test_load_file(self):
        with mock.patch("classes.Roller.file_to_list") as ftl_mock:
            ftl_mock.return_value = ['a', 'b', '']
            roller = Roller()
            roller.load_file("/tmp/1.txt")
            assert ['a', 'b'] == roller.data

    def test_get(self):
        roller = Roller()
        roller.data = ['a', 'b']
        assert 'a' == roller.get()
        assert 'b' == roller.get()
        assert 'a' == roller.get()
