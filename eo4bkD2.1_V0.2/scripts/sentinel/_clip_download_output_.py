import rioxarray 
from shapely.geometry import mapping 

def clipping_datacube(output_download, lcs_eo4bkdata):
    
    datacube = output_download.sentle.rio.write_crs(lcs_eo4bkdata.crs)
    output_download_clipped = datacube.rio.clip(lcs_eo4bkdata.geometry.apply(mapping), lcs_eo4bkdata.crs)
        
    return output_download_clipped