import logging
import os

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

# function saves the zarr
def save_as_zarr(output_eo4bk_minicube,lcs_eo4bkdata, main_direction, detail):
    '''
    This function save the data from xarray_output to a zarr file
    '''
    # keys = output_eo4bk_minicube.keys()
    # da = output_eo4bk_minicube #[f'{list(keys)[0]}']

    main_direction = main_direction
    
    # # is to create different folders for ld and hd data. 
    # if hd == True:
    #     detail = 'hd'
    # else:
    #     detail = 'ld'

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
    output_eo4bk_minicube.to_zarr(f"{dir}/{eo4bkclass}_{nuts_3}_{id}.zarr",
           mode = "w", compute = True)
    
    logger.info(f"> Successfully saved the Minicube {id} at: {dir}/{eo4bkclass}_{nuts_3}_{id}") # logs when it is saved 
 
