import numpy as np
import xarray as xr
import warnings
import numpy as np
import math
from datetime import datetime, timedelta
import pandas as pd
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
    sh=u_300.where(lat<-40, drop=True)

    #calculating max over lat. return position
    jet_nh=nh.idxmax(dim='lat', keep_attrs=True)
    jet_nh.name='jet_nh'
    jet_nh.attrs['units']='°'
    jet_nh_val=nh.max(dim='lat', keep_attrs=True)
    jet_nh_val.attrs=u_wind.attrs
    jet_nh_val.name='jet_nh_val'
    jet_sh=sh.idxmax(dim='lat', keep_attrs=True)
    jet_sh.name='jet_sh'
    jet_sh.attrs['units']='°'
    jet_sh_val=sh.max(dim='lat', keep_attrs=True)
    jet_sh_val.attrs=u_wind.attrs
    jet_sh_val.name='jet_sh_val'
    jet_sh_val.attrs['standard_name']='total wind'
    jet_nh_val.attrs['standard_name']='total wind'
    jet_sh_val.attrs['long_name']='total wind'
    jet_nh_val.attrs['long_name']='total wind'
    return jet_nh, jet_nh_val, jet_sh, jet_sh_val

def mass_weighted_jet(sfc_file):
    ds=xr.open_mfdataset(sfc_file, combine='by_coords')
    u=ds['u']
    v=ds['v']
    uabs=np.sqrt(u**2+v**2)
    pres=ds['pressure_levels']
    lat=ds['lat']
    pres_new=pres.where(pres<40000, drop=True).where(pres>10000, drop=True)
    uabs=uabs.where(pres_new, drop=True).where(pres_new, drop=True)
    m=pres_new/9.81
    mwu=m*uabs
    mwu_sum=mwu.sum(dim='pressure_levels')
    ws=mwu_sum/m.sum()
    ws.attrs=u.attrs
    ws.attrs['standard_name']='mass_weighter_avg_u_abs'
    ws.attrs['long_name']='mass weighted average wind speed'
    
    #mass flux weighted pressure
    mwp=mwu*pres_new
    P=mwp.sum(dim='pressure_levels')/mwu_sum
    P.attrs=pres.attrs
    P.attrs['name']='mass_flux_weighted_p'
    P.attrs['long_name']='mass flux weighted pressure'
    
    #three jets
    lat_nh=lat.where(lat<70, drop=True).where(lat>15, drop=True)
    lat_sht=lat.where(lat>-40, drop=True).where(lat<-15, drop=True)
    lat_shp=lat.where(lat>-70, drop=True).where(lat<-40, drop=True)

    #mass flux weighted latitude
    mwl=mwu_sum.where(lat_nh, drop=True)*lat_nh
    mwl_sum=mwl.sum(dim='lat')
    L_nh=mwl_sum/(mwu_sum.where(lat_nh, drop=True).sum(dim='lat'))
    mwl=mwu_sum.where(lat_sht, drop=True)*lat_sht
    mwl_sum=mwl.sum(dim='lat')
    L_sht=mwl_sum/(mwu_sum.where(lat_sht, drop=True).sum(dim='lat'))
    mwl=mwu_sum.where(lat_shp, drop=True)*lat_shp
    mwl_sum=mwl.sum(dim='lat')
    L_shp=mwl_sum/(mwu_sum.where(lat_shp, drop=True).sum(dim='lat'))
    L_nh.attrs=lat.attrs
    L_sht.attrs=lat.attrs
    L_shp.attrs=lat.attrs
    
    ws.name='mw_avg_u_abs'#
    P.name='mw_pres'
    L_nh.name='mw_jet_nh'
    L_sht.name='mw_jet_sht'
    L_shp.name='mw_jet_shp'
    
    ws_jet_nh=ws.sel(lat=L_nh, method='nearest')
    ws_jet_sht=ws.sel(lat=L_sht, method='nearest')
    ws_jet_shp=ws.sel(lat=L_shp, method='nearest')
    
    ws_jet_nh.name='nh_jet_u'
    ws_jet_sht.name='sht_jet_u'
    ws_jet_shp.name='shp_jet_u'
    
    return ws , P , L_nh, L_sht, L_shp, ws_jet_nh, ws_jet_sht, ws_jet_shp


def SSW_analysis(sfc_file):
    """saves SSW central dates in a text file"""
    ds=xr.open_mfdataset(sfc_file, combine='by_coords')
    pv=polar_vortex(fc_file)
    seas = pv.where(pv.time_counter.dt.month.isin([1, 2, 3, 4, 11, 12])) #NDJFM and April
    SSW=seas.where(seas<0)
    SSW_np=np.array(SSW)#
    date=np.array(SSW.time_counter)

    #turn westerly again
    west=[]
    for i in range(len(SSW_np)):
        if math.isnan(SSW_np[i])==False:
            if math.isnan(SSW_np[i+1]):
                west.append(pd.to_datetime(date[i+1]))

    ###SSW events
    SSW_date=[]
    for i in range(len(SSW_np)):
        if i!=0 and i!=len(SSW_np)-1 and not math.isnan(SSW_np[i]) and math.isnan(SSW_np[i-1]) and not math.isnan(SSW_np[i+1]):
            if SSW_date==[]:
                for j in range(len(west)):
                    if west[j]>pd.to_datetime(date[i]) and west[j]-pd.to_datetime(date[i]) < timedelta(days=30) and pd.to_datetime(date[i]).month!=4:
                        if SSW_date==[]:
                            SSW_date.append(pd.to_datetime(date[i]))
                        elif SSW_date[-1]!=pd.to_datetime(date[i]):
                            SSW_date.append(pd.to_datetime(date[i]))


            elif pd.to_datetime(date[i])-timedelta(days=20)>pd.to_datetime(SSW_date[-1]) and np.isnan(SSW_np[i-11:i]).all(): #no new SSW date during 20 days after SSW date
                for j in range(len(west)):
                    if west[j]>pd.to_datetime(date[i]) and west[j]-pd.to_datetime(date[i]) < timedelta(days=30) and pd.to_datetime(date[i]).month!=4 and SSW_date[-1]!=pd.to_datetime(date[i]):
                        SSW_date.append(pd.to_datetime(date[i]))

    SSW_date=xr.DataArray(SSW_date)
    SSW_date.name='SSW_central_date'
    SSW_date.attrs=ds['time_counter'].attrs
    SSW_date=SSW_date.assign_coords({'dim_0':SSW_date})
    SSW_date=SSW_date.rename({'dim_0':'time_counter'})
    return SSW_date
            
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
            result[item]=SSW_analysis(sfc_file)
        elif item =='jet':
            result[item+'_nh_pos'],result[item+'_nh_value'],result[item+'_sh_pos'],result[item+'_sh_value']=Jet_position_and_strength(sfc_file)
        elif item=='mw_jet':
            result['mwu'], result['mwp'], result['mw_jet_nh'], result['mw_jet_sht'], result['mw_jet_shp'], result['ws_jet_nh'], result['ws_jet_sht'], result['ws_jet_shp']=mass_weighted_jet(sfc_file)
    return result

def to_netcdf(d, path_name):
    """d is a dictionary, path_name is a string, writes d on disk as netCDF"""
    data=d.values()
    ds=xr.merge(data, compat='override')
    ds.to_netcdf(path=path_name)
