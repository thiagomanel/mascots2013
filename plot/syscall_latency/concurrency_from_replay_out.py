import sys
sys.path.append("../concurrency/")
from concurrency import *

def concurrency_format(replay_probes):
    events = []
    count = 0
    for probe in replay_probes:
        latency, stamp = probe[1], probe[4]
        events.append((count, "begin", long(stamp)))
        events.append((count, "end", long(stamp) + long(latency)))
        count = count + 1

    return sorted(events, key=lambda x: x[2])

if __name__ == "__main__":
    """
        It defines concurrency level for a joined replay output file.

        Input format:
            operation_type latency actual_rvalue tid stamp order timing sample id
            p.s (header content may change) but we expect from order to end we
            see experimental config tags

        Output format:
            the same from input but two columns: "concurrency", "cgroup"
    """

    header = sys.stdin.readline()
    print "\t".join(header.split() + ["concurrency", "cgroup"])

    configs = {}
    for line in sys.stdin:
        probe = line.split()
        cfg = tuple(probe[5:-1])#from 5 to end is the experimental configuration values
        if not cfg in configs:
            configs[cfg] = []
        configs[cfg].append(probe)

    for (cfg, probes) in configs.iteritems():
        c_events = concurrency_format(probes)
        c_level, cgroup = concurrency(c_events)
        for i in range(len(probes)):
            group = cgroup[i]
            group_str = [str(sibling) for sibling in group]
            print "\t".join(probes[i] + [str(c_level[i])] + ["#".join(group_str)])
