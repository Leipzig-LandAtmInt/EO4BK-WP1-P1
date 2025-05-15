from scipy.signal import find_peaks
import numpy as np
def filter_peaks(variable, threshold_value):


    threshold_value = float(threshold_value)
    # mask out nan values
    # mask = np.isfinite(variable)
    # y_vals_clean = variable[mask]

    # map valleys and peaks

    # add savety 
    if np.all(np.isnan(variable)):
        return [], []
    
    peaks, _ = find_peaks(variable, prominence=0.02, distance=20) # output is the index of the interp curve
    # valleys, _ = find_peaks(-variable, prominence=0.02, distance=10)

    # for peak in peaks:
    #     # left_valleys = valleys[valleys < peak]
    #     # right_valleys = valleys[valleys > peak]

    #     # if len(left_valleys) > 0 and len(right_valleys) > 0:
    #         # left_valley_idx = left_valleys[-1]
    #         # right_valley_idx = right_valleys[0]

    #     amplitudes = variable[peak] #- variable[left_valley_idx]
        
    #     # peak_time = time_index[peak]
    
    
    #     peak_amplitudes.append((peak, amplitudes))


    # Calculate amplitudes at all peaks
    peak_amplitudes = [(peak, variable[peak]) for peak in peaks]
    

    if len(peaks) == 0:
        return [], []
    
    filtered_list = []
    rpd_list = []

    if peak_amplitudes: 

        for i in range(len(peak_amplitudes)-1):
            amp1 = peak_amplitudes[i][1]
            amp2 = peak_amplitudes[i+1][1]
            rpd = np.abs((amp1 - amp2) / ((amp1 + amp2) / 2)) * 100 
            rpd_list.append(rpd)

        rpd_list = sorted(rpd_list)
        # 1 filter by threshold 
        max_min_amp = max(amplitudes for _, amplitudes in peak_amplitudes)
        threshold = threshold_value * max_min_amp
        filtered_list = [(p, a) for p, a in peak_amplitudes if a >= threshold]

        

        if len(rpd_list) <2:
            rpd_list.append(0)

        # 2 filter to get only the two highest values in case after applying the threshold three will remain
        sorted_peaks = sorted(filtered_list, key=lambda x: x[1], reverse=True)
        top_two = sorted_peaks[:2]
        rpd_two = rpd_list[:2]

        return top_two, rpd_two





        
    # rpd_list = []
    # if peak_amplitudes:


    # #     # filter by threshold 
    #     max_min_amp = max(amplitudes for _, amplitudes in peak_amplitudes)


    #     threshold = threshold_value * max_min_amp

    #     for i in range(len(peak_amplitudes)):
    #         rpd = np.abs((peak_amplitudes[i][1] - max_min_amp)/max_min_amp*100)
    #         rpd_list.append(rpd)   
        
    #     filtered = [(p, a) for p, a in peak_amplitudes if a >= threshold]

    # return filtered, rpd_list

    # #     # filter to get only the two highest values in case after applying the threshold three will remain

    # #     top_two_filtered = sorted(filtered, key=lambda x: x[1], reverse=True)[:2]
    # #     # the peak position is extracted 
    # #     # top_two_filtered_peaks = [p for p, _ in top_two_filtered]

    # return top_two_filtered