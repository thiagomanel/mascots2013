import sys

SEC_TO_USEC= 1000000

def elapsed_millis(begin_sec, begin_usec, end_sec, end_usec):
    return ((end_sec * SEC_TO_USEC + end_usec) -
                       (begin_sec * SEC_TO_USEC + begin_usec))

def stamp(stamp_sec, stamp_usec):
    return (stamp_sec * SEC_TO_USEC + stamp_usec)

if __name__ == "__main__":
    """ It converts replayer output to ease plotting:
        output format: operation_type\tlatency\texpected_rvalue\tactual_rvalue

        Usage: python transform_output.py workflow_expected replay_output > output

        workflow_expected is a text file, in which each line is a 2-tuple likewise:
		open	18
		close	0
		open	23
		close	0
		open	18
		close	0
		open	43
		fstat	0
		llseek	0
		read	100

        For the N-th line, first token is the syscall for N-th replay operation, second token
        is the expected return value.
    """
    workflow_exp_path = sys.argv[1]#it starts by real operation
    replay_out_path = sys.argv[2]#it starts by fake root it

    with open(workflow_exp_path) as workflow_exp:
        with open(replay_out_path) as replay_out:
            replay_out.readline()#excluding fake root
            for op_line in workflow_exp:
                operation_type, exp_rvalue = op_line.split()

                tokens = replay_out.readline().split()
                begin_secs, begin_usec, end_sec, end_usec,\
                    sched_secs, sched_usec, delay,\
                    exp_rvalue, actual_rvaluec, tid = tokens


                elapsed = elapsed_millis(long(begin_secs), long(begin_usec),\
                              long(end_sec), long(end_usec))
                stamp_begin = stamp(long(begin_secs), long(begin_usec))

                sys.stdout.write("\t".join([operation_type,
                                            str(elapsed),
                                            str(exp_rvalue),
                                            str(actual_rvaluec),
                                            str(tid),
                                            str(stamp_begin)])
                                 + "\n")
