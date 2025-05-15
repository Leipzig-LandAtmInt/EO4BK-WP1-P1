import pandas as pd
import numpy as np


def check_order(sos_day_list, pos_day_list, eos_day_list):
    
    sos_day1 = pos_day1 = eos_day1 = sos_day2 = pos_day2 = eos_day2 = np.nan

    if len(pos_day_list) > 1: 
        sos_day1 = sos_day_list[0]
        
        pos_day1 = pos_day_list[0]
        
        eos_day1 = eos_day_list[0]
        
        sos_day2 = sos_day_list[1]
        
        pos_day2 = pos_day_list[1]
        
        eos_day2 = eos_day_list[1]
    
    if len(pos_day_list) == 1:

        sos_day1 = sos_day_list[0]

        pos_day1 = pos_day_list[0]

        eos_day1 = eos_day_list[0]

        return sos_day1, pos_day1, eos_day1

    if not pd.isnull(sos_day1) and not pd.isnull(pos_day1):

        if sos_day1.values > pos_day1.values:

            sos_day1 = np.nan
    if not pd.isnull(sos_day1) and not pd.isnull(pos_day2):

        if sos_day1.values > pos_day2.values:

            sos_day1 = np.nan 

    if not pd.isnull(eos_day1) and not pd.isnull(pos_day1):

        if eos_day1.values < pos_day1.values:

            eos_day1 = np.nan

    if not pd.isnull(eos_day1) and not pd.isnull(pos_day2):

        if eos_day1.values > pos_day2.values:

            eos_day1 = np.nan

    if not pd.isnull(eos_day1) and not pd.isnull(sos_day2):

        if eos_day1.values > sos_day2.values:

            eos_day1 = np.nan
    
    if not pd.isnull(sos_day2) and not pd.isnull(pos_day2):

        if sos_day2.values > pos_day2.values:

            sos_day2 = np.nan

    if not pd.isnull(sos_day2) and not pd.isnull(pos_day1):

        if sos_day2.values < pos_day1.values:

            sos_day2 = np.nan

    if not pd.isnull(eos_day2) and not pd.isnull(pos_day1):

        if eos_day2.values < pos_day1.values:

            eos_day2 = np.nan
    
    if not pd.isnull(eos_day2) and not pd.isnull(pos_day2):

        if eos_day2 < pos_day2:

            eos_day2 = np.nan



    return sos_day1, pos_day1, eos_day1, sos_day2, pos_day2, eos_day2