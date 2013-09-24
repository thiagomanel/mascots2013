import sys
import os

if __name__ == "__main__":
    """
        It joins issue error data from replay output
        layout: out_dir/order_timing/$sample.$random.issue_error
        Usage: python join_input.py out_dir > output.join
    """
    #we assume out_dir has no files, only directories
    out_dir_path = sys.argv[1]
    probes = {}
    for root, dirs, files in os.walk(out_dir_path):
        if files:
            for _file in files:
                if _file.find("issue_error") >= 0:
                    config = os.path.basename(root).split("-")
                    order, timing = config[0], config[1]
                    sample = _file.split(".")[0]

                    if not (sample, order, timing) in probes:
                        probes[(sample, order, timing)] = []

                    probe_path = os.path.join(root, _file)
                    with open(probe_path) as data:
                        for line in data:
                            r_begin, r_end, sched_stamp, r_delay, issue_error = line.split()
                            probes[(sample, order, timing)]\
                                    .append((r_begin, r_end, sched_stamp, r_delay, issue_error))

    print "\t".join(["sample", "order", "timing",\
                     "min", "interval",\
                     "i",\
                     "r_begin", "r_end", "sched_stamp", "delay", "issue_error",\
                     "ops_interval"])

    for (sample, order, timing), probes in probes.iteritems():
        min_stamp = float("inf")
        for (r_begin, r_end, sched_stamp, r_delay, issue_error) in probes:
            min_stamp = min(min_stamp, long(r_begin))

        events_by_interval = {}
        final_probes = []

        for (r_begin, r_end, sched_stamp, r_delay, issue_error) in probes:
            interval = (long(r_begin) - min_stamp) / 1000000
            final_probes.append((r_begin, r_end, sched_stamp, r_delay,\
                                 issue_error, interval))

            if not interval in events_by_interval:
                events_by_interval[interval] = 0
            events_by_interval[interval] = events_by_interval[interval] + 1

        count = 0
        for (r_begin, r_end, sched_stamp, r_delay, issue_error, interval) in final_probes:
            ops_interval = events_by_interval[interval]
            print "\t".join([sample, order, timing,\
                             str(min_stamp), str(interval),\
                             str(count),\
                             r_begin, r_end, sched_stamp, r_delay, issue_error,\
                             str(ops_interval)])
            count = count + 1
