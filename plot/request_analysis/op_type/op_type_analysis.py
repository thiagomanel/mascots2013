import sys
import json
sys.path.append("../../../TheBeefsReplayer/data/")
from workflow import *

if __name__ == "__main__":
    """
       It extracts the type of the request in a workload input file
       Usage: python $0 < filepath > out
    """
    sys.stdin.readline()#exclude header
    for line in sys.stdin:
        _json = json.loads(line)
        try:
            wline = WorkflowLine.from_json(_json)
            call_type = wline.clean_call.call
            print call_type.strip()
        except:
            sys.stderr.write(" ".join(["Bad line", line]) + "\n")
            continue
