
import numpy as np
import rioxarray as rio
from _create_cglob_attributes_ import create_cglob_attributes
from _create_reference_attributes_ import create_ref_attributes
import xarray as xr




def build_datacube(value_dic, lon, lat, polygon,CROPTYPE,  VARIABLE,YEAR1, YEAR2, YEAR_overlap):

    fixed_time = [f'{YEAR1}-07-31',f'{YEAR1}-08-10',f'{YEAR1}-08-20',f'{YEAR1}-08-31',f'{YEAR1}-09-10',f'{YEAR1}-09-20',f'{YEAR1}-09-30',f'{YEAR1}-10-10',
              f'{YEAR1}-10-20',f'{YEAR1}-10-31', f'{YEAR1}-11-10',f'{YEAR1}-11-20',f'{YEAR1}-11-30',f'{YEAR1}-12-10',f'{YEAR1}-12-20',
              f'{YEAR1}-12-31',f'{YEAR2}-01-10',f'{YEAR2}-01-20',f'{YEAR2}-01-31',f'{YEAR2}-02-10',f'{YEAR2}-02-20',f'{YEAR2}-02-28',f'{YEAR2}-03-10',
              f'{YEAR2}-03-20',f'{YEAR2}-03-31',f'{YEAR2}-04-10',f'{YEAR2}-04-20',f'{YEAR2}-04-30',f'{YEAR2}-05-10',f'{YEAR2}-05-20',
              f'{YEAR2}-05-31',f'{YEAR2}-06-10',f'{YEAR2}-06-20',f'{YEAR2}-06-30',f'{YEAR2}-07-10',f'{YEAR2}-07-20',f'{YEAR2}-07-31',f'{YEAR2}-08-10']

    var_list = [f'{VARIABLE}','LENGTH_AFTER','LENGTH_BEFORE','NOBS','QFLAG','RMSE']

    # build data_vars 
    data_vars = {}
    for key in var_list:
        if key in value_dic:
            values = []
            for time in fixed_time:
                try:
                    value = value_dic[key][time]
                except KeyError:
                    value = np.full_like(next(iter(value_dic[key].values())), np.nan, dtype = np.float64)
                values.append(value)

            data_vars[f'cglob_{key}'] = (["time", "lat", "lon"], values)

    
    VARNAME = f'{VARIABLE}_{YEAR2}'

    data_vars['lcs_point_id'] = (["index"], polygon['point_id'])

    datacube = xr.Dataset(
        data_vars=data_vars,
        coords=dict(
            lon=("lon", np.sort(lon)),
            lat=("lat", sorted(lat, reverse = True)),
            time=("time", fixed_time)
        )
    )

    datacube.attrs['Acknowledgment'] = 'All EO4BK data providers are acknowledged inside each variable'
    datacube.attrs['Description'] = 'Data variables with the prefix "cglob_" are referring to Copernicus Global Land Operations "CGLOPS-1", \nData varaibales with the prefix "lcs_" are referring to Reference data variables'

    for var, attr in create_cglob_attributes(YEAR1 = YEAR1, YEAR2 = YEAR2, VAR=VARNAME).items():

        datacube[f'cglob_{var}'].attrs.update(attr)

    for var, attr in create_ref_attributes(CROPTYPE, polygon['point_id'], YEAR_overlap).items():
        datacube[f'lcs_{var}'].attrs.update(attr)
    
    return datacube