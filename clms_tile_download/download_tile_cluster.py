from terracatalogueclient import Catalogue
from terracatalogueclient.config import CatalogueConfig, CatalogueEnvironment
import jinja2
import datetime as dt
import pandas as pd
import sys
import logging
import os 
import shutil

config = CatalogueConfig.from_environment(CatalogueEnvironment.CGLS)
catalogue = Catalogue(config)

variable = 'fcover'

YEAR = '2018'

COLLECTION = f"clms_global_{variable}_300m_v1_10daily_netcdf"
rows = []
# get_products needs argument collection 
# dt.date (YEAR, D, M)
products = catalogue.get_products(
    collection = COLLECTION,
    # geometry = geometry_wkt.iloc[0],   # is always a global product
    start=f"{YEAR}-01-01",
    end = f"{YEAR}-12-31"
    )

for product in products:
    rows.append([product.id, product.data[0].href, (product.data[0].length/(1024*1024))])

df = pd.DataFrame(data = rows, columns = ['Identifier', 'URL', 'Size(MB)'])

#https://land.copernicus.eu/en/technical-library/product-user-manual-fraction-of-green-vegetation-cover-333-m-version-1-1/@@download/file
# Description of RT, RT is omitted in the final product 
# Becaue End does not work just filter for 2018
df = df[df['Identifier'].str.contains(f"{YEAR}")]
# Because the final product does not contain RT

# Because 2020 there a two July and Augsut Products for 2020:
if YEAR == '2020':
    df = df[(df['Identifier'].str.contains("RT6")) | (~df['Identifier'].str.contains("RT"))]
    df = df[(~df['Identifier'].str.contains("c_gls_LAI300_202008310000")) & 
            (~df['Identifier'].str.contains("c_gls_LAI300_20200820000"))  & 
            (~df['Identifier'].str.contains("c_gls_LAI300_202008100000")) & 
            (~df['Identifier'].str.contains("c_gls_LAI300_202007310000")) & 
            (~df['Identifier'].str.contains("c_gls_LAI300_202007200000")) & 
            (~df['Identifier'].str.contains("c_gls_LAI300_202007100000"))]

if YEAR == '2017' or YEAR == '2018' or YEAR == '2019':
    df = df[~df['Identifier'].str.contains("RT")]  # for 2018 // 2017

elif YEAR == '2021' or YEAR == '2022' or YEAR == '2023':
    df = df[df['Identifier'].str.contains("RT6")]   # for 2022'





formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# first logger file for working polygons 
logger = setup_logger('successful download',f'sentinel_{COLLECTION}.log') 

# second logger file for error messages 
logger_error = setup_logger('error download', f'sentinel_ERROR_{COLLECTION}.log')


def main_download(idx):
    # Short List 
    filtered_identifiers = df['Identifier'].tolist()[idx]

    # Long List 
    product_list = list(catalogue.get_products(
        COLLECTION,
    )) 

    download_list = []
    
    download_folder = os.makedirs(f'cglob_{variable.upper()}300_{YEAR}_GLOBE', exist_ok = True)
    download_folder = f'cglob_{variable.upper()}300_{YEAR}_GLOBE'


    # New List 
    for x in product_list:
        if x.id in filtered_identifiers:
            download_list.append(x)


    logger.info(f'Download: {filtered_identifiers} of {COLLECTION}, Number: {idx}')
    try:
        catalogue.download_products(download_list, f'{download_folder}/./',raise_on_failure = True)
    except Exception as e:
        logger_error.error(f'Download: {filtered_identifiers} of {COLLECTION}, Number: {idx}; Did not download data')

    
    file_list = os.listdir(f'{download_folder}')

    for folder in file_list:

        folder_path = os.path.join(download_folder, folder)  # Full path of the subfolder
        
        # Ensure it's a directory before proceeding
        if os.path.isdir(folder_path):
            try:
                file_to_move = os.path.join(folder_path, f"{folder}.nc")  # File inside subfolder
            
                if os.path.exists(file_to_move):  # Check if the file exists
                    shutil.move(file_to_move, download_folder)  # Move the file
                else:
                    print(f"File not found: {file_to_move}")
                os.rmdir(folder_path)
            except NotADirectoryError:
                pass
        


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)

    number = int(sys.argv[1])
    main_download(number)