#!/bin/bash
COUNTER = 0 
for i in {20..400} # 684   # {99..977}   #977
do
  python main_execute.py $i 
  COUNTER=$(( COUNTER + 1 ))
  printf "After 'COUNTER=\$(( COUNTER + 1 ))', COUNTER=%d\n" $COUNTER
done


#seq 0 10 | parallel -j 5 python main_execute.py {}

