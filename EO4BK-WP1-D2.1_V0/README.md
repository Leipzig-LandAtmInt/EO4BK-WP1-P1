# EO4BK-WP1-P1

## Install Conda environment
Create conda environment from yml file using following command in your terminal
```
$ conda env create -f wp1v3.yml
```
Alternatively, The conda environment can be given a customised name with following command in your terminal. 
```
$ conda env create -f wp1v3.yml -n <your name>
```
Check whether the new environment is installed.
```
$ conda info --envs
```
After that conda environment can be activated with
```
$ conda activate wp1v3
```
## Use jupyter notebooks
1_LUCAS2022_Preprocessing pipeline to preprocess LUCAS 2022 Copernicus dataset \
2_Download_EO4BK_Minicubes to create zarr files with LUCAS 2022 Copernicus information and the corresponding Sentinel 1 and 2 dataset

## Use without jupyter notebook

Open the eo4bksentle folder: \
Open "main_execute.py" and change following input variables. 

```
# The input for the LUCAS Dataset and the output path in which the final zarr datasets are saved must be defined in the .env data
LUCAS2022 = os.getenv('LUCAS2022')
MINICUBE_OUT = os.getenv('MINICUBE_OUT')

# The landcover class and the level of detail can be selected, ld_data = low detail and hd_data = high_detail
lucaspoly = gpd.read_file(f'{LUCAS2022}/wheat_eo4bk.gpkg', layer = 'ld_data')

# change time span of download period
time_span = "2024-05-01/2024-07-15"
```
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
