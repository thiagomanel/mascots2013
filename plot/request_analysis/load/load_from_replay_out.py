import sys
from output_load import *

def load_format(replay_probes):
    events = []
    count = 0
    for probe in replay_probes:
        latency, stamp = probe[1], probe[4]
        events.append( (long(stamp), long(stamp) + long(latency)) )
    return sorted(events, key=lambda x: x[0])

if __name__ == "__main__":
    """
        It defines replay load for a joined replay output file.

        Input format:
            operation_type latency actual_rvalue tid stamp order timing sample id
            p.s (header content may change) but we expect from order to end we
            see experimental config tags

        Output format:
            order timing sample (id) relative_stamp stamp load load_type
    """
    header = sys.stdin.readline().split()[5:8]
    print "\t".join(header + ["relative_stamp", "stamp", "load", "load_type"])

    configs = {}
    for line in sys.stdin:
        probe = line.split()
        cfg = tuple(probe[5:8])
        if not cfg in configs:
            configs[cfg] = []
        configs[cfg].append(probe)

    for (cfg, probes) in configs.iteritems():
        events = load_format(probes)

        sys.stderr.write(str(cfg) + "\n")

        dispatch = dispatch_load(events)
        for data in dispatch:
            data_str = map(str, data)
            print "\t".join([str(token) for token in cfg] + data_str + ["dispatch"])
