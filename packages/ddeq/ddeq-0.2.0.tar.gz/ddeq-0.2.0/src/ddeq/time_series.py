


"""
Estimate time profiles of emissions using satellite observations.


annual time profile
- low-order polynomial
- periodic boundary conditions
- a priori state vector and covariance matrix
- ...

weekly cycle:
- weekday and weekend value
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import scipy.optimize
import xarray

import ddeq

#import smartcarb.io
#import smartcarb.misc


def read_emissions(origin='Berlin'):
    co2 = smartcarb.io.read_emissions(origin, 'raw', use_constant=False,
                                      tracer='CO2')

    no2 = smartcarb.io.read_emissions(origin, 'raw', use_constant=False,
                                      tracer='NO2')
    return co2, no2


def plot_diurnal_cycle(origin, norm=False, ax=None, add_legend=True, only_co2=False):
    """
    Plot diurnal cycle of CO2 and NO2 emissions as well as CO2:NOX emission
    ratios.
    """
    if ax is None:
        fig, ax = plt.subplots(1,1)

    co2, no2 = read_emissions(origin)

    hod = np.arange(0,24)
    co2 = np.array([np.mean(co2[co2.index.hour == h]) for h in hod])
    no2 = np.array([np.mean(no2[no2.index.hour == h]) for h in hod])

    if norm:
        co2 /= co2.mean()
        no2 /= no2.mean()
        factor = 1.0
    else:
        factor = 1e3
    
    lines = []
    lines += ax.plot(hod, co2, 'o-',
                      label='CO$_2$ emissions (Mt CO$_2$ yr$^{-1}$)')
    
    if not only_co2:
        lines += ax.plot(hod, factor*no2, 's-',
                          label='NO$_\mathrm{x}$ emissions (kt NO$_2$ yr$^{-1}$)')

    ax.grid(True)
    ax.set_xlabel('Hour of day (UTC)')
    ax.set_ylabel('Emissions')

    ax.set_xticks(np.arange(0,25,3))
    
    if norm:
        ax.set_ylim(0.5,1.5)
    else:
        ax.set_ylim(0,40)

    if not norm:
        ax2 = ax.twinx()
        lines += ax2.plot(hod, co2/no2, 'rv-', label='CO$_2$:NO$_\mathrm{x}$ emission ratios')
        ax2.set_ylabel('CO$_2$:NO$_\mathrm{x}$ emission ratios', color='red')

        ax2.set_ylim(600,1400)
        ax2.set_yticks(np.arange(600,1401,100))
        ax2.set_yticklabels(np.arange(600,1401,100), color='red')

    if add_legend:
        plt.tight_layout()
        plt.legend(lines, [l.get_label() for l in lines])
       
    return hod, co2, no2



def plot_seasonal_cycle(origin, norm=False, ax=None, add_legend=True, only_co2=False, short_month=False):
    
    if ax is None:
        fig, ax = plt.subplots(1,1)

    co2, no2 = read_emissions(origin)

    moy = np.arange(1,13)
    co2 = np.array([np.mean(co2[co2.index.month == m]) for m in moy])
    no2 = np.array([np.mean(no2[no2.index.month == m]) for m in moy])

    if norm:
        co2 /= co2.mean()
        no2 /= no2.mean()
        factor = 1.0
    else:
        factor = 1e3
    
    lines = []
    lines += ax.plot(moy, co2, 'o-',
                      label='CO$_2$ emissions (Mt CO$_2$ yr$^{-1}$)')
    
    if not only_co2:
        lines += ax.plot(moy, factor*no2, 's-',
                          label='NO$_\mathrm{x}$ emissions (kt NO$_2$ yr$^{-1}$)')

    ax.grid(True)
    ax.set_xlabel('Month of year')
    ax.set_ylabel('Emissions')

    ax.set_xticks(np.arange(1,13))
    if short_month:
        ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J',
                            'J', 'A', 'S', 'O', 'N', 'D'])
    else:
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.set_xlim(0.5, 12.5)
    
    if norm:
        ax.set_ylim(0.5, 1.5)
    else:
        ax.set_ylim(0,40)

    if not norm: 
        ax2 = ax.twinx()
        lines += ax2.plot(moy, co2/no2, 'rv-', label='CO$_2$:NO$_\mathrm{x}$ emission ratios')
        ax2.set_ylabel('CO$_2$:NO$_\mathrm{x}$ emission ratios', color='red')

        ax2.set_ylim(600,1400)
        ax2.set_yticks(np.arange(600,1401,100), color='red')

    if add_legend:
        plt.tight_layout()
        plt.legend(lines, [l.get_label() for l in lines])


def plot_weekly_cycle(origin, norm=False, ax=None, add_legend=True, only_co2=False):
    
    if ax is None:
        fig, ax = plt.subplots(1,1)

    co2, no2 = read_emissions(origin)
    
    dow = np.arange(0,7)
    co2 = np.array([np.mean(co2[co2.index.weekday == d]) for d in dow])
    no2 = np.array([np.mean(no2[no2.index.weekday == d]) for d in dow])

    if norm:
        co2 /= co2.mean()
        no2 /= no2.mean()
        
    lines = []
    lines += ax.plot(dow, co2, 'o-',
                     label='CO$_2$ emissions (Mt CO$_2$ yr$^{-1}$)')
    
    if not only_co2:
        lines += ax.plot(dow, 1e3*no2, 's-',
                         label='NO$_\mathrm{x}$ emissions (kt NO$_2$ yr$^{-1}$)')

    ax.grid(True)
    ax.set_xlabel('Day of week')
    ax.set_ylabel('Emissions')

    ax.set_xticks(np.arange(7))
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    ax.set_xlim(-0.5, 6.5)
    
    if norm:
        ax.set_ylim(0.5,1.5)
    else:
        ax.set_ylim(0,40)

    if not norm:
        ax2 = ax.twinx()
        lines += ax2.plot(dow, co2/no2, 'rv-', label='CO$_2$:NO$_\mathrm{x}$ emission ratios')
        ax2.set_ylabel('CO$_2$:NO$_\mathrm{x}$ emission ratios', color='red')

        ax2.set_ylim(600,1400)
        ax2.set_yticks(np.arange(600,1401,100), color='red')

    if add_legend:
        plt.tight_layout()
        plt.legend(lines, [l.get_label() for l in lines])




def hermite_spline(x, p, t):
    """
    Hermite spline with periodic boundary conditions.
    """
    delta = np.diff(p)
    m = np.zeros_like(p)
    
    m[0] = 0.5 * (p[0] - p[-2])
    m[-1] = m[0]

    for k in range(1,m.size-1):
        m[k] = 0.5 * (p[(k+1) % p.size] - p[(k-1) % p.size])

    # compute spline
    y = np.zeros(x.shape, dtype='f8')
    k = 0
    for i in range(x.size):
        if x[i] > t[k+1] and k < t.size-2:
            k += 1

        s = (x[i] - t[k]) / (t[k+1] - t[k])

        y[i] += p[k] * (1 + 2*s) * (1 - s)**2
        y[i] += m[k] * s * (1 - s)**2
        y[i] += p[k+1] * s**2 * (3 - 2*s)
        y[i] += m[k+1] * s**2 * (s - 1)

    return y



class SeasonalCycle:
    def __init__(self, x, y, knots, ystd=1.0, gamma=None):
        self.x = x
        self.y = y

        self.gamma = gamma

        if np.all(ystd == 0.0):
            print('All ystd are 0.0: Set weights to 1.0!')
            self.ystd = np.ones_like(ystd)
        else:
            self.ystd = ystd

        self.knots = knots
        self.w0 = np.full(knots.size-1, y.mean())


    def __call__(self, w, x=None):
        w = np.append(w, w[0])
        s = hermite_spline(self.x if x is None else x,
                           w, self.knots)

        return s

    def integrate(self, w, w_std=None):
        """
        Integrate seasonal cycle to obtain annual emissions.

        w:      emissions at knots
        w_std:  uncertainty at knots
        """
        total = 0.0
        unc = 0.0

        for k in range(w.size-1):

            if w_std is not None:
                unc += w_std[(k-1)%w.size]**2 * ( 1/24)**2
                unc += w_std[k]**2            * (13/24)**2
                unc += w_std[(k+1)%w.size]**2 * (13/24)**2
                unc += w_std[(k+2)%w.size]**2 * ( 1/24)**2

            p0 = w[k]
            p1 = w[(k+1)%w.size]
            m0 = 0.5 * (w[(k+1)%w.size] - w[(k-1)%w.size])
            m1 = 0.5 * (w[(k+2)%w.size] - w[k])
            
            total += 1/2 * p0 + 1/12 * m0 + 1/2 * p1 - 1/12 * m1

        if w_std is not None:
            unc = np.sqrt(unc) / (w.size - 1)

            return total / (w.size-1), unc

        return total / (w.size-1)



    def residual(self, w):

        res = (self(w) - self.y) / self.ystd

        if self.gamma is not None:
            d = self.gamma * np.append(np.diff(w), w[-1] - w[0])
            res = np.concatenate([res, d])

        return res



def fit(times, ts, ts_std, n_knots=4, gamma=None, use_std=True):

    # seconds per year
    knots = np.linspace(0, 31536000, n_knots+1)

    # x- and y-data for fit
    start = np.datetime64('2015-01-01', 's')
    xdata =  (times - start) / np.timedelta64(1, 's')
    ydata = ts.values
    ystd  = ts_std.values

    # remove invalid data
    valids = np.isfinite(ydata) & np.isfinite(ystd)

    xdata = xdata[valids]
    ydata = ydata[valids]
    ystd = ystd[valids]

    # model
    if use_std:
        cycle = SeasonalCycle(xdata, ydata, knots, ystd=ystd, gamma=gamma)
    else:
        cycle = SeasonalCycle(xdata, ydata, knots, ystd=0.0, gamma=gamma)

    # fit
    if ydata.size < n_knots:
        res = None
        x = np.full(n_knots, np.nan)
        x_std = np.full(n_knots, np.nan)
        chi2 = np.nan
    else:
        res = scipy.optimize.least_squares(cycle.residual, cycle.w0, method='lm')
        x = res.x
        K = res.jac

        chi2 = np.sum( cycle.residual(x)**2 ) / (ydata.size - x.size)
        
        # compute uncertainty assuming moderate quality of fit
        #Sx = chi2 * np.linalg.inv(K.T @ K)

        # compute uncertainty
        if use_std:
            Sx = np.linalg.inv(K.T @ K)
        else:
            inv_Se = np.diag(1.0 / ystd**2)
            Sx = np.linalg.inv(K.T @ inv_Se @ K)

        res.x_std = np.sqrt(Sx.diagonal())


    # hourly values
    seconds = np.arange(0, 31536000, 60*60)
    times = start + seconds.astype('timedelta64[s]')

    return res, cycle, times, cycle(x, seconds), chi2



def add_cycle(dataset, n_knots=4, nsat=None, gamma=None,
              varname='est_emissions', cyclename='fitted_cycle',
              use_error=True):

    if nsat is not None:
        lon_eqs_in_constellation = ddeq.smartcarb.lon_eq_by_nsat(nsat)
        valids = np.isin(dataset.lon_eq, lon_eqs_in_constellation)
        valids &= np.isfinite(dataset[varname])
        valids &= np.isfinite(dataset[varname+'_std'])
    else:
        valids = np.isfinite(dataset[varname])
        valids &= np.isfinite(dataset[varname+'_std'])

    if use_error:
        ystd = dataset[varname+'_std'][valids]
    else:
        ystd = xarray.zeros_like(dataset[varname])[valids]
        
    fit_result, func, times, cycle, chi2 = fit(dataset['overpass'][valids],
                                               dataset[varname][valids],
                                               ystd,
                                               n_knots=n_knots, gamma=gamma)

    dataset[cyclename] = xarray.DataArray(cycle, dims='time')
    if fit_result is None:
        dataset[cyclename].attrs['annual_mean'] = np.nan
        dataset[cyclename].attrs['annual_mean_std'] = np.nan
    else:
        em, em_std = func.integrate(fit_result.x, fit_result.x_std)
        dataset[cyclename].attrs['annual_mean'] = em
        dataset[cyclename].attrs['annual_mean_std'] = em_std

    dataset[cyclename].attrs['units'] = '' # TODO
    dataset[cyclename].attrs['chi2'] = chi2

    dataset[cyclename].attrs['number of overpasses'] = int(valids.sum())

    return dataset


