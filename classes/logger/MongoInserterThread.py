import threading
import time
import Queue

from classes.Registry import Registry


class MongoLoggerThread(threading.Thread):
    """

    :type pool: list
    :type queue: Queue.Queue
    """
    daemon = True

    mdb = None
    queue = None
    pool = None
    pool_count_limit = None
    working = True
    sleep_time_per_step = 1

    def __init__(self, queue):
        threading.Thread.__init__(self)

        self.pool = []
        self.mdb = Registry().get('mongo')
        self.queue = queue
        self.pool_count_limit = int(Registry().get('config')['main']['mongo_logger_items_pool_count_limit'])

    def insert_pool(self):
        need_create_indexes = 'items' not in self.mdb.collection_names()
        coll = self.mdb.items

        coll.insert_many(self.pool)

        if need_create_indexes:
            coll.create_index([('scan_hash', 1), ('positive', 1)])
            coll.create_index([('hash', 1)])

        self.pool = []

    def run(self):
        while self.working or self.queue.qsize():
            try:
                item = self.queue.get(False)

                self.pool.append(item)

                if len(self.pool) > self.pool_count_limit:
                    self.insert_pool()
            except Queue.Empty:
                time.sleep(self.sleep_time_per_step)

        if len(self.pool):
            self.insert_pool()
