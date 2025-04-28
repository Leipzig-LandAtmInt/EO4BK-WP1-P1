# import logging
import os
import shutil 
import logging
import os
import zarr

#from dotenv import load_dotenv


#load_dotenv('/home/sc.uni-leipzig.de/ds28kene/eo4bksentleD2.1_V0.1/eo4bksentleD2.1_V0.1/.env')

#YEAR = os.getenv('YEAR')
#CROPTYPE = os.getenv('CROPTYPE')
#DETAIL_LEVEL = os.getenv('DETAIL_LEVEL')

#YEAR = '2018'



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



# function saves the zarr
def save_as_zarr(output_eo4bk_minicube, CROPTYPE, lcs_eo4bkdata, main_direction ,detail):
    '''
    This function save the data from xarray_output to a zarr file
    '''
    
    # keys = output_eo4bk_minicube.keys()
    # da = output_eo4bk_minicube #[f'{list(keys)[0]}']

    main_direction = main_direction
    
    # defines the output direction
    eo4bkclass = CROPTYPE

            
    nuts_0 =  lcs_eo4bkdata['nuts0'].iloc[0]
    nuts_3 = lcs_eo4bkdata['nuts3'].iloc[0]
    

    dir = f'{main_direction}/{eo4bkclass}/{detail}/{nuts_0}'
    os.makedirs(dir, exist_ok=True)
    id = lcs_eo4bkdata['point_id'].iloc[0]


    # NOTE: Save as .zarr
#   output_eo4bk_minicube.to_zarr(f"{dir}/{eo4bkclass}_{nuts_3}_{id}.zarr",
#           mode = "w", compute = True)

    # NOTE: Update save in .zip file
    
    # path to the .zipp archive

    zip_path = f'{dir}/{eo4bkclass}_{nuts_3}_{id}.zarr.zip'

    # Initialize ZipStore
    zip_store = zarr.ZipStore(zip_path, mode = 'w')

    # save into ZipStore
    output_eo4bk_minicube.to_zarr(store = zip_store, mode = 'w', compute = True)

    # close Zipstore

    zip_store.close()

  
    #shutil.rmtree(MINICUBE_DUMMYSAVE)
 
