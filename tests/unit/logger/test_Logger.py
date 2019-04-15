# -*- coding: utf-8 -*-

import os

import pytest
import shutil

from classes.logger.Logger import Logger
from classes.Registry import Registry


class Test_Logger(object):
    logger = None

    def setup(self):
        test_tmp_dir = '/tmp/wsunittestdir/'
        if os.path.exists(test_tmp_dir):
            shutil.rmtree(test_tmp_dir)
        os.mkdir(test_tmp_dir)
        os.mkdir(test_tmp_dir + "/logs")
        os.mkdir(test_tmp_dir + "/dafs")

        Registry().set('wr_path', test_tmp_dir)
        self.logger = Logger('dafs', True)

        assert self.logger.logs_dir is not None

    def test_init_with_items(self):
        assert self.logger.items_dir is not None
        assert os.path.exists(self.logger.items_dir)

    def test_init_without_items(self):
        self.logger = Logger('dafs', False)
        assert self.logger.items_dir is None

    log_provider = [
        (True),
        (False),
    ]
    @pytest.mark.parametrize("newstr", log_provider)
    def test_log(self, newstr):
        self.logger.log("test", newstr, False)
        self.logger.stop()

        if newstr:
            assert "test\n" in open(self.logger.logs_dir + "/run.log").read()
        else:
            assert "test\n" not in open(self.logger.logs_dir + "/run.log").read()
            assert "test" in open(self.logger.logs_dir + "/run.log").read()

    item_provider = [
        (True, True),
        (False, True),
        (False, False),
    ]
    @pytest.mark.parametrize("binary,positive", item_provider)
    def test_item(self, binary, positive):
        self.logger.item("test", "blah", binary, positive)
        item_filename = "test.bin" if binary else "test.txt"
        if positive:
            assert os.path.exists(self.logger.items_dir + "/" + item_filename)
            assert "blah" == open(self.logger.items_dir + "/" + item_filename).read()
        else:
            assert not os.path.exists(self.logger.items_dir + "/" + item_filename)

    def test_ex(self):
        try:
            raise BaseException("test")
        except BaseException as e:
            pass

        self.logger.ex(e)

        ex_content = open(self.logger.logs_dir + "/run.log").read()
        assert "test_Logger.py" in ex_content
        assert "raise BaseException" in ex_content

    def teardown(self):
        self.logger.stop()
