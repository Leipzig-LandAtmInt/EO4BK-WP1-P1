import numpy as np
import xarray as xr
from scores.continuous import rmse

def build_datacube(xarray_data, vi, smoothed_data, result_dic_season1, result_dic_season2=None, rpd = None):
    '''
    Dataset:
    - smoothed_kndvi: (INTER, time, lat, lon)
    - smoothed_ndvi:  (INTER, time, lat, lon)
    - smoothed_nirv:  (INTER, time, lat, lon)
    - kndvi_QF:       (INTER, QF, lat, lon)
    - ndvi_QF:        (INTER, QF, lat, lon)
    - nirv_QF:        (INTER, QF, lat, lon)
    - pheno_kndvi:    (INTER, PHENO, lat, lon)
    - pheno_ndvi:     (INTER, PHENO, lat, lon)
    - pheno_nirv:     (INTER, PHENO, lat, lon)
    '''   

    inter_results_smoothed = []
    inter_results_qf = []
    inter_results_pheno = []
    inter_results_pheno2 = []

    smoothing_results_dict = {
        "HANTS": smoothed_data  # shape: (time, lat, lon)
    }

    qf_vars = [
        'RMSE',
        'RSQ',
        'NUM_ORIG_DJF',
        'NUM_ORIG_MAM',
        'NUM_ORIG_JJA',
        'NUM_ORIG_SON'
    ]

    time = xarray_data.time.data
    lat = xarray_data.lat.data
    lon = xarray_data.lon.data


    varname = vi.name  # e.g. "kndvi"

    for method_name, smoothed_array in smoothing_results_dict.items():  # Dict[method_name] = ndarray(time, lat, lon)
        inter_id = method_name.lower()

        # Smoothed DataArray
        smoothed_da = xr.DataArray(
            data=smoothed_array,
            dims=["time", "lat", "lon"],
            coords={"time": time, "lat": lat, "lon": lon}
        ).expand_dims(INTER=[inter_id])
        inter_results_smoothed.append(smoothed_da)


        smoothed_da.attrs = vi.attrs

        smoothed_da.attrs['Processing Steps'] += '. The time-series was interpolated according to the INTER Coordinate.'


        # Quality Flags (QFs)
        pearson_corr = xr.corr(vi, smoothed_da.sel(INTER = 'hants'), dim="time")
        rsq = pearson_corr**2
        rmse_val = rmse(vi, smoothed_da.sel(INTER = 'hants'), reduce_dims='time')

        season_counts = {
            f'NUM_ORIG_{season}': vi[vi.time.dt.season == season].count(dim='time')
            for season in ['DJF', 'MAM', 'JJA', 'SON']
        }

        qf_data_vars = {
            'RMSE': rmse_val,
            'RSQ': rsq,
            **season_counts
        }

        qf_stack = np.stack([qf_data_vars[var].data for var in qf_vars], axis=0)

        qf_da = xr.DataArray(
            data=qf_stack,
            dims=["QF", "lat", "lon"],
            coords={"QF": qf_vars, "lat": lat, "lon": lon}
        ).expand_dims(INTER=[inter_id])

        inter_results_qf.append(qf_da)

        # Phenometric Season 1
        qf_vars_pheno = ['SOS_10', 'EOS_10', 'SOS_20', 'EOS_20', 'SOS_30', 'EOS_30', 'POS']
        qf_data_vars_pheno = {}

        for per in ['10', '20', '30']:
            SOS, EOS, POS = result_dic_season1[per]
            qf_data_vars_pheno[f'SOS_{per}'] = SOS
            qf_data_vars_pheno[f'EOS_{per}'] = EOS
            qf_data_vars_pheno['POS'] = POS

        # Assume POS is the same for all, or take the one from '10'
        # qf_data_vars_pheno['POS'] = result_dic_season1['10'][2]
        
        qf_stack_pheno = np.stack(
            [qf_data_vars_pheno[var].data for var in qf_vars_pheno],
            axis=0
        )

        qf_da_pheno = xr.DataArray(
            data=qf_stack_pheno,
            dims=["PHENO", "lat", "lon"],
            coords={"PHENO": qf_vars_pheno, "lat": lat, "lon": lon}
        ).expand_dims(INTER=[inter_id])

        inter_results_pheno.append(qf_da_pheno)      

        # for season 2 
        if result_dic_season2:

            qf_data_vars_pheno2 = {}

            for per in ['10', '20', '30']:
                try:
                    SOS, EOS, POS = result_dic_season2[per]

                    if not np.all(np.isnan(SOS)):
                        qf_data_vars_pheno2[f'SOS_{per}'] = SOS

                    if not np.all(np.isnan(EOS)):
                        qf_data_vars_pheno2[f'EOS_{per}'] = EOS

                    if not np.all(np.isnan(POS)):
                        qf_data_vars_pheno2['POS'] = POS  # Only one POS key, possibly overwritten

                    if rpd:

                        rpd_ = rpd[per]

                        if not np.all(np.isnan(rpd_)):

                            qf_data_vars_pheno2[f'RPD'] = rpd_


                except (KeyError, ValueError):  # Covers missing or unpacking issues
                    pass
        

            qf_vars_pheno2 = list(qf_data_vars_pheno2.keys())
            
            qf_stack_pheno2 = np.stack(
                [qf_data_vars_pheno2[var].data for var in qf_vars_pheno2],
                axis=0
            )
            qf_da_pheno2 = xr.DataArray(
                data=qf_stack_pheno2,
                dims=["PHENO2", "lat", "lon"],
                coords={"PHENO2": qf_vars_pheno2, "lat": lat, "lon": lon}
            ).expand_dims(INTER=[inter_id])

            inter_results_pheno2.append(qf_da_pheno2)      



    # Final concatenation across smoothing methods
    smoothed_combined = xr.concat(inter_results_smoothed, dim="INTER")
    qf_combined = xr.concat(inter_results_qf, dim="INTER")
    qf_combined_pheno = xr.concat(inter_results_pheno, dim="INTER")

    # Build the dataset dictionary step by step
    datacube_vars = {
        f"{varname}_inter": smoothed_combined,
        f"{varname}_QF": qf_combined,
        f"{varname}_PHENO": qf_combined_pheno,
        "lcs_point_id":xarray_data.lcs_point_id
    }
    
    datacube_vars[f'{varname}_PHENO'].attrs = {'Description':'Phenological dates of the first growing season.','Processing Steps':'Phenological dates start of the season (SOS), end of the season (EOS) and the peak of the season (POS) were calculated using the 10%, 20%, 30% threshold according to Maleki et al., 2020 (doi:10.3390/rs12132104).'}
    datacube_vars[f'{varname}_QF'].attrs = {'Long Name':'Quality Flags','Processing Steps':"RSQ (Coefficient of determination) is the squared Pearson's r from the xarray package between the original time-series of a Vegetation Index (VI) and its interpolated counterpart. \nRMSE (Root Mean Squared Error) is calculated using the scores package 2.0.0 between the original time-series and its interpolated counterpart. \nThe NUM_ORIG (number of original observations) per season is the sum of the original observations per season."}
    # Optionally add PHENO2 if available
    if "inter_results_pheno2" in locals():
        try:
            qf_combined_pheno2 = xr.concat(inter_results_pheno2, dim="INTER")
            datacube_vars[f"{varname}_PHENO2"] = qf_combined_pheno2
            datacube_vars[f"{varname}_PHENO2"].attrs = {'Description':'Phenological dates of the second growing season.','Processing Steps':'Phenological dates start of the season (SOS), end of the season (EOS) and the peak of the season (POS) were calculated using the 10%, 20%, 30% threshold according to Maleki et al., 2020 (doi:10.3390/rs12132104).'}
        except Exception:
            pass  # silently ignore if inter_results_pheno2 is defined but invalid

    # Create the final datacube
    datacube = xr.Dataset(datacube_vars)
    datacube.attrs['Description'] = xarray_data.attrs['Description']
    datacube.attrs['Acknowledgment'] = xarray_data.attrs['acknowledgment']
    return datacube
