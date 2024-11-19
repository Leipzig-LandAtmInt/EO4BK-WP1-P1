# EO4BK-WP1-P1

## Install Conda environment
Create conda environment from yml file using following command in your terminal
```
$ conda env create -f wp1_d21_v0.yml
```
Alternatively, The conda environment can be given a customised name with following command in your terminal. 
```
$ conda env create -f wp1_d21_v0.yml -n <your name>
```
Check whether the new environment is installed.
```
$ conda info --envs
```
After that conda environment can be activated with
```
$ conda activate wp1_d21_v0
```

## Branch D2.1_V1.1_0.1

The branch D2.1_V1.1_0.1 containts the D2.1_V1.1_0.1 eo4bk sentle pipline build up on the sentle==2024.10.2 version. This pipeline showed to be unstable due to dask. 

## Branch D2.1_V1.1_0.2 

The branch D2.1_V1.1_0.2 contains the D2.1_V1.1_0.2 eo4bk sentle pipline build on the sentle==2024.10.5 version. 

## Jupyter Notebooks

The branch Jupyter Notebooks contains the Jupyter Notebooks on preprocessing LUCAS 2018 and LUCAS 2022 to the newest (V1.1) EO4BK Nomenclature. 

## Reference

The Vegetation Indicies (VI) are computed with spyndex (https://github.com/awesome-spectral-indices/spyndex)

The Sentinel 1 and 2 download is done with sentle (https://github.com/cmosig/sentle/tree/main)
