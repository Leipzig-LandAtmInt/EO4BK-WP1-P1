#!/bin/bash
#SBATCH --job-name=pheno_barley_hd_2018  # Job name
#SBATCH --output=logger/pheno_barley_hd_2018/trash/master_output_%A_%a.out  # Output file for each job (%A is the master job ID, %a is the array index)
#SBATCH --error=logger/pheno_barley_hd_2018/master_error_%A_%a.err    # Error file for each job
#SBATCH --time=01:00:00          # Max time per job
#SBATCH --partition=paul          # Replace with your appropriate partition
#SBATCH --array=0-2292%100            # 116-350%20
#SBATCH --mem=32G

python main_eo4bk_phenology.py $SLURM_ARRAY_TASK_ID


