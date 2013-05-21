"""
Add _week_start_at field to all documents in all collections
"""
from backdrop.core.bucket import utc
from backdrop.core.records import Record
from backdrop.core.validation import key_is_internal, key_is_reserved
import logging

log = logging.getLogger(__name__)


def up(db):
    for name in db.collection_names():
        log.info("Migrating collection: {0}".format(name))
        collection = db[name]
        query = {
            "_timestamp": {"$exists": True},
            "_month_start_at": {"$exists": False}
        }
        for document in collection.find(query):
            document['_timestamp'] = utc(document['_timestamp'])

            for key in document.keys():
                if key_is_internal(key) and not key_is_reserved(key):
                    document.pop(key)

            record = Record(document)

            collection.save(record.to_mongo())
