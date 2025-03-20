# EO4BK Copernicus Land Monitoring Service
This pipeline includes two steps. 

## 1) Download globale copernicus land monitoring service netcdf
This global product has a revisiting time of approximately 10 days and a spatial resolution of 300 m. For some years, e.g. 2022 December is missing. One netcdf file corresponds to one time-step and has a size of ~ 2 GB. 

To download different years and variables, fcover must be changed to lai or fapar, and years must be changed to the desired year in ```download_tile_cluster.py```.

```
variable = 'fcover'

YEAR = '2018'
```
To  download, execute the shell script. It should download a whole year. The shell script inserts a 'y' variable everytime the API askes for permission to downloading a netcdf file.

### Known Problems

Check whether the ```clob_VARIABLE300_YEAR_GLOBE``` folder only contains netcdf files without subfolders. The script should unpack the subfolders that are created during the download and then delete them. However, this sometimes seems to fail.

## 2) Create datacubes from the global netcdf files
In the second step, the pipeline essentially clips the netcdf data with the reference polygons (as done for V1) to create .zarr.zip files. There is no need to change create_lucas_attribues.py for the brazilien reference datasets as it assigns the correct attributes according to following logic:
```
CONAB; Soybean, Coffee, Cotton, Soybean-maize, Rice.
MapBiomas; Fruit and Nut, Oil Pam
TerraClass; Sugarcane <- is missing

```
In main_cglob_execute.py, the following variables needs to be changed:
```

HOME = 'folder/of/the/netcdffiles'

YEAR1 = '2017'
YEAR2 = '2018'
YEAR_overlap = '1718' # for overlapping years

VARIABLE = 'FCOVER'  # change to LAI, FCOVER

DETAIL_LEVEL = 'hd'
CROPTYPE = 'Rice'  

OUTPUT_MAIN = f'directory/to/store/datacubes/cglob_datacube/Output_{VARIABLE}/{YEAR_overlap}'
```
