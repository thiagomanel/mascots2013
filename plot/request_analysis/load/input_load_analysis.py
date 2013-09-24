import sys
import json
sys.path.append("../../../TheBeefsReplayer/data/")
from workflow import *

def timestamp(wline):
    _call = wline.clean_call
    begin, elapsed = _call.stamp()
    return begin

def bin_index(timestamp, first_stamp, bin_width):
    return (timestamp - first_stamp) / bin_width

def bin_begin(bin_index, first_stamp, bin_width):
    return first_stamp + (bin_index * bin_width)

if __name__ == "__main__":
    """
       Usage: python input_load_analysis.py us_bin_width filepath > out
    """
    bin_width = int(sys.argv[1])
    filepath = sys.argv[2]

    bin_counter = {}

    with open(filepath, 'r') as data:
        lines = data.readline()#excluding header
        first_stamp = None

        for line in data:
            _json = json.loads(line)
            try:
                wline = WorkflowLine.from_json(_json)
            except:
                sys.stderr.write(" ".join(["Bad line", line]) + "\n")
                continue

            line_stamp = timestamp(wline)
            if not first_stamp:
                first_stamp = line_stamp
            b_index = bin_index(line_stamp, first_stamp, bin_width)
            b_begin  = bin_begin(b_index, first_stamp, bin_width)

            if not b_begin in bin_counter:
                bin_counter[b_begin] = 0
            bin_counter[b_begin] = bin_counter[b_begin] + 1

    _min = None
    sorted_keys = sorted(bin_counter.keys())
    key = _min = sorted_keys[0]
    last_stamp = sorted_keys[-1] + bin_width
    #so, we add the intervals with 0 events

    while (key <= last_stamp):
        load = 0
        if key in bin_counter:
            load = bin_counter[key]
        print (key - _min), key, load
        key = key + bin_width

