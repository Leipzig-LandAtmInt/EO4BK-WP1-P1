# load packages
import os
import glob
import xarray as xr
import sys
from _smoothing_ import smoothing_methods
import numpy as np
from _get_phenometric_ import get_phenometric
from scores.continuous import rmse
import pandas as pd
from _build_datacube_ import build_datacube
import re
import zarr
import logging
import pandas as pd
# load directions

#HOME = '/home/sc.uni-leipzig.de/ds28kene/eo4bksentleD2.2_V0.1'
HOME = '/work/ds28kene-d2v2'

INPUT_FOLDER = 'output_sentinel/Europe'

YEAR = '2018'

# CROPTYPE = 'Barley'

DETAIL_LEVEL = 'hd'

CONTINENT = 'Europe'


# get Croptype variable from shell-script
if len(sys.argv) != 3:
    print("Usage: python main_execute.py <CROPTYPE> <SLURM_ARRAY_TASK_ID>")
    sys.exit(1)

# Get the crop type and SLURM_ARRAY_TASK_ID from the command-line arguments
CROPTYPE = sys.argv[1]

INPUT_DATA = f'{HOME}/{INPUT_FOLDER}/{YEAR}/{CROPTYPE}/{DETAIL_LEVEL}'


OUTPUT_DATA = f'{HOME}/output_pheno/{CONTINENT}/{YEAR}/{CROPTYPE}/{DETAIL_LEVEL}'

os.makedirs(OUTPUT_DATA, exist_ok = True)

NUT_LIST = os.listdir(INPUT_DATA) 


# load variables 

# for HANTS parameter

# As I understood the HANTS algorithm fits a convoluted set of Harmonics, by calculating the Fourier Coefficients (?)
# using least square method to the original datapoints. After the first fit, the residuals where calculated and 
# outlier detected. Then it fits another harmonic function, newly calculated by the the original datapoints - outlier,
# to the remaining points and another set of outliers are detected. This is repeated until either all the data are 
# within the threshold of fit error tolerance around the curve, or the minimum required points to calculate the 
# Fourier coefficients, which is (2*nf)-1 + dod is reached and no other curve can be fit.

# dod = Degree of overdetermination, which is a number of datapoints which can be added to the minimum required datapoints 
# to make the fit more robust. However, since all the np.nan need to be converted to 0, I assume this variable does not work as intended 

# fet = Fit error tolerance, defines the intervall in which all the datapoint should be to end the HANTS algorithm

# nf = number of frequencies, 0 frequency is the mean of the time-series, 1 frequency results in one amplitude, which is roughly speaking one season, 2 is two amplitudes,...

# delta = two supress high amplitudes, I don't know how that works. Value is taken from the literature and is normally 0.5

# HiLo = High or Low outlier direction. Can be set to 'Hi' or 'Lo'. Since at this stage HANTS does not accept np.nan, needs to be set to Lo to supress all 0 values

# low = Minimum value of the valid value range NIRv (0,...), NDVI (0,1), kNDVI (0,1). NIRv is not an index, but as far as I remeber the lowest value is not negative

# high = Maximum value of the valid value range. See above. Is defined on the run depending on ndvi, kndvi, nirv
# for kndvi and ndvi it is 1, and nirv it is the maximum value of the entire xarray dataset

# fill_val = Fill value of missing data 


# HiLo = 'Lo'

# low = 0  # is defined in the main_function 

# fet = 0.05

# nf = 4 

# dod = 0.5

# delta = 0.5 

# fill_val = 0

HiLo = 'Lo'

low = 0  # is defined in the main_function 

fet = 0.05

nf = 4 

dod = 5

delta = 0.5 

fill_val = 0


# define loggerfiles

log_dir = f'logger/phenometric_{YEAR}_hd/{CROPTYPE}/'
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

logger = setup_logger('successful download',f'{log_dir}/pheno_{CROPTYPE}_{YEAR}_{DETAIL_LEVEL}.log') 

# second logger file for error messages 

logger_error = setup_logger('error download', f'{log_dir}/pheno_ERROR_{CROPTYPE}_{YEAR}_{DETAIL_LEVEL}.log')

# define main_function 

data_list = []

def get_data(NUT_LIST):

    for nut_region in NUT_LIST:

        region_path = os.path.join(INPUT_DATA, nut_region, "*.zarr.zip")
        region_files = glob.glob(region_path)
        data_list.extend(region_files)

    
    return data_list
        

# because the data for europe is inside the nutregion subfolder only applies for Europe not for Brazil

data_list = []

if CONTINENT == 'Europe':
    

    data = get_data(NUT_LIST)
    
    
    data_list.append(data) 

else:

    data_list = glob.glob(os.path.join(f"{INPUT_DATA}/Brazil/*zarr.zip"))



