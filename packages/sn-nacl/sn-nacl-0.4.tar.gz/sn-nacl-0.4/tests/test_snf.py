import numpy as np
import pylab as pl
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)
from nacl import dataset
from nacl.dataset import TrainingDataset
from nacl.models.salt import SALT2Like, SALT2Eval
from nacl.models.constraints import SALT2LikeConstraints
from nacl.models.regularizations import NaClSplineRegularization
from nacl import minimize
from nacl.fit import fit
import helpers

snf_tds = None

def load():
    global snf_tds
    if snf_tds is None:
        snf_tds = dataset.read_hdf('snf_tds_spline.hd5')
    return snf_tds

def filter_tds(tds, min_wavelength=3600.):
    idx = tds.spectrophotometric_data.wavelength <= min_wavelength
    logging.info(f'invalidating {idx.sum()} measurements outside wl range')
    tds.spectrophotometric_data.valid[idx] = 0
    # tds.kill_sne(['PTF12ikt', 'PTF10zdk', 'PTF11bgv'])
    tds.kill_sne(['SN2004gc', 'PTF11kly', 'SN2005cg'])
    tds.kill_photometric_spectra([1121, 3116, 3307, 1803, 690,
                                   788, 1670, 1056, 1057, 732, 1614,
                                   817, 1224, 1225, 1226, 1227, 1228,
                                  1229, 1230, 1231, 1232, 1233, 1234,
                                  1235, 1236, 1237, 1238, 1239, 1240,
                                  1241, 1242, 1243, 1244, 1245, 1246,
                                  1580, 1854])

    flux = tds.spectrophotometric_data.flux
    fluxerr = tds.spectrophotometric_data.fluxerr
    ey = np.sqrt(fluxerr**2 + 0.05**2 * flux**2)
    tds.spectrophotometric_data.nt['fluxerr'] = ey

    tds.compress()

    return tds


def train(tds):
    model = SALT2Like(tds,
                      init_from_salt2_file='salt2.npz',
                      init_from_training_dataset=True)
    # we start with a simple light curve fit
    lcfit = fit(model, block_names=['X0', 'X1', 'col', 'tmax'],
                n_iter=10)

    # then, we fit the model itself
    model = SALT2Like(tds, phase_range=(-20, 50.),
                      wl_range=(3000., 10000.),
                      basis_knots=(600, 50),
                      init_from_salt2_file='salt2.npz')
    for block_name in ['X0', 'X1', 'col', 'tmax']:
        model.pars[block_name].full[:] = lcfit['pars'][block_name].full[:]

    # fit the model
    modfit = fit(model, block_names=['M0', 'M1', 'CL'],
                 init_pars=lcfit['pars'])
    p = modfit['pars']

    # then, we release everything
    allfit = fit(model, block_names=['M0', 'M1', 'CL',
                                     'X0', 'X1', 'col', 'tmax'],
                 init_pars=p,
                 n_iter=10)

    return allfit

def plot_results(res):
    model = res['model']
    tds = model.training_dataset
    v = model(model.pars.free, jac=False)


    # residuals
    pl.figure()
    x = np.arange(len(v))
    idx = tds.spectrophotometric_data.valid > 0
    res = tds.get_all_fluxes() - v
    yerr=tds.get_all_fluxerr()
    print(x, idx, res)
    pl.plot(x, res, ls='', color='r', marker='.')
    pl.errorbar(x[idx], res[idx], yerr=tds.get_all_fluxerr()[idx],
                ls='', color='k', marker='.')

    # SN_chi2
    pl.figure()
    wres = res / yerr
    sn_chi2 = np.bincount(tds.spectrophotometric_data.sn_index[idx],
                          wres[idx]**2)
    sn_nmeas = np.bincount(tds.spectrophotometric_data.sn_index[idx])
    rchi2_sn = sn_chi2 / sn_nmeas
    pl.plot(rchi2_sn, 'ro')
    pl.title('SN $\chi^2$')
    pl.xlabel('sn_index$')
    pl.ylabel('SN $\chi^2$')
    print('SNe with chi2 > 50')
    isn = np.where(rchi2_sn > 50)[0]
    print(isn)
    print(tds.sn_data.sn_set[isn])

    # spectrum chi2
    pl.figure()
    spec_chi2 = np.bincount(tds.spectrophotometric_data.spec_index[idx],
                            wres[idx]**2)
    spec_nmeas = np.bincount(tds.spectrophotometric_data.spec_index[idx])
    rchi2_spec = spec_chi2 / spec_nmeas
    pl.plot(rchi2_spec, 'ro')
    pl.title('spectrum $\chi^2$')
    pl.xlabel('spec_index')
    pl.ylabel('$\chi^2$')
    print('spectra with chi2 > 50')
    ispec = np.where(rchi2_spec > 50)[0]
    print(ispec)
    print(tds.spectrophotometric_data.spec_set[ispec])

