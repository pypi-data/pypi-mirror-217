
import os
import warnings

from scipy.interpolate import RectSphereBivariateSpline,SmoothSphereBivariateSpline
import cdsapi
import numpy as np
import cartopy.crs as ccrs
import pandas as pd
import xarray as xr

from ddeq.smartcarb import DOMAIN
import ddeq


def get_wind_at_location(winds, lon0, lat0):
    """\
    Obtain wind at location given by lon0 and lat0 in wind field (xr.Dataset)
    using nearest neighbor interpolation.
    """
    lat = winds['lat'].data
    lon = winds['lon'].data

    if np.ndim(lat) == 2:
        dist = (lat - lat0)**2 + (lon - lon0)**2
        i, j = np.unravel_index(dist.argmin(), dist.shape)
    else:
        i = np.argmin(np.abs(lat-lat0))
        j = np.argmin(np.abs(lon-lon0))

    return np.array([float(winds['U'][i,j]), float(winds['V'][i,j])])


def read_smartcarb(time, lon, lat, radius=None, data_path='.', method='linear',
                   average=False):
    """\
    Read SMARTCARB winds at given location at given `time`. The location is
    interpolated from SMARTCARB model grid to given `lon` and `lat`. If `lon`
    and `lat` are given as scalar, it is possible to provide a radius around
    location for which are extracted.

    radius :: radius around location given in rotated degrees
    data_path :: path to SMARTCARB wind fields
    method :: interpolation method (used by xr.DataArray.interp method)
    average :: average extracted winds

    Return xr.Dataset with wind components `U` and `V` as well as `wind speed`
    and `direction`.
    """
    lon = np.atleast_1d(lon).flatten()
    lat = np.atleast_1d(lat).flatten()

    if lon.size > 1 and radius is not None:
        raise ValueError(
            'Please provide lon and lat as scalar if radius is given.'
        )

    rlon, rlat, _ = np.transpose(
        DOMAIN.proj.transform_points(ccrs.PlateCarree(), lon, lat)
    )

    filename = time.round('H').strftime('SMARTCARB_winds_%Y%m%d%H.nc')
    filename = os.path.join(data_path, filename)

    with xr.open_dataset(filename) as nc:
        if radius is None:
            u = [float(nc['U_GNFR_A'].interp(rlon=rlon[i], rlat=rlat[i],
                                             method=method))
                 for i in range(rlon.size)]

            v = [float(nc['V_GNFR_A'].interp(rlon=rlon[i], rlat=rlat[i],
                                             method=method))
                 for i in range(rlon.size)]

        else:
            distance = np.sqrt((nc.rlon - rlon)**2 + (nc.rlat - rlat)**2)

            if np.any(distance <= radius):
                region = nc.where(distance <= radius, drop=True)

                lon = region.lon.values.flatten()
                lat = region.lat.values.flatten()
                u = region['U_GNFR_A'].values.flatten()
                v = region['V_GNFR_A'].values.flatten()
            else:
                lon = lon
                lat = lat
                u = np.array([np.nan])
                v = np.array([np.nan])

    wind = xr.Dataset()
    wind['lon'] = xr.DataArray(lon, dims='index')
    wind['lat'] = xr.DataArray(lat, dims='index')
    wind['U'] = xr.DataArray(u, dims='index')
    wind['V'] = xr.DataArray(v, dims='index')

    if average:
        u_std = wind['U'].std()
        v_std = wind['V'].std()
        wind = wind.mean('index')
        wind['U_std'] = u_std
        wind['V_std'] = v_std

    wind['speed'] = np.sqrt(wind.U**2 + wind.V**2)
    wind['speed_precision'] = 1.0 # FIXME
    wind['direction'] = ddeq.wind.calculate_wind_direction(wind.U, wind.V)

    return wind.where(np.isfinite(wind['U']), drop=True)


def read_era5(time, lon, lat, data_path='.', method='linear'):

    lon = np.atleast_1d(lon).flatten()
    lat = np.atleast_1d(lat).flatten()

    u = np.zeros_like(lon)
    v = np.zeros_like(lon)

    for i in range(lon.size):
        p, u_profile, v_profile = get_era5_wind_profile(time, lon[i], lat[i],
                                                        data_path=data_path)

        # TODO: use weights
        u[i] = u_profile.mean('level')
        v[i] = v_profile.mean('level')


    wind = xr.Dataset()
    wind['lon'] = xr.DataArray(lon, dims='index')
    wind['lat'] = xr.DataArray(lat, dims='index')
    wind['U'] = xr.DataArray(u, dims='index')
    wind['V'] = xr.DataArray(v, dims='index')

    wind['speed'] = np.sqrt(wind.U**2 + wind.V**2)
    wind['speed_precision'] = 1.0 # FIXME
    wind['direction'] = ddeq.wind.calculate_wind_direction(wind.U, wind.V)

    return wind.where(np.isfinite(wind['U']), drop=True)





