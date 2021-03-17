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
    
    ###Calculation of CRF, is this correct?
    CRF_LW=ttrc-ttr
    CRF_SW=tsrc-tsr
    CRF=CRF_SW+CRF_LW
    CRF_lat_mean=CRF.mean('lat')
    CRF_global_mean=CRF_lat_mean.mean('lon')/10800 #for unit in W/m²
    
    ###plotting
    plt.figure(figsize=(15,5))
    CRF_global_mean.plot()
    plt.ylabel('CRF [$W/m^2$]')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'.png')
