from itertools import groupby
from bson import Code
from pprint import pprint


def build_query(**params):
    query = {}
    if 'start_at' in params:
        query['_timestamp'] = {
            '$gte': params['start_at']
        }
    if 'end_at' in params:
        if '_timestamp' not in query:
            query['_timestamp'] = {}
        query['_timestamp']['$lt'] = params['end_at']

    if 'filter_by' in params:
        for key, value in params['filter_by']:
            query[key] = value
    return query


class Repository(object):
    def __init__(self, collection):
        self._collection = collection

    def find(self, query):
        return self._collection.find(query).sort('_timestamp', -1)

    def group(self, group_by, query):
        return self._collection.group(
            key=[group_by],
            condition=query,
            initial={'count': 0},
            reduce=Code("""
                function(current, previous) { previous.count++; }
                """)
        )

    def save(self, obj):
        self._collection.save(obj)

    def multi_group(self, key1, key2, query):
        results = self._collection.group(
            key=[key1, key2],
            condition=query,
            initial={'count': 0},
            reduce=Code("""
                function(current, previous) { previous.count++; }
                """)
        )

        for result in results:
            if result[key1] is None or result[key2] is None:
                return []

        output = {}
        for result in results:
            output = self._recursive_merge(output, [key1, key2], result)

        result = []
        for key1_value, value in sorted(output.items()):
            result.append({
                key1: key1_value,
                "count": len(value),
                key2: value
            })

        return result

    def _recursive_merge(self, output, keys, value):
        if len(keys) == 0:
            return value
        key = value.pop(keys[0])
        if key not in output:
            output[key] = {}
        output[key].update(self._recursive_merge(output[key], keys[1:], value))

        return output
