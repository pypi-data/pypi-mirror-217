
import os

import cartopy.crs as ccrs
import numpy as np
import skimage
import ucat
import xarray as xr

CASES = [
    ['DWD', 'Belchatow'],
    ['DWD', 'Jaenschwalde'],
    ['Empa', 'Belchatow'],
    ['Empa', 'Berlin'],
    ['Empa', 'Jaenschwalde'],
    ['Empa', 'Lipetsk'],
    ['Empa', 'Matimba'],
    ['Empa', 'Paris'],
    ['LSCE', 'Paris'],
    ['TNO', 'Belchatow'],
    ['TNO', 'Belchatow', 'wNO'],
    ['TNO', 'Berlin'],
    ['TNO', 'Jaenschwalde'],
    ['TNO', 'Jaenschwalde', 'wNO'],
    ['TNO', 'Randstad_S'],
    ['TNO', 'Randstad_W'],
    ['WUR', 'Belchatow'],
    ['WUR', 'Belchatow', 'wNO'],
    ['WUR', 'Jaenschwalde'],
    ['WUR', 'Jaenschwalde', 'wNO'],
    ['WUR', 'Lipetsk'],
    ['WUR', 'Lipetsk', 'wNO'],
    ['WUR', 'Matimba'],
    ['WUR', 'Matimba', 'wNO']
]

DATA_PATH = '/project/coco2/jupyter/WP4/powerplants/library_of_plumes/'


def read_level2(team, region, suffix='', data_path=DATA_PATH, filename=None,
                co2_noise=0.7, no2_noise=33e-6, mask_out_of_domain=False,
                drop_duplicates=True):
    """\
    Read CO2M-like Level-2 from CoCO2 library of plumes.

    co2_noise: random uncertainty for CO2 field (in ppm)
    no2_noise: random uncertainty for NO2/NOx field (in mol/m²)
               (default: 33 µmol/m² = 2e15 molecules/cm²)
    """
    if filename is None:
        if suffix:
            filename = f'{team}_{region}_{suffix}.nc'
        else:
            filename = f'{team}_{region}.nc'

        filename = os.path.join(data_path, filename)

    # read data
    d = xr.open_dataset(filename)
    d = d.rename_vars({'lon_bnds': 'lonc', 'lat_bnds': 'latc',
                       'surface_pressure': 'psurf'})
    d = d.rename_dims({'x': 'nobs', 'y': 'nrows'})

    if region in ['Berlin', 'Paris']:
        name = 'CITY'
    elif region in ['Randstad_S', 'Randstad_W']:
        name = 'RS'
    else:
        name = 'PP_M'

    shape = d[f'XCO2_{name}'].shape
    d['CO2'] = d[f'XCO2_{name}'] \
               + d.get('XCO2_ANTH', 0.0) \
               + d.get('XCO2_BIO', 0.0) \
               + d.get('XCO2_BG', 0.0) \
               + co2_noise * np.random.randn(*shape)

    d['CO2_signal'] = d[f'XCO2_{name}'].copy()
    d['CO2_std'] = xr.full_like(d['CO2'], co2_noise)
    d['CO2'].attrs['units'] = 'ppm'
    d['CO2'].attrs['noise_level'] = co2_noise

    if f'NO2_{name}' in d and f'NO_{name}' in d:
        d['NOx'] = d[f'NO_{name}'] + d[f'NO2_{name}'] \
                   + d['NO_BG'] + d['NO2_BG'] \
                   + d.get('NO_ANTH', 0.0) + d.get('NO2_ANTH', 0.0) \
                   + d.get('NO_BIO', 0.0) + d.get('NO2_BIO', 0.0) \
                   + no2_noise * np.random.randn(*shape)
        d['NOx_signal'] = d[f'NO_{name}'] + d[f'NO2_{name}']
        d['NOx_std'] = xr.full_like(d['NOx'], no2_noise)

        d['NOx'].attrs['units'] = 'mol m-2'
        d['NOx'].attrs['noise_level'] = no2_noise

    if f'NO2_{name}' in d:
        d['NO2'] = d[f'NO2_{name}'] \
                   + d['NO2_BG'] \
                   + d.get('NO2_ANTH', 0.0) \
                   + d.get('NO2_BIO', 0.0) \
                   + no2_noise * np.random.randn(*shape)
        d['NO2_signal'] = d[f'NO2_{name}'].copy()
        d['NO2_std'] = xr.full_like(d['NO2'], no2_noise)

        d['NO2'].attrs['units'] = 'mol m-2'
        d['NO2'].attrs['noise_level'] = no2_noise

    d['clouds'] = xr.zeros_like(d['CO2'])

    # remove non-continous fields on boundary (only WUR MicroHH)
    if mask_out_of_domain:
        mask = np.any(np.isnan(d['CO2'].values), axis=0)
        mask = skimage.morphology.dilation(mask, skimage.morphology.square(10))

        for name in ["CO2", "NOx", "NO2"]:
            if name in d:
                d[name].values[:,mask] = np.nan
                d[name + "_signal"].values[:,mask] = np.nan
                d[name + "_std"].values[:,mask] = np.nan

    if drop_duplicates:
        d = d.drop_duplicates('time')

    return d


