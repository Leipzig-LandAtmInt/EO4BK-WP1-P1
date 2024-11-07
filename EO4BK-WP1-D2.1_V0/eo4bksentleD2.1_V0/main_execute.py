import os
from dotenv import load_dotenv
import geopandas as gpd
import sys
from _downloadsentle_ import sentle_download
from _getdata_harmo_ import getdata_harmonized
from _create_xarray_harmo_ import create_xarray
from _save_xarray_ import save_as_zarr
import torch
import logging
import time 


# environment
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
torch.cuda.device_count()
# Define working direction path 

load_dotenv()

LUCAS = os.getenv('LUCAS_D21_V01')
MINICUBE_OUT= os.getenv('MINICUBE_OUT_D21_V01')
YEAR = os.getenv('YEAR')
CROPTYPE = os.getenv('CROPTYPE')
DETAIL_LEVEL = os.getenv('DETAIL_LEVEL')

logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Logs to the console
        logging.FileHandler(f'sentinel_{CROPTYPE}_{YEAR}_{DETAIL_LEVEL}.log')  # Logs to a file
    ]
)
logger = logging.getLogger()

lucaspoly = gpd.read_file(f'{LUCAS}/{YEAR}/{CROPTYPE}_2018_eo4bk.gpkg', layer = f'{DETAIL_LEVEL}_data')


# change time span of download period
time_span = f"{YEAR}-01-01/{YEAR}-12-31"

# because polygons less then 100 sqm are smaller than one pixel
lucaspoly_ov_100sqm = lucaspoly[lucaspoly['poly_area_sqm'] > 100]

# to have a test subset, only downloads the first two polygons
id_list = list(lucaspoly_ov_100sqm['point_id']) #[:3]

# define the main direction, the save function then builds additional direction inside this direciton 
main_direciton = MINICUBE_OUT

# function 
def main_function(idx):
    '''
    To execute all the above in the right sequence.
    '''
    # global counter
    i = id_list[idx]
    output_download = sentle_download(lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i], time_span = time_span )
    # important to set hd = True when dealing with hd data, and ld when dealing with low detail data. 
    variables = getdata_harmonized(output_download=output_download, lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i])
    # It is less important here, but savings are being made in the wrong direction. 
    xarray_output = create_xarray(variables, YEAR)
    save_as_zarr(output_eo4bk_minicube=xarray_output, lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i], main_direction=main_direciton, detail = DETAIL_LEVEL)
    logger.info(f"> Starts Sleeping") # Log when Pause starts
    time.sleep(30)
    logger.info(f"> Ends Sleeping")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)

    number = int(sys.argv[1])
    main_function(number)
