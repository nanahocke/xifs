import numpy as np
import xarray as xr
import warnings
import numpy as np
warnings.filterwarnings("ignore")

def CRF_glomean(filename):
    """calculates CRF on lat/lon grid, plots global mean in a time series"""

    ds=xr.open_dataset(filename)
    weights=np.cos(np.deg2rad(ds.lat))

    ###variables
    ttrc=ds.ttrc
    tsrc=ds.tsrc
    ttr=ds.ttr
    tsr=ds.tsr

	###Calculation of CRF
    CRF_LW=ttrc-ttr
    CRF_SW=tsrc-tsr
    CRF=CRF_SW+CRF_LW
    CRF_weighted=CRF.weighted(weights)
    CRF_global_mean=CRF_weighted.mean(('lat', 'lon'))
    CRF_global_mean.attrs={'long_name': 'CRF',
                          'units': 'J/m²'}
    CRF_global_mean.name='glomean_crf'
    return CRF_global_mean

def output_variable_glomean(filename, var):
    """input: netcdf data, variable; plots global mean in a time series"""
    ds=xr.open_dataset(filename)
    
    variable=ds[var]
    weights=np.cos(np.deg2rad(ds.lat))
    var_weighted=variable.weighted(weights)
    
    var_global_mean=var_weighted.mean(('lat', 'lon'))
    var_global_mean.attrs=variable.attrs
    var_global_mean.name='glomean_'+var
    
    return var_global_mean
    
def output_variable_seasonal_map(filename, var):
    """input: netcdf data, variable, season; plots seasonal average of variable as Mollweide projection"""
    ds=xr.open_dataset(filename)
    variable=ds[var]
    month_length=variable.time_counter.dt.days_in_month
    weights = month_length.groupby('time_counter.season') / month_length.groupby('time_counter.season').sum()
    np.testing.assert_allclose(weights.groupby('time_counter.season').sum().values, np.ones(4))
    ds_weighted = (variable * weights).groupby('time_counter.season').sum(dim='time_counter')
    
    var_season=ds_weighted
    var_season.attrs=variable.attrs
    var_season.name='seasmean_'+var
    return var_season

def polar_vortex(filename):
    ds=xr.open_dataset(filename)
    u=ds['u']
    lat=u.lat
    u_mean=u.sel(lat=60, pressure_levels=1000,method='nearest').mean('lon')
    u_mean.resample(time_counter="D").mean()
    u_mean.attrs=u.attrs
    u_mean.name='u_polar_vortex'
    return u_mean

def QBO(filename):
    ds=xr.open_dataset(filename)
    u=ds['u']
    lat=u.lat
    lon=u.lon
    u_mean=u.sel(lat=1.29,lon=103.85,method='nearest')
    u_mean.resample(time_counter="M").mean()
    u_mean.attrs=u.attrs
    u_mean.name='u_Singapore'
    return u_mean
    
def analysis(analysis_list, sfc_file):

    result = {} # empty dictionary
    for item in analysis_list:
        if item == 'glomean_crf':
            result['glomean_crf'] = CRF_glomean(sfc_file)
        elif item[:8]=='seasmean':
            result[item] = output_variable_seasonal_map(sfc_file, item[9:])
        elif item[:7]=='glomean':
            result[item] = output_variable_glomean(sfc_file, item[8:])    
        elif item=='polar_vortex':
            result[item]=polar_vortex(sfc_file)
        elif item=='QBO':
            result[item]=QBO(sfc_file)
    return result

def to_netcdf(d, path_name):
    """d is a dictionary, path_name is a string, writes d on disk as netCDF"""
    data=d.values()
    ds=xr.merge(data, compat='override')
    ds.to_netcdf(path=path_name)
