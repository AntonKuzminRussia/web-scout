# -*- coding: utf-8 -*-
"""
This is part of WebScout software
Docs EN: http://hack4sec.pro/wiki/index.php/WebScout_en
Docs RU: http://hack4sec.pro/wiki/index.php/WebScout
License: MIT
Copyright (c) Anton Kuzmin <http://anton-kuzmin.ru> (ru) <http://anton-kuzmin.pro> (en)

Class of selenium browser - main object for selenium work
"""

import time

from selenium import webdriver


class SeleniumBrowser(webdriver.Firefox):
    """ Class of selenium browser - main object for selenium work """
    re_phrases = [
        'ENTITY connectionFailure.longDesc',
    ]
    profile_path = None

    def __init__(self, profile, firefox_binary, browser_wait_re, proxy=None):
        super(SeleniumBrowser, self).__init__(profile, firefox_binary=firefox_binary, proxy=proxy)
        self.browser_wait_re = browser_wait_re
        self.profile_path = profile.path

    def get(self, url, from_blank=True):
        """ Get a url, but with check on recreate browser need and browser wait need """
        if from_blank:
            super(SeleniumBrowser, self).get("about:blank")
        super(SeleniumBrowser, self).get(url)

        for re_phrase in self.re_phrases:
            if self.page_source.count(re_phrase):
                time.sleep(5)
                return self.get(url)

        if self.browser_wait_re:
            while self.browser_wait_re.findall(self.page_source):
                time.sleep(1)

    def element_exists(self, by, _id):
        """ Method check is element geted by selector exists """
        try:
            self.find_element(by, _id)
        except BaseException:
            return False
        return True

