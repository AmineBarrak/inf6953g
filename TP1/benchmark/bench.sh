#!/bin/bash

TEST=""
MACHINE=""
OUTPUT=""
addC=0
clef=""

usage() {
	echo "        #####"
	echo "AIDE:"
	echo "./bench.sh [-t|--test test] [-m|--machine adresse] [-i clef privee] [-o|--output sortie.txt]"
	echo "TESTS:"
	echo "CPU: test= install_cpu|cpu"
	echo "IO: test= io"
	echo "IOPS: test=install_iops|iops|iops_small|iops_amlarge|iops_d5|"
	echo "MEMORY: test=install_memory|memory"
	echo "NET: test=install_net|net"
	echo "DISK: install_disk|disk"
	echo Exemple: ./bench.sh -t cpu -m ubuntu@ec2-54-187-77-250.us-west-2.compute.amazonaws.com -i xx.pem -o sortie.txt
	echo "        #####"
}

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -t|--test)
    TEST="$2"
    shift
    ;;
    -i)
    FCLEF="$2"
    addC=1
    shift
    ;;
    -m|--machine)
    MACHINE="$2"
    shift
    ;;
    -o|--output)
    OUTPUT="$2"
    shift
    ;;
    *)
        echo "Argument inconnu: ${1}"
        exit
    ;;
esac
shift
done

if test -z $TEST || test -z $MACHINE || test -z $OUTPUT
then
	usage
	exit
fi

if test $addC -eq 1
then
	clef="-i $FCLEF"
fi

###################

SSHCMD="ssh -o StrictHostKeyChecking=no"

####################

setVar() {
	#Variables distantes
	LCPUDIR=/home/ubuntu/tmpCpu
	LCPURES=$LCPUDIR/tmpRes
	LIODIR=/home/ubuntu/tmpIO
	LIORES=$LIODIR/tmpRes
	LIOPSDIR=/home/ubuntu/tmpIOPS
	LIOPSRES=$LIOPSDIR/tmpRes
	LNETDIR=/home/ubuntu/tmpNet
	LNETRES=$LNETDIR/tmpRes
	LDISKDIR=/home/ubuntu/tmpDisk
	LDISKRES=$LDISKDIR/tmpRes
	LMEMDIR=/home/ubuntu/tmpMem
	LMEMRES=$LMEMDIR/tmpRes
}


###################
##     CPU       ##
###################
dist_cpu_bench() {
	mkdir -p $LCPUDIR
	cd $LCPUDIR
	:>$LCPURES
	for i in $(seq 20000 5000 100000)
	do
		sysbench --test=cpu --cpu-max-prime=$i run >> $LCPURES 2>&1
	done
}

dist_cpu2_bench() {
	mkdir -p $LCPUDIR
	cd $LCPUDIR
	:>$LCPURES
	for size in 20000 50000 80000 100000 150000
	do
		for i in 1 2 3
		do
			sysbench --test=cpu --cpu-max-prime=$size --num-threads=$(nproc) run >> $LCPURES 2>&1
		done
	done
}

dist_cpu3_bench() {
	mkdir -p $LCPUDIR
	cd $LCPUDIR
	:>$LCPURES
	for size in 20000 50000 80000
	do
		sysbench --test=cpu --cpu-max-prime=$size run >> $LCPURES 2>&1
	done
}

launch_install_cpu_bench() {
	$SSHCMD $clef $1 "$(typeset -f); sudo apt-get update; sudo apt-get install -y sysbench; exit"
}

launch_cpu_bench() {
	# Argument 1: machine distante
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_cpu_bench; exit"
	#ssh -i "tp1.pem" $1 "$(typeset -f); setVar; dist_cpu_bench"
	#Argument 2: nom du fichier de resultat en local
	tmpCpu="tmpCpu$1"
	scp $clef -r $1:$LCPURES $tmpCpu
	grep -o "total time: *[0-9]*.[0-9]*s" $tmpCpu | grep -o [0-9]*.[0-9]*s | sort > ./$2
	rm $tmpCpu
}

launch_cpu2_bench() {
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_cpu2_bench; exit"
	tmpCpu="tmpCpu$1"
	scp $clef -r $1:$LCPURES $tmpCpu
	grep -o "total time: *[0-9]*.[0-9]*s" $tmpCpu | grep -o [0-9]*.[0-9]*s | sort > ./$2
	rm $tmpCpu
}

launch_cpu3_bench() {
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_cpu3_bench; exit"
	tmpCpu="tmpCpu$1"
	scp $clef -r $1:$LCPURES $tmpCpu
	grep -o "total time: *[0-9]*.[0-9]*s" $tmpCpu | grep -o [0-9]*.[0-9]*s | sort > ./$2
	rm $tmpCpu
}

###################
##     DISK      ##
###################

dist_disk_bench() {
	mkdir -p $LDISKDIR
	cd $LDISKDIR
	:>$LDISKRES
	for i in 1 2 3 4 5
	do
		sudo hdparm -Tt /dev/xvda >> $LDISKRES 2>&1
	done
	#touch $global
}

dist_net_bench() {
	mkdir -p $LNETDIR
	cd $LNETDIR
	:>$LNETRES
	for i in 1 2 3 4 5
	do
		speedtest >> $LNETRES 2>&1
	done
}

dist_io_bench() {
	mkdir -p $LIODIR
	cd $LIODIR
	:>$LIORES
	for i in 1 2 3 4 5
	do
		dd if=/dev/zero of=sb-io-test bs=1M count=1k conv=fdatasync >> $LIORES 2>&1
	done
	rm sb-io-test
}



####################

launch_install_net_bench() {
	$SSHCMD $clef $1 "$(typeset -f); sudo apt-get update; sudo apt-get install -y speedtest-cli; exit"
}

launch_install_disk_bench() {
	$SSHCMD $clef $1 "$(typeset -f); sudo apt-get update; sudo apt-get install -y hdparm; exit"
}


launch_net_bench() {
	# Argument 1: machine distante
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_net_bench; exit"
	scp $clef -r $1:$LNETRES ./$2
}

launch_disk_bench() {
	# Argument 1: machine distante
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_disk_bench; exit"
	scp $clef -r $1:$LDISKRES ./$2
}

launch_io_bench() {
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_io_bench; exit"
	tmpIO="tmpIO$1"
	scp $clef -r $1:$LIORES $tmpIO
	grep -o '[0-9]*.[0-9]* MB/s' $tmpIO | sort > ./$2
	rm $tmpIO
}

###################
##     IOPS      ##
###################

launch_install_iops_bench() {
	$SSHCMD $clef $1 "$(typeset -f); sudo apt-get update; sudo apt-get install -y bonnie++; exit"
}

launch_iops_bench() {
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_iops_bench; exit"
	scp $clef -r $1:$LIOPSRES ./$2
}
launch_iops_small_bench() {
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_iops_small_bench; exit"
	scp $clef -r $1:$LIOPSRES ./$2
}
launch_iops_amlarge_bench() {
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_iops_amlarge_bench; exit"
	scp $clef -r $1:$LIOPSRES ./$2
}
launch_iops_d5_bench() {
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_iops_d5_bench; exit"
	scp $clef -r $1:$LIOPSRES ./$2
}

dist_iops_bench() {
	mkdir -p $LIOPSDIR
	cd $LIOPSDIR
	:>$LIOPSRES
	for i in 1 2 3 4 5
	do
		bonnie++ -b >> $LIOPSRES 2>&1
		sleep 10
	done
}

dist_iops_small_bench() {
	mkdir -p $LIOPSDIR
	cd $LIOPSDIR
	:>$LIOPSRES
	for i in 1 2 3 4 5
	do
		bonnie++ -b >> $LIOPSRES 2>&1
		sleep 10
	done
}

dist_iops_amlarge_bench() {
	mkdir -p $LIOPSDIR
	cd $LIOPSDIR
	:>$LIOPSRES
	for i in 1 2 3 4 5
	do
		bonnie++ -b -s 8000 -r 4000 >> $LIOPSRES 2>&1
		sleep 10
	done
}

launch_iops_az_bench() {
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_iops_az_bench; exit"
	scp $clef -r $1:$LIOPSRES ./$2
}
dist_iops_az_bench() {
	mkdir -p $LIOPSDIR
	cd $LIOPSDIR
	:>$LIOPSRES
	for i in 1 2 3 4 5
	do
		sudo bonnie++ -d /mnt/ -b -u root >> $LIOPSRES 2>&1
		sleep 10
	done
}


dist_iops2_bench() {
	mem=$(free -m | grep -o '[0-9]*' | head -1)
}
###################
##    MEMOIRE    ##
###################

launch_install_memory_bench() {
	$SSHCMD $clef $1 "$(typeset -f); sudo apt-get update; sudo apt-get install -y stress-ng; exit"
}

launch_memory_bench() {
	$SSHCMD $clef $1 "$(typeset -f); setVar; dist_memory_bench; exit"
	scp $clef -r $1:$LMEMRES ./$2
}

dist_memory_bench() {
	mkdir -p $LMEMDIR
	cd $LMEMDIR
	:>$LMEMRES
	for i in 1 2 3 4 5
	do
		sudo stress-ng --brk 10 --stack 10 --bigheap 10 --metrics-brief --aggressive -t 30 >> $LMEMRES 2>&1
		sleep 10
	done
}

####################

setVar
cmd="launch_"$TEST"_bench"
#echo $cmd $MACHINE $OUTPUT
#exit
echo "Execution de $cmd sur $MACHINE"

$cmd $MACHINE $OUTPUT

echo "$cmd sur $MACHINE terminé, sortie dans $OUTPUT"



#ssh poly 'bash -s' < f
#echo $LCPURES
