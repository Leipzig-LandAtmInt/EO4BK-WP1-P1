import numpy as np
from _phenometric_ import phenometric
from _find_peaks_ import filter_peaks
from _check_pheno_order_ import check_order
import pandas as pd
import xarray as xr


def get_phenometric(smoothed_array, xarray_data, threshold_amplitude):

    result_dic_season1 = {}
    result_dic_season2 = {}
    amplitude_dic = {}

    for percentage in range(10,60,10):

        season_one_array = np.full((3, smoothed_array.shape[1], smoothed_array.shape[2]), np.nan)
        season_two_array = np.full((3, smoothed_array.shape[1], smoothed_array.shape[2]), np.nan)
        amplitudes_array = np.full((2, smoothed_array.shape[1], smoothed_array.shape[2]), np.nan)

        for lat in range(smoothed_array.shape[1]):

            for lon in range(smoothed_array.shape[2]):
                

                y = smoothed_array[:, lat, lon]
                
                time_array = xarray_data.time


                season1 = np.full((3, ), np.nan)
                season2 = np.full((3, ), np.nan)
                amplitudes = np.full((2, ), np.nan)


                if np.all(np.isnan(y)):
                    continue

                filtered_peak, rpd_peak = filter_peaks(smoothed_array[:,lat, lon], threshold_amplitude)

                if not filtered_peak:
                    continue

                sos_doy_list = []
                
                pos_doy_list = []

                eos_doy_list = []
                
                sos_day_list = []
                
                pos_day_list = []

                eos_day_list = []

                # rpd_list = []

                rpd_list = sorted(rpd_peak)

                for peak in sorted(filtered_peak):

                    peak_value = y[peak[0]]

                    # rpd_value = rpd_peak

                    phenometric_class = phenometric(y, time_array)

                    sos_doy, eos_doy, pos_doy, sos_day, eos_day, pos_day = phenometric_class.percentage(peak_value, percentage)


                    sos_doy_list.append(sos_doy)

                    pos_doy_list.append(pos_doy)

                    eos_doy_list.append(eos_doy)


                    sos_day_list.append(sos_day)

                    pos_day_list.append(pos_day)

                    eos_day_list.append(eos_day)

                    # rpd_list.append(rpd_value)
                    
                if len(pos_doy_list) > 1: 

                    sos_day1, pos_day1, eos_day1, sos_day2, pos_day2, eos_day2 = check_order(sos_day_list, pos_day_list, eos_day_list)
                        
                    if not pd.isnull(sos_day1): season1[0] = int(sos_doy_list[0]) if not pd.isnull(sos_day1) else np.nan
                    if not pd.isnull(pos_day1): season1[1] = int(pos_doy_list[0]) if not pd.isnull(pos_day1) else np.nan
                    if not pd.isnull(eos_day1): season1[2] = int(eos_doy_list[0]) if not pd.isnull(eos_day1) else np.nan

                    if not pd.isnull(sos_day2): season2[0] = int(sos_doy_list[1]) if not pd.isnull(sos_day2) else np.nan
                    if not pd.isnull(pos_day2): season2[1] = int(pos_doy_list[1]) if not pd.isnull(pos_day2) else np.nan
                    if not pd.isnull(eos_day2): season2[2] = int(eos_doy_list[1]) if not pd.isnull(eos_day2) else np.nan
                    
                    if not pd.isnull(pos_day1): amplitudes[0] = float(rpd_list[0]) if not pd.isnull(pos_day1) else np.nan
                    if not pd.isnull(pos_day2): amplitudes[1] = float(rpd_list[1]) if not pd.isnull(pos_day2) else np.nan
                
                    

                if len(pos_doy_list) == 1: 

                    sos_day1, pos_day1, eos_day1= check_order(sos_day_list, pos_day_list, eos_day_list)


                    if not pd.isnull(sos_day1): season1[0] = int(sos_doy_list[0]) if not pd.isnull(sos_day1) else np.nan
                    if not pd.isnull(pos_day1): season1[1] = int(pos_doy_list[0]) if not pd.isnull(pos_day1) else np.nan
                    if not pd.isnull(eos_day1): season1[2] = int(eos_doy_list[0]) if not pd.isnull(eos_day1) else np.nan

                    if not pd.isnull(pos_day1): amplitudes[0] = float(rpd_list[0]) if not pd.isnull(pos_day1) else np.nan

                season_one_array[:, lat, lon ]   = season1
                season_two_array[:, lat, lon]    = season2
                amplitudes_array[:, lat, lon]    = amplitudes

            result_dic_season1[f'{percentage}'] = season_one_array
            result_dic_season2[f'{percentage}'] = season_two_array
            amplitude_dic[f'{percentage}'] = amplitudes_array

    return result_dic_season1, result_dic_season2, amplitude_dic