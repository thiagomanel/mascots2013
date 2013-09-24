#!/bin/bash
#
# It generates data to plot for a collection of energy replay output files
# Usage: for dir in `ls /path/to/experiment/output/`; do echo $dir; bash generate_data_to_plot.sh $dir $dir.join 2> /tmp/err;done;

if [ $# -ne 2 ]
then
	echo "Usage:" $0 "output_dir outfile"
	exit 1
fi

outdir=$1
outfile=$2

if [ ! -d $outdir ]
then
    echo "directory" $outdir "not found"
    exit 1
fi

echo -e "operation_type\tlatency\tactual_rvalue\ttid\tstamp\torder\ttiming\tsample" > $outfile

# output_dir/factor_i/$sample.$random.replay.out
# e.g out_dir/conservative_dependency-fullspeed_timing/0.5235816.replay.out

#outdir follows this format xpto_machine_xpto
machine=`basename $outdir | cut -d"_" -f2`
trace_exp=`python machine_name2expected_file.py $machine`

if [ ! -f $trace_exp ]
then
    echo "expected trace output" $trace_exp "not found"
    exit 1
fi

for factor_dir in `ls $outdir`
do
	for file in `find ${outdir}/${factor_dir} -name "*.replay.out"`
    	do
        	#4.2676313.replay.out
		factor_path=`dirname $file`
		factor=`basename $factor_path`
		order=`echo $factor | cut -d"-" -f1`
		timing=`echo $factor | cut -d"-" -f2`

	        sample=`basename $file | cut -d"." -f1`
        	plot_data=`basename $file`.plot.data
	        #transformed output format -> operation_type latency expected_rvalue actual_rvalue tid begin_stamp
        	python transform_output.py $trace_exp $file > $plot_data.tmp

	        #final format (sep by \t)
        	awk -v args="$order\t$timing\t$sample" '{ printf("%s\t%s\t%s\t%s\t%s\t%s\n", $1, $2, $4, $5, $6, args); }' $plot_data.tmp >> $outfile
	        rm $plot_data.tmp
	done
done
