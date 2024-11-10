



def create_sentinel_attributes():
    
    '''
    This function creates all the attributes to descripe the variables in the final .zarr data. 
    '''

    # Defines the Attributes for Sentinel-2
    sentinel_attributes = {
            'b01': {'long_name': 'Sentinel-2 Band 01 - Aerosol', 'Wavelength S2A': '443.9 nm', 'Wavelength S2B': '442.3 nm', 'Original resolution': '60 m' , 'Pixel Size': '10 m', 'Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b02': {'long_name': 'Sentinel-2 Band 02 - Blue', 'Wavelength S2A': '496.6 nm', 'Wavelength S2B': '492.1 nm', 'Original resolution': '10 m', 'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b03': {'long_name': 'Sentinel-2 Band 03 - Green', 'Wavelength S2A': '560 nm', 'Wavelength S2B': '559 nm', 'Original resolution': '10 m', 'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b04': {'long_name': 'Sentinel-2 Band 04 - Red', 'Wavelength S2A': '664.5 nm', 'Wavelength S2B': '665 nm', 'Original resolution': '10 m', 'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b05': {'long_name': 'Sentinel-2 Band 05 - Red Edge 1', 'Wavelength S2A': '703.9 nm', 'Wavelength S2B': '703.8 nm', 'Original resolution': '20 m', 'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b06': {'long_name': 'Sentinel-2 Band 06 - Red Edge 2', 'Wavelength S2A': '740.2 nm', 'Wavelength S2B': '739.1 nm', 'Original resolution': '20 m',  'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b07': {'long_name': 'Sentinel-2 Band 07 - Red Edge 3', 'Wavelength S2A': '782.5 nm', 'Wavelength S2B': '779.7 nm', 'Original resolution': '20 m',  'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b08': {'long_name': 'Sentinel-2 Band 08 - NIR', 'Wavelength S2A': '835.1 nm', 'Wavelength S2B': '833 nm', 'Original resolution': '10 m', 'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b08a': {'long_name': 'Sentinel-2 Band 8A - Red Edge 4', 'Wavelength S2A': '864.8 nm', 'Wavelength S2B': '864 nm', 'Original resolution': '20 m',  'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b09': {'long_name': 'Sentinel-2 Band 09 - Water vapor', 'Wavelength S2A': '945 nm', 'Wavelength S2B': '943.2 nm', 'Original resolution': '60 m',  'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b11': {'long_name': 'Sentinel-2 Band 11 - SWIR 1', 'Wavelength S2A': '1613.7 nm', 'Wavelength S2B': '1610.4 nm', 'Original resolution': '20 m', 'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            'b12': {'long_name': 'Sentinel-2 Band 12 - SWIR 2', 'Wavelength S2A': '2202.4 nm', 'Wavelength S2B': '2185.7 nm', 'Original resolution': '20 m',  'Pixel Size': '10 m','Processing level':'Level 2A','Processing steps':'Data was received via sentle package, Cloud masking == True, snow masking == True, 7d temporal average composite'},
            }
    # Attributes for Sentinel 1
    sentinel_1_attributes = {
            'vh' : {'long_name': 'Sentinel-1 Vertical-Horizontal (VH)','Additional Description':'Dual-band cross polarization, waves are transmitted vertically and received horizontally','Usage':'VH is more sensetive to change in vegetation density and structure','Original resolution':'10 m','Pixel Size':'10 m','Processing steps':'Data was received via sentle package, 7d temporal average composite'},
            'vv' : {'long_name': 'Sentinel-1 Vertical-Vertical (VV)','Additional Description':'Single co-polarization, waves are transmitted and received vertically', 'Usage':'VV is more sensetive to vegetation phenology or water content','Original resolution':'10 m','Pixel Size':'10 m','Processing steps':'Data was received via sentle package, 7d temporal average composite'}
            }
    # Attributes for Sentinel Vegetation Indices
    sentinel_vi_attributes = {
            'ndvi':   {'long_name':'Normalized Vegetation Index', 'Processing Steps':'Index was calculated with spyndex v. 0.6.0 package', 'Pixel Size':'10 m'},
            'nirv':   {'long_name':'Near Infrared Reflectance of Vegetation', 'Processing Steps':'Index was calculated with spyndex v. 0.6.0 package', 'Pixel Size':'10 m'},
            'kndvi':  {'long_name':'kernel Normalized Vegetation Index', 'Processing Steps':'Index was calculated with spyndex v. 0.6.0 package', 'Pixel Size':'10 m'}
        }


    
    return sentinel_attributes, sentinel_1_attributes, sentinel_vi_attributes

  