# EO4BK-WP1-P1 D2.1_1.1_0.2

## Install the D2.1_1.1_0.2 branch

The branch can be installed in the terminal with
```
git clone -b D2.1_V1.1_0.2  https://github.com/Leipzig-LandAtmInt/EO4BK-WP1-P1.git
```

### Install Conda environment
Create conda environment from yml file using following command in your terminal
```
$ conda env create -f wp1_d21_V02.yml
```
Alternatively, The conda environment can be given a customised name with following command in your terminal. 
```
$ conda env create -f wp1_d21_V02.yml -n <your name>
```
Check whether the new environment is installed.
```
$ conda info --envs
```
After that conda environment can be activated with
```
$ conda activate wp1_d21_V02
```

## How to use this pipeline

### Change Input Variables
Open the D2.1_V1.1_0.2 folder: \
Open the ‘.env’ file to change the input variables. If .env is hidden by Github by default, open .env with ```nano``.
The .env looks like:

```
HOME = '/net/projects/EO4BK/WP1/P1-EO4BK/scripts/EO4BK-Github'

LUCAS_D21_V01 = 'EO4BK-WP1-P1/data/lucas_data_d2.1_V0.1'
MINICUBE_OUT_D21_V01 = 'EO4BK-WP1-P1/data/minicube_europe_d2.1_V0.1'


YEAR = '2018'
DETAIL_LEVEL = 'hd'
CROPTYPE = 'Barley'
```
```HOME``` must be changed to the home directory in which this repository is installed. \
```YEAR``` must be changed to the YEAR that is downloaded. \
```DETAIL_LEVEL``` must be changed in to the level of detail as specified by the Lucas data. The input lucas_2022.gpgk and the output folder are changed, but not the attributes of the .zarr file, which is due to storage limitations.\
```CROPTYPE``` must be changed according to the LUCAS reference cropy type defined in the EO4BK nomenclature (V1.1) for which Sentinel data is downloaded. \

After changes are made the ```.env``` needs to be saved. 

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
```#SBATCH --array=0-419%40 ``` is set to the index 0 to 419, but can be changed to any integer. %40 refers to a maximum of 40 jobs that are commited in parallel. As soon as one job is finished, another one starts, but never more than 40 jobs simultaneously. The amount of parallel jobs must be changed according to the CPU limitations.
```#SBATCH --mem=16G`` defines the amount of memory used by the jobs.\

Start the job in the terminal with:
```
sbatch run_script_parallel.sh
```
### Run in queque 

Then open ‘run_script_parallel.sh’ to change how many polygons are used to download Sentinel data.
```
# At the moment it iterates from 0 to 2 over the id_list inside "main_execute.py". This means that the first three polygons of the wheat_eo4bk.gpkg with low detail are taken. 
for i in {0..2} # 684   # {99..977}   #977
do
  python main_execute.py $i
done
```
To start download the Sentinel data, describe the attributes, create an xarray and save the xarray as zarr, execute the following commands in the terminal
```
$ conda activate wp1v3
$ ./run_script_parallel.sh
```

To make a download in the background, execute following commands in the terminal

```
# to create a new session
$ tmux new -s <name>
# then execute the commands from above
$ conda activate wp1v3
$ ./run_script_parallel.sh
# go back outside the session without closing
$ tmux detach
# check on existing sessions
$ tmux ls 
# open the session again
$ tmux attach -t <name>
# end the session when it is finished
$ exit 
```
## Reference

The Vegetation Indicies (VI) are computed with spyndex (https://github.com/awesome-spectral-indices/spyndex)

The Sentinel 1 and 2 download is done with sentle (https://github.com/cmosig/sentle/tree/main)
