import os
from dotenv import load_dotenv
import sys
from _dirdict_ import create_dic_from_dir
from _check_quality_zarr_ import zarr_quality_check


load_dotenv('/home/sc.uni-leipzig.de/ds28kene/Github_Upload/EO4BK/D2.1_V1.1_0.2/.env')


HOME = f'{os.getenv("HOME")}/Github_Upload/EO4BK'
LUCAS = os.getenv('LUCAS_D21_V01')
MINICUBE_OUT= os.getenv('MINICUBE_OUT_D21_V01')
YEAR = os.getenv('YEAR')
CROPTYPE = 'Other_grassland' #os.getenv('CROPTYPE')
DETAIL_LEVEL = os.getenv('DETAIL_LEVEL')
ZARR_ZIP_DATA = "zarr_zip"
# load data 

data_path = f'{HOME}/{MINICUBE_OUT}/{YEAR}/{CROPTYPE}/{DETAIL_LEVEL}'

nut3_list = os.listdir(data_path)

def main_function(idx):
    i = nut3_list[idx]
    zarr_dic = create_dic_from_dir(data_path, ZARR_ZIP_DATA, i)
    zarr_quality_check(zarr_dic, data_path, i, CROPTYPE)


if __name__ =="__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)
    number = int(sys.argv[1])
    main_function(number)