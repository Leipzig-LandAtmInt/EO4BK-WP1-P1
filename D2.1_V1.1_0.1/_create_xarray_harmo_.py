import xarray as xr
from _create_lucas_attributes_ import create_lucas_attributes
from _create_sentinel_attributes_ import create_sentinel_attributes

def create_xarray(variables, year):
    

    '''
    This function creates an xarray with the corresponding attributes 
    '''

    lat = variables['lat']
    lon = variables['lon']
    time = variables['time']  # Ensure proper datetime precision

    sent_keys = ['b01', 'b02', 'b03', 'b04', 'b05', 'b06', 'b07', 'b08', 'b08a', 'b09', 'b11', 'b12', 'vh', 'vv', 'ndvi', 'nirv', 'kndvi']
    data_vars = {}

    # Populate data_vars with Sentinel variables
    for key in sent_keys:
        if key in variables:
            data_vars[f'sent_{key}'] = (["time", "lat", "lon"], variables[key])

    # Add LUCAS point ID
    data_vars['lcs_point_id'] = (["index"], variables['point_id'])

    # Create the xarray Dataset
    datacube = xr.Dataset(
        coords=dict(
            lon=("lon", lon),
            lat=("lat", lat),
            time=("time", time)
        ),
        data_vars=data_vars
    )

  ## Pass the attributes       
    # Global attributes 
    datacube.attrs['acknowledgment'] = 'All EO4BK data providers are acknowledged inside each variable'
    datacube.attrs['Description'] = 'Data variables with the prefix "sent_" are referring to Sentinel variables, \nData varaibales with the prefix "lcs_" are referring to LUCAS variables'
            # Local Sentinel-2 attributes 

    # # get the attributes from the create_attributes directory
    for band, attr in create_sentinel_attributes()[0].items():                                   # Parallel iteration through band and attr, where elements of sentinel_attributes.items() is unpacked in key and value pair 
        datacube[f'sent_{band}'].attrs['long_name'] = attr['long_name']          # key is in reference of the current key, and value gets the reference for the value
        datacube[f'sent_{band}'].attrs['Wavelength S2A'] = attr['Wavelength S2A']
        datacube[f'sent_{band}'].attrs['Wavelentgh S2B'] = attr['Wavelength S2B']
        datacube[f'sent_{band}'].attrs['Original Resolution'] = attr['Original resolution']
        datacube[f'sent_{band}'].attrs['Pixel Size'] = attr['Pixel Size']
        datacube[f'sent_{band}'].attrs['Processing Steps'] = attr['Processing steps']
    for band, attr in create_sentinel_attributes()[1].items():
        datacube[f'sent_{band}'].attrs['long_name'] = attr['long_name']
        datacube[f'sent_{band}'].attrs['Description'] = attr['Additional Description']
        datacube[f'sent_{band}'].attrs['Usage'] = attr['Usage']
        datacube[f'sent_{band}'].attrs['Original Resolution'] = attr['Original resolution']
        datacube[f'sent_{band}'].attrs['Pixel Size'] = attr['Pixel Size']
        datacube[f'sent_{band}'].attrs['Processing Steps'] = attr['Processing steps']
    for band, attr in create_sentinel_attributes()[2].items():
        datacube[f'sent_{band}'].attrs['long_name'] = attr['long_name']
        datacube[f'sent_{band}'].attrs['Processing Steps'] = attr['Processing Steps']
        datacube[f'sent_{band}'].attrs['Pixel Size'] = attr['Pixel Size']

    # # get the lucas attributes from the lucas_core_directory, because of lucas hd and ld input differences it must be flexible
    
    for var, attr in create_lucas_attributes(variables['point_id'], year).items():
        datacube[f'lcs_{var}'].attrs['long_name'] = attr['long_name']
        datacube[f'lcs_{var}'].attrs['Description'] = attr['description']
        datacube[f'lcs_{var}'].attrs['Value Origin'] = attr['value_origin']
        datacube[f'lcs_{var}'].attrs['Original Name'] = attr['original_name']
        datacube[f'lcs_{var}'].attrs['Acknowledgment'] = attr['acknowledgement']
        datacube[f'lcs_{var}'].attrs['PID'] = attr['PID']
        datacube[f'lcs_{var}'].attrs['How to cite'] = attr['How to cite']
        datacube[f'lcs_{var}'].attrs['Download link'] = attr['Download_link']
        datacube[f'lcs_{var}'].attrs['Detailed description'] = attr.get('Detailed_description', 'No detailed description available')
        datacube[f'lcs_{var}'].attrs['Processing Step'] = attr.get('processing_steps', 'Processing is conducted by LUCAS')

    # here the difference from the processing steps between lucas hd and ld are considered


    return datacube