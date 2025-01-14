#!/bin/bash
#SBATCH --job-name=barley  # Job name
#SBATCH --output=Logs/trash/master_output_%A_%a.out  # Output file for each job (%A is the master job ID, %a is the array index)
#SBATCH --error=Logs/master_error_%A_%a.err    # Error file for each job
#SBATCH --time=1-00:00:00                   # Max time per job
#SBATCH --partition=clara              # Replace with your appropriate partition
#SBATCH --array=0-419%40             # 116-350%20
#SBATCH --mem=16G


python main_execute.py $SLURM_ARRAY_TASK_ID


