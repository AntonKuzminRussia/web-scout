import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from classes.XmlOutput import XmlOutput
from libs.common import file_get_contents


class Test_XmlOutput(object):
    def test_build(self):
        report_path = "/tmp/testreportxml"
        xmloutput = XmlOutput(report_path)

        test_data_progress = ["testprogress1", "testprogress2", "testprogress3", "testprogress4", "testprogress5", "testprogress5"]
        xmloutput.put_progress(test_data_progress[0], test_data_progress[1], test_data_progress[2], test_data_progress[3], test_data_progress[4], test_data_progress[5])
        for test_data in test_data_progress:
            assert test_data in file_get_contents(report_path + "-progress.xml")

        test_data_result = ["testprogress6", "testprogress7"]
        xmloutput.put_result({test_data_result[0]: test_data_result[1]})
        for test_data in test_data_result:
            assert test_data in file_get_contents(report_path + "-result.xml")

        test_data_error = ["testprogress8", "testprogress8"]
        xmloutput.put_error(test_data_error[0], test_data_error[1])
        for test_data in test_data_error:
            assert test_data in file_get_contents(report_path + "-errors.xml")



