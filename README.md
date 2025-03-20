# EO4BK Copernicus Land Monitoring Service
This pipeline includes two steps. 

## 1) Download globale copernicus land monitoring service netcdf
This global product has a revisiting time of approximately 10 days and a spatial resolution of 300 m. For some years, e.g. 2022 December is missing. One netcdf file corresponds to one time-step and has a size of ~ 2 GB. 

To download different years and variables, fcover must be changed to lai or fapar, and years must be changed to the desired year in ```download_tile_cluster.py```.

```
variable = 'fcover'

YEAR = '2018'
```

## 2) 
