from rasterio.enums import Resampling
import rioxarray as rio
import numpy as np
import xarray as xr


def reproject_datacube(datacube):
    datacube = datacube.rename({'lon': 'x','lat': 'y'})
    datacube = datacube.rio.write_crs("EPSG:4326")

    # because reproject does not work with 1 dimensional data 

    if datacube.x.size == 1 and datacube.y.size ==1:
        
        new_x = np.array([datacube.x.item(), datacube.x.item() + 0.0029761904762040103])
        new_y = np.array([datacube.y.item(), datacube.y.item() + 0.0029761904762040103])
        datacube1 = datacube.reindex(x=new_x, y=new_y, fill_value=np.nan)
    
    elif datacube.y.size == 1:

        new_y = np.array([datacube.y.item(), datacube.y.item() + 0.0029761904762040103])
        datacube1 = datacube.reindex(y=new_y, fill_value=np.nan)

    elif datacube.x.size ==1:
        new_x = np.array([datacube.x.item(), datacube.x.item() + 0.0029761904762040103])
        datacube1 = datacube.reindex(x=new_x, fill_value=np.nan)
    else:
        datacube1 = datacube

    datacube2 = datacube1.rio.reproject("EPSG:5641",resampling=Resampling.nearest  ,nodata=np.nan , resolution = (200,300)) 
    # drop artificial extention again to reduce size
    #if datacube.x.size == 1 and datacube.y.size ==1:

    datacube2 = datacube2.dropna(dim="x", how="all")
    datacube2 = datacube2.dropna(dim="y", how="all")
    #elif datacube.x.size ==1:
    #    datacube2 = datacube2.dropna(dim="x", how ="all")
    #elif datacube.y.size ==1:
    #    datacube2 = datacube2.dropna(dim="x", how ="all")
    
    # rename
    datacube = datacube2.rename({'x': 'lon','y': 'lat'})
    
    return datacube