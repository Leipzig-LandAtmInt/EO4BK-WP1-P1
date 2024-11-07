from sentle import sentle 
import rioxarray 
from shapely.geometry import mapping 
import geopandas as gpd
import os
from dotenv import load_dotenv


def sentle_download(lcs_eo4bkdata, time_span:str ):
    '''
    This function downloads the Sentinel data
    '''


    boundary = lcs_eo4bkdata.geometry.bounds
    bound_left = int(boundary.minx.iloc[0])
    bound_bottom = int(boundary.miny.iloc[0])
    bound_right = int(boundary.maxx.iloc[0])
    bound_top = int(boundary.maxy.iloc[0])

    da = sentle.process(target_crs= lcs_eo4bkdata.crs,
                        bound_left=bound_left,
                        bound_bottom=bound_bottom,
                        bound_right=bound_right,
                        bound_top=bound_top,
                        datetime=time_span,
                        target_resolution=10,
                        dask_scheduler_port=16012,
                        dask_dashboard_address='127.0.0.1:38382',
                        S2_mask_snow=True,
                        S2_cloud_classification=True,
                        S2_cloud_classification_device="cuda",
                        S1_assets=["vv", "vh"],
                        S2_apply_snow_mask=True,
                        S2_apply_cloud_mask=True,
                        time_composite_freq="7d",
                        num_workers=40,
                        )

    da = da.rio.write_crs(lcs_eo4bkdata.crs)
    output_download = da.rio.clip(lcs_eo4bkdata.geometry.apply(mapping), lcs_eo4bkdata.crs)
        
    return output_download


