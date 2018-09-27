#!/bin/bash

sysbench --test=oltp --oltp-table-size=5000  --mysql-db=sakila --mysql-user=root --mysql-password=comelit prepare

for each in 1 2 4 8 16 32 64 128 ; do

sysbench --test=oltp --oltp-table-size=5000 --oltp-test-mode=complex --oltp-read-only=off --num-threads=$each --max-time=30 --max-requests=0 --mysql-db=sakila --mysql-user=root --mysql-password=comelit run

sleep 1

done


sysbench --test=oltp --mysql-db=sakila --mysql-user=root --mysql-password=comelit cleanup

