replay_out_dir=$1
script_path="/local2/thiagoepdc/cppworkspace/TheBeefsReplayer/verification/accuracy/issue_error.py"

for file in `find $replay_out_dir/ -name "*replay.out"`
do
    python $script_path < $file > $file.issue_error
done

#for file in `find $replay_out_dir/fs-timestamp/ -name "*replay.out"`
#do
#    python $script_path < $file > $file.issue_error
#done

#for file in `find $replay_out_dir/con-timestamp/ -name "*replay.out"`
#do
#    python $script_path < $file > $file.issue_error
#done
