import os
from dotenv import load_dotenv
import geopandas as gpd
import sys
from _downloadsentle_ import sentle_download
from _clipp_download_output_ import clipping_datacube
from _getdata_harmo_ import getdata_harmonized
from _create_xarray_harmo_ import create_xarray
from _save_xarray_ import save_as_zarr
import torch
import logging
import time 
from rasterio.crs import CRS
import xarray as xr


# environment
load_dotenv(f'/net/projects/EO4BK/WP1/P1-EO4BK/scripts/EO4BK-Github/D2.1_V1.1_0.2/.env')

HOME = os.getenv('HOME')
LUCAS = os.getenv('LUCAS_D21_V01')
MINICUBE_OUT= os.getenv('MINICUBE_OUT_D21_V01')
YEAR = os.getenv('YEAR')
CROPTYPE = os.getenv('CROPTYPE')
DETAIL_LEVEL = os.getenv('DETAIL_LEVEL')

MINICUBE_DUMMYSAVE = (f'{MINICUBE_OUT}/dummyfolder')

# Logger
#logging.basicConfig(
#     level=logging.INFO,  # Set the desired logging level
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.StreamHandler(),  # Logs to the console
#         logging.FileHandler(f'Logs/sentinel_{CROPTYPE}_{YEAR}_{DETAIL_LEVEL}.log')  # Logs to a file
#     ]
# )
# logger = logging.getLogger()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
    
# first logger file for working polygons 
logger = setup_logger('successful download',f'sentinel_{CROPTYPE}_{YEAR}_{DETAIL_LEVEL}.log') 

# second logger file for error messages 
logger_error = setup_logger('error download', f'sentinel_ERROR_{CROPTYPE}_{YEAR}_{DETAIL_LEVEL}.log')


# Polygon
lucaspoly = gpd.read_file(f'{HOME}/{LUCAS}/{YEAR}/{CROPTYPE}_{YEAR}_eo4bk.gpkg', layer = f'{DETAIL_LEVEL}_data')

# Polygon-CRS
targetcrs  = CRS.from_string("EPSG:3035")
# change time span of download period
time_span = f"{YEAR}-01-01/{YEAR}-12-31"

# because polygons less then 100 sqm are smaller than one pixel
lucaspoly_ov_100sqm = lucaspoly[lucaspoly['poly_area_sqm'] > 100]

# to have a test subset, only downloads the first two polygons
id_list = list(lucaspoly_ov_100sqm['point_id'])

# define the main direction, the save function then builds additional direction inside this direciton 
main_direciton = MINICUBE_OUT

# function 
def main_function(idx):
    '''
    To execute all the above in the right sequence.
    '''
    # global counter
    i = id_list[idx]
    logger.info(f'Point ID: {i}, Processing ID: {idx}')
    logger_error.info(f'Point ID: {i}, Processing ID: {idx}')
    try: 
        sentle_download(lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i], MINICUBE_DUMMYSAVE = f'{MINICUBE_DUMMYSAVE}/{idx}',targetcrs = targetcrs, time_span = time_span )
    except Exception as e:
        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not download data.')
        return 
    try:
        sentle_dummy_save = xr.open_zarr(f'{MINICUBE_DUMMYSAVE}/{idx}')
        output_download_clipped = clipping_datacube(sentle_dummy_save, lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i])
    except Exception as e:
        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not clip data.')
        return 
    try:
        # important to set hd = True when dealing with hd data, and ld when dealing with low detail data. 
        variables = getdata_harmonized(output_download_clipped=output_download_clipped, lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i])
        # It is less important here, but savings are being made in the wrong direction. 
        xarray_output = create_xarray(variables, YEAR)
    except Exception as e:
        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not create xarray.')
        return
    try:
        save_as_zarr(output_eo4bk_minicube=xarray_output, lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i], main_direction=main_direciton, detail = DETAIL_LEVEL, MINICUBE_DUMMYSAVE= f'{MINICUBE_DUMMYSAVE}/{idx}')
    except Exception as e:
        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not save xarray as datacube.')
        return 
        
    logger.info(f"> Starts Sleeping") # Log when Pause starts
    time.sleep(30)
    logger.info(f"> Ends Sleeping")
    logger.info(f"Save Point ID: {i} & Processing ID: {idx}")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)

    number = int(sys.argv[1])
    main_function(number)
