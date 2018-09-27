#!/bin/sh

res="allRes.csv"

:>$res
for file in `ls *.data`
do
	m=$(basename $file .data)
	echo $file vers $res
	sed "s/\(.*\)/$m \1/g" $file >> $res
done
