import pytest

from classes.Roller import Roller


class Test_Roller(object):
    def build_test_file(self, is_blank=False):
        fh = open("/tmp/1.txt", "w")
        fh.write("123\n456\n789" if not is_blank else "")
        fh.close()

    def test_get(self):
        self.build_test_file()

        roller = Roller("/tmp/1.txt")
        assert '123' == roller.get()
        assert '456' == roller.get()
        assert '789' == roller.get()
        assert '123' == roller.get()

    def test_blank_file_ex(self):
        self.build_test_file(True)
        with pytest.raises(BaseException) as e:
            roller = Roller("/tmp/1.txt")
            roller.get()

        assert "has not lines" in str(e)

    def test_notfound_file_ex(self):
        self.build_test_file(True)
        with pytest.raises(BaseException) as e:
            roller = Roller("/tmp/1eg3g2egwegwewegwegwegwegweg.txt")
            roller.get()

        assert "not found" in str(e)