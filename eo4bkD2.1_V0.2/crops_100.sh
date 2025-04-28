#!/bin/bash
#SBATCH --partition=paul
#SBATCH --mem=32G

# Define crop types list for under 200
CROPTYPES=("Rice" "Other_cereals" "Cotton" "Other_root_crops" "Grapes" "Flax" "Other_single_crops" "Olive_groves" "Fruit_and_nut" "Other_permanent_crop" "Sorghum" "Millet")

# Loop over each crop type
for CROPTYPE in "${CROPTYPES[@]}" 
do
    
    # Export the crop type to the job script
    export CROPTYPE="$CROPTYPE"

    # Submit the job array for this crop type
    sbatch job.sh
done