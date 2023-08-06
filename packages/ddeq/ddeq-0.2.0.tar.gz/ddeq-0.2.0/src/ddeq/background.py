

import numpy as np
import scipy.ndimage
import skimage.morphology
import xarray

import ddeq


def create_gaussian_kernel(sigma):
    """
    Creat a Gaussian kernel with standard deviation `sigma`. The size of the
    kernel is at least 11x11 but at least 5*sigma.
    """

    # size should be odd and at least 11 pixels
    size = max(11, int(5 * sigma))
    if size%2 == 0:
        size += 1

    kernel = np.zeros((size,size))
    kernel[size//2,size//2] = 1.0
    kernel = scipy.ndimage.gaussian_filter(kernel, sigma=sigma)

    return kernel




def estimate(data, variable, sigma=10.0, mask_hits=True, extra_dilation=None):
    """\
    Estimate (smooth) CO2 background using normalized convolution.
    
    extra_dilation: if not None add extra dilation using a disk with given radius.
    """
    c = np.array(data[variable])

    # only use pixels that are in plume area around plume without enhanced values
    if mask_hits:
        valids = np.array(~data.is_hit)
    else:
        valids = np.array(~data.plume_area)

    valids[~np.isfinite(c)] = False

    if extra_dilation is not None:
        disk = skimage.morphology.disk(extra_dilation)
        valids = ~skimage.morphology.dilation(~valids, disk)
    
    
    kernel = create_gaussian_kernel(sigma)

    c[~valids] = np.nan
    bg_est = ddeq.misc.normalized_convolution(c, kernel, mask=~valids)
    bg_est = xarray.DataArray(bg_est, name=f'{variable}_estimated_background',
                              dims=data[variable].dims)
    bg_est.attrs['long name'] = f'estimated {variable} background'
    bg_est.attrs['method'] = 'normalized convolution (sigma = %.1f px)' % sigma

    data[f'{variable}_estimated_background'] = bg_est


    return data
 
