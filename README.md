# xifs
## What is xifs?
The xifs package is a post-processing tool for OpenIFS model output data. Seasonal and global means, global mean CRF, jet propertes, SSW dates, etc. can be easily calculated. Examples can be found here: notebooks/xifs_plots.ipynb

## How to use xifs
After the installation (see below), xifs can be imported to a Python script:
```python
import xifs.xifs as xifs

```
To run an analysis, we need the path to a netCDF file and a list of keywords that need to be calculated. The output will be a dictionary which can be saved as a netCDF file by using the to_netcdf function:

```python
list = ['kw1','kw2',kw3']
result = xifs.analysis(list, 'path/to/input/netcdf/file.nc')
xifs.to_netcdf(result, 'path/to/where/you/want/your/file/to/be/saved.nc')

```
## What does xifs.analysis calculate?
### global means
Global means are weighted by latitude. Keywords for global means must be 'glomean_'+ variable name of your input data, e.g. 'glomean_2t'. The output unit is the same as the input.
### seasonal means
Seasonal means are weighted by the length of the months. Keywords for seasonal means must be 'seasmean_'+ variable name of your input data, e.g. 'seasmean_2t'.
The output unit is the same as the input.
### global CRF
The global mean Cloud Radiative Force (CRF) can be selected with 'glomean_crf'. The unit is given in J/m².
### Stratospheric and Tropospheric jet properties
* The Polar Vortex can be selected by 'polar_vortex'. The output is the zonal wind at 60°N and 10hPa over time. (unit = m/s)
* 'QBO' calculates the Quasi Biennial Oscillation Index by selecting the grid point closest to Singapore (lat=1.29,lon=103.85), and returning monthly means. The output array is 3-dimensional (u (unit=m/s), pressure_level, time).
* To find Stratospheric Sudden Warming Events, 'SSW' has to be used. It returns a 1D-array with all SSW events found in the input Dataset. SSW central dates are defined as zonal mean zonal wind reversal (westerly to easerly) at 10hPa and 60°N. For this analysis, an extended winter season NDJFM was selected. To find the SSW events, three conditions were used.
 1. No SSW can be selected within the 20 days time-range after a previous SSW event.
 2. If the winds turn easterly for 30 consecutive days without turning westerly again before April 30th, these events are assumed to be final warmings and are discarded.
 3. Before a SSW event, there need to be (at least) 10 consecutive days of westerlies.

For tropospheric jet calculation we have two options:
* Keyword 'jet' returns four variables: 'jet_nh_pos', 'jet_sh_value', 'jet_sh_pos', 'jet_sh_value'. All arrays are 3-dimenional (lat/u, time, longitude). It basically returns the position and strength of the northern and southern hemispheric tropospheric jet by finding the total wind maximum at 300hPa at 40-90°N / 40-90°S.
* Keyword 'mw_jet' returns eight variables:
  * 'mwu' is a 4-dimensional output array (mass weighted average wind speed, latitude, longitude, time).
  * 'mwp' is a 4-dimensional output array (mass flux weighted pressure, latitude, longitude, time).
  * 'mw_jet_nh' is the position of the mass weighted northern hemispheric jet. It is a 3-dimensional output array (latitude, longitude, time).
  * 'mw_jet_sht' is the position of the mass weighted southern hemispheric subtropical jet. It is a 3-dimensional output array (latitude, longitude, time).
  * 'mw_jet_shp' is the position of the mass weighted southern hemispheric polar jet. It is a 3-dimensional output array (latitude, longitude, time).
  * 'ws_jet_nh' is the mass weighted wind speed of the northern hemispheric jet and is 3-dimensional (wind speed, longitude, time) 
  * 'ws_jet_sht' is the mass weighted wind speed of the southern hemispheric subtropical jet and is 3-dimensional (wind speed, longitude, time)
  * 'ws_jet_shp' is the mass weighted wind speed of the southern hemispheric polar jet and is 3-dimensional (wind speed, longitude, time)
 All mass weighted calculations were done analogous to Archer, Caldeira (2008).

## Installation
install dependencies
```
curl -X GET "https://raw.githubusercontent.com/nanahocke/xifs/main/xifs_environment.yml" -o xifs_environment.yml
conda env create -n xifs_env -f xifs_environment.yml
```
Install xifs
```
conda activate xifs_env
pip install git+https://github.com/nanahocke/xifs.git@main
```