def read_coco2_era5(time, lon, lat, suffix=None, method='linear'):
    """
    Read ERA-5 data from CoCO2 project on ICOS-CP.
    """
    warnings.warn('CoCO2-specific function will be removed in future.',
                  DeprecationWarning, stacklevel=2)

    if suffix is None:
        filename = time.strftime(
            '/project/coco2/jupyter/WP4/ERA5/ERA5-gnfra-%Y%m%dt%H00.nc'
        )
    else:
        filename = time.strftime(
            f'/project/coco2/jupyter/WP4/ERA5/ERA5-gnfra-%Y%m%dt%H00_{suffix}.nc'
        )

    lon = np.atleast_1d(lon)
    lat = np.atleast_1d(lat)

    with xr.open_dataset(filename) as nc:

        u = [float(nc['U_GNFR_A'].interp(longitude=lon[i], latitude=lat[i],
                                         method=method))
             for i in range(lon.size)]

        v = [float(nc['V_GNFR_A'].interp(longitude=lon[i], latitude=lat[i],
                                         method=method))
                 for i in range(lon.size)]

    wind = xr.Dataset()
    wind['lon'] = xr.DataArray(lon, dims='index')
    wind['lat'] = xr.DataArray(lat, dims='index')
    wind['U'] = xr.DataArray(u, dims='index')
    wind['V'] = xr.DataArray(v, dims='index')

    wind['speed'] = np.sqrt(wind.U**2 + wind.V**2)
    wind['speed_precision'] = 1.0 # FIXME
    wind['direction'] = ddeq.wind.calculate_wind_direction(wind.U, wind.V)

    return wind


def calculate_wind_direction(u, v):
    return (270.0 - np.rad2deg(np.arctan2(v,u))) % 360


def download_era5_winds(time, data_path='.', overwrite=False, full_day=False):

    if full_day:
        era5_filename = os.path.join(data_path,
                                     time.strftime('ERA5-wind-%Y%m%d.nc'))
    else:
        era5_filename = os.path.join(data_path,
                                     time.strftime('ERA5-wind-%Y%m%d_%H%M.nc'))

    if os.path.exists(era5_filename) and not overwrite:
        return

    cds = cdsapi.Client()

    query = {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            'geopotential', 'temperature', 'u_component_of_wind',
            'v_component_of_wind',
        ],
        'pressure_level': [
            '700', '750', '775',
            '800', '825', '850',
            '875', '900', '925',
            '950', '975', '1000',
        ],
        "area": [90, -180, -90, 180], # north, east, south, west
    }

    if full_day:
        query['year'] = f'{time.year}'
        query['month'] = f'{time.month:02d}'
        query['day'] = f'{time.day:02d}'
        query['time'] = [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
        ]
    else:
        query["date"] = time.strftime('%Y-%m-%d')
        query["time"] = time.strftime('%H:00')

    r = cds.retrieve('reanalysis-era5-pressure-levels', query, era5_filename)


def get_era5_wind_profile(time, lon, lat, data_path='.'):

    era5_filename = os.path.join(data_path,
                                 time.strftime('ERA5-wind-%Y%m%d_%H%M.nc'))
    download_era5_winds(time, data_path, overwrite=False)

    with xr.open_dataset(era5_filename) as era5:
        era5 = era5.load().sel(time=time, longitude=lon, latitude=lat,
                               method='nearest')

    pressure = era5['level']
    u_profile = era5['u']
    v_profile = era5['v']

    return pressure, u_profile, v_profile



def calculate_pressure_levels(surface_pressure, nlevels=37, which='middle'):

    filename= os.path.join(os.path.dirname(__file__), 'data',
                           'ERA5 L137 model level definitions.csv')

    level_definitions = pd.read_csv(filename, index_col=0)

    a = np.array(level_definitions['a [Pa]'])
    b = np.array(level_definitions['b'])

    # pressure at boundary of model layers
    ph = a + b * float(surface_pressure)

    # TODO: how to interpolate?
    #ph = np.interp(np.linspace(0,138,nlevels+1), np.arange(138), ph)

    # pressure at middle of model layers
    pf = 0.5 * (ph[1:] + ph[:-1])

    if which == 'middle':
        return pf
    elif which == 'boundary':
        return ph
    else:
        raise ValueError


