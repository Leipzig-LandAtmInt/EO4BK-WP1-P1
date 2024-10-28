# EO4BK-WP1-P1

# EO4BK-WP1-D2.1_V0/ 
The folder contains eo4bksentleD2.1_V0/ and jupyter_notebooks/. The eo4bksentleD2.1_V0/ folder stores the Sentinel downloading pipeline. The jupyter_notebook folder contains LUCAS Preprocessing Notebooks that describe the workflow for LUCAS COPERNICUS 2018 and 2022 and LUCAS theoretical points 2018 and 2022 to create EO4BK single cropping and double cropping, permanent crops and grassland classes. In addition, it contains a notebook describing how to create the harmonised LUCAS 2018/2022 for downloading longer time series. EO4BK_Sentle_Download.ipynb uses the eo4bsentleD2.1_V0/*.py scripts to download and saving Sentinel data, and plotting a time-series. 

# eo4bksentleD2.1_V0/

The eo4bsentleD2.1_V0 pipeline can be executed in a tmux session 

```
tmux new -s download
conda activate wp1v3
./run_script_parallel_copy.sh
```
The main_execute.py executes following tasks, which are defined in the main_function(): \
For each polgyon of the inpute data  (e.g., Barley_2022_eo4bk.gpkg, layer = hd_data): \

1. Downloads the data with sentle (https://github.com/cmosig/sentle) via senntle_download from _downloadsentle_.py within the polygon boundaries and then crops the Sentinel data with the polygon
2. 
