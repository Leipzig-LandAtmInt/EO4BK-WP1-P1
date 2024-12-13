import xarray as xr
import zarr 
import pandas as pd
import os 
import glob
import geopandas as gpd


ZARR_ZIP_DATA = "zarr_zip"
GEOPACKAGE_DATA = "gpkg"
ZARR_DATA = "zarr"

def create_dic_from_dir(data_path, datatype, *args, suffix = None, shapefile = None):


    # check if args is called to create the right path
    if args: 

        args_path = "/".join(args)
        file_path = f'{data_path}/{args_path}'

    else:

        file_path = f'{data_path}'

    if datatype == ZARR_ZIP_DATA:
        file_path = f'{file_path}/*zarr.zip'

    elif datatype == ZARR_DATA:

        file_path = f'{file_path}/*.zarr'
    
    elif datatype == GEOPACKAGE_DATA:

        file_path = f'{file_path}/*gpkg'

    files = list(glob.iglob(file_path))


    data_dict = {}
    
    for file in files:

        # creates key for dictionary 
        key = os.path.splitext(os.path.basename(file))[0]

        # checks whether its ZARR_ZIP
        if datatype == ZARR_ZIP_DATA:    
            store = zarr.ZipStore(f'{file}', mode = 'r')

            data = xr.open_zarr(store=store)
        
        elif datatype == ZARR_DATA:

            data = xr.open_xarray(f'{file}')

        elif datatype == GEOPACKAGE_DATA:

            data = gpd.read_file(f'{file}', layer = f'{shapefile}_data' or "defaul_layer")
            

        data_dict[key] = data
    return data_dict