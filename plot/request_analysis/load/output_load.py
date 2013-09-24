import sys

def bin_offset(timestamp, first_stamp, bin_width):
    def bin_index():
        return (timestamp - first_stamp) / bin_width

    return first_stamp + (bin_index() * bin_width)

def emit_count(counter, offset):
    if not offset in counter:
        counter[offset] = 0
    counter[offset] = counter[offset] + 1

def running_load(replay):
    count = running_count(replay, 1000000)
    _min = -1

    result = []
    for key in sorted(count.keys()):
        if (_min == -1):
            _min = key
        result.append(((key - _min), key, count[key]))
    return result

def running_count(replay, time_window):
    #counter functions return a {time_stamp:event_count} dict of the
    #number of running and dispatch operations by timestamp
    replay_begin = replay[0][0]
    bin_counter = {}

    for replay_event in replay:
        dispatch_begin = replay_event[0]
        dispatch_end = replay_event[1]

        start_offset = bin_offset(dispatch_begin, replay_begin, time_window)
        end_offset = bin_offset(dispatch_end, replay_begin, time_window)

        for offset in range(start_offset, end_offset + 1):
            emit_count(bin_counter, offset)

    return bin_counter

def dispatch_load(replay):
    """
        from a (begin, end) sequence
        returns a (relative_stamp, stamp, load) sequence
    """
    count = dispatch_count(replay, 1000000)
    _min = -1

    result = []
    for key in sorted(count.keys()):
        if (_min == -1):
            _min = key
        result.append(((key - _min), key, count[key]))
    return result

def dispatch_count(replay, time_window):
    replay_begin = replay[0][0]
    bin_counter = {}

    for replay_event in replay:
        dispatch_begin = replay_event[0]
        offset = bin_offset(dispatch_begin, replay_begin, time_window)
        emit_count(bin_counter, offset)
    return bin_counter

if __name__ == "__main__":
    """
       It analyses replay output load
       Input format:
           op_begin op_end
       Usage: python output_load_analysis.py < replay_out > analysis.out
    """
    replay_out = []
    for line in sys.stdin:
        begin, end = line.split()
        replay_out.append((long(begin), long(end)))

    load = dispatch_load(replay_out)
    for l in load:
        relat_stamp, stamp, load = l
        print relat_stamp, stamp, load, "dispatch"

    load = running_load(replay_out)
    for l in load:
        relat_stamp, stamp, load = l
        print relat_stamp, stamp, load, "running"
