import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

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
    