def calculate_level_heights(temperature, pressure, which='middle'):
    """
    temperature at middle of layers
    pressure at boundary of layers
    """
    g = 9.80665
    R = 287.06

    p1 = pressure[1:]
    p2 = pressure[:-1]

    dh = R * temperature / g * np.log(p1 / p2)

    hh = np.concatenate([[0.0], dh[::-1].cumsum()])
    hh = hh[::-1]

    hf = 0.5 * (hh[1:] + hh[:-1])

    if which == 'middle':
        return hf
    elif which == 'boundary':
        return hh
    else:
        raise ValueError


def read_gnfra_wind(folder, date, UTC='11:00:00', latlims=None, lonlims=None, dataset='ERA5'):
    '''
    Parameters
    ----------
    folder : str
        Path to folder where wind data is located.
    date : str or datetime
        Date of the data.
    UTC : str, optional
        UTC time stamp as 'hh:mm:ss'. The default is '11:00:00'.
    latlims : tuple of float, optional
        Latitude limits to focus the data into a region. The default is None.
    lonlims : tuple of float, optional
        Latitude limits to focus the data into a region. The default is None.
    dataset : str, optional
        Dataset of wind data, choices are 'ERA5' or 'SMARTCARB'. The default is 'ERA5'.

    Returns
    -------
    ds : xarray dataset
        Wind data.
    '''
    if (latlims is None and lonlims is not None) or (latlims is not None and lonlims is None):
        raise ValueError('Provide either both or neither of longitude and latitude limits')

    # lims = True if both latlims and lonlims are provided
    lims = latlims is not None and lonlims is not None
    date_str = date.replace('-','') if isinstance(date, str) else date.strftime('%Y%m%d')
    utc_str = UTC.replace(':','')

    if dataset == 'ERA5':
        ds = xr.open_dataset(f'{folder}/ERA5-gnfra-{date_str}t{utc_str[:4]}.nc')
        if lims:
            wlon, wlat = ds['longitude'][:].data, ds['latitude'][:].data
            lat_slice = (min(latlims)-0.5 <= wlat) & (wlat <= max(latlims)+0.5)
            lon_slice = (min(lonlims)-0.5 <= wlon) & (wlon <= max(lonlims)+0.5)
            ds = ds.where(xr.DataArray(lat_slice[:,None] & lon_slice[None,:], dims=['latitude','longitude']), drop=True)

    elif dataset == 'SMARTCARB':
        # Read data
        ds = xr.open_dataset(f'{folder}/SMARTCARB_winds_{date_str}{utc_str[:2]}.nc',
                             drop_variables=['height_10m','U','V','U_10M','V_10M','HHL'])

        # Reindex latitude into decreasing order, the highest latitude at index 0 and the lowest at -1
        ds = ds.reindex(rlat=ds['rlat'][::-1].data)

        # If limits are given, slice data to the area of interest 
        if lims:
            wlon, wlat = ds['lon'][:,:].data.flatten(), ds['lat'][:,:].data.flatten()
            shape = (ds['rlat'].size, ds['rlon'].size)

            top_right = np.unravel_index(np.argmin((wlon-max(lonlims))**2+(wlat-max(latlims))**2),shape)
            bottom_right = np.unravel_index(np.argmin((wlon-max(lonlims))**2+(wlat-min(latlims))**2),shape)
            bottom_left = np.unravel_index(np.argmin((wlon-min(lonlims))**2+(wlat-min(latlims))**2),shape)
            top_left = np.unravel_index(np.argmin((wlon-min(lonlims))**2+(wlat-max(latlims))**2),shape)

            row_index = np.arange(0,shape[0],1,dtype=int)
            col_index = np.arange(0,shape[1],1,dtype=int)

            lat_slice = (min(top_left[0],top_right[0])-1 <= row_index) & (row_index <= max(bottom_left[0],bottom_right[0])+1)
            lon_slice = (min(top_left[1],bottom_left[1])-1 <= col_index) & (col_index <= max(top_right[1],bottom_right[1])+1)
            ds = ds.where(xr.DataArray(lat_slice[:,None] & lon_slice[None,:], dims=['rlat','rlon']), drop=True)

    return ds


