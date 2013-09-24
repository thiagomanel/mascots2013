#!/bin/bash

# This script checks replay output against its expected returned values
out_dir=$1

if [ ! -d $out_dir ]
then
	echo "Trace output dir <" $out_dir "> not found"
	exit 1
fi

expected_input=$2
#"/local/thiagoepdc/beefs_trace_replay/input/2011_10_21-abelhinha.clean.cut.order.expected"
check_script="/local2/thiagoepdc/cppworkspace/TheBeefsReplayer/data/debug/check_replay_responsed.py"

if [ ! -f $expected_input ]
then
	echo "Expected input <" $expected_input "> not found"
	exit 1
fi

if [ ! -f $check_script ]
then
	echo "Expected sanity script <" $check_script "> not found"
	exit 1
fi

for file in `find $out_dir -name "*.out"`
do
	python $check_script $expected_input $file > /tmp/check
	f=`grep False /tmp/check | wc -l`
	t=`grep True /tmp/check | wc -l`
	echo $file "false:" $f "true:" $t
done
