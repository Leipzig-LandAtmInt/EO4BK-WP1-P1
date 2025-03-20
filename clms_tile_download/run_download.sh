#!/bin/bash
#SBATCH --time=2-00:00:00                   # Max time per job
#SBATCH --partition=clara              # Replace with your appropriate partition
#SBATCH --mem=32G

COUNTER=0 
for i in {0..36} # 684   # {99..977}   #977
do
  yes | python download_tile_cluster.py $i 
  COUNTER=$(( COUNTER + 1 ))
  printf "After 'COUNTER=\$(( COUNTER + 1 ))', COUNTER=%d\n" $COUNTER 
done
