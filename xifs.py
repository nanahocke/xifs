import numpy as np
import xarray as xr
import warnings
import numpy as np
import math
warnings.filterwarnings("ignore")

def CRF_glomean(filename):
    """calculates CRF on lat/lon grid, plots global mean in a time series"""

    ds=xr.open_mfdataset(filename, combine='by_coords')
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
    ds=xr.open_mfdataset(filename, combine='by_coords')
    
    variable=ds[var]
    weights=np.cos(np.deg2rad(ds.lat))
    var_weighted=variable.weighted(weights)
    
    var_global_mean=var_weighted.mean(('lat', 'lon'))
    var_global_mean.attrs=variable.attrs
    var_global_mean.name='glomean_'+var
    
    return var_global_mean
    
def output_variable_seasonal_map(filename, var):
    """input: netcdf data, variable, season; plots seasonal average of variable as Mollweide projection"""
    ds=xr.open_mfdataset(filename, combine='by_coords')
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
    ds=xr.open_mfdataset(filename, combine='by_coords')
    u=ds['u']
    lat=u.lat
    u_mean=u.sel(lat=60, pressure_levels=1000,method='nearest').mean('lon')
    u_mean.resample(time_counter="D").mean()
    u_mean.attrs=u.attrs
    u_mean.name='u_polar_vortex'
    return u_mean

def QBO(filename):
    ds=xr.open_mfdataset(filename, combine='by_coords')
    u=ds['u']
    lat=u.lat
    lon=u.lon
    u_mean=u.sel(lat=1.29,lon=103.85,method='nearest')
    u_mean.resample(time_counter="M").mean()
    u_mean.attrs=u.attrs
    u_mean.name='u_Singapore'
    return u_mean

def Jet_position_and_strength(sfc_file):
    ds=xr.open_mfdataset(sfc_file, combine='by_coords')
    u_wind=ds['u']
    v=ds['v']
    u=np.sqrt(u_wind**2+v**2)
    u.attrs['units']=u_wind.attrs['units']
    lat=ds['lat']
    u_300=u.sel(pressure_levels=30000, method='nearest')
    #selecting ranges for NH and SH
    nh=u_300.where(lat>40, drop=True)
    nh=nh.where(lat<90, drop=True)
    sh=u_300.where(lat>-40, drop=True)
    sh=sh.where(lat>-90, drop=True)

    #calculating max over lat. return position
    jet_nh=nh.idxmax(dim='lat')
    jet_nh_val=nh.max(dim='lat')
    jet_sh=sh.idxmax(dim='lat')
    jet_sh_val=sh.max(dim='lat')
    return jet_nh, jet_nh_val, jet_sh, jet_sh_val


def SSW_analysis(sfc_file):
    """saves SSW central dates in a text file"""
    pv=polar_vortex(sfc_file)
    seas = pv.sel(time_counter=pv.time_counter.dt.month.isin([1, 2, 3, 11, 12]))
    SSW=seas.where(seas<=0)
    SSW_np=np.array(SSW)#
    date=np.array(SSW.time_counter)
    SSW_date=[]
    for i in range(len(SSW_np)):
        if math.isnan(SSW_np[i])==False:
            if math.isnan(SSW_np[i-1]):
                SSW_date.append(str(date[i]))
    with open('SSW.txt', 'w') as f:
        for item in SSW_date:
            f.write("%s\n" % item)
            
            
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
        elif item=='SSW':
            SSW_analysis(sfc_file)
        elif item =='jet':
            result[item+'_nh_pos'],result[item+'_nh_value'],result[item+'_sh_pos'],result[item+'_sh_value']=Jet_position_and_strength(sfc_file)
    return result

def to_netcdf(d, path_name):
    """d is a dictionary, path_name is a string, writes d on disk as netCDF"""
    data=d.values()
    ds=xr.merge(data, compat='override')
    ds.to_netcdf(path=path_name)
