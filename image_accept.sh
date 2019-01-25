#!/bin/bash
cd /home/hk/Desktop/tst/2/
ls | sort
for i in {1..5}
do
			ls | sort | awk 'NR==$i{print $1}'
done
