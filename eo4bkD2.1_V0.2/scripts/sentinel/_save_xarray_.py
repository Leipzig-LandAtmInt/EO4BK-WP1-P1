# import logging
import os
import shutil 
import logging
import os
import zarr

from dotenv import load_dotenv


# load_dotenv('/home/sc.uni-leipzig.de/ds28kene/eo4bksentleD2.1_V0.1/eo4bksentleD2.1_V0.1/.env')

# YEAR = os.getenv('YEAR')
# #CROPTYPE = os.getenv('CROPTYPE')
# DETAIL_LEVEL = os.getenv('DETAIL_LEVEL')


# function saves the zarr
def save_as_zarr(output_eo4bk_minicube, lcs_eo4bkdata, main_direction, detail, MINICUBE_DUMMYSAVE):
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

    elif 'lc_eo4bk' in lcs_eo4bkdata:
        eo4bkclass = lcs_eo4bkdata['lc_eo4bk'].iloc[0] # For Brazil          
  
    nuts_0 =  lcs_eo4bkdata['nuts0'].iloc[0]
    nuts_3 = lcs_eo4bkdata['nuts3'].iloc[0]
    
    
    if 'survey_year_2022' in lcs_eo4bkdata:
        year = lcs_eo4bkdata['survey_year_2022'].iloc[0]
    elif 'survey_year_2018' in lcs_eo4bkdata:
        year = lcs_eo4bkdata['survey_year_2018'].iloc[0]
    dir = f'{main_direction}/{eo4bkclass}/{detail}/{nuts_0}'
    os.makedirs(dir, exist_ok=True)
    id = lcs_eo4bkdata['point_id'].iloc[0]


    # path to the .zipp archive
    zip_path = f'{dir}/{eo4bkclass}_{nuts_3}_{id}.zarr.zip'
    
    zip_store = zarr.ZipStore(zip_path, mode = 'w')
    
    output_eo4bk_minicube.to_zarr(store = zip_store, mode = 'w', compute = True)

    zip_store.close()
    # Open or create the ZipStore
    # zipp_stor = zarr.ZipStore(zip_path, mode='a')
        # Save the xarray dataset as a Zarr group
   # output_eo4bk_minicube.to_zarr(zipp_stor, group=f'{eo4bkclass}_{nuts_3}_{point_id}.zarr', mode='w', compute = True)
    
#    output_eo4bk_minicube.to_zarr(f"{dir}/{eo4bkclass}_{nuts_3}_{id}.zarr",
#           mode = "w", compute = True)
    
  
    shutil.rmtree(MINICUBE_DUMMYSAVE)
 
