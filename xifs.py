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
    
    
def surface_pressure(filename):
    """input: netcdf data, plots global average of surface pressure"""
    ds=xr.open_dataset(filename)
    
    #variable
    sp=ds.sp
    
    #weights
    weights=np.cos(np.deg2rad(ds.lat))
    sp_weighted=sp.weighted(weights)
    sp_global_mean=sp_weighted.mean(('lat', 'lon'))/100
    
    ###plotting
    plt.figure(figsize=(15,5))
    sp_global_mean.plot()
    plt.ylabel('surface pressure [hPa]')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'_sp.png')
    
def total_column_cloud_liquid_water(filename):
    """input: netcdf data, plots global average of total column cloud liquid water"""
    ds=xr.open_dataset(filename)
    
    tclw=ds.tclw
    weights=np.cos(np.deg2rad(ds.lat))
    tclw_weighted=tclw.weighted(weights)
    
    tclw_global_mean=tclw_weighted.mean(('lat', 'lon'))
    
    ###plotting
    plt.figure(figsize=(15,5))
    tclw_global_mean.plot()
    plt.ylabel('Total column cloud liquid water [kg/m²]')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'_tclw.png')
    
def total_column_cloud_ice_water(filename):
    """input: netcdf data, plots global average of total column cloud ice water"""
    ds=xr.open_dataset(filename)
    
    tciw=ds.tciw
    weights=np.cos(np.deg2rad(ds.lat))
    tciw_weighted=tciw.weighted(weights)
    
    tciw_global_mean=tciw_weighted.mean(('lat', 'lon'))
    
    ###plotting
    plt.figure(figsize=(15,5))
    tciw_global_mean.plot()
    plt.ylabel('Total column cloud ice water [kg/m²]')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'_tciw.png')
    
def total_column_water_vapour(filename):
    """input: netcdf data, plots global average of total column water vapour"""
    ds=xr.open_dataset(filename)
    
    tcwv=ds.tcwv
    weights=np.cos(np.deg2rad(ds.lat))
    tcwv_weighted=tcwv.weighted(weights)
    tcwv_global_mean=tcwv_weighted.mean(('lat', 'lon'))
    
    ###plotting
    plt.figure(figsize=(15,5))
    tcwv_global_mean.plot()
    plt.ylabel('Total column water vapour [kg/m²]')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'_tcwv.png')
    
def large_scale_precipitation(filename):
    """input: netcdf data, plots global average of large scale precipitation in mm/day"""
    ds=xr.open_dataset(filename)
    
    lsp=ds.lsp
    weights=np.cos(np.deg2rad(ds.lat))
    lsp_weighted=lsp.weighted(weights)
    lsp_global_mean=lsp_weighted.mean(('lat', 'lon'))*8*1000
    
    ###plotting
    plt.figure(figsize=(15,5))
    lsp_global_mean.plot()
    plt.ylabel('large scale precipitation [mm/day]')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'_lsp.png')
    
def convective_precipitation(filename):
    """input: netcdf data, plots global average of convective precipitation in mm/day"""
    ds=xr.open_dataset(filename)
    
    cp=ds.cp
    weights=np.cos(np.deg2rad(ds.lat))
    cp_weighted=cp.weighted(weights)
    cp_global_mean=cp_weighted.mean(('lat', 'lon'))*8*1000
    
    ###plotting
    plt.figure(figsize=(15,5))
    cp_global_mean.plot()
    plt.ylabel('convective precipitation [mm/day]')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'_cp.png')
    
def snowfall(filename):
    """input: netcdf data, plots global average of snowfall [mm/day] for water equivalent"""
    ds=xr.open_dataset(filename)
    
    sf=ds.sf
    weights=np.cos(np.deg2rad(ds.lat))
    sf_weighted=sf.weighted(weights)
    sf_global_mean=sf_weighted.mean(('lat', 'lon'))*8*1000
    
    ###plotting
    plt.figure(figsize=(15,5))
    sf_global_mean.plot()
    plt.ylabel('snowfall [mm/day] of water equivalent')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'_sf.png')
    
def surface_sensible_heat_flux(filename):
    """input: netcdf data, plots global average of surface sensible heat flux [W/m²]"""
    ds=xr.open_dataset(filename)
    
    sshf=ds.sshf
    weights=np.cos(np.deg2rad(ds.lat))
    sshf_weighted=sshf.weighted(weights)
    sshf_global_mean=sshf_weighted.mean(('lat', 'lon'))/10800
    
    ###plotting
    plt.figure(figsize=(15,5))
    sshf_global_mean.plot()
    plt.ylabel('surface sensible heat flux [W/m²]')
    plt.xlabel('Time')
    plt.savefig(filename[:-3]+'_sshf.png')
