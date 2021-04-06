import numpy as np
import xarray as xr
import warnings
warnings.filterwarnings("ignore")

def CRF(filename):
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
    
    return CRF_global_mean

def output_variable(filename, var):
    """input: netcdf data, variable; plots global mean in a time series"""
    ds=xr.open_dataset(filename)
    
    variable=ds[var]
    weights=np.cos(np.deg2rad(ds.lat))
    var_weighted=variable.weighted(weights)
    
    var_global_mean=var_weighted.mean(('lat', 'lon'))
    var_global_mean.attrs=variable.attrs
    
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
    return var_season
    
def analysis(analysis_list, sfc_file):

    result = {} # empty dictionary
    for item in analysis_list:
        if item == 'glomean_crf':
            result['glomean_crf'] = CRF(sfc_file)
        elif item[:8]=='seasmean':
            result[item] = output_variable_seasonal_map(sfc_file, item[9:])
        else:
            result[item]=output_variable(sfc_file, item)
    
    return result
