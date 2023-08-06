
import numpy as np
import pandas
import xarray
import ucat
import ddeq


def compute_plume_signal(data, trace_gas):
    """
    Compute plume signal for trace gas
    """
    name = f'{trace_gas}_minus_estimated_background'
    signal = data[trace_gas] - data[f'{trace_gas}_estimated_background']

    data[name] = xarray.DataArray(signal, dims=data[trace_gas].dims,
                                  attrs=data[trace_gas].attrs)
    return data


def prepare_data(data, trace_gas='CO2'):
    """
    Prepare mass-balance approach:
    - estimate CO2 and NO2 background
    - convert units to mass column densities (kg/m²)
    """
    data[f'{trace_gas}_isfinite'] = np.isfinite(data[trace_gas])

    # estimate background
    data = ddeq.background.estimate(data, trace_gas)

    # compute CO2/NO2 enhancement
    data = compute_plume_signal(data, trace_gas)

    # convert ppm to kg/m2
    for variable in [trace_gas,
                     f'{trace_gas}_estimated_background', 
                     f'{trace_gas}_minus_estimated_background']:

        values = data[variable]
        attrs = values.attrs

        name = f'{variable}_mass'

        if data[trace_gas].attrs['units'] == 'molecules cm-2':
            input_unit = 'cm-2'
        elif data[trace_gas].attrs['units'] == 'ppm':
            input_unit = 'ppmv'
        else:
            input_unit = str(data[trace_gas].attrs['units'])

        if trace_gas == 'NOx':
            molar_mass = 'NO2'
        else:
            molar_mass = str(trace_gas)

        data[name] = xarray.DataArray(
            ucat.convert_columns(
                values, input_unit, 'kg m-2', p=data['psurf'],
                molar_mass=molar_mass
            ),
            dims=values.dims, attrs=values.attrs
        )

        if 'noise_level' in attrs:
            noise_level = attrs['noise_level']

            # noise scenarios from SMARTCARB project
            if isinstance(noise_level, str):
                if trace_gas == 'CO2':
                    noise_level = {
                        'low': 0.5,
                        'medium': 0.7,
                        'high': 1.0
                    }[noise_level]

                elif trace_gas in ['NO2', 'NOx']:
                    noise_level = {
                        'low': 1.0e15,
                        'high': 2e15,
                        'S5': 1.3e15
                    }[noise_level]
                else:
                    raise ValueError

            attrs['noise_level'] = ucat.convert_columns(
                noise_level, input_unit, 'kg m-2', molar_mass=molar_mass,
                p=np.nanmean(data['psurf'])
            )

        data[name].attrs.update(attrs)
        data[name].attrs['units'] = 'kg m-2'

    return data



def convert_NO2_to_NOx_emissions(results, f=1.32):
    """
    Convert NO2 fluxes/emissions (i.e. units: "kg s-1") to NOx fluxes/emissions
    using the NO2 to NOx conversion factor assuming that a fraction of NOx is in
    is nitrogen monoxide. The default literature value (f = 1.32) should be
    used with caution, because the spatial and temporal variability is expected
    to be high.
    """
    for key in results:
        if key.startswith('NO2') and results[key].attrs.get('units') == 'kg s-1':
            new_key = key.replace('NO2', 'NOx')
            results[new_key] = f * xarray.DataArray(results[key], dims=results[key].dims)
            results[new_key].attrs.update(results[key].attrs)
    return results
