import threading

from classes.Registry import Registry


class AbstractThread(threading.Thread):
    daemon = True

    last_action = 0
    logger = None
    queue = None
    counter = None
    result = None

    done = False

    retest_delay = None
    retest_limit = None

    def __init__(self):
        threading.Thread.__init__(self)

        self.logger = Registry().get('logger')

        self.retest_limit = int(Registry().get('config')['main']['retest_limit'])
        self.retest_delay = int(Registry().get('config')['main']['retest_delay'])

    def xml_log(self, data):
        if Registry().isset('xml'):
            Registry().get('xml').put_result(data)

    def is_test(self):
        return Registry().isset('tester')

    def is_test_done(self):
        return Registry().get('tester').done()

    def test_put(self, item, data):
        Registry().get('tester').put(item, data)
        if self.is_test_done():
            self.done = True