def main_function(idx):
    

    data = data_list[idx]

    logger.info(f'Processing data: {data}, Processing ID: {idx}')
    

    try: 

        # needs to be sorted in an acending way for numpy to work

        xarray_data = xr.open_zarr(data).sortby("time")
        

        # some dataset include one day of the next year
        if CONTINENT == 'Europe':

            xarray_data = xarray_data.sel(time=xarray_data.time.dt.year == int(YEAR))

        result_dic_season1 = {}
        result_dic_season2= {}
        smoothed_arrays = {}
        smoothing_classes = {}
        rpd_dic = {}
        
        all_datacubes = []

        for vi_type in ['ndvi','nirv', 'kndvi', 'evi']: #, 'nirv', 'kndvi']:

            vis = xarray_data[f'sent_{vi_type}']
        
            smoothed_array_vi = np.full(vis.shape, np.nan)
            
                    # kndvi.shape[0] -> time
                    # kndvi.shape[1] -> lat
                    # kndvi.shape[2] -> lon 

            vi_dic = {}

            for i in range(vis.shape[1]):

                for j in range(vis.shape[2]):

                    y = vis[:,i,j]

                    time_array = xarray_data.time

                            # np.all -> Test whether all array elements along a given axis evaluate to True
                            # np.isnan -> Test element-wise for NaN and return as a boolean array

                            # checks if pixel only have nans

                    if np.all(np.isnan(y)):
                            continue 
            
                    try:
                        smoothing_class_vi = smoothing_methods(y, time_array)

                        if vi_type in ['nirv']:

                            high = np.nanmax(y)
                            low = np.nanmin(y)
                            HiLo = None
                        else:
                            high = 1
                            low = np.nanmin(y)
                            HiLo = HiLo
                        
                        vi_dic = smoothing_class_vi.HANTS(HiLo= HiLo, low = low, high = high, fet = fet, nf = nf, dod = dod, delta = delta, fill_val = fill_val, pad_len = 10)

                        smoothed = vi_dic[f'{smoothing_class_vi.varname}_HANTS']
                        smoothed_array_vi[:, i, j] = smoothed

                        y_true = y.compute()
                        mask = ~np.isnan(y_true)
                        
                        ss_res = np.sum((y_true[mask] - smoothed[mask])**2)
                        ss_tot = np.sum((y_true[mask] - np.nanmean(y_true[mask]))**2)
                        r2 = 1 - ss_res / ss_tot  
                        
                        if r2 > 0.998:
                            vi_dic = smoothing_class_vi.HANTS(HiLo= HiLo, low = low, high = high, fet = fet, nf = 3, dod = dod, delta = delta, fill_val = fill_val, pad_len = 10)

                            smoothed = vi_dic[f'{smoothing_class_vi.varname}_HANTS']
                            smoothed_array_vi[:, i, j] = smoothed

                    except Exception as e:

                        logger_error.error(f"Error at lat{i}, lon {j}:{e}")

            smoothed_arrays[vi_type] = smoothed_array_vi

            data_range = np.nanmax(smoothed_arrays[vi_type]) - np.nanmin(smoothed_arrays[vi_type])


            relative_prominence = 0.02 * data_range
            # smoothing_classes[vi_type] = smoothing_class_vi
            

            # here the Phenometrics are calculated on a pixel basis
            


            season1, season2, rpd = get_phenometric(smoothed_arrays[vi_type], xarray_data, 0.4, relative_prominence)
            result_dic_season1[vi_type] = season1
            result_dic_season2[vi_type] = season2   
            rpd_dic[vi_type]            = rpd

            # checks if all entries of the entire result_dic_season2 is empty 
            if all(np.all(pd.isna(v)) for v in result_dic_season2[vi_type].values()) is True:

                cube = build_datacube(xarray_data, xarray_data[f'sent_{vi_type}'], smoothed_arrays[vi_type], result_dic_season1[vi_type], rpd_dic[vi_type])
                
            else:

                cube = build_datacube(xarray_data, xarray_data[f'sent_{vi_type}'], smoothed_arrays[vi_type], result_dic_season1[vi_type],rpd_dic[vi_type], result_dic_season2[vi_type])


            all_datacubes.append(cube)

        datacube = xr.merge(all_datacubes)
            # save zarr block 

        if CONTINENT == 'Europe':

            s = data_list[idx].replace(f"{INPUT_DATA}","")
            match = re.search(rf'{CROPTYPE}_(\w{{2}})', s)


            nut0 = match.group(1)
            OUTPUT_SAVE_PATH = f'{OUTPUT_DATA}/{nut0}'
            os.makedirs(OUTPUT_SAVE_PATH, exist_ok = True)

            file_name = data_list[idx]
            file_name = file_name.replace(f"{INPUT_DATA}", "")
            file_name = re.sub(rf'^.*?({CROPTYPE}.*)$', r'\1', file_name)
            file_name = file_name.replace(".zarr.zip","")
                
            zip_path = f'{OUTPUT_SAVE_PATH}/{file_name}.zarr.zip'
            zip_store = zarr.ZipStore(zip_path, mode = 'w')
            datacube.to_zarr(store = zip_store, mode = 'w', compute = True)

            zip_store.close()

        else:

            OUTPUT_SAVE_PATH = f'{OUTPUT_DATA}'
            os.makedirs(OUTPUT_SAVE_PATH, exist_ok = True)

            file_name = data_list[idx]
            file_name = file_name.replace(f"{INPUT_DATA}", "")
            file_name = re.sub(rf'^.*?({CROPTYPE}.*)$', r'\1', file_name)
            file_name = file_name.replace(".zarr.zip","")
                
            zip_path = f'{OUTPUT_SAVE_PATH}/{file_name}.zarr.zip'
            zip_store = zarr.ZipStore(zip_path, mode = 'w')
            datacube.to_zarr(store = zip_store, mode = 'w', compute = True)

            zip_store.close()

        logger.info(f'Saved data: {data}, Processing ID: {idx}')

    except Exception as e:

        logger_error.error(f'Problem {e} of {data} of idx {idx} of pixel j: {j} and i: {i}')

            

# if __name__ == "__main__":
   

#     if len(sys.argv) != 2:
#         print("Usage: python script.py <number>")
#         sys.exit(1)

#     number = int(sys.argv[1])
#     main_function(number)
if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python script.py <number>")
        sys.exit(1)

    number = int(sys.argv[2])
    main_function(number)