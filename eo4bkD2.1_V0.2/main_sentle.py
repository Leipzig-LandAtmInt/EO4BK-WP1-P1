import os
import geopandas as gpd
import sys
sys.path.append(r"/home/sc.uni-leipzig.de/ds28kene/eo4bkD2.1_V0.2/scripts")
from sentinel import sentle_download, clipping_datacube, getdata_harmonized,create_xarray, save_as_zarr
import torch
import logging
import time 
from rasterio.crs import CRS
import xarray as xr
import glob

# Define where the folders are

# the variables that are set by the user are written in upper case, the variables that are defined during the pipeline are written in lower case


SCRIPT_FOLDER  = "/home/sc.uni-leipzig.de/ds28kene/eo4bkD2.1_V0.2"
OUTPUT_FOLDER = "/work/ds28kene-d2v2"
CONTINENT = 'Brazil' # alternative set to Brazil 
REFERENCE_DATA_FOLDER = f"{SCRIPT_FOLDER}/ref_data/{CONTINENT}"

YEAR1 = "2017" 
YEAR2 = "2018"
YEAR_OVERLAP = "1718"

if CONTINENT == 'Europe':
    YEAR_ATTR = YEAR2
else:
    YEAR_ATTR = YEAR_OVERLAP

MINICUBE_FOLDER = f"{OUTPUT_FOLDER}/output_sentinel/{CONTINENT}/{YEAR2}"
os.makedirs(MINICUBE_FOLDER, exist_ok = True)
DETAIL_LEVEL = "hd"
TARGET_CRS  = CRS.from_string("EPSG:5641") #CRS.from_string("EPSG:3035")
TIME_SPAN = f"{YEAR1}-08-01/{YEAR2}-07-31"   #f"{YEAR1}-08-01/{YEAR2}-07-31"

REFERENCE_SOURCE = 'CONAB'




# takes the CROPTYPE from crops_100.sh shell-script
if len(sys.argv) != 3:
    print("Usage: python main_execute.py <CROPTYPE> <SLURM_ARRAY_TASK_ID>")
    sys.exit(1)

# Get the crop type and SLURM_ARRAY_TASK_ID from the command-line arguments
CROPTYPE = sys.argv[1]


minicube_dummysave_folder = (f'{OUTPUT_FOLDER}/output_sentinel/{CONTINENT}/dummyfolder/{CROPTYPE}')
os.makedirs(minicube_dummysave_folder, exist_ok = True)


# Get the reference data, which should be in a geopackage format
if CONTINENT == 'Brazil':
    REF_DATA = gpd.read_file(f"{REFERENCE_DATA_FOLDER}/{CROPTYPE}_{YEAR_OVERLAP}_{REFERENCE_SOURCE}_eo4bk.gpkg")
    
elif CONTINENT == 'Europe':
    REF_DATA = gpd.read_file(f'{REFERENCE_DATA_FOLDER}/{YEAR2}/{CROPTYPE}_{YEAR2}_eo4bk.gpkg', layer = f'{DETAIL_LEVEL}_data')


# only take into account reference data bigger than 100 sqm (minimum size of a sentinel pixel)

ref_data_100sqm = REF_DATA[REF_DATA['poly_area_sqm'] > 100]

id_list = list(ref_data_100sqm['point_id'])


# In case the job-pipeline crushes:


CROP_LIST = os.listdir(f'{MINICUBE_FOLDER}')
data_list = []

def get_data(NUT_LIST):
    # This function collects the files from all nut regions
    data_list = []
    for nut_region in NUT_LIST:
        region_path = os.path.join(INPUT_DATA, nut_region, "*.zarr.zip")
        region_files = glob.glob(region_path)
        data_list.extend(region_files)

    return data_list
        
