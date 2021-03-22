import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import hvplot.xarray
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import cartopy.crs as ccrs

def CRF(filename):
    """loads netCDF file, calculates CRF on lat/lon grid, plots global mean in a time series"""
    
    ds=xr.open_dataset(filename)
    
    ###variables
    ttrc=ds.ttrc
    tsrc=ds.tsrc
    ttr=ds.ttr
    tsr=ds.tsr
    
    weights=np.cos(np.deg2rad(ds.lat))
    
    ###Calculation of CRF, is this correct?
    CRF_LW=ttrc-ttr
    CRF_SW=tsrc-tsr
    CRF=CRF_SW+CRF_LW
    CRF_weighted=CRF.weighted(weights)
    CRF_global_mean=CRF_weighted.mean(('lat', 'lon'))/10800
    
    ###plotting
    plt.figure(figsize=(15,5))
    CRF_global_mean.plot()
    plt.ylabel('CRF [$W/m^2$]')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'_CRF.png')
    
    
def output_variable(filename, var):
    """input: netcdf data, string of variable, plots global average of variable over time"""
    ds=xr.open_dataset(filename)
    
    variable=ds[var]
    weights=np.cos(np.deg2rad(ds.lat))
    var_weighted=variable.weighted(weights)
    
    var_global_mean=var_weighted.mean(('lat', 'lon'))
    
    ###plotting
    plt.figure(figsize=(15,5))
    var_global_mean.plot()
    plt.ylabel(var+' ['+variable.attrs['units']+']')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'_'+var+'.png')    
    
def output_variable_seasonal_map(filename, var, seas):
    """input: netcdf data, variable, season; plots seasonal average of variable as Mollweide projection"""
    ds=xr.open_dataset(filename)
    
    month_length=ds[var].time_counter.dt.days_in_month
    weights = month_length.groupby('time_counter.season') / month_length.groupby('time_counter.season').sum()
    np.testing.assert_allclose(weights.groupby('time_counter.season').sum().values, np.ones(4))
    ds_weighted = (ds[var] * weights).groupby('time_counter.season').sum(dim='time_counter')
    
    var_season=ds_weighted.sel(season=seas)
    
    ###plotting
    plt.figure(figsize=(10,5))
    p = var_season.plot(cmap='Spectral',
        subplot_kws=dict(projection=ccrs.Mollweide(0), facecolor="gray"),
        transform=ccrs.PlateCarree(),
    )
    plt.title(var+' ['+ds[var].attrs['units']+']\nseason='+seas)
    p.axes.gridlines()
    p.axes.coastlines()    

