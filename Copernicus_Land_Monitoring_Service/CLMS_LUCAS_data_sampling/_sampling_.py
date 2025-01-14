import pandas as pd
import numpy as np

data_dict = {}
result_df_notempty = pd.DataFrame()

def sampling(crop, centroid_list, nc_dict, crop_nc_data, ACRONYM):


    var_list = [f'{ACRONYM}','LENGTH_AFTER','LENGTH_BEFORE','NOBS','QFLAG','RMSE']

    for var in var_list:
        for timestep in sorted(list(nc_dict.keys())):
            point_ids = []
            nc_data = []
                  
            for point in range(len(centroid_list[crop]['Centroid'])):
                point_id = centroid_list[f'{crop}']['Index'][point]
                
                point_lat = centroid_list[crop]['Centroid'].x.iloc[point]
                point_lon = centroid_list[crop]['Centroid'].y.iloc[point]
                variables = nc_dict[timestep].sel(lat=point_lat, lon=point_lon, method='nearest')[var].data
                # checks if the variables is an np.ndarray and convert variables into an scalar 
                if isinstance(variables, np.ndarray):
                    variables = variables.item()
                if isinstance(variables,float) and np.isnan(variables):
                    variables = pd.NA

                point_ids.append(point_id)


                nc_data.append(variables)


            
            data_dict[timestep] = nc_data
            
            crop_nc_data['POINT_ID'] = point_ids

            new_data = pd.DataFrame({f'{var}_{timestep}': data_dict[timestep]})

            crop_nc_data = pd.concat([crop_nc_data, new_data], axis = 1)
            # Filter nan values of FAPAR
            crop_subset = crop_nc_data.filter(like = ACRONYM).copy()

            crop_subset.dropna(axis = 0, how = 'all', inplace = True)

            result_df_notempty = crop_nc_data[crop_nc_data.index.isin(crop_subset.index)]
            
    return result_df_notempty
