import xarray as xr
import pandas as pd
import numpy as np

class phenometric():

    def __init__(self, variables, timestamp):

        self.time = timestamp
        self.doy = timestamp.dt.dayofyear
        self.year = timestamp.dt.year
        self.var = variables
        # first peak of the season as the maximum of the time-series
        self.maximum = variables.max()
        # the day of the first peak of the season
        self.season_max_day = np.array(self.time[self.var == self.maximum])

        
    def percentage(self, peak, per):

        sos_doy = None
        eos_doy = None
        pos_doy = None
        sos_day = None
        eos_day = None


        pos_day = self.time[self.var == peak]

        pos_doy = pos_day.dt.dayofyear.data[0]


        
        # SOS the day at which the time-series is the first time over the threshold
        pct = ((np.max(self.var) - np.min(self.var)) * per / 100) + np.min(self.var)

        #sos_doy = self.doy[self.doy <= peak][self.var[self.doy <= peak] <= pct].max() + 1  # to get the first date that has crossed the threshold

        sos_mask = (self.time.data <= pos_day.data) & (self.var <= pct)
        filtered_sos_day = self.time[sos_mask]

        if len(filtered_sos_day) == 0:
            sos_day = None
        else:
            sos_day = filtered_sos_day.max() 
            sos_doy = sos_day.dt.dayofyear.data

        # EOS as the day at which the time-series is the first time under the threshold
       
        eos_mask = (self.time.data >= pos_day.data) & (self.var <= pct)

        filtered_eos_day = self.time[eos_mask]

        
        if len(filtered_eos_day) == 0:
            eos_day = None
        else:
            eos_day = filtered_eos_day.min()
            eos_doy = eos_day.dt.dayofyear.data
        
        return sos_doy, eos_doy, pos_doy, sos_day, eos_day, pos_day

