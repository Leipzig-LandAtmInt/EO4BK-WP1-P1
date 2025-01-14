import xarray as xr
import numpy as np
import pandas as pd
import os
import glob
from dotenv import load_dotenv
import geopandas as gpd
from _centroid_list_ import create_centroid_list
from _sampling_ import sampling
import sys

load_dotenv('/home/sc.uni-leipzig.de/ds28kene/testing_stage/copernicus_gls_v2/.env')

WORKDIR = os.getenv('WORKDIR')
LUCAS = f'{WORKDIR}/lucas_data_d2.1_V0.1'
YEAR = os.getenv('YEAR')
DETAIL_LEVEL = os.getenv('DETAIL_LEVEL')
ACRONYM = os.getenv('ACRONYM')
DOWNLOAD_NAME = os.getenv('DOWNLOAD_NAME')
# CHANGE HER 



SAVE_RESULT = f'{WORKDIR}/c_gls_csv/c_gls_{ACRONYM}300_{DOWNLOAD_NAME}_EO4BK_LUCAS_{YEAR}'
os.makedirs(f'{SAVE_RESULT}/{YEAR}', exist_ok= True)
# Get the netfcdf-data as a list 
#TODO ADD IF 2022 RT ELSE 
files = glob.iglob(f"{WORKDIR}/c_gls/c_gls_{ACRONYM}300_{YEAR}_{DOWNLOAD_NAME}/*.nc")

nc_dict = {}

# get the data from the folder
for file in files:
    key = os.path.splitext(os.path.basename(file))[0]
    key = key.split('_')[3][:8] # third word, first 7 digits
    time_steps = f"{key[:4]}-{key[4:6]}-{key[6:]}"
    ncs = xr.open_dataset(file)
    nc_dict[time_steps] = ncs

# assign time-steps to the single nc-files from the name of the data
first_item = list(nc_dict)[0]
dim_names = list(nc_dict[f'{first_item}'].dims)

if 'time' not in dim_names:

   for time_step in nc_dict.keys():
      nc_dict[time_step] = nc_dict[time_step].assign_coords(coords={"time":time_step})



lucas_files = glob.iglob(f"{LUCAS}/{YEAR}/*{YEAR}_eo4bk.gpkg")

# gdfs = (gpd.read_file(file, layer = 'hd_data') for file in files )
gpkg_dict = {}

if YEAR == '2018':
    for file in lucas_files:

        # basename: returns the basename of the pathname path: e.g., basename(foo/bar.exe) --> 'bar.exe'
        # splitext: splits the pathname into pair (root, ext): e.g., splitext(bar.exe) --> ('bar','.exe)
        # index to avoid brakets 
        key = os.path.splitext(os.path.basename(file))[0]

        # Read the geopackage as geodataframe
        gdf = gpd.read_file(file)
        
        # stores the geodataframes in dictionary, for each key
        gpkg_dict[key] = gdf

elif YEAR == '2022':
    for file in lucas_files:

        # basename: returns the basename of the pathname path: e.g., basename(foo/bar.exe) --> 'bar.exe'
        # splitext: splits the pathname into pair (root, ext): e.g., splitext(bar.exe) --> ('bar','.exe)
        # index to avoid brakets 
        key = os.path.splitext(os.path.basename(file))[0]

        # Read the geopackage as geodataframe
        try:
            gdf = gpd.read_file(file, layer = f'{DETAIL_LEVEL}_data')
        
        # stores the geodataframes in dictionary, for each key
            gpkg_dict[key] = gdf
        except Exception:
            pass

croptypelist = list(gpkg_dict.keys())
#TODO ADD filter for nan
def main_function(idx):
    crop = croptypelist[idx]
    centroid_list = create_centroid_list(crop=crop, gpkg_dict=gpkg_dict)
    result_df_empty = pd.DataFrame()
    result_df = sampling(crop = crop,centroid_list = centroid_list,nc_dict = nc_dict,crop_nc_data = result_df_empty,ACRONYM = ACRONYM)
    result_df.to_csv(f'{SAVE_RESULT}/{YEAR}/{crop}_{ACRONYM}_300.csv', sep=';')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)
    number = int(sys.argv[1])
    main_function(number)

