import json


def pretty_print(data):
    """
    Pretty prints out a json object.

    @param data: json
    @return: None
    """
    print json.dumps(data, sort_keys=True,
                     indent=4, separators=(',', ': '))
