import copy

from libs.common import is_binary_content_type
from classes.Registry import Registry
from classes.threads.AbstractThread import AbstractThread
from libs.common import get_response_size


class HttpThread(AbstractThread):
    http = None

    def test_log(self, url, resp, positive_item):
        if self.is_test():
            self.test_put(
                url,
                {
                    'code': resp.status_code if resp is not None else 0,
                    'positive': positive_item,
                    'size': get_response_size(resp) if resp is not None else 0,
                    'content': resp.content if resp is not None else '',
                }
            )

    def __init__(self):
        AbstractThread.__init__(self)
        self.http = copy.deepcopy(Registry().get('http'))

    def is_response_content_binary(self, resp):
        return resp is not None \
            and 'content-type' in resp.headers \
            and is_binary_content_type(resp.headers['content-type'])

    def get_headers_text(self, resp):
        response_headers_text = ''
        for header in resp.headers:
            response_headers_text += '{0}: {1}\r\n'.format(header, resp.headers[header])
        return response_headers_text

    def is_response_right(self, resp):
        if resp is None:
            return False

        if self.not_found_size != -1 and self.not_found_size == len(resp.content):
            return False

        if self.not_found_re and not self.is_response_content_binary(resp) and (
                    self.not_found_re.findall(resp.content) or
                    self.not_found_re.findall(self.get_headers_text(resp))):
            return False

        if str(resp.status_code) in self.not_found_codes:
            return False

        return True

    def log_item(self, item_str, resp, is_positive):
        if isinstance(resp, basestring):
            log_content = resp
        else:
            log_content = resp.content if not resp is None else ""

        Registry().get('logger').item(
            item_str,
            log_content,
            self.is_response_content_binary(resp) if not isinstance(resp, basestring) else False,
            positive=is_positive
        )

    def check_positive_limit_stop(self, result, rate=1):
        if len(result) >= (int(Registry().get('config')['main']['positive_limit_stop']) * rate):
            Registry().set('positive_limit_stop', True)

    def is_retest_need(self, word, resp):
        try:
            if resp is not None:
                if (len(self.retest_codes) and str(resp.status_code) in self.retest_codes) or \
                        (self.retest_phrase and len(self.retest_phrase) and self.retest_phrase in resp.content):
                    if word not in self.retested_words.keys():
                        self.retested_words[word] = 0
                    self.retested_words[word] += 1

                    return self.retested_words[word] <= self.retest_limit
        except BaseException as e:
            print(e)
        return False