# Jupyter_Notebooks/

The folder Jupyter_Notebooks contains the folder LUCAS_Polygon_Preprocessing/ and EO4BK_Sentle_Download.ipynb.

# LUCAS_Polygon_Preprocessing/

The folder contains LUCAS2022_Preprocessing_d2.1_v00.ipynb, which was used to create the EO4BK-Nomenclature (V1.0) and LUCAS2022_Preprocessing_d2.1_v01.ipynb, which was used to update the EO4BK-Nomenclature to V1.1. 

## Input Data

For lucas_2022 l2022_survey_crop_poly_rad_allatr.gpkg downloadable at (https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/LUCAS/LUCAS_2022_Copernicus/output/) is used. It can be downloaded and used under Creative Commons Attribution 4.0 International (CC BY 4.0) licence (https://creativecommons.org/licenses/by/4.0).\
For lucas_2018 LUCAS_2018_Copernicus is used, which can be downloaded at (https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/LUCAS/LUCAS_2018_Copernicus/) and  used with Creative Commons Attribution 4.0 International (CC BY 4.0) (https://creativecommons.org/licenses/by/4.0). After downloading, LUCAS_2018_Copernicus_polygons.shp are connected to LUCAS_2018_Copernicus_attributes.csv and 
filtered with ```COPERNICUS_CLEANED==True``` using QGIS.

# Reference

European Union, 1995-2024: LUCAS/LUCAS_2018_Copernicus, https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/LUCAS/LUCAS_2018_Copernicus/ \
European Union, 1995-2024: l2022_survey_cop_poly_rad_allatr, https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/LUCAS/LUCAS_2022_Copernicus/output/