def spatial_interpolation(data,wlon,wlat,lon,lat):
    '''
    Interpolates wind in spatial dimensions to given pixels lon-lat pixels.

    Parameters
    ----------
    data : 1d-array or 2d-array
        Wind data.
    wlon : 1d-array or 2d-array
        Wind longitude coordinates.
    wlat : 1d-array or 2d-array
        Wind latitude coordinates.
    lon : 1d-array
        Longitude coordinates to be interpolated.
    lat : 1d-array
        Latitude coordinates to be interpolated.

    Returns
    -------
    interp : 1d-array
        Interpolated data values.
    '''
    if wlon.ndim == 1 and wlat.ndim == 1:
        if data.ndim == 1:
            data = data.reshape((len(wlat),len(wlon)))
        # Interpolator in regular rectangular lat-lon grid
        interpolator = RectSphereBivariateSpline(np.deg2rad(90-wlat),np.deg2rad(wlon),data)
    elif wlon.ndim == 2 and wlat.ndim == 2:
        wlon, wlat = wlon.flatten(), wlat.flatten()
        if data.ndim == 2:
            data = data.flatten()
        # Same weights for each data value, the square sum of weights is exactly one
        weights = np.ones(len(data))/np.sqrt(len(data))
        # Interpolator on the irregular spherical lat-lon grid, requires smoothing factor s, for the chosen 
        # weights the function to to optimized is the root-mean-square distance between the data and the spline
        interpolator = SmoothSphereBivariateSpline(np.deg2rad(90-wlat.flatten()),np.deg2rad(wlon.flatten()),data,w=weights,s=1e-2*len(data))
    else:
        pass
    # Evaluate interpolator at requested coordinates
    interp = interpolator.ev(np.deg2rad(90-lat),np.deg2rad(lon))
    return interp


def read(time, sources, product='ERA5', data_path='.', radius=0.05):
    """\
    Read wind dataset for sources.

    Product: ERA5, SMARTCARB, ...
    """
    if isinstance(time, xr.DataArray):
        time = pd.Timestamp(time.to_pandas())

    winds = {}
    for name, source in sources.groupby('source', squeeze=False):
        if product in ['SC', 'SMARTCARB']:
            winds[name] = read_smartcarb(
                time, source.lon_o.values, source.lat_o.values,
                data_path=data_path,
                radius=radius, method='linear', average=True
            )
        elif product in ['ERA-5', 'ERA5']:
            wind = read_era5(
                time, source.lon_o.values, source.lat_o.values,
                data_path=data_path, method='linear'
            )
            winds[name] = wind.rename_dims({'index': 'source'})
        else:
            raise ValueError

    winds = xr.concat(winds.values(), dim='source')
    winds['source'] = xr.DataArray(sources.source, dims='source')

    return winds


def read_field(filename, wind_alti_file=None, product='ERA5',
               altitude='GNFR-A', average_below=False):
    """\
    Return wind field from file for different products. 3D wind fields are
    taken at nearest altitude or averaged_below. If altitude is "GNFR_A", use
    vertically weighted wind field.
    """
    with xr.open_dataset(filename) as rfile:

        if product == 'SMARTCARB':

            lat = rfile.variables['lat'][:]
            lon = rfile.variables['lon'][:]

            if altitude == 'GNFR-A':
                u = np.squeeze(rfile['U_GNFR_A'][:])
                v = np.squeeze(rfile['V_GNFR_A'][:])
            else:
                u = np.squeeze(rfile['U'][:])
                v = np.squeeze(rfile['V'][:])
                h = np.squeeze(rfile['HHL'].values[:])  # altitude in m
                h = h[:] - h[-1]                        # above surface
                h = 0.5 * (h[1:] + h[:-1])               # at layer center

        elif product == 'ERA5':

            lat = rfile.variables['latitude'][:]
            lon = rfile.variables['longitude'][:]

            if altitude == 'GNFR-A':
                u = np.squeeze(rfile.variables['U_GNFR_A'][:])
                v = np.squeeze(rfile.variables['V_GNFR_A'][:])
            else:
                u = np.squeeze(rfile.variables['u'][:])
                v = np.squeeze(rfile.variables['v'][:])

                raise NotImplementedError
        else:
            raise ValueError(f'Unknown wind product "{product}".')

    # average wind below altitude
    if not isinstance(altitude, str):
        if average_below:
            u = np.nanmean(np.where(h < altitude, u, np.nan), axis=0)
            v = np.nanmean(np.where(h < altitude, v, np.nan), axis=0)
        else:
            # extract value at level
            k = np.argmin(np.abs(h - altitude), axis=0)

            unew = np.zeros(u.shape[1:])
            vnew = np.zeros(v.shape[1:])

            # quickest when itereating over small number of indices
            for index in set(k.flatten()):
                mask = (k == index)
                unew[mask] = u.values[index, mask]
                vnew[mask] = v.values[index, mask]

            u = xr.DataArray(unew, dims=u.dims[1:], attrs=u.attrs)
            v = xr.DataArray(vnew, dims=v.dims[1:], attrs=v.attrs)

    # Create wind dataset
    attrs = {}
    attrs['wind_product'] = product
    attrs['altitude'] = str(altitude)

    wind_field = xr.Dataset(attrs=attrs)

    wind_field['U'] = xr.DataArray(data=u)
    wind_field['V'] = xr.DataArray(data=v)
    wind_field['lat'] = xr.DataArray(data=lat)
    wind_field['lon'] = xr.DataArray(data=lon)

    return wind_field

