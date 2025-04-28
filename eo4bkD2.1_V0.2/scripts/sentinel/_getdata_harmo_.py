import xarray as xr
import numpy as np
from shapely import wkt
import spyndex

def getdata_harmonized(output_download_clipped, lcs_eo4bkdata):

    '''
    This function gets the data from LUCAS and from Sentinel Download / and calculates indices, because they are not directly available in sentle
    '''
    sen_data = output_download_clipped
    lcs_eo4bkdata = lcs_eo4bkdata
    # eo4bkdata_lcs_xarray = lcs_eo4bkdata.to_xarray()

    # get LUCAS data

    point_id = lcs_eo4bkdata['point_id'].values.astype(str)

    # get all the bands from the sentinel download
    b01 = sen_data.sel(band = 'B01').data
    b02 = sen_data.sel(band = 'B02').data
    b03 = sen_data.sel(band = 'B03').data
    b04 = sen_data.sel(band = 'B04').data
    b05 = sen_data.sel(band = 'B05').data
    b06 = sen_data.sel(band = 'B06').data
    b07 = sen_data.sel(band = 'B07').data
    b08 = sen_data.sel(band = 'B08').data
    b08a = sen_data.sel(band = 'B8A').data
    b09 = sen_data.sel(band = 'B09').data
    b11 = sen_data.sel(band = 'B11').data
    b12 = sen_data.sel(band = 'B12').data
    vh_asc = sen_data.sel(band = 'vh_asc').data
    vh_desc = sen_data.sel(band = 'vh_desc').data
    vv_asc = sen_data.sel(band = 'vv_asc').data  
    vv_desc = sen_data.sel(band = 'vv_desc').data  
    
    # get dimension data from sentinel download

    lon = sen_data.x.data
    lat = sen_data.y.data
    time = np.array(sen_data.time.data, dtype='datetime64[ns]')
    
 
    ## Calculate Indicies 
        
    # NDVI 
    ndvi = spyndex.computeIndex(
        index = ["NDVI"],
        params = {
            "N" : b08,
            "R" : b04
        }
    )

    # NIRv

    nirv = spyndex.computeIndex(
        index = ["NIRv"],
        params = {
            "N" : b08,
            "R" : b04
        }
        
    )
    # kNDVI
    params = {
        "kNN" : 1.0,
        "kNR" : spyndex.computeKernel(
            kernel = "RBF",
            params = {"a": b08,
                      "b": b04,
                      "sigma": 0.5 *( b08 + b04)}
                      ),
            }

    kndvi = spyndex.computeIndex("kNDVI", params)

    evi = spyndex.computeIndex(
        index=["EVI"],
        params={
            "C1": spyndex.constants["C1"].value,
            "C2": spyndex.constants["C2"].value,
            "g": spyndex.constants["g"].value,
            "L": spyndex.constants["L"].value,
            "N": b08/10000,
            "R": b04/10000,
            "B": b02/10000,
        },
    )

    return {
        "point_id": point_id,
        "lon":  lon,
        "lat":  lat,
        "time": time,
        "b01":  b01,
        "b02":  b02,
        "b03" : b03,
        "b04":  b04,
        "b05" : b05,
        "b06" : b06,
        "b07" : b07, 
        "b08" : b08,
        "b08a": b08a,
        "b09" : b09,
        "b11" : b11,
        "b12" : b12,
        "vh_asc"  : vh_asc,
        "vh_desc" : vh_desc,
        "vv_asc"  : vv_asc,
        "vv_desc" : vv_desc,             
        "ndvi": ndvi,
        "nirv": nirv,
        "kndvi": kndvi,
        "evi": evi
        
    }
