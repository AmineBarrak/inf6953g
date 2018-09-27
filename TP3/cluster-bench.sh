#!/bin/bash

sysbench --test=oltp --oltp-table-size=5000  --mysql-db=sakila --mysql-user=root --mysql-host='master' --mysql-table-engine=NDBCLUSTER prepare

for each in 1 2 4 8 16 32 64 128 ; do 

sysbench --test=oltp --oltp-table-size=5000 --oltp-test-mode=complex --oltp-read-only=off --num-threads=$each --max-time=30 --max-requests=0 --mysql-host='master' --mysql-db=sakila --mysql-user=root --mysql-table-engine=NDBCLUSTER run


done


sysbench --test=oltp --mysql-db=sakila --mysql-user=root  --mysql-host='master' cleanup

