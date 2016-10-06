#!/bin/bash

LIST=`cat /root/hosts.txt`

for host in $LIST

do

ping -c2 $host &> /dev/null			# -c option for the ping count. In this case pings twice.

if [ "$?" = 0 ]

then

echo "$host is OK. Adding it to the pingable list"

echo $host >> /root/pingable.txt

else

echo "$host is DOWN. Adding it to the unpingable list"

echo $host >> /root/unpingable.txt

fi

done
