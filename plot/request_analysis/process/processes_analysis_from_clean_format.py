import sys
import json
sys.path.append("/local2/thiagoepdc/cppworkspace/TheBeefsReplayer/data/")
from workflow import *
from clean_trace import *

def count(result, line):
    clean_call = CleanCall.from_str(line.strip())
    process_id = "!".join([clean_call.pid, clean_call.tid,\
                            clean_call.pname])

    if not process_id in result:
        result[process_id] = 0
    result[process_id] = result[process_id] + 1

if __name__ == "__main__":
    """
       It defines the number of requests made by each alive process from the
       trace replay clean format.

       e.g
       <uid=0\> <pid=1102\> <tid=18247\> <pname=(automount)\> <call=open\> <stamp=1318613016175808-19\> <arg=/home\> <arg=624640\> <arg=-1217757196\> <rvalue=18\>
       <uid=0\> <pid=1102\> <tid=18247\> <pname=(automount)\> <call=close\>
       Usage: python $0 < filepath > out
    """
    counter_by_process = {}
    for line in sys.stdin:
        count(counter_by_process, line)

    for (process, count) in counter_by_process.iteritems():
        print "\t".join([process.strip(), str(count)])
