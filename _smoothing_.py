import pandas as pd
from scipy import signal  
import numpy as np
import math
from copy import deepcopy


class smoothing_methods:

    def __init__(self, variable, time):

        # self.time = pd.to_datetime(timestamp)
        self.time = time
        self.doy = self.time.dt.dayofyear
        self.var = variable

        self.varname = variable.name
        self.year = self.time.dt.year
        
        self.datadict = {'TIME':self.time, 'DOY': self.doy, f'{self.varname}':self.var}
        # self.lower = self.var.reindex(np.arange(-180,self.var.index.max(),1), fill_value = self.var.iloc[0]) # fills up the lower boundaries by the first value of the time-series
        # self.upper = self.var.reindex(np.arange(0,self.var.index.max()+180,1), fill_value = self.var.iloc[-1]) # fills up the upper boundaries by the last value of the time-series
        # self.extentvar = pd.concat([self.lower, self.upper ]).groupby(level=0).first()
        # self.extentdoy = self.extentvar.index
        # self.extentdict = {'DOY':self.extentdoy, f'{self.varname}':self.extentvar}
        # # self.datadict = {f'YEAR{self.year.unique().item()}':{'TIME': self.time, 'VAR':self.var}}



    
    # def clip_extention(self):

    #     resultdict = {}
    #     for key in self.extentdict.keys():
    #         resultdict['TIME'] = self.time
    #         resultdict[key] = self.extentdict[key][(self.extentdict['DOY'] >= 0) & (self.extentdict['DOY'] < self.doy.max())]
            
    #     return resultdict



    def HANTS_function(self, ni, nb, nf, y, ts, HiLo, low, high, fet, dod, delta, fill_val):
        '''
        This function applies the Harmonic ANalysis of Time Series (HANTS)
        algorithm originally developed by the Netherlands Aerospace Centre (NLR)
        (http://www.nlr.org/space/earth-observation/).

        This python implementation was based on two previous implementations
        available at the following links:
        https://codereview.stackexchange.com/questions/71489/harmonic-analysis-of-time-series-applied-to-arrays
        http://nl.mathworks.com/matlabcentral/fileexchange/38841-matlab-implementation-of-harmonic-analysis-of-time-series--hants-
        '''
        # Arrays
        mat = np.zeros((min(2*nf+1, ni), ni))
        # amp = np.zeros((nf + 1, 1))

        # phi = np.zeros((nf+1, 1))
        yr = np.zeros((ni, 1))
        y_len = len(y)
        outliers = np.zeros((1, y_len))

        # Filter
        sHiLo = 0
        if HiLo == 'Hi':
            sHiLo = -1
        elif HiLo == 'Lo':
            sHiLo = 1

        nr = min(2*nf+1, ni)
        noutmax = ni - nr - dod
        # dg = 180.0/math.pi
        mat[0, :] = 1.0

        ang = 2*math.pi*np.arange(nb)/nb
        cs = np.cos(ang)
        sn = np.sin(ang)

        i = np.arange(1, nf+1)
        for j in np.arange(ni):
            index = np.mod(i*ts[j], nb)
            mat[2 * i-1, j] = cs.take(index)
            mat[2 * i, j] = sn.take(index)

        p = np.ones_like(y)
        bool_out = (y < low) | (y > high)
        p[bool_out] = 0
        outliers[bool_out.reshape(1, y.shape[0])] = 1
        nout = np.sum(p == 0)

        if nout > noutmax:
            if np.isclose(y, fill_val).any():
                ready = np.array([True])
                yr = y
                outliers = np.zeros((y.shape[0]), dtype=int)
                outliers[:] = fill_val
            else:
                raise Exception('Not enough data points.')
        else:
            ready = np.zeros((y.shape[0]), dtype=bool)

        nloop = 0
        nloopmax = ni

        while ((not ready.all()) & (nloop < nloopmax)):

            nloop += 1
            za = np.matmul(mat, p*y)

            A = np.matmul(np.matmul(mat, np.diag(p)),
                            np.transpose(mat))
            A = A + np.identity(nr)*delta
            A[0, 0] = A[0, 0] - delta

            zr = np.linalg.solve(A, za)

            yr = np.matmul(np.transpose(mat), zr)
            diffVec = sHiLo*(yr-y)
            err = p*diffVec

            err_ls = list(err)
            err_sort = deepcopy(err)
            err_sort.sort()

            rankVec = [err_ls.index(f) for f in err_sort]

            maxerr = diffVec[rankVec[-1]]
            ready = (maxerr <= fet) | (nout == noutmax)

            if (not ready):
                i = ni - 1
                j = rankVec[i]
                while ((p[j]*diffVec[j] > 0.5*maxerr) & (nout < noutmax)):
                    p[j] = 0
                    outliers[0, j] = 1
                    nout += 1
                    i -= 1
                    if i == 0:
                        j = 0
                    else:
                        j = 1

        return [yr, outliers]


#    def savgol(self,ws = None, po = None):
        
#        sv = signal.savgol_filter(x = self.datadict[f'{self.varname}'], window_length = ws, polyorder = po)
#        sv = pd.Series(sv)
        
#        self.datadict['SAVGOL'] = sv
#        return self.datadict

    # def savgol(self,ws = None, po = None):
        
    #     sv = signal.savgol_filter(x = self.extentdict[f'{self.varname}'], window_length = ws, polyorder = po)
    #     sv = pd.Series(sv, index = self.extentdict['DOY'] )
    #     self.extentdict['SAVGOL'] = sv

    #     # Clip th extented dic to the original expansion 
    #     resultdict = self.clip_extention()
        
    #     #return self.extentdict
    #     return resultdict


    def HANTS(self, HiLo = None, low = None, high = None, fet = None, nf = None, dod = None, delta = None, fill_val = None):

        y = np.array(self.var.data)
        y = np.where(np.isnan(y), 0, y)
        ni = len(y)

        nb = len(y)

        ts = list(range(0,len(y)))
        hants = self.HANTS_function(ni = ni, nb = nb, nf = nf, y = y, ts = ts, HiLo = HiLo, low = low, high = high, fet = fet, dod = dod, delta = delta, fill_val = fill_val)[0]
        
        self.datadict[f'{self.varname}_HANTS'] = hants


        return self.datadict