#!/bin/bash
for i in `seq 1 10`;
do
	echo "iteration $i\n">>ubuntu
	echo "iteration $i\n">>time-spark
	echo "iteration $i\n">>time-hadoop
	time (cat pg4300.txt | tr ' ' '\n\r' | sort | uniq -c )2>>ubuntu
	time (hadoop jar /usr/local/hadoop-2.7.3/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.3.jar wordcount /amine/pg4300.txt /output/$i) 2>> time-hadoop
	time (spark-submit wordcount.py hdfs://localhost:/amine/pg4300.txt) 2>> time-spark

        echo $i
done

