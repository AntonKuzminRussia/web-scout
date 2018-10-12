from bson import Binary

from classes.Registry import Registry
from libs.common import md5


class WSMongo:
    content_hashes = set()
    inserts = 0

    @staticmethod
    def load_mongo_content_hash(content):
        content_hash = md5(content)
        if content_hash not in WSMongo.content_hashes:
            coll = Registry().get('mongo').responses_content
            if coll.find({'hash': content_hash}).count() == 0:
                data = {
                    'hash': content_hash,
                    'content': Binary(content),
                }
                coll.insert(data)
                WSMongo.inserts += 1 #TODO debug logging here?

            WSMongo.content_hashes.add(content_hash)
        return content_hash