def plot_spectrum(tds, v, spec):
    pl.figure()
    idx = tds.spectrophotometric_data.spec == spec
    pl.plot(tds.spectrophotometric_data.wavelength[idx],
            tds.spectrophotometric_data.flux[idx], 'r+')
    pl.errorbar(tds.spectrophotometric_data.wavelength[idx],
                tds.spectrophotometric_data.flux[idx],
                yerr=tds.spectrophotometric_data.fluxerr[idx],
                ls='', marker='.', label='data')
    pl.plot(tds.spectrophotometric_data.wavelength[idx], v[idx],
            color='r', lw=2, ls='-', zorder=10,
            label='trained model')
    pl.title(f'spectrum #{spec}', fontsize=16)
    pl.xlabel('observer frame $\lambda\ [\AA]$', fontsize=16)
    pl.ylabel('flux', fontsize=16)
    pl.legend(loc='best')

def plot_stacked_residuals(tds, model, v=None):
    """
    """
    if v is None:
        v = model(model.pars.free, jac=False)

    wl = tds.spectrophotometric_data.wavelength / (1. + tds.spectrophotometric_data.z)
    ph = (tds.spectrophotometric_data.mjd - model.pars['tmax'].full[tds.spectrophotometric_data.sn_index]) / (1 + tds.spectrophotometric_data.z)

    pl.figure(figsize=(14, 10))
    idx = tds.get_valid() > 0
    res = tds.get_all_fluxes() - v
    wres = res / tds.get_all_fluxerr()
    pl.hexbin(wl[idx], ph[idx], wres[idx], vmin=-2.5, vmax=2.5)
    pl.title('weighted residuals', fontsize=16)
    pl.xlabel('restframe $\lambda [\AA]$', fontsize=16)
    pl.ylabel('restframe phase [days]', fontsize=16)
    pl.colorbar()

def plot_chi2(tds, model, v=None):
    if v is None:
        v = model(model.pars.free, jac=False)
    wl = tds.spectrophotometric_data.wavelength / (1. + tds.spectrophotometric_data.z)
    ph = (tds.spectrophotometric_data.mjd - model.pars['tmax'].full[tds.spectrophotometric_data.sn_index]) / (1 + tds.spectrophotometric_data.z)

    pl.figure(figsize=(14, 10))
    idx = tds.get_valid() > 0
    res = tds.get_all_fluxes() - v
    wres = res / tds.get_all_fluxerr()
    chi2, _, _ = np.histogram2d(wl, ph, bins=(400,50), weights=wres**2)
    cc, _, _ = np.histogram2d(wl, ph, bins=(400,50))
    rchi2 = chi2 / cc
    pl.imshow(rchi2.T[::-1,:], vmin=0, vmax=10,
              aspect='auto',
              interpolation='none',
              extent=[wl.min(), wl.max(), ph.min(), ph.max()])
    pl.title('local $\chi^2$', fontsize=16)
    pl.xlabel('restframe $\lambda [\AA]$', fontsize=16)
    pl.ylabel('restframe phase [days]', fontsize=16)
    pl.colorbar()





def train_orig(tds):
    """Fit a NaCl model on the TrainingDataset
    """
    # we start with a light curve fit
    model = SALT2Like(tds, init_from_salt2_file='salt2.npz')
    model.init_from_training_dataset()

    model.pars.fix()
    model.pars['X0'].release()
    model.pars['X1'].release()
    model.pars['col'].release()
    model.pars['tmax'].release()

    # reg = NaClSplineRegularization(model, to_regularize=['M0'],
    #                                order=0, mu=1.)
    wres = minimize.WeightedResiduals(model)
    chi2 = minimize.LogLikelihood(wres)
    minz = minimize.Minimizer(chi2)
    ret = minz.minimize(model.pars.free, dchi2_stop=0.1)

    # now, we fix everything but M0 (and M1)
    for block_name in ['X0', 'X1', 'col', 'tmax']:
        model.pars[block_name].full[:] = ret['pars'][block_name].full[:]
    model.pars.fix()
    for block_name in ['M0', 'M1', 'CL']:
        model.pars[block_name].release()

    reg = NaClSplineRegularization(model, to_regularize=['M0', 'M1'],
                                    order=0, mu=1.)
    wres = minimize.WeightedResiduals(model)
    chi2 = minimize.LogLikelihood(wres, reg=[reg])
    minz = minimize.Minimizer(chi2)
    ret = minz.minimize(model.pars.free)

    return ret, minz


