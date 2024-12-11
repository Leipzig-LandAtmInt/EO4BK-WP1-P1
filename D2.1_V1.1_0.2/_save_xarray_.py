# import logging
import os
import shutil 
import logging
import os
import zarr

from dotenv import load_dotenv


load_dotenv('/home/sc.uni-leipzig.de/ds28kene/eo4bksentleD2.1_V0.1/eo4bksentleD2.1_V0.1/.env')

YEAR = os.getenv('YEAR')
CROPTYPE = os.getenv('CROPTYPE')
DETAIL_LEVEL = os.getenv('DETAIL_LEVEL')


# is for logging
#logging.basicConfig(
#    level=logging.INFO,  # Set the desired logging level
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

# logger for successfully download datacubes
logger = setup_logger('successful download', f'sentinel_{CROPTYPE}_{YEAR}_{DETAIL_LEVEL}.log') 
# logger for unsuccessfully downloaded datacubes
logger_error = setup_logger('error download', f'sentinel_ERROR_{CROPTYPE}_{YEAR}_{DETAIL_LEVEL}.log')

# function saves the zarr
def save_as_zarr(output_eo4bk_minicube,lcs_eo4bkdata, main_direction, detail, MINICUBE_DUMMYSAVE):
    '''
    This function save the data from xarray_output to a zarr file
    '''
    # keys = output_eo4bk_minicube.keys()
    # da = output_eo4bk_minicube #[f'{list(keys)[0]}']

    main_direction = main_direction
    
    # defines the output direction
    if 'lc_eo4bk_2022' in lcs_eo4bkdata:
        eo4bkclass =lcs_eo4bkdata['lc_eo4bk_2022'].iloc[0]

    elif 'lc_eo4bk_2018' in lcs_eo4bkdata:
        eo4bkclass = lcs_eo4bkdata['lc_eo4bk_2018'].iloc[0]
            
    nuts_0 =  lcs_eo4bkdata['nuts0'].iloc[0]
    nuts_3 = lcs_eo4bkdata['nuts3'].iloc[0]
    if 'survey_year_2022' in lcs_eo4bkdata:
        year = lcs_eo4bkdata['survey_year_2022'].iloc[0]
    elif 'survey_year_2018' in lcs_eo4bkdata:
        year = lcs_eo4bkdata['survey_year_2018'].iloc[0]
    dir = f'{main_direction}/{year}/{eo4bkclass}/{detail}/{nuts_0}'
    os.makedirs(dir, exist_ok=True)
    id = lcs_eo4bkdata['point_id'].iloc[0]

    logger.info(f"> Save the Minicube {id} ...") # logs when it starts saving, not before, because saving is what takes the most time

    # NOTE: Save as .zarr
#   output_eo4bk_minicube.to_zarr(f"{dir}/{eo4bkclass}_{nuts_3}_{id}.zarr",
#           mode = "w", compute = True)

    # NOTE: Update save in .zip file
    
    # path to the .zipp archive

    zip_path = f'{dir}/{eo4bkclass}_{nuts_3}_{id}.zip'

    # Initialize ZipStore
    zip_store = zarr.ZipStore(zip_path, mode = 'w')

    # save into ZipStore
    output_eo4bk_minicube.to_zarr(store = zip_store, mode = 'w', compute = True)

    # close Zipstore

    zip_store.close()

    logger.info(f"> Successfully saved the Minicube {id} at: {dir}/{eo4bkclass}_{nuts_3}_{id}") # logs when it is saved 
  
    shutil.rmtree(MINICUBE_DUMMYSAVE)
 
