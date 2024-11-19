# EO4BK-WP1-P1 D2.1_1.1_0.1

This pipeline uses LUCAS reference datasets changed by the Jupyter-Notebook in the Jupyter_Notebook branch to download Sentinel data with the sentle version (sentle==2024.10.2) by Clemens Mosig. 
It commits following tasks:
1. main_execute.py: Pulls input variables from .env; main_function(idx) uses index the from run_script_linear.sh file to run through the following steps. After each iteration, the job sleeps for 30 seconds.
2. _downloadsentle_.py: Uses the sentle==2024.10.2 package to download sentinel data. ```S2_cloud_classification``` is set to GPU with ```cuda```, but can also be set to cpu if the sentle description (https://github.com/cmosig/sentle) is followed. The ```num_workers=40``` is set to 40 workers in parallel using dask. After ```sentle.process()``` is committed the Sentinel download is clipped to the polygon extention. 
3. _getdata_harmo_.py: Pulls dimensions and data variables of the clipped Sentinel download to calculate NDVI, NIRv, kNDVI with spyndex==0.6.0.
4. _create_xarray_harmo_.py: Retrieves variables, indices and dimensions from ```_getdata_harmo_.py ```. Assigns attributes with ```_create_lucas_attributes_.py``` and ```_create_sentinel_attributes_.py```. Stores everything in an ```xarray.Dataset```.
5._save_xarray_.py: Saves the ```xarray.Dataset```. 

## Install the D2.1_1.1_0.1 branch

The branch can be installed in the terminal with
```
git clone -b D2.1_V1.1_0.1  https://github.com/Leipzig-LandAtmInt/EO4BK-WP1-P1.git
```

### Install Conda environment
Create conda environment from yml file using following command in your terminal
```
$ conda env create -f wp1_d21_V01.yml
```
Alternatively, The conda environment can be given a customised name with following command in your terminal. 
```
$ conda env create -f wp1_d21_V01.yml -n <your name>
```
Check whether the new environment is installed.
```
$ conda info --envs
```
After that conda environment can be activated with
```
$ conda activate wp1_d21_V01
```

## How to use this pipeline

### Change Input Variables
Open the D2.1_V1.1_0.1 folder: \
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

#### Run in for loop 
The main_execute.py is executed in a for loop. Open ```run_script_linear.sh``:
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
## Reference

The Vegetation Indicies (VI) are computed with spyndex (https://github.com/awesome-spectral-indices/spyndex)

The Sentinel 1 and 2 download is done with sentle (https://github.com/cmosig/sentle/tree/main)

