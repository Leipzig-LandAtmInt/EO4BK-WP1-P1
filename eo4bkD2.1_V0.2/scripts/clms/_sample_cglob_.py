import rasterio
from rasterio import mask
from rasterio.transform import xy
import shapely
import xarray as xr
import numpy as np
import logging
import glob 
import os 

import warnings

import h5py



def sample_cglob(NC_FILES, polygon, VARIABLE):

    

    
    
    polygon = polygon.to_crs(4326)

    time_steps = []

    value_dic = {}

    data_dic = {}

    var_list = [f'{VARIABLE}','LENGTH_AFTER','LENGTH_BEFORE','NOBS','QFLAG','RMSE']

    for var in var_list:
        value_dic[var] = {}

    for file in sorted(NC_FILES):

        key = os.path.splitext(os.path.basename(file))[0]

        key = key.split('_')[3][:8] # third word, first 7 digits
        time_step = f"{key[:4]}-{key[4:6]}-{key[6:]}"
        time_steps.append(time_step)
   
        shapes = polygon.geometry

        for var in var_list:

            #result = []
                

            with rasterio.open(f'netcdf:"{file}":{var}') as scr:
                
                fill_value = scr.nodatavals[0]
                    
                scale_factor = scr.tags(1).get('scale_factor')
                add_offset = scr.tags(1).get('add_offset')
                if scale_factor is None or add_offset is None:
                    scale_factor = 1.0
                    add_offset = 0.0
                else:
                    #scale_factor, add_offset = get_factor(file, var)
                    scale_factor = float(scale_factor)
                    add_offset = float(add_offset)
                    
                out_image, out_transform = rasterio.mask.mask(scr, shapes, crop=True, all_touched=True)
                    
                    # get lat and lon from pixel
                height = out_image.shape[1]
                width = out_image.shape[2]

                cols, rows = np.meshgrid(np.arange(width), np.arange(height))
                xs, ys = rasterio.transform.xy(out_transform, rows, cols)
                lons = np.array(xs).flatten()
                lats = np.array(ys).flatten()

                    # remove duplicates 
                lon = list(set(lons))
                lat = list(set(lats))
                    
                out_image = out_image.astype('float32')
                out_image[out_image == fill_value] = float('nan')
                out_image = out_image.astype('float32') * scale_factor + add_offset
 
            value_dic[var][time_step] = out_image[0].copy()
            

    return value_dic, lon, lat       




    
        
