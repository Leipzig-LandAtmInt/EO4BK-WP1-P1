# Test downloadsentle from _sentle_download_
from sentle import sentle 
import rioxarray

from shapely.geometry import mapping 
import geopandas as gpd
import os
from dotenv import load_dotenv


def sentle_download(lcs_eo4bkdata,MINICUBE_DUMMYSAVE, targetcrs, time_span):
    '''
    This function downloads the Sentinel data
    '''


    boundary = lcs_eo4bkdata.geometry.bounds
    bound_left = int(boundary.minx.iloc[0])
    bound_bottom = int(boundary.miny.iloc[0])
    bound_right = int(boundary.maxx.iloc[0])
    bound_top = int(boundary.maxy.iloc[0])
    
    sentle.process(zarr_store = MINICUBE_DUMMYSAVE,
                   target_crs= targetcrs,
                   bound_left=bound_left,
                   bound_bottom=bound_bottom,
                   bound_right=bound_right,
                   bound_top=bound_top,
                   datetime=time_span,
                   target_resolution=10,
                   S2_mask_snow=True,
                   S2_cloud_classification=True,
                   S2_cloud_classification_device="cpu",
                   S1_assets=["vv", "vh"],
                   S2_apply_snow_mask=True,
                   S2_apply_cloud_mask=True,
                   time_composite_freq="7d",
                   num_workers=4
                   )
        