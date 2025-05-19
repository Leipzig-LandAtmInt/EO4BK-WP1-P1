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




    # def HANTS(self, HiLo = None, low = None, high = None, fet = None, nf = None, dod = None, delta = None, fill_val = None):

    #     y = np.array(self.var.data)
    #     y = np.where(np.isnan(y), 0, y)
    #     ni = len(y)

    #     nb = len(y)

    #     ts = list(range(0,len(y)))
    #     hants = self.HANTS_function(ni = ni, nb = nb, nf = nf, y = y, ts = ts, HiLo = HiLo, low = low, high = high, fet = fet, dod = dod, delta = delta, fill_val = fill_val)[0]
        
    #     self.datadict[f'{self.varname}_HANTS'] = hants


    #     return self.datadict

    def HANTS(self, HiLo=None, low=None, high=None, fet=None, nf=None, dod=None, delta=None, fill_val=None, pad_len=5):
        
        
        y_orig = np.array(self.var.data)
        y_orig = np.where(np.isnan(y_orig), 0, y_orig)
        ni_orig = len(y_orig)

        # Pad data with repeated endpoints
        y_pad = np.concatenate((
            np.full(pad_len, y_orig[0]),
            y_orig,
            np.full(pad_len, y_orig[-1])
        ))
        ts_pad = list(range(len(y_pad)))
        ni = len(y_pad)
        nb = len(y_pad)

        # Run padded HANTS
        hants_padded = self.HANTS_function(
            ni=ni,
            nb=nb,
            nf=nf,
            y=y_pad,
            ts=ts_pad,
            HiLo=HiLo,
            low=low,
            high=high,
            fet=fet,
            dod=dod,
            delta=delta,
            fill_val=fill_val
        )[0]

        # Remove padding from result
        hants_result = hants_padded[pad_len:-pad_len]

        # Save to dictionary
        self.datadict[f'{self.varname}_HANTS'] = hants_result

        return self.datadict