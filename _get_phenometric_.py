import copy
import numpy as np
from _phenometric_ import phenometric
import pandas as pd
import xarray as xr



def is_valid(val):
    if val is None:
        return False
    if isinstance(val, float) and np.isnan(val):
        return False
    if isinstance(val, np.datetime64) and np.isnat(val):
        return False
    return True



# def to_scalar(dt):
#     return dt.item() if isinstance(dt, xr.DataArray) else dt


def check_order(sos_day1, pos_day1, eos_day1, sos_day2, pos_day2, eos_day2):
    # Convert all dates to scalars for reliable comparison
    pos1 = pos_day1
    pos2 = pos_day2
    sos1 = sos_day1
    eos1 = eos_day1
    sos2 = sos_day2
    eos2 = eos_day2

    if pos1.values < pos2.values:
        if not pd.isnull(sos1):
            if sos1.values > pos1.values or sos1.values > pos2.values:
                sos_day1 = np.nan
        if not pd.isnull(eos1):
            if eos1.values < pos1.values or eos1.values > pos2.values:
                eos_day1 = np.nan
        if not pd.isnull(sos2):
            if sos2.values < pos2.values or sos2.values > pos1.values:
                sos_day2 = np.nan
        if not pd.isnull(eos2):
            if eos2.values < pos1.values or eos2.values < pos2.values:
                eos_day2 = np.nan
        if not pd.isnull(eos1) and not pd.isnull(sos2):
            if eos1.values > sos2.values:
                eos_day1 = np.nan

    elif pos2.values < pos1.values:
        if not pd.isnull(sos1):
            if sos1.values > pos1.values or sos1.values < pos2.values:
                sos_day1 = np.nan
        if not pd.isnull(eos1):
            if eos1.values < pos1.values or eos1.values < pos2.values:
                eos_day1 = np.nan
        if not pd.isnull(sos2):
            if sos2.values > pos2.values or sos2.values > pos1.values:
                sos_day2 = np.nan
        if not pd.isnull(eos2):
            if eos2.values > pos1.values or eos2.values < pos2.values:
                eos_day2 = np.nan
        if not pd.isnull(eos2) and not pd.isnull(sos1):
            if eos2.values > sos1.values:
                eos_day2 = np.nan

    return sos_day1, pos_day1, eos_day1, sos_day2, pos_day2, eos_day2



def get_phenometric(smoothed_array, xarray_data, DIFFERENCE_BETWEEN_PEAKS, WINDOW_WITHOUT_SECOND_POS):

    # print("Function get_phenometric called")
    WINDOW_WITHOUT_SECOND_POS = int(WINDOW_WITHOUT_SECOND_POS)
    DIFFERENCE_BETWEEN_PEAKS = int(DIFFERENCE_BETWEEN_PEAKS)

    season1_array = np.full((3, smoothed_array.shape[1], smoothed_array.shape[2]), np.nan)
    season2_array = np.full((3, smoothed_array.shape[1], smoothed_array.shape[2]), np.nan)
    rpd_array = np.full((smoothed_array.shape[1], smoothed_array.shape[2]), np.nan)

    result_dic_season1 = {}
    result_dic_season2 = {}
    result_dic_rpd = {}

    for per in range(10, 40, 10):
        for i in range(smoothed_array.shape[1]):
            for j in range(smoothed_array.shape[2]):
                y = smoothed_array[:, i, j]
                time_array = xarray_data.time

                if np.all(np.isnan(y)):
                    continue

                try:
                    # print(f"Trying pixel ({i}, {j}) at {per}%")
                    phenoclass = phenometric(y, time_array)

                    # Arrays for storing phenometrics of early and late season
                    early_season_array = np.full((3,), np.nan)
                    late_season_array = np.full((3,), np.nan)
                    phenometric_rpd_array = np.full((1,), np.nan)

                    # === Season 1 (Main peak) ===
                    sos1, eos1, pos1, sos_day1, eos_day1, pos_day1 = phenoclass.percentage(phenoclass.maximum, per)

                    # Define mask for second season search
                    if is_valid(sos_day1) and is_valid(eos_day1):
                        mask = (phenoclass.time <= sos_day1) | (phenoclass.time >= eos_day1)
                    else:
                        half_width = int(WINDOW_WITHOUT_SECOND_POS/2)
                        mask = (phenoclass.time <= pos_day1.data - np.timedelta64(half_width, 'D')) | \
                               (phenoclass.time >= pos_day1.data + np.timedelta64(half_width, 'D'))

                    off_season_max = np.max(phenoclass.var[mask])
                    rpd = np.abs(off_season_max - phenoclass.maximum) / phenoclass.maximum * 100
                    phenometric_rpd_array = float(rpd)

                    # Only accept second season if is smaller than difference_between_peaks
                    if rpd <= DIFFERENCE_BETWEEN_PEAKS:
                        sos2, eos2, pos2, sos_day2, eos_day2, pos_day2 = phenoclass.percentage(off_season_max, per)
                    else:
                        sos2 = eos2 = pos2 = sos_day2 = eos_day2 = pos_day2 = np.nan
                    
                    
                    

                    # === Compare and Sort Seasons ===
                    if (is_valid(pos_day1) and is_valid(pos_day2)):
                        if pos_day1.data < pos_day2.data:


                            sos_day1, pos_day1, eos_day1, sos_day2, pos_day2, eos_day2 = check_order(sos_day1, pos_day1, eos_day1, sos_day2, pos_day2, eos_day2)


                            if is_valid(pos_day1): early_season_array[2] = int(pos1) if is_valid(pos_day1) else np.nan
                            if is_valid(sos_day1): early_season_array[0] = int(sos1) if is_valid(sos_day1) else np.nan
                            if is_valid(eos_day1): early_season_array[1] = int(eos1) if is_valid(eos_day1) else np.nan

                            if is_valid(pos_day2): late_season_array[2] = int(pos2) if is_valid(pos_day2) else np.nan
                            if is_valid(sos_day2): late_season_array[0] = int(sos2) if is_valid(sos_day2) else np.nan
                            if is_valid(eos_day2): late_season_array[1] = int(eos2) if is_valid(eos_day2) else np.nan

                        elif pos_day1.data > pos_day2.data:

                            sos_day1, pos_day1, eos_day1, sos_day2, pos_day2, eos_day2 = check_order(sos_day1, pos_day1, eos_day1, sos_day2, pos_day2, eos_day2)

                           

                            if is_valid(pos_day2): early_season_array[2] = int(pos2) if is_valid(pos_day2) else np.nan
                            if is_valid(sos_day2): early_season_array[0] = int(sos2) if is_valid(sos_day2) else np.nan
                            if is_valid(eos_day2): early_season_array[1] = int(eos2) if is_valid(eos_day2) else np.nan

                            if is_valid(pos_day1): late_season_array[2] = int(pos1) if is_valid(pos_day1) else np.nan
                            if is_valid(sos_day1): late_season_array[0] = int(sos1) if is_valid(sos_day1) else np.nan
                            if is_valid(eos_day1): late_season_array[1] = int(eos1) if is_valid(eos_day1) else np.nan



                        season1_array[:, i, j] = early_season_array
                        season2_array[:, i, j] = late_season_array
                        rpd_array[i, j] = phenometric_rpd_array

                        # print(f'season2_array {i}, {j}:', season2_array[:, i, j])

                    elif is_valid(pos_day1) and is_valid(pos_day2) == False:
                        # Only main season is valid
                        temp = np.full((3,), np.nan)
                        temp[2] = int(pos1)
                        if is_valid(sos_day1): temp[0] = int(sos1)
                        if is_valid(eos_day1): temp[1] = int(eos1)
                        season1_array[:, i, j] = temp

                    elif is_valid(pos_day2) and is_valid(pos_day1) == False:
                        # Only second season is valid
                        temp = np.full((3,), np.nan)
                        temp[2] = int(pos2)
                        if is_valid(sos_day2): temp[0] = int(sos2)
                        if is_valid(eos_day2): temp[1] = int(eos2)
                        season1_array[:, i, j] = temp

                except Exception as e:
                    print(f"Error at pixel ({i}, {j}) with percentage {per}: {e}")
                    traceback.print_exc() 

        # Store results for this percentile
        result_dic_season1[f'{per}'] = copy.deepcopy(season1_array)
        result_dic_season2[f'{per}'] = copy.deepcopy(season2_array)
        result_dic_rpd[f'{per}'] = copy.deepcopy(rpd_array)

    return result_dic_season1, result_dic_season2, result_dic_rpd





# import copy 
# import numpy as np
# from _phenometric_ import phenometric


# def get_phenometric(smoothed_array, xarray_data, DIFFERENCE_BETWEEN_PEAKS ):
    

