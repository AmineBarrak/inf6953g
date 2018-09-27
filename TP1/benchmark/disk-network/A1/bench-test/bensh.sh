
#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential
sudo apt install speedtest-cli

cmp=0
mkdir -p disk2 speed2
#______________________________________________________


for i in `seq 1 5`
do



#3-network test
speedtest-cli >>speed2/speedtest"$cmp".txt

#4-Disk performance
#speed of a disk
sudo hdparm -Tt /dev/sda >>disk2/disk"$cmp".txt

sleep 20s

cmp=$((cmp+1))

done

