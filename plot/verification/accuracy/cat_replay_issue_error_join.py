import sys

if __name__ == "__main__":
    """
	    It concats multiple data frame, so that we can
	    plot things from multiple, arbitrary, experimental
	    configurations.
	    Usage: python $0 frame1 id_frame1 ... frameN id_frameN
	"""

print "\t".join(["sample", "order", "timing", "min", "interval", "i", "r_begin",\
                 "r_end", "sched_stamp", "delay", "issue_error",\
                 "ops_interval", "parent_end", "replay_ratio", "id"])

for i in range(1, len(sys.argv), 2):
    path_frame = sys.argv[i]
    frame_id = sys.argv[i + 1]
    with open(path_frame) as data:
        data.readline()#exclude header
        for line in data:
            tokens = line.split()
            tokens.append(frame_id)
            print "\t".join(tokens)
