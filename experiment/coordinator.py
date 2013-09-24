import sys
import os
import random
import subprocess
import ConfigParser
from deploy import *
from time import sleep

def start_replay(replayer_path, in_path, timing_police, out_path, err_path):
    with open(out_path, 'w') as replay_out:
        with open(err_path, 'w') as replay_err:
            cmd = " ".join([replayer_path, in_path, timing_police, "10", "0", "debug", "&"])
            #cmd = " ".join([replayer_path, in_path, timing_police, "&"])
            print "start cmd", cmd
            return process(cmd, replay_out, replay_err)

def wait_replay():
    def replayer_is_running():
        out, err, rcod = execute("ps xau | grep beefs_replayer | grep -v grep")
        return out#if it is running, out it not empty, so it's is true

    sys.stdout.write("wait for replay termination\n")
    while replayer_is_running():
        sys.stdout.write("Waiting job termination\n")
        sleep(30)

def start_probe(probe_script_path, args, out_path, err_path):
    args_str = " ".join(args)
    cmd = " ".join(["stap -g --skip-badvars -DSTP_NO_OVERLOAD -DMAXACTION=100000\
                    -DMAXMAPENTRIES=10000 -DMAXSTRINGLEN=2048 -F -o",
                    out_path,
                    probe_script_path,
                    args_str])
    print "probe cmd", cmd
    with open(err_path, 'w') as probe_err:
        return process(cmd, None, probe_err)

def mount(mount_point):
    print "mounting"
    print execute("mount -a")

def umount(mount_point):
    print "umount point=", mount_point
    print execute(" ".join(["umount", mount_point]))

def main(num_samples, config):

    def base_out_path(out_dir, sample):
        #out_dir/sample.random
        _random = int(random.random() * 10000000)
        return os.path.join(out_dir, ".".join([str(sample), str(_random)]))

    mount_point = config.get("target_fs", "mount_point")
    replayer_target_dir = config.get("target_fs", "replayer_target_dir")
    backup_dir = config.get("target_fs", "fs_raw_data_backup")

    pre_replay_path = config.get("pre_replay", "pre_replayer_path")
    pre_replay_checker_path = config.get("pre_replay", "pre_replayer_checker_path")
    pre_replay_input = config.get("pre_replay", "pre_replay_input")

    replayer_path = config.get("replayer", "replayer_path")
    trace_replay_input = config.get("replayer", "trace_replay_input")
    replayer_out_dir = config.get("replayer", "replayer_out_dir")
    timing_police = config.get("replayer", "timing_police")

    rollback(None, backup_dir, replayer_target_dir)

    for sample in range(num_samples):

        sys.stdout.write("Running sample " + str(sample) + "\n")

        umount(mount_point)
        mount(mount_point)
        rollback(None, backup_dir, replayer_target_dir)
        umount(mount_point)
        mount(mount_point)

        sys.stdout.write("executing pre_replay\n")
        out, err, rcode = execute(" ".join(["python", pre_replay_path, "<", pre_replay_input]))
        sys.stdout.write("pre_replay out: " + str(out) + "\n")
        sys.stdout.write("pre_replay err: " + str(err) + "\n")

        sys.stdout.write("checking pre_replay\n")
        out, err, rcode = execute(" ".join(["bash", pre_replay_checker_path, pre_replay_input]))
        if not rcode == 0:
            sys.stderr.write("pre_replay didn't work\n")
            sys.stderr.write("pre_replay out " + str(out) + "\n")
            sys.stderr.write("pre_replay err " + str(err) + "\n")

        base_out = base_out_path(replayer_out_dir, sample)
        out_file, err_file = base_out + ".replay.out", base_out + ".replay.err"

        start_replay(replayer_path, trace_replay_input, timing_police, out_file, err_file)
        #we use shell=True in the POpen args, so we will no be able to get the
        #correct pid when calling process.pid
        sleep(2)
        pid, _, _ = execute("pgrep beefs_replayer")
        print "replayer pid", pid

        wait_replay()
        sleep(30)
        execute("killall stapio")

def load(config_path):
    try:
        config = ConfigParser.RawConfigParser(allow_no_value=True)
    except:
        config = ConfigParser.RawConfigParser()

    config.read(config_path)
    return config

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: python coordinator.py num_samples config_file\n")
        sys.exit(-1)

    num_samples = int(sys.argv[1])
    config_file = sys.argv[2]
    config = load(config_file)

    main(num_samples, config)
