# EO4BK D2.1_V0.2

This pipeline uses LUCAS, CONAB, LEM, LEM+, MapBiomasDirect and TerraClass reference datasets to download Sentinel-2 data with the sentle version (sentle==2025.1.4) by Clemens Mosig. 
It commits following tasks:
1. main_sentle.py: The variables YEAR, CONTINENT, TARGET_CRS, TIME_SPAN and REFERENCE_SOURCE are set in the begining of the script. CROPTYPE is defined in crops_100.sh. The main_function(idx) uses index from job.sh to run through the following steps. After each iteration, the job sleeps for 30 seconds.
2. _downloadsentle_.py: Uses the sentle==2025.1.4 package to download sentinel data. Since ```save_zarr``` is now stored inside ```sentle.process()```, a dummy_datacube is saved in a folder named after the current index. ```S2_cloud_classification``` is set to ```cpu```, but can also be set to gpu if the description (https://github.com/cmosig/sentle) is followed.
3. _clipp_download_output_.py: The dummy_datacube is clipped to the polygon extentions.
4. _getdata_harmo_.py: Pulls dimensions and data variables of the clipped dummy_datacube to calculate NDVI, NIRv, kNDVI with spyndex==0.6.0.
5. _create_xarray_harmo_.py: Retrieves variables, indices and dimensions from ```_getdata_harmo_.py ```. Assigns attributes with ```_create_lucas_attributes_.py``` and ```_create_sentinel_attributes_.py```. Stores everything in an ```xarray.Dataset```.
6._save_xarray_.py: Saves the ```xarray.Dataset``` and deletes the dummy_datacube. If the script does not run to the end, the dummy_datacube is not deleted and must be deleted manually to avoid blocking the process for datacubes with the same index.

## Install the D2.1_V0.2 branch

The branch can be installed in the terminal with
```
git clone -b D2.1_V0.2  https://github.com/Leipzig-LandAtmInt/EO4BK-WP1-P1.git
```

### Install Conda environment
Create conda environment from yml file using following command in your terminal
```
$ conda env create -f eo4bk.yml
```
Alternatively, The conda environment can be given a customised name with following command in your terminal. 
```
$ conda env create -f eo4bk.yml -n <your name>
```
Check whether the new environment is installed.
```
$ conda info --envs
```
After that conda environment can be activated with
```
$ conda activate eo4bk
```

## How to use this pipeline

### Change Input Variables
Open the eo4bkD2.1_V0.2 folder: 
Open main_sentle.py and change the following input-variables:
```
SCRIPT_FOLDER "/Directory/of/the/scripts"
OUTPUT_FOLDER = "/output/folder"
CONTINENT = 'Brazil'
YEAR1 = '2017'
YEAR2 = '2018'
YEAR_OVERLAP = '1718'
DETAIL_LEVEL = 'hd'
TARGET_CRS  = CRS.from_string("EPSG:5641")

REFERENCE_SOURCE = 'CONAB'
```
```SCRIPT_FOLDER``` must be changed to the directory in which this repository is installed. \
```YEAR1``` must be set to the starting year of the desired time span to be downloaded. \
```YEAR2``` must be set to the ending year of the desired time span to be downloaded. \
```YEAR_OVERLAP``` must be change to the last digets of the starting and ending year -> 2017 and 2018 results in 1718. \
```DETAIL_LEVEL``` must be changed in to the level of detail as specified by the Lucas data. The input data, e.g. lucas_2018.gpgk and lucas_2022.gpgk, and the output folder are changed, but not the attributes of the .zarr file, which is due to storage limitations.\
```TARGET_CRS```  = Defines the crs the Sentinel-2 will be transformed to. 
```REFERENCE_SOURCE``` = Defines the reference source that is used to as the reference polygon. Can be either ```LUCAS```, ```CONAB```, ```LEM```, ```LEMplus```, ```MapBiomasDirect``` or ```TerraClass```.
After changes are made ```main_sentle.py``` must be saved. 

#### Run in parallel

After the input variables are defined. Open ```run_script_parallel.sh```\
```
#!/bin/bash
#SBATCH --job-name=barley  # Job name
#SBATCH --output=Logs/trash/master_output_%A_%a.out  # Output file for each job (%A is the master job ID, %a is the array index)
#SBATCH --error=Logs/master_error_%A_%a.err    # Error file for each job
#SBATCH --time=1-00:00:00                   # Max time per job
#SBATCH --partition=clara              # Replace with your appropriate partition
#SBATCH --array=0-419%40             # 116-350%20
#SBATCH --mem=16G


python main_execute.py $SLURM_ARRAY_TASK_ID
```
```#SBATCH --array=0-419%40 ``` is set to the index 0 to 419, but can be changed to any integer. %40 refers to a maximum of 40 jobs that are commited in parallel. As soon as one job is finished, another one starts, but never more than 40 jobs simultaneously. The amount of parallel jobs must be changed according to the CPU limitations.\
```#SBATCH --mem=16G``` defines the amount of memory used by the jobs.\

Execute main_execute.py in the terminal with:
```
conda activate wp1_d21_V02
sbatch run_script_parallel.sh
```
#### Run in for loop 
Alternatively, the main_execute.py can also be executed in a for loop. Open ```run_script_linear.sh``:
```
#!/bin/bash
COUNTER=0 
for i in {0..1} # 684   # {99..977}   #977
do
  python main_execute.py $i 
  COUNTER=$(( COUNTER + 1 ))
  printf "After 'COUNTER=\$(( COUNTER + 1 ))', COUNTER=%d\n" $COUNTER 
done
```
```{0..1}`` defines the index via which the code is run through in a loop.\
Start the job in the terminal using: 
```
conda activate wp1_d21_V02
./run_script_linear.sh
```
### TMUX
Both variants can be executed in the background by executing the following commands in the terminal. In the example the ```run_script_linear.sh``` is executed. 

```
# to create a new session
$ tmux new -s <name>
# then execute the commands from above
$ conda activate wp1_d21_V02
$ ./run_script_linear.sh
# go back outside the session without closing
$ tmux detach
# check on existing sessions
$ tmux ls 
# open the session again
$ tmux attach -t <name>
# end the session when it is finished
$ exit 
```

# EO4BK-WP1-P1 Quality Check

This script allows the user to check the quality of the minicubes. It can be executed via terminal command with ```run_qc.sh```. The output is an Excel file that is stored in the minicube fodler and contains the following columns:
- FILE: Is idantical with the name of the minicube
- START_TIME: Is the start date of the minicube from ```time.min()```
- END_TIME: Is the end date of the minicube form ```time.max()```
- LEN_LON: Is the length of the longitude-index
- LEN_LAT: Refers to the length of the latitude-index
- LEN_TIME: Is the length of the time-index 

The other columns store the number of bytes (```nbytes```) of the ```minicube.data_vars()```.

## Reference

The Vegetation Indicies (VI) are computed with spyndex (https://github.com/awesome-spectral-indices/spyndex)

The Sentinel 1 and 2 download is done with sentle (https://github.com/cmosig/sentle/tree/main)
