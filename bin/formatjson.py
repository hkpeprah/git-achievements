#!/usr/bin/env python
if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        print "Usage: {0} input-file [output-file]".format(sys.argv[0])

    data = None
    with open(sys.argv[1], 'r') as inputfile:
        data = inputfile.readlines()

    data = json.loads("\n".join(data))
    data = json.dumps(data, separators=(',', ': '), indent=4)
    if len(sys.argv) == 2:
        print data
    else:
        with open(sys.argv[2], 'w') as output:
            output.write(data)