#     DIFFERENCE_BETWEEN_PEAKS = int(DIFFERENCE_BETWEEN_PEAKS)

#     season1_array   = np.full(shape = (3, smoothed_array.shape[1], smoothed_array.shape[2]), fill_value = np.nan)
#     season2_array   = np.full(shape = (3, smoothed_array.shape[1], smoothed_array.shape[2]), fill_value = np.nan)
    
#     rpd_array   =    np.full(shape = (1, smoothed_array.shape[1], smoothed_array.shape[2]), fill_value = np.nan)                 
        
#     result_dic_season1  = {}
#     result_dic_season2  = {}
    
#     result_dic_rpd = {}

#     for per in range(10, 40, 10):

#         for i in range(smoothed_array.shape[1]):

#             for j in range(smoothed_array.shape[2]):

#                 y = smoothed_array[:,i,j]
#                 time_array = xarray_data.time
                

#                 if np.all(np.isnan(y)):
#                     continue

                
#                 try:

#                     phenoclass = phenometric(y, time_array)

#                     # === Season 1 (Main Peak) ===
#                     phenometric_sgl_array = np.full((3,), np.nan)
#                     phenomtric_rpd_array = np.full(1, fill_value = np.nan)

#                     sos1, eos1, pos1, sos_day1, eos_day1, pos_day1 = phenoclass.percentage(phenoclass.maximum, per)

                        
#                     if sos1 is not None:

#                         phenometric_sgl_array[0] = int(sos1)
 
#                     if eos1 is not None:
                            
#                         phenometric_sgl_array[1] = int(eos1)
                        
#                     phenometric_sgl_array[2] = int(pos1)


#                     # === Try Season 2 (Off-Season Peak) ===
#                     try:

#                         if sos_day1 is not None and eos_day1 is not None:

#                             mask = (phenoclass.time <= sos_day1) | (phenoclass.time >= eos_day1)

#                         else:
#                             mask = (phenoclass.time <= pos_day1.data - np.timedelta64(80, 'D')) | (phenoclass.time >= pos_day1.data + np.timedelta64(80, 'D'))

#                         off_season_max = np.max(phenoclass.var[mask])

#                         rpd = ((np.abs(off_season_max - phenoclass.maximum))/(phenoclass.maximum))*100

#                         phenomtric_rpd_array[0] = float(rpd)

#                         if rpd <= DIFFERENCE_BETWEEN_PEAKS:

#                             phenometric_dbl_array = np.full((3,), np.nan)

#                             sos2, eos2, pos2, sos_day2, eos_day2, pos_day2 = phenoclass.percentage(off_season_max, per)

#                             if sos2 is not None:

#                                 phenometric_dbl_array[0] = int(sos2)

#                             if eos2 is not None:

#                                 phenometric_dbl_array[1] = int(eos2)
                                
#                             if pos2 is not None:

                                        
#                                 phenometric_dbl_array[2] = int(pos2)

#                             # if pos_day2 is not None:

#                             #     phenometric_dbl_array[5] = int(pos_day2)

#                         else:
                            
#                             phenometric_dbl_array = None
#                             pos_day2 = np.nan


#                     except (AttributeError, TypeError):
#                         phenometric_dbl_array = None
#                         pos_day2 = np.nan
                    
#                     try:

#                         if (not np.isnan(pos_day1)) and (not np.isnan(pos_day2)):


#                             if pos_day1.data < pos_day2.data:

#                                 season1_array[:,i,j]= phenometric_sgl_array
#                                 season2_array[:,i,j]= phenometric_dbl_array
#                             else:
#                                 season1_array[:,i,j]= phenometric_dbl_array
#                                 season2_array[:,i,j]= phenometric_sgl_array
                            
#                             rpd_array[:,i,j] = phenomtric_rpd_array

#                         elif not np.isnan(pos_day1.data):

#                             season1_array[:,i,j]= phenometric_sgl_array

#                         elif np.isnan(pos_day1.data) and not np.isnan(pos_day2.data):

#                             season1_array[:,i,j] = phenometric_dbl_array

#                     except Exception as e:
#                         print({e})

#                 except Exception as e:
#                     print({e})
        
        
#         result_dic_season1[f'{per}'] = copy.deepcopy(season1_array)
#         result_dic_season2[f'{per}'] = copy.deepcopy(season2_array)
#         result_dic_rpd[f'{per}'] = copy.deepcopy(rpd_array[0])


#     return result_dic_season1, result_dic_season2, result_dic_rpd

