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
# import numpy as np

# is for logging
logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Logs to the console
        logging.FileHandler('sentinel_processing_2510.log')  # Logs to a file
    ]
)
logger = logging.getLogger()


# environment
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
torch.cuda.device_count()
# Define working direction path 

load_dotenv()

LUCAS = os.getenv('LUCAS_D21_V01')
MINICUBE_OUT= os.getenv('MINICUBE_OUT_D21_V01')
# MINICUBE_OUT= os.getenv('MINICUBE_OUT')
# MINICUBE_OUT = os.getenv('MINICUBE_OUT_2018')

lucaspoly = gpd.read_file(f'{LUCAS}/2018/Barley_2018_eo4bk.gpkg', layer = 'hd_data')



# change time span of download period
time_span = "2018-01-01/2018-12-31"

# because polygons less then 100 sqm are smaller than one pixel
lucaspoly_ov_100sqm = lucaspoly[lucaspoly['poly_area_sqm'] > 100]

# to have a test subset, only downloads the first two polygons
id_list = list(lucaspoly_ov_100sqm['point_id']) #[:3]

# define the main direction, the save function then builds additional direction inside this direciton 
main_direciton = MINICUBE_OUT

# counter = 0
# function 
def main_function(idx):
    '''
    To execute all the above in the right sequence.
    '''
    global counter
    i = id_list[idx]
    output_download = sentle_download(lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i], time_span = time_span )
    # important to set hd = True when dealing with hd data, and ld when dealing with low detail data. 
    variables = getdata_harmonized(output_download=output_download, lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i])
    # It is less important here, but savings are being made in the wrong direction. 
    xarray_output = create_xarray(variables)
    save_as_zarr(output_eo4bk_minicube=xarray_output, lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i], main_direction=main_direciton, hd = True)

    # for i in id_list:

    #     output_download = sentle_download(lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i], time_span = time_span )
    #     # important to set hd = True when dealing with hd data, and ld when dealing with low detail data. 
    #     variables = _getdata_(output_download=output_download, lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i])
    #     # It is less important here, but savings are being made in the wrong direction. 
    #     xarray_output = _create_xarray_(variables)
    #     save_as_zarr(output_eo4bk_minicube=xarray_output, lcs_eo4bkdata= lucaspoly_ov_100sqm[lucaspoly_ov_100sqm['point_id']== i], main_direction=main_direciton, hd = False)
    #     # return xarray_output
    # counter += 1
    # logger.info(f"> Successfully processed {counter} polygons.")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)

    number = int(sys.argv[1])
    main_function(number)
