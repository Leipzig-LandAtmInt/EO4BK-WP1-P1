import pandas as pd
import xarray as xr

def zarr_quality_check(zarr_dict, data_path, NUT3, CROPTYPE):
    quality_check = pd.DataFrame()

    # initialize lists
    start_times = []
    end_times = []
    key_list = []
    lon_list = []
    lat_list = []
    time_list = []

    # iter creates an iteration over the keys. 
    # next() retrieves the first key from the iteration. This is used to access the first element of the minicube_dict without explicity knowing the keys
    ## {var: [] for var in...} is dictionary comprehension. It iterates over the list of variable names var and initializes an empty list for each variable
    attr_bytes_dict = {var: [] for var in list(zarr_dict[next(iter(zarr_dict))].data_vars)}
    for key in zarr_dict.keys():
    
        # Compute Key
        key_list.append(key)
    
        # compute START_TIME
    
        start_time = zarr_dict[key].time.min().data
        start_times.append(start_time)

        # compute END_TIME

        end_time = zarr_dict[key].time.max().data
        end_times.append(end_time)
    
        # check dimenstions
        lon_dim = len(zarr_dict[key].lon)
        lon_list.append(lon_dim)

        lat_dim = len(zarr_dict[key].lat)
        lat_list.append(lat_dim)

        time_dim = len(zarr_dict[key].time)
        time_list.append(time_dim)

        # check bytes of data_vars
        # iterates over all variables data_vars in the current minicube, which is accessed as zarr_dict[key]
        # everytime the loop processes a new key (zarr_dict[key]) it adds to the existing list of attr_bytes_dict list, because lists are mutable and do not get overwritten
        for var in zarr_dict[key].data_vars:
            attr_bytes_dict[var].append(zarr_dict[key][var].nbytes)

    # Convert to Pandas Series
    key_list = pd.Series(key_list, name='FILE')
    start_times = pd.Series(start_times, name='START_TIME')

    # Create the DataFrame
    quality_check = pd.DataFrame({'FILE': key_list,
                                'START_TIME': start_times, 
                                'END_TIME': end_times, 
                                'LEN_LON': lon_list,
                                'LEN_LAT':lat_list,
                                'LEN_TIME':time_list})





    # Add attribute bytes to the DataFrame
    # var is the key
    # bytes_list are the entry of the specific key
    for var, bytes_list in attr_bytes_dict.items():
        quality_check[f'{var.upper()}_BYTES'] = bytes_list

    quality_check.to_excel(f"{data_path}/{NUT3}/Quality_check_{CROPTYPE}_{NUT3}.xlsx", sheet_name = f'{CROPTYPE}_{NUT3}', header = True)

