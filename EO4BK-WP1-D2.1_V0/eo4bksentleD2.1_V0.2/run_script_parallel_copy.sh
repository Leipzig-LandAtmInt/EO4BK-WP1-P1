#!/bin/bash
#SBATCH --job-name=download_in_parallel_10  # Job name
#SBATCH --output=master_output_%A_%a.out  # Output file for each job (%A is the master job ID, %a is the array index)
#SBATCH --error=master_error_%A_%a.err    # Error file for each job
#SBATCH --array=0-99%10                   # Array index (0–99), %10 limits to 10 parallel tasks
#SBATCH --time=00:30:00                   # Max time per job
#SBATCH --partition=clara-long               # Replace with your appropriate partition

# Calculate start and end of the range for the task
start=$((SLURM_ARRAY_TASK_ID * 10))
end=$((start + 9))

echo "Master script running tasks from $start to $end"

# Loop through the calculated range and execute commands or call scripts
# for (start, end, increase by one); do main_execute.py $ i "&" for parallization
for ((i=start;i<=end;i++)); do
    main_execute.py $i &
done

# Wait for all background processes to finish
wait
echo "Finished tasks $start to $end"
