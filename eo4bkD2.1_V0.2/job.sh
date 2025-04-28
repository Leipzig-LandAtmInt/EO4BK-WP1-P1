#!/bin/bash
#SBATCH --job-name=sentinel_2018_hd  # Job name
#SBATCH --time=2-00:00:00            # Max time per job
#SBATCH --partition=clara            # Adjust partition as needed
#SBATCH --array=0-600%80              # 64 tasks, 40 in parallel
#SBATCH --mem=32G
#SBATCH --output=logger/trash/sentinel_2018_hd/%x/%A_%a.out
#SBATCH --error=logger/trash/sentinel_2018_hd/%x/%A_%a.err

# Load crop types and job counts
# CROPTYPE will be exported from the parent script (crops.sh)
echo "Running job for crop type: $CROPTYPE"
echo "Array Job ID: $SLURM_ARRAY_JOB_ID, Array Task ID: $SLURM_ARRAY_TASK_ID"

# Define log paths dynamically (moved **after** CROPTYPE is determined)
LOG_DIR_OUT="logger/sentinel_2018_hd/${CROPTYPE}/trash"
LOG_DIR_ERROR="logger/sentinel_2018_hd/${CROPTYPE}"
mkdir -p "$LOG_DIR_OUT"  # Ensure the directory exists
mkdir -p "$LOG_DIR_ERROR"  # Ensure the directory exists

OUTPUT_FILE="$LOG_DIR_OUT/master_output_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out"
ERROR_FILE="$LOG_DIR_ERROR/master_error_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err"

# Run the Python script with the determined crop type and task ID
python main_execute.py "$CROPTYPE" "$SLURM_ARRAY_TASK_ID"