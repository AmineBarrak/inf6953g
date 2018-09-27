#!/bin/sh

for file in `ls *.log`
do
	m=$(basename $file .log)
	newF=$m.data
	echo $file vers $newF
	:>$newF
	grep '\[[0-9]*\] brk' $file | awk '{printf("%s %s\n",$4,$9)}' >> $newF
	grep '\[[0-9]*\] bigheap' $file | awk '{printf("%s %s\n",$4,$9)}' >> $newF
	grep '\[[0-9]*\] stack' $file | awk '{printf("%s %s\n",$4,$9)}' >> $newF
done
