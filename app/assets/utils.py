import json
import collections


def find_nested_json(obj, keys):
    """
    Finds a nested value in an object, given a list of keys.  If
    any object is an array within the nested object, returns an
    array of the resulting call.

    @param obj: json
    @param keys: list of string
    @return: object
    """
    enqueued = collections.deque([(obj, keys)])
    results = []

    while len(enqueued) > 0:
        obj, keys = enqueued.popleft()
        keys_queue = collections.deque(keys)
        # Iterate over the list of keys
        while len(keys_queue) > 0:
            key = keys_queue.popleft()
            # Check if key is in the object
            if not key in obj:
                return None

            # Key is in the object, if found a list, enqueue
            # the list, otherwise enqueue the single item
            obj = obj[key]
            keys.pop(0)

            if type(obj) == list:
                enqueued.extend((o, keys[:]) for o in obj)
                keys_queue.clear()

            elif len(keys_queue) == 0:
                results.append(obj)

    if len(results) == 0:
        return None

    return results
