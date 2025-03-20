#!/bin/bash
#SBATCH --job-name=other_cereals_2018_lai  # Job name
#SBATCH --output=logger/other_cereals_2018_lai/trash/master_output_%A_%a.out  # Output file for each job (%A is the master job ID, %a is the array index)
#SBATCH --error=logger/other_cereals_2018_lai/master_error_%A_%a.err    # Error file for each job
#SBATCH --time=01:00:00          # Max time per job
#SBATCH --partition=paula          # Replace with your appropriate partition
#SBATCH --array=0-30%100            # 116-350%20
#SBATCH --mem=32G

python main_cglob_execute.py $SLURM_ARRAY_TASK_ID


