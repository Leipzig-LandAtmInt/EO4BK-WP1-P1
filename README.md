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

## 2) 
