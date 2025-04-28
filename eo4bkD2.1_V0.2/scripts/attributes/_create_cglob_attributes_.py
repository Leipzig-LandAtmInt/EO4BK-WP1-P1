#TODO extent by the other years

def create_cglob_attributes(YEAR1, YEAR2, VAR = None,**kwargs):
    
    '''
    This function creates all the attributes to descripe the variables in the final .zarr data. 
    '''

    # Defines the Attributes for Sentinel-2
    
    YEAR1 = int(YEAR1)
    YEAR2 = int(YEAR2)

    if YEAR1 < 2021 or YEAR2 < 2021:

        
        if VAR ==f'LAI_{YEAR2}':
        
            cglob_lai_global_attributes = {'Original resolution': '333 m' , 'Pixel Size': '333 m', 'Temporal Resolution':'10 days','Sensor':'Based on PROBA-V (from January 2014 to June 2020) \nBased on OLCI from July 2020 onwards.',
            'Previous Product Identifier':f'urn:cgls:global:lai300_v1_333m:LAI300_{YEAR2}XXXXXXXX_GLOBE_PROBAV_V1.0.1','Processing Level':'L3', 'Reference':'https://land.copernicus.eu/global/products/lai', 
            'Copyright':f'Copernicus Service information {YEAR1} & {YEAR2}'}

            cglob_attributes = {
                'LAI': {'Long name': 'Leaf Area Index 333m', 'Units': 'm^2/m^2',**cglob_lai_global_attributes},
                'LENGTH_AFTER':{'Long name':'Length of semi-period after product date', 'Units':'days',**cglob_lai_global_attributes},
                'LENGTH_BEFORE':{'Long name':'Length of semi-period before product date', 'Units':'days',**cglob_lai_global_attributes},
                'NOBS':{'Long name':'leaf_area_index number_of_observations', 'Units':'','Valid range':'0,60',**cglob_lai_global_attributes},
                'QFLAG':{'Long name':'Quality Flag on LAI 333m', 'Units':'','Flag meanings':'LLand EBF Interpolated_missing_dekad From_previous_dekadal_products Polynomial_fit Linear_fit Interpolated_nearest_dates Nearest_fit Instantaneous_value',**cglob_lai_global_attributes},
            'RMSE':{'Long name':'RMSE on LAI 333m', 'Units':'',**cglob_lai_global_attributes}
            }

        elif VAR == f'FAPAR_{YEAR2}':

            cglob_fapar_global_attributes = {'Original resolution': '333 m' , 'Pixel Size': '333 m', 'Temporal Resolution':'10 days','Sensor':'Based on PROBA-V (from January 2014 to June 2020) \nBased on OLCI from July 2020 onwards.',
            'Previous Product Identifier':'urn:cgls:global:fapar300_v1_333m_V1.0.1','Processing Level':'L3', 'Reference':'http://land.copernicus.eu/global/products/fapar', 
            'Copyright':f'Copernicus Service information {YEAR1} & {YEAR2}'}

            cglob_attributes = {
                'FAPAR': {'Long name': 'Fraction of Absorbed Photosynthetically Active Radiation 333m', 'Units': '',**cglob_fapar_global_attributes},
                'LENGTH_AFTER':{'Long name':'Length of semi-period after product date', 'Units':'days',**cglob_fapar_global_attributes},
                'LENGTH_BEFORE':{'Long name':'Length of semi-period before product date', 'Units':'days',**cglob_fapar_global_attributes},
                'NOBS':{'Long name':'fraction_of_surface_downwelling_photosynthetic_radiative_flux_absorbed_by_vegetation number_of_observations', 'Units':'',**cglob_fapar_global_attributes},
                'QFLAG':{'Long name':'Quality flag on FAPAR 333m', 'Units':'','Flag meanings':'Land EBF Interpolated_missing_dekad From_previous_dekadal_products Polynomial_fit Linear_fit Interpolated_nearest_dates Nearest_fit Instantaneous_value',**cglob_fapar_global_attributes},
                'RMSE':{'Long name':'RMSE on FAPAR 333m', 'Units':'',**cglob_fapar_global_attributes}
            }

        elif VAR == f'FCOVER_{YEAR2}':

            cglob_fcover_global_attributes = {'Original resolution': '333 m' , 'Pixel Size': '333 m', 'Temporal Resolution':'10 days',
            'Sensor':'Based on PROBA-V (from January 2014 to June 2020) \nBased on OLCI from July 2020 onwards.',
            'Previous Product Identifier':f'urn:cgls:global:fcover300_v1_333m:FCOVER300_{YEAR2}XXXXXXXX_GLOBE_PROBAV_V1.0.1','Processing Level':'L3', 'Reference':'http://land.copernicus.eu/global/products/fcover', 
            'Copyright':f'Copernicus Service information {YEAR1} & {YEAR2}'}

            cglob_attributes = {
                'FCOVER': {'Long name': 'Fraction of green Vegetation Cover 333m', 'Units': '',**cglob_fcover_global_attributes},
                'LENGTH_AFTER':{'Long name':'Length of semi-period after product date', 'Units':'days',**cglob_fcover_global_attributes},
                'LENGTH_BEFORE':{'Long name':'Length of semi-period before product date', 'Units':'days',**cglob_fcover_global_attributes},
                'NOBS':{'Long name':'vegetation_area_fraction number_of_observations', 'Units':'',**cglob_fcover_global_attributes},
                'QFLAG':{'Long name':'Quality flag on FCover 333m', 'Units':'','Flag meanings':'Land EBF Interpolated_missing_dekad From_previous_dekadal_products Polynomial_fit Linear_fit Interpolated_nearest_dates Nearest_fit Instantaneous_value',**cglob_fcover_global_attributes},
                'RMSE':{'Long name':'RMSE of FCover 333m', 'Units':'',**cglob_fcover_global_attributes}
            }
            


    elif YEAR1 >= 2021 and YEAR2 >= 2021:
        
        if VAR ==f'LAI_{YEAR2}': 
        
            cglob_lai_global_attributes = {'Original resolution': '333 m' , 'Pixel Size': '333 m', 'Temporal Resolution':'10 days','Sensor':'OLCI',
            'Previous Product Identifier':f'urn:cgls:global:lai300_v1_333m:LAI300_{YEAR2}XXXXXXXX_GLOBE_OLCI_V1.0.1','Processing Level':'L3', 'Reference':'https://land.copernicus.eu/global/products/lai', 
            'Copyright':f'Copernicus Service information {YEAR1} & {YEAR2}'}

            cglob_attributes = {
                'LAI': {'Long name': 'Leaf Area Index 333m', 'Units': 'm^2/m^2',**cglob_lai_global_attributes},
                'LENGTH_AFTER':{'Long name':'Length of semi-period after product date', 'Units':'days',**cglob_lai_global_attributes},
                'LENGTH_BEFORE':{'Long name':'Length of semi-period before product date', 'Units':'days',**cglob_lai_global_attributes},
                'NOBS':{'Long name':'leaf_area_index number_of_observations', 'Units':'','Valid range':'0,60',**cglob_lai_global_attributes},
                'QFLAG':{'Long name':'Quality Flag on LAI 333m', 'Units':'','Flag meanings':'LLand EBF Interpolated_missing_dekad From_previous_dekadal_products Polynomial_fit Linear_fit Interpolated_nearest_dates Nearest_fit Instantaneous_value',**cglob_lai_global_attributes},
                'RMSE':{'Long name':'RMSE on LAI 333m', 'Units':'',**cglob_lai_global_attributes}
            }


        
        elif VAR == f'FAPAR_{YEAR2}':

            cglob_fapar_global_attributes = {'Original resolution': '333 m' , 'Pixel Size': '333 m', 'Temporal Resolution':'10 days',
            'Sensor':'OLCI','Previous Product Identifier':'urn:cgls:global:fapar300_v1_333m:FAPAR300-RT6_2022XXXXXXXX_GLOBE_OLCI_V1.1.2','Processing Level':'L3', 
            'Reference':'http://land.copernicus.eu/global/products/fapar', 'Copyright':f'Copernicus Service information {YEAR1} & {YEAR1}'}

            cglob_attributes = {
                'FAPAR': {'Long name': 'Fraction of Absorbed Photosynthetically Active Radiation 333m', 'Units': '',**cglob_fapar_global_attributes},
                'LENGTH_AFTER':{'Long name':'Length of semi-period after product date', 'Units':'days',**cglob_fapar_global_attributes},
                'LENGTH_BEFORE':{'Long name':'Length of semi-period before product date', 'Units':'days',**cglob_fapar_global_attributes},
                'NOBS':{'Long name':'fraction_of_surface_downwelling_photosynthetic_radiative_flux_absorbed_by_vegetation number_of_observations', 'Units':'',**cglob_fapar_global_attributes},
                'QFLAG':{'Long name':'Quality flag on FAPAR 333m', 'Units':'','Flag meanings':'Land EBF Missing_dekad_interpolated From_previous_dekadal_product_or_missing 2nd_degree_polynomial_fit Linear_fit Interpolated_two_nearest_dates Nearest_in_5_day_window Instantaneous_ebf',**cglob_fapar_global_attributes},
                'RMSE':{'Long name':'RMSE on FAPAR 333m', 'Units':'',**cglob_fapar_global_attributes}
            }
            

        elif VAR == f'FCOVER_{YEAR2}':

            cglob_fcover_global_attributes = {'Original resolution': '333 m' , 'Pixel Size': '333 m', 'Temporal Resolution':'10 days','Sensor':'OLCI',
            'Previous Product Identifier':f'urn:cgls:global:fcover300_v1_333m:FCOVER300-RT6_{YEAR2}XXXXXXXX_GLOBE_OLCI_V1.1.2','Processing Level':'L3', 'Reference':'http://land.copernicus.eu/global/products/fcover', 'Copyright':f'Copernicus Service information {YEAR1} & {YEAR2}'}

            cglob_attributes = {
                'FCOVER': {'Long name': 'Fraction of green Vegetation Cover 333m', 'Units': '',**cglob_fcover_global_attributes},
                'LENGTH_AFTER':{'Long name':'Length of semi-period after product date', 'Units':'days',**cglob_fcover_global_attributes},
                'LENGTH_BEFORE':{'Long name':'Length of semi-period before product date', 'Units':'days',**cglob_fcover_global_attributes},
                'NOBS':{'Long name':'vegetation_area_fraction number_of_observations', 'Units':'',**cglob_fcover_global_attributes},
                'QFLAG':{'Long name':'Quality flag on FCover 333m', 'Units':'','Flag meanings':'Land EBF Missing_dekad_interpolated From_previous_dekadal_product_or_missing 2nd_degree_polynomial_fit Linear_fit Interpolated_two_nearest_dates Nearest_in_5_day_window Instantaneous_ebf',**cglob_fcover_global_attributes},
                'RMSE':{'Long name':'RMSE of FCover 333m', 'Units':'',**cglob_fcover_global_attributes}
            }
          
    return cglob_attributes