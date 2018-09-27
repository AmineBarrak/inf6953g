#!/bin/sh

InstFile="instances.txt"

t2small=$(cat $InstFile | grep small | cut -d= -f2)
m4large=$(cat $InstFile | grep m4large | cut -d= -f2)
c4large=$(cat $InstFile | grep c4large | cut -d= -f2)
A1=$(cat $InstFile | grep A1 | cut -d= -f2)
D5_v2=$(cat $InstFile | grep D5 | cut -d= -f2)

usage() {
	echo "1 argument: cpu|iops|memory"
}

TEST=$1


if test -z $TEST
then
	usage
	exit
fi

cpuBench() {
	instance=$1
	machine=$2
	echo "$instance: debut de l'installation"
	#./bench.sh -t install_cpu -m $machine -i tp1.pem -o dummy
	echo $instance: installation terminée

	echo $instance: benchmarking cpu
	./bench.sh -t cpu2 -m $machine -i tp1.pem -o sysbench/"$instance".txt
	echo $instance: benchmarking cpu terminé 
}

cpu() {
	for instance in m4large c4large
	do
		machine=$(eval "echo \$$instance")
		#echo $instance
		cpuBench $instance $machine &
		#./bench -t install_cpu 
	done
}

iops() {
	for machine in $small $m4large $c4large
	do
		./bench.sh -t install_iops -m $machine -i tp1.pem -o dummy
	done
	./bench.sh -t iops_small -m $small -i tp1.pem -o bonnie/t2small.txt &
	./bench.sh -t iops_m4large -m $m4large -i tp1.pem -o bonnie/m4large.txt &
	./bench.sh -t iops_c4large -m $c4large -i tp1.pem -o bonnie/c4large.txt &
}

memory() {
	for machine in $t2small $A1 $D5_v2
	do
		./bench.sh -t install_memory -m $machine -i tp1.pem -o dummy
	done
	for instance in t2small A1 D5_v2
	do
		machine=$(eval "echo \$$instance")
		./bench.sh -t memory -m $machine -i tp1.pem -o stress/"$instance".log &
	done

}

$1


