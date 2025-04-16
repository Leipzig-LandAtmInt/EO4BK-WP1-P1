import copy 
import numpy as np
from _phenometric_ import phenometric


def get_phenometric(smoothed_array, xarray_data, DIFFERENCE_BETWEEN_PEAKS ):
    

    DIFFERENCE_BETWEEN_PEAKS = int(DIFFERENCE_BETWEEN_PEAKS)

    season1_array   = np.full(shape = (3, smoothed_array.shape[1], smoothed_array.shape[2]), fill_value = np.nan)
    season2_array   = np.full(shape = (3, smoothed_array.shape[1], smoothed_array.shape[2]), fill_value = np.nan)
    rpd_array   =    np.full(shape = (1, smoothed_array.shape[1], smoothed_array.shape[2]), fill_value = np.nan)                 
        
    result_dic_season1  = {}
    result_dic_season2  = {}

    result_dic_rpd = {}

    for per in range(10, 40, 10):

        for i in range(smoothed_array.shape[1]):

            for j in range(smoothed_array.shape[2]):

                y = smoothed_array[:,i,j]
                time_array = xarray_data.time
                

                if np.all(np.isnan(y)):
                    continue

                
                try:

                    phenoclass = phenometric(y, time_array)

                    # === Season 1 (Main Peak) ===
                    phenometric_sgl_array = np.full((3,), np.nan)
                    phenomtric_rpd_array = np.full(1, fill_value = np.nan)

                    sos1, eos1, pos1, sos_day1, eos_day1, pos_day1 = phenoclass.percentage(phenoclass.maximum, per)

                        
                    if sos1 is not None:

                        phenometric_sgl_array[0] = int(sos1)
 
                    if eos1 is not None:
                            
                        phenometric_sgl_array[1] = int(eos1)
                        
                    phenometric_sgl_array[2] = int(pos1)


                    # === Try Season 2 (Off-Season Peak) ===
                    try:

                        if sos_day1 is not None and eos_day1 is not None:

                            mask = (phenoclass.time <= sos_day1) | (phenoclass.time >= eos_day1)

                        else:
                            mask = (phenoclass.time <= pos_day1.data - np.timedelta64(60, 'D')) | (phenoclass.time >= pos_day1.data + np.timedelta64(60, 'D'))

                        off_season_max = np.max(phenoclass.var[mask])

                        rpd = ((np.abs(off_season_max - phenoclass.maximum))/(phenoclass.maximum))*100

                        phenomtric_rpd_array[0] = float(rpd)

                        if rpd >= DIFFERENCE_BETWEEN_PEAKS:

                            phenometric_dbl_array = None
                            pos_day2 = np.nan

                        else:
                            
                            phenometric_dbl_array = np.full((3,), np.nan)

                            sos2, eos2, pos2, sos_day2, eos_day2, pos_day2 = phenoclass.percentage(off_season_max, per)

                            if sos2 is not None:

                                phenometric_dbl_array[0] = int(sos2)

                            if eos2 is not None:

                                phenometric_dbl_array[1] = int(eos2)
                                        
                            phenometric_dbl_array[2] = int(pos2)


                    except (AttributeError, TypeError):
                        phenometric_dbl_array = None
                        pos_day2 = np.nan
                    
                    try:

                        if (not np.isnan(pos_day1)) and (not np.isnan(pos_day2)):


                            if pos_day1.data < pos_day2.data:

                                season1_array[:,i,j]= phenometric_sgl_array
                                season2_array[:,i,j]= phenometric_dbl_array
                            else:
                                season1_array[:,i,j]= phenometric_dbl_array
                                season2_array[:,i,j]= phenometric_sgl_array
                            
                            rpd_array[:,i,j] = phenomtric_rpd_array

                        # elif not np.isnan(pos_day1.data):

                        #     season1_array[:,i,j]= phenometric_sgl_array

                        # elif not np.isnan(pos_day2.data) and phenometric_dbl_array is not None:

                        #     season1_array[:,i,j] = phenometric_dbl_array

                    except Exception as e:
                        print({e})

                except Exception as e:
                    print({e})
        
        
        result_dic_season1[f'{per}'] = copy.deepcopy(season1_array)
        result_dic_season2[f'{per}'] = copy.deepcopy(season2_array)
        result_dic_rpd[f'{per}'] = copy.deepcopy(rpd_array[0])


    return result_dic_season1, result_dic_season2, result_dic_rpd

