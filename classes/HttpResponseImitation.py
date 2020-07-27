import codecs


class HttpResponseImitation:
    headers = None
    content = None
    text = None
    status_code = None

    def __init__(self, status_code, headers, content):
        self.status_code = status_code
        self.headers = headers
        self.content = content
        self.text = codecs.decode(content, 'utf-8', 'ignore')

    def close(self):
        pass
