from terracatalogueclient import Catalogue
from terracatalogueclient.config import CatalogueConfig, CatalogueEnvironment
import jinja2
import datetime as dt
import pandas as pd
import sys
import logging

config = CatalogueConfig.from_environment(CatalogueEnvironment.CGLS)
catalogue = Catalogue(config)

YEAR = '2018'

COLLECTION = "clms_global_fcover_300m_v1_10daily_netcdf"
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

if YEAR == '2018':
    df = df[~df['Identifier'].str.contains("RT")] # for 2018

elif YEAR == '2022':
    df = df[df['Identifier'].str.contains("RT6")]   # for 2022





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
    # New List 
    for x in product_list:
        if x.id in filtered_identifiers:
            download_list.append(x)


    logger.info(f'Download: {filtered_identifiers} of {COLLECTION}, Number: {idx}')
    try:
        catalogue.download_products(download_list, './')
    except Exception as e:
        logger_error.error(f'Download: {filtered_identifiers} of {COLLECTION}, Number: {idx}; Did not download data')


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)

    number = int(sys.argv[1])
    main_download(number)