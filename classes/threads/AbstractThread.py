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

    def __init__(self):
        threading.Thread.__init__(self)

        self.logger = Registry().get('logger')
