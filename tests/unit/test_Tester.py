from classes.Tester import Tester
from classes.Registry import Registry


class Test_Tester(object):
    def setup(self):
        Registry().set('config', {'test': {'display_items_content': True, 'requests_count': 3}})

    def test_init(self):
        tester = Tester()
        assert tester.display_items_content
        assert 3 == tester.requests_count

    def test_done(self):
        tester = Tester()
        assert not tester.done()
        tester.items = {'a': 'b', 'c': 'd', 'e': 'f'}
        assert tester.done()

    def test_put(self):
        tester = Tester()
        tester.put("a", 1)
        tester.put("b", 2)
        tester.put("c", 3)
        tester.put("d", 4)
        assert 3 == len(tester.items)

    def test_put_duplicate(self):
        tester = Tester()
        tester.put("a", {'b': 'c'})
        tester.put("a", {'b': 'd'})
        assert 1 == len(tester.items)
        assert tester.items['a']['b'] == 'd'