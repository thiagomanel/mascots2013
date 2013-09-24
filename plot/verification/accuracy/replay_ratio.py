import sys
import json

# hardwired for now
con_input = "new.conservative.timing_exp.2011_10_21-abelhinha.clean.cut.order"
fs_input = "new.wfs.timing_exp.2011_10_21-abelhinha.clean.cut.order"

def load(path):
    json_requests = []
    with open(path) as data:
        data.readline()#exclude header
        for line in data:
            json_requests.append(json.loads(line))
    return json_requests

def order(json_requests):
    _order = {}
    for request in json_requests:
        _order[request["id"]] = request["parents"]
    return _order

if __name__ == "__main__":
    """
        Find the issue_error/(request_delay) ratio
        Usage: python $0 < issue_error_data
    """
    con_order = order(load(con_input))
    fs_order = order(load(fs_input))

    sys.stdout.write("\t".join(["sample", "order", "timing", "min", "interval",\
                                "i", "r_begin", "r_end", "sched_stamp",\
                                "delay", "issue_error", "ops_interval",\
                                "parent_end", "replay_ratio\n"]))
    sys.stdin.readline()#header

    request_stamps = {}
    for line in sys.stdin:
        sample, _order, timing, _min, interval, i, r_begin, r_end, sched_stamp,\
            delay, issue_error, ops_interval = line.split()

        config = (sample, _order, timing, i)
        request_stamps[config] = (r_begin , r_end)

        parents = None
        if _order == "fs":
            if not i == "0":#issue error include the root element
                parents = fs_order[int(i)]
        elif _order == "con":
            if not i == "0":
                parents = con_order[int(i)]
        else:
            stderr.write("We accept <fs> or <con> ordering\n")
            sys.exit(1)

        parent_end = -1
        ratio = -1
        if parents:
            parent_id = parents[0]
            parent_begin, parent_end = request_stamps[(sample, _order, timing,\
                                                       str(parent_id))]
            replay_delay = long(r_begin) - long(parent_end)
            ratio = (float(issue_error)/replay_delay)

        print "\t".join([sample, _order, timing, _min, interval, i, r_begin, r_end,\
                        sched_stamp, delay, issue_error, ops_interval,\
                        str(parent_end), str(ratio)])

