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

class XmlOutput:
    report_name = None

    progress_root = None
    progress_doc = None

    errors_root = None
    errors_doc = None

    results_root = None
    results_doc = None

    def __init__(self, report_name):
        self.report_name = report_name

        self.progress_root = eTree.Element("root")
        self.progress_doc = eTree.SubElement(self.progress_root, "progress")

        self.errors_root = eTree.Element("root")
        self.errors_doc = eTree.SubElement(self.errors_root, "errors")

        self.results_root = eTree.Element("root")
        self.results_doc = eTree.SubElement(self.results_root, "results")

    def put_progress(self, count_now, full_count, percent_done, time_now, time_left, speed):
        eTree.SubElement(self.progress_doc, "count_now").text = str(count_now)
        eTree.SubElement(self.progress_doc, "full_count").text = str(full_count)
        eTree.SubElement(self.progress_doc, "percent_done").text = str(percent_done)
        eTree.SubElement(self.progress_doc, "time_now").text = str(time_now)
        eTree.SubElement(self.progress_doc, "time_left").text = str(time_left)
        eTree.SubElement(self.progress_doc, "speed").text = str(speed)

        eTree.ElementTree(self.progress_root).write(self.report_name + "-progress.xml")

    def put_result(self, data):
        item = eTree.SubElement(self.results_doc, "item")
        for field in data.keys():
            eTree.SubElement(item, field).text = data[field]
        eTree.ElementTree(self.results_root).write(self.report_name + "-result.xml")

    def put_error(self, error_text, trace_str):
        item = eTree.SubElement(self.errors_doc, "error")
        eTree.SubElement(item, "text").text = error_text
        eTree.SubElement(item, "trace").text = trace_str

        eTree.ElementTree(self.errors_root).write(self.report_name + "-errors.xml")