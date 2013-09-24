import sys
import json
sys.path.append("/local2/thiagoepdc/cppworkspace/TheBeefsReplayer/data/")
from workflow import *

if __name__ == "__main__":
    """
       It defines the number of requests made by each alive process
       Usage: python $0 < filepath > out
    """
    sys.stdin.readline()#exclude header
    counter_by_process = {}
    for line in sys.stdin:
        _json = json.loads(line)
        try:
            wline = WorkflowLine.from_json(_json)
            clean_call = wline.clean_call
            process_id = "#".join([clean_call.pid, clean_call.tid,\
                                    clean_call.pname])
            if not process_id in counter_by_process:
                counter_by_process[process_id] = 0
            counter_by_process[process_id] = counter_by_process[process_id] + 1
        except:
            sys.stderr.write(" ".join(["Bad line", line]) + "\n")
            continue

    for (process, count) in counter_by_process.iteritems():
        print "\t".join([process.strip(), str(count)])