# because the data for europe is inside the nutregion subfolder only applies for Europe not for Brazil
if CONTINENT == 'Europe':
    
    try: 
        # Initialize the list to collect data for this crop
        INPUT_DATA = f'{OUTPUT_FOLDER}/{YEAR2}/{CROPTYPE}/{DETAIL_LEVEL}'
        NUT_LIST = os.listdir(INPUT_DATA)
        crop_data_list = get_data(NUT_LIST)
        crop_data_list = [os.path.basename(f).replace(".zarr.zip", "") for f in crop_data_list]
        crop_data_list = [os.path.basename(f).replace(f"{CROPTYPE}_", "") for f in crop_data_list]
        crop_data_list = [item.split('_')[1] for item in crop_data_list]
        #file_names = [os.path.basename(f).replace("Soybean_RS_", "") for f in file_names]
        
        # Print the number of files found for the crop
        # print(crop, len(crop_data_list))
        # print(crop, crop_data_list)

        id_list = [id_ for id_ in id_list if id_ not in crop_data_list]



    except FileNotFoundError:
        pass

#TODO add structure of brazil 



# define the main direction, the save function then builds additional direction inside this direciton 
# main_direciton = MINICUBE_OUT




# The logger-set-up is defined here
# Folder for the logger_file
log_dir = f'logger/sentinel_{CONTINENT}_{YEAR2}_{DETAIL_LEVEL}/{CROPTYPE}'
os.makedirs(log_dir, exist_ok=True)  


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
    
# first logger file for working polygons 
logger_info = setup_logger('successful download',f'{log_dir}/sentinel_{CONTINENT}_{CROPTYPE}_{YEAR2}_{DETAIL_LEVEL}.log') 

# second logger file for error messages 
logger_error = setup_logger('error download', f'{log_dir}/sentinel_ERROR_{CONTINENT}_{CROPTYPE}_{YEAR2}_{DETAIL_LEVEL}.log')


        



# function 
def main_function(idx):
    '''
    To execute all the above in the right sequence.
    '''
    # global counter
    i = id_list[idx]
    logger_info.info(f'Point ID: {i}, Processing ID: {idx}')
    
    try: 
        sentle_download(lcs_eo4bkdata= ref_data_100sqm[ref_data_100sqm['point_id']== i], MINICUBE_DUMMYSAVE = f'{minicube_dummysave_folder}/{idx}',targetcrs = TARGET_CRS, time_span = TIME_SPAN )
    except Exception as e:
        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not download data. Problem: {e}')
        return 
    try:
        sentle_dummy_save = xr.open_zarr(f'{minicube_dummysave_folder}/{idx}')
        output_download_clipped = clipping_datacube(sentle_dummy_save, ref_data_100sqm[ref_data_100sqm['point_id']== i])
    except Exception as e:
        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not clipp data. Problem: {e}')
        return 
    try:
        # important to set hd = True when dealing with hd data, and ld when dealing with low detail data. 
        variables = getdata_harmonized(output_download_clipped=output_download_clipped, lcs_eo4bkdata= ref_data_100sqm[ref_data_100sqm['point_id']== i])
        # It is less important here, but savings are being made in the wrong direction. 
        xarray_output = create_xarray(variables, YEAR_ATTR, REFERENCE_SOURCE)
    except Exception as e:
        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not create xarray. Problem: {e}')
        return
    try:
        logger_info.info(f"> Save the Minicube {idx} ...")
        
        save_as_zarr(output_eo4bk_minicube=xarray_output, lcs_eo4bkdata= ref_data_100sqm[ref_data_100sqm['point_id']== i], main_direction=MINICUBE_FOLDER, detail = DETAIL_LEVEL, MINICUBE_DUMMYSAVE= f'{minicube_dummysave_folder}/{idx}')
        
        logger_info.info(f"> Successfully saved the Minicube {idx} at: {MINICUBE_FOLDER}/{CROPTYPE}_{idx}") # logs when it is saved 

    except Exception as e:
        logger_error.error(f'Point ID: {i}, Processing ID: {idx}; Did not save xarray as datacube. Problem: {e}')
        return 
        
    logger_info.info(f"> Starts Sleeping") # Log when Pause starts
    time.sleep(20)
    logger_info.info(f"> Ends Sleeping")
    logger_info.info(f"Save Point ID: {i} & Processing ID: {idx}")



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python script.py <number>")
        sys.exit(1)

    number = int(sys.argv[2])
    main_function(number)


# # if __name__ == "__main__":
   

# #     if len(sys.argv) != 2:
# #         print("Usage: python script.py <number>")
# #         sys.exit(1)

# #     number = int(sys.argv[1])
# #     main_function(number)
