import os 
from dotenv import load_dotenv
import geopandas as gpd
import sys
import logging
import time
import xarray as xr
import rasterio
import glob 
from _sample_cglob_ import sample_cglob
from _reproject_ import reproject_datacube
from _save_xarray_ import save_as_zarr
from _build_datacube_ import build_datacube
import threading 
import itertools

# INPUTDATA
HOME = 'C:/Users/dominic/Documents/PROJECTS/EO4BK_CGLOB/data'

YEAR1 = '2017'
YEAR2 = '2018'
YEAR_overlap = '1718'

VARIABLE = 'FCOVER'

DETAIL_LEVEL = 'hd'
CROPTYPE = 'Rice'


POLYGON = gpd.read_file(f"{HOME}/brazil/{CROPTYPE}_{YEAR_overlap}_eo4bk.gpkg")

# CGLOB Data 
VARIABLE = 'FCOVER'

CGLOB_FILES_YEAR1 = glob.iglob(f"{HOME}/cglob_{VARIABLE}300_{YEAR1}_GLOBE/*.nc")# & 'YEAR2/*.nc' 

CGLOB_FILES_YEAR2 = glob.iglob(f"{HOME}/cglob_{VARIABLE}300_{YEAR2}_GLOBE/*.nc")# & 'YEAR2/*.nc' 

CGLOB_FILES = itertools.chain(CGLOB_FILES_YEAR1, CGLOB_FILES_YEAR2)

# Output 

OUTPUT_MAIN = f'C:/Users/dominic/Documents/PROJECTS/EO4BK_CGLOB/data/cglob_datacube/Output_{VARIABLE}/{YEAR_overlap}'

os.makedirs(OUTPUT_MAIN, exist_ok = True)
# Sample-list

POLYGON_ov_100sqm = POLYGON[POLYGON['poly_area_sqm'] > 100]

id_list = list(POLYGON_ov_100sqm['point_id'])
#id_list = id_list[9900:]

# Logger 
log_dir = f'logger/clgob_{YEAR_overlap}_hd/{CROPTYPE}/'
os.makedirs(log_dir, exist_ok=True)  # Creates the directory if it doesn't exist


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
    
# first logger file for working polygons 

logger = setup_logger('successful download',f'{log_dir}/cglob_{VARIABLE}_{CROPTYPE}_{YEAR_overlap}_{DETAIL_LEVEL}.log') 

# second logger file for error messages 

logger_error = setup_logger('error download', f'{log_dir}/cglob_ERROR_{VARIABLE}_{CROPTYPE}_{YEAR_overlap}_{DETAIL_LEVEL}.log')


def main_function(idx):


    i = id_list[idx]
    logger.info(f'Point ID: {i}, Processing ID: {idx}')
    logger_error.info(f'Point ID: {i}, Processing ID: {idx}')
    try:
        value_dic, lon, lat   = sample_cglob(NC_FILES = CGLOB_FILES, polygon = POLYGON_ov_100sqm[POLYGON_ov_100sqm['point_id'] == i], VARIABLE = VARIABLE)
        
    except Exception as e:

        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not sample data.')
    
    try: 
        datacube = build_datacube(value_dic, lon, lat, POLYGON_ov_100sqm[POLYGON_ov_100sqm['point_id'] == i], CROPTYPE, VARIABLE, YEAR1, YEAR2, YEAR_overlap)

    except Exception as e:


      logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not create datacube.')
       
    try:
        datacube = reproject_datacube(datacube)

    except Exception as e:


        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not reproject datacube.')
    
    try: 
        save_as_zarr(output_eo4bk_minicube=datacube,CROPTYPE = CROPTYPE, lcs_eo4bkdata= POLYGON_ov_100sqm[POLYGON_ov_100sqm['point_id']== i], main_direction=OUTPUT_MAIN, detail = DETAIL_LEVEL)

    except Exception as e:
        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not save xarray as datacube.')
        return 
    logger.info(f"> Starts Sleeping") # Log when Pause starts
    time.sleep(10)
    logger.info(f"> Ends Sleeping")
    logger.info(f"Save Point ID: {i} & Processing ID: {idx}")



if __name__ == "__main__":
   

    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)

    number = int(sys.argv[1])
    main_function(number)
