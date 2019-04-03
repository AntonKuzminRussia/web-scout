# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of xml ouput functional
"""

import xml.etree.cElementTree as eTree
import time


class XmlOutput:
    report_name = None

    errors_root = None
    errors_doc = None

    results_root = None
    results_doc = None

    errors_counter = 0
    errors_limit = 100

    def flush_result(self):
        eTree.ElementTree(self.results_root).write(self.report_name + "-result.xml")

    def flush_errors(self):
        eTree.ElementTree(self.errors_root).write(self.report_name + "-errors.xml")

    def __init__(self, report_name):
        self.report_name = report_name

        self.errors_root = eTree.Element("root")
        self.errors_doc = eTree.SubElement(self.errors_root, "errors")
        self.flush_errors()

        self.results_root = eTree.Element("root")
        self.results_doc = eTree.SubElement(self.results_root, "results")
        self.flush_result()

    def put_progress(self, count_now, full_count, percent_done, time_now, time_left, speed):
        progress_root = eTree.Element("root")
        progress_doc = eTree.SubElement(progress_root, "progress")

        eTree.SubElement(progress_doc, "count_now").text = str(count_now)
        eTree.SubElement(progress_doc, "full_count").text = str(full_count)
        eTree.SubElement(progress_doc, "percent_done").text = str(percent_done)
        eTree.SubElement(progress_doc, "time_now").text = str(time_now)
        eTree.SubElement(progress_doc, "time_left").text = str(time_left)
        eTree.SubElement(progress_doc, "speed").text = str(speed)

        eTree.ElementTree(progress_root).write(self.report_name + "-progress.xml")

    def put_result(self, data):
        for field in data.keys():
            data[field] = str(data[field])
        item = eTree.SubElement(self.results_doc, "item")
        for field in data.keys():
            eTree.SubElement(item, field).text = data[field]
        self.flush_result()

    def put_error(self, error_text, trace_str):
        # This decision using because counting&loggins errors
        # e1  - 1, e2 - 2, e3 - 3
        # has realization (same errors has text with small differences)  and
        # concurrency trouble with big errors count
        if self.errors_counter > self.errors_limit:
            return

        item = eTree.SubElement(self.errors_doc, "error")
        eTree.SubElement(item, "text").text = error_text
        eTree.SubElement(item, "trace").text = trace_str
        eTree.SubElement(item, "timestamp").text = str(int(time.time()))

        self.flush_errors()

        self.errors_counter += 1
