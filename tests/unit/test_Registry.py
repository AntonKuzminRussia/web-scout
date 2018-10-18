import pytest

from classes.Registry import Registry


class Test_Registry(object):
    def setup(self):
        Registry.data = {}
        
    def test_set_and_get(self):
        with pytest.raises(KeyError):
            Registry().get('aaa')
        Registry().set('aaa', 'bbb')
        assert Registry().get('aaa') == 'bbb'

    def test_isset(self):
        assert not Registry().isset("aaa")
        Registry().set('aaa', 'bbb')
        assert Registry().isset("aaa")