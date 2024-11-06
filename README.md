# EO4BK-WP1-P1

# EO4BK-WP1-D2.1_V0/ 
The folder contains eo4bksentleD2.1_V0/ eo4bsentleD2.1_V0.1/ and jupyter_notebooks/. The eo4bksentleD2.1_V0/ folder stores the Sentinel downloading pipeline. The jupyter_notebook folder contains LUCAS Preprocessing Notebooks that describe the workflow for LUCAS COPERNICUS 2018 and 2022 and LUCAS theoretical points 2018 and 2022 to create EO4BK single cropping and double cropping, permanent crops and grassland classes. In addition, it contains a notebook describing how to create the harmonised LUCAS 2018/2022 for downloading longer time series. EO4BK_Sentle_Download.ipynb uses the eo4bsentleD2.1_V0/*.py scripts to download and saving Sentinel data, and plotting a time-series. 

# jupyter_notebooks/
This folder contains LUCAS_Polygon_Preprocessing/ and EO4BK_Sentle_Download.ipynb. LUCAS_Polygon_Preprocessing contains following jupyter notebooks:

## 1_LUCAS2022_Preprocessing_d2.1_v00.ipynb

This notebook describes how to retrieve the EO4BK crop-type classes from LUCAS_2018.gpkg and LUCAS_2022.gpkg according to the nomenclature introduced in the proposel. 

## 1_LUCAS2022_Preprocessing_d2.1_v01.ipynb

This notebook describes the procedure for creating the EO4BK crop-type classes from LUCAS_2018.gpkg and LUCAS_2022.gpkg following the nomenclature introduced in the document D1.1 (05.11.2024).

## 1a_LUCAS2018to2022.ipynb

This notebook describes the harmonisation process of both LUCAS_2018.gpkg and LUCAS_2022.gpkg. 

## Input data 

The LUCAS_2022.gpkg can be downloaded from 

# eo4bksentleD2.1_V0/

The eo4bsentleD2.1_V0 pipeline can be executed in a tmux session 

```
tmux new -s download
conda activate wp1v3
./run_script_parallel_copy.sh
```
The main_execute.py executes following tasks, which are defined in the main_function(): \
For each polgyon of the inpute data  (e.g., Barley_2022_eo4bk.gpkg, layer = hd_data): 

1. Downloads the data with sentle (https://github.com/cmosig/sentle) via senntle_download() from _downloadsentle_.py within the polygon boundaries and then crops the Sentinel data with the polygon
2. Copying all Sentinel bands from step 1 and the point_id from the polygon input and calculating Vegetation Indicies (VI) like kNDVI, NDVI and NIRv with spyndex (https://pypi.org/project/spyndex/) via get_harmonized() from _getdata_harmo_.py
3. Create a xarray.Dataset, from all variables from step 2 with the Metadata information stored in _create_lucas_attributes_.py and _create_sentinel_attribute_.py, with the create_xarray() function from _create_xarray_harmo_.py
4. Save xarray.Dataset from step 3 with save_as_zarr() from _save_xarray_.py as .zarr file in a folder that is created depending on the hd =True/False, reference polygon survey year, reference polygon nut0 region, and reference polygon id. Xarray.Dataset is saved with .to_zarr(mode = "w", compute = True).

The steps are conducted in a for loop. \
eo4bksentleD2.1_V0 is based on sentle package version 2024.10.1, which uses dask for parallel downloading. As this could lead to crashes on the cluster GPUs, sentle version 2024.10.3 was introduced. The eo4bksentleD2.1_V0.1/ is based on the new sentle package:

# eo4bksentleD2.1_V0.1/

The eo4bksentleD2.1_V0.1 pipeline will be executable in a for-loop as soon as issue #31 of sentle package version 2024.10.3 is solved. 
Downloading Sentinel data is similar to eo4bksentleD2.1_V0, with the following exceptions:
- a dummy .zarr is saved, because saving a .zarr is now a mendetory argument in sentle.process()
- steps 2-4 of eo4bksentleD2.1_V0/ are applied to the dummy .zarr file
- the dummy .zarr file is then deleted to save space

The process could be slower compared to eo4bksentleD2.1_V0/, but should be more robust, which needs to be tested. 

# Acknowledgments
Many thanks to: \
sentle package by Clemens Mosig (https://github.com/cmosig/sentle) \
spyndex package by Montero et al., 2023 (https://pypi.org/project/spyndex/)
