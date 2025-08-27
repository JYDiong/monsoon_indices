# 🌏 Monsoon Indices 
**Generalized Monsoon Indices Plotting**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)
[![GitHub stars](https://img.shields.io/github/stars/jeongyik/monsoon_indices)](https://github.com/jeongyik/monsoon_indices/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/jeongyik/monsoon_indices)](https://github.com/jeongyik/monsoon_indices/network/members)
[![Last Commit](https://img.shields.io/github/last-commit/jeongyik/monsoon_indices)](https://github.com/jeongyik/monsoon_indices/commits/main)



### 📖 Overview
This repository provides a **generalized Python framework** for:  
- Loading any NetCDF dataset  
- Automatically detecting `u`/`v` wind components  
- Computing multiple climate indices  
- Interactive plotting functions (via `mia.py`)  

## 📂 Repository Structure 

│

├── mia.py                 # Contains all plotting functions

├── monsoon\_indices.py     # Main script to load data, process, and call plotting functions

├── README.md              # This README file

└── requirements.txt       # Required Python packages



**Requirements**

Python >= 3.9 with the following packages:

xarray

pandas

matplotlib

seaborn

netCDF4

argparse (standard library)

You can install the dependencies using:

pip install xarray pandas matplotlib seaborn netCDF4

**Features**

Modular plotting functions in mia.py

Automatic detection of u/v wind variable names in NetCDF files

Daily averaging of wind data

Flexible region selection

User can choose which indices to plot

Input either a local/remote NetCDF file or fetch GFS 0.25° data by date and cycle

Automatic creation of output directories

CSV export for all indices

User-friendly CLI with --help

**Usage**

***Show help***

python monsoon\_indices.py --help
Output:

usage: monsoon\_indices.py \[-h] \[--file FILE] \[--date DATE] \[--cycle {00z,06z,12z,18z}]

&nbsp;                          \[--outdir OUTDIR] \[--indices INDICES]

***Plot indices from a NetCDF file***

python monsoon\_indices.py --file /path/to/data.nc --indices SWMI1,NEMI

This will:
Read /path/to/data.nc
Compute and plot SWMI1 and NEMI
Save CSV and PNG files to the default output directory /home/index/GFS (can be changed with --outdir)










