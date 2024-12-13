#!/bin/bash
#SBATCH --time=2-00:00:00                   # Max time per job
#SBATCH --partition=clara              # Replace with your appropriate partition
#SBATCH --mem=2G 
for i in {0..2} # 684   # {99..977}   #977
do
  python main_qc_of_output.py $i 
done


