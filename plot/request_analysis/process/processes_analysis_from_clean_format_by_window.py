import sys
import json
sys.path.append("/local2/thiagoepdc/cppworkspace/TheBeefsReplayer/data/")
from clean_trace import *
from processes_analysis_from_clean_format import *

def dump(stamp, result):
    total_req = sum(result.values())
    for (process_str, count) in result.iteritems():
        print "\t".join([str(stamp), str(len(result)), str(total_req),\
                         process_str, str(count)])

if __name__ == "__main__":
    """
       It defines the number of requests made by each alive process from the
       trace replay clean format splited by a timestamp window

       Usage: python $0 < filepath window_us > out
    """
    window = long(sys.argv[1])
    result = {}
    last_window = None
    for line in sys.stdin:
        clean_call = CleanCall.from_str(line.strip())
        stamp_begin, _ = clean_call.stamp()
        if not last_window:
            last_window = stamp_begin
        if (last_window + window) < stamp_begin:
            dump(last_window, result)
            result = {}
            last_window = stamp_begin

        count(result, line)
