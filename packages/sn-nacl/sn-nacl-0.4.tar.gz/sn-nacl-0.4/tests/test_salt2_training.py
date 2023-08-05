import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)

import numpy as np
import pylab as pl
from nacl.dataset import TrainingDataset
from nacl.models.salt import SALT2Like
from nacl.models.constraints import SALT2LikeConstraints
from nacl.models.regularizations import NaClSplineRegularization
from nacl import minimize
import helpers

tds, model = helpers.generate_dataset(1000, seed=42, string_ids=False)
p_truth = model.pars.copy()

def test_lightcurve_fit(fit=True, linesearch=False, start_from_truth=False):
    """fit the light curves, not the model
    """
    # re-init model parameters
    model.pars.full[:] = p_truth.full[:]

    # fix everything but the SN parameters of interest
    model.pars.fix()
    for block_name in ['X0', 'X1', 'col', 'tmax']:
        model.pars[block_name].release()

    # tds_lc = TrainingDataset(tds.sn_data, tds.lc_data,
    #                          load_filters=True)
    # model_lc = SALT2Like(tds_lc, init_fr)

    valid = tds.spec_data.valid.copy()
    tds.spec_data.valid[:] = 0

    # scramble the initial state
    if not start_from_truth:
        sz = len(model.pars['X0'].free)
        model.pars['X0'].free *= np.random.normal(size=sz, loc=1., scale=0.1)
        model.pars['X1'].free += np.random.normal(size=sz, scale=1.)
        model.pars['col'].free += np.random.normal(size=sz, scale=0.3)
        model.pars['tmax'].free += np.random.normal(size=sz, scale=1.)

    wres = minimize.WeightedResiduals(model)
    chi2 = minimize.LogLikelihood(wres)
    minz = minimize.Minimizer(chi2)
    if fit:
        res = minz.minimize(model.pars.free, linesearch=linesearch)
    else:
        res = None

    return res, minz


def test_model_fit_no_constraints():
    """Simple model fit, some regularization, no constraints,
    just fixing a couple of SNe to break the degeneracies.
    """
    model.pars.release()
    model.pars.full[:] = p_truth.full[:]

    model.pars.fix()
    for block_name in ['X0', 'X1', 'col', 'tmax', 'M0', 'M1', 'CL']:
        model.pars[block_name].release()
    for sn in [0,1,2,3]:
        model.pars['X0'].fix(sn)
        model.pars['X1'].fix(sn)
        model.pars['col'].fix(sn)
        model.pars['tmax'].fix(sn)

    reg = NaClSplineRegularization(model, to_regularize=['M0', 'M1'],
                                   order=1, mu=1.E-0)
    wres = minimize.WeightedResiduals(model)
    chi2 = minimize.LogLikelihood(wres, reg=[reg])
    minz = minimize.Minimizer(chi2)
    res = minz(model.pars.free, linesearch=False)

    # res['cons'] = cons
    res['reg'] = reg
    res['chi2'] = chi2

    return res


def test_training_fit_new_likelihood(start_from_truth=True):
    """
    """
    model.pars.release()
    model.pars.full[:] = p_truth.full[:]

    # we start with a simple light curve fit
    # to do this, we extract just the light curves
    # from the training dataset
    lc_tds = TrainingDataset(sne=tds.sn_data.nt, lc_data=tds.lc_data.nt)
    lc_model = SALT2Like(lc_tds, init_from_salt2_file='salt2.npz')
    lc_model.init_from_training_dataset()

    # scramble the initial parameters
    if not start_from_truth:
        sz = len(lc_model.pars['X0'].free)
        lc_model.pars['X0'].free *= np.random.normal(size=sz, loc=1., scale=0.1)
        lc_model.pars['X1'].free += np.random.normal(size=sz, scale=1.)
        lc_model.pars['col'].free += np.random.normal(size=sz, scale=0.3)
        lc_model.pars['tmax'].free += np.random.normal(size=sz, scale=1.)

    lc_model.pars.fix()
    lc_model.pars['sigma_snake'].full[:] = 0.05
    for block_name in ['X0', 'X1', 'col', 'tmax']:
        lc_model.pars[block_name].release()
    chi2 = minimize.LogLikelihood2(lc_model,
                                   # variance_model=lc_model.error_snake
                                   force_default_spgemm=False)
    minz = minimize.Minimizer(chi2)
    res = minz.minimize(lc_model.pars.free)  # , mode='simplicial', beta=1.E-6)

    # and initialize the full model with the results of the light curve fit
    for block_name in ['X0', 'X1', 'col', 'tmax']:
        model.pars[block_name].full[:] = lc_model.pars[block_name].full[:]
    # then, release the other parameters and start the real fit
    model.pars.fix()
    model.pars['sigma_snake'].full[:] = 0.05
    for block_name in ['X0', 'X1', 'col', 'tmax',
                       'M0', 'M1', 'CL']: # 'SpectrumRecalibration']:
        model.pars[block_name].release()

    # at first order, make sure that the constraints are respected
    model.pars['X1'].full -= model.pars['X1'].full.mean()
    model.pars['X1'].full /= model.pars['X1'].full.std()
    model.pars['col'].full -= model.pars['col'].full.mean()
    cons = SALT2LikeConstraints(model,
                                active={'M0': 10**(-0.4 * (30-19.5)),
                                        'dM0': 0.,
                                        'M1': 0.,
                                        'dM1': 0.,
                                        'col': 0.,
                                        'X1': 0.,
                                        'X1_var': 1.}, mu=1.E6)
    reg = NaClSplineRegularization(model, to_regularize=['M0', 'M1'],
                                   order=0, mu=1.)
    chi2 = minimize.LogLikelihood2(model, reg=[reg], cons=[cons],
                                   force_default_spgemm=False
                                   # variance_model=model.error_snake
                                   )
    minz = minimize.Minimizer(chi2)
    res = minz.minimize(model.pars.free)

    res['cons'] = cons
    res['reg'] = reg
    res['chi2'] = chi2

    return res




def test_training_fit(start_from_truth=True):
    """fit the light curves and a block of the model
    """
    model.pars.release()
    model.pars.full[:] = p_truth.full[:]

    # we start with a simple light curve fit
    # to do this, we extract just the light curves
    # from the training dataset
    lc_tds = TrainingDataset(sne=tds.sn_data.nt, lc_data=tds.lc_data.nt)
    lc_model = SALT2Like(lc_tds, init_from_salt2_file='salt2.npz')
    lc_model.init_from_training_dataset()

    # scramble the initial parameters
    if not start_from_truth:
        sz = len(lc_model.pars['X0'].free)
        lc_model.pars['X0'].free *= np.random.normal(size=sz, loc=1., scale=0.1)
        lc_model.pars['X1'].free += np.random.normal(size=sz, scale=1.)
        lc_model.pars['col'].free += np.random.normal(size=sz, scale=0.3)
        lc_model.pars['tmax'].free += np.random.normal(size=sz, scale=1.)

    lc_model.pars.fix()
    for block_name in ['X0', 'X1', 'col', 'tmax']:
        lc_model.pars[block_name].release()
    wres = minimize.WeightedResiduals(lc_model)
    chi2 = minimize.LogLikelihood(wres)
    minz = minimize.Minimizer(chi2)
    res = minz.minimize(lc_model.pars.free)

    # and initialize the full model with the results of the light curve fit
    for block_name in ['X0', 'X1', 'col', 'tmax']:
        model.pars[block_name].full[:] = lc_model.pars[block_name].full[:]
    # then, release the other parameters and start the real fit
    model.pars.fix()
    for block_name in ['X0', 'X1', 'col', 'tmax',
                       'M0', 'M1', 'CL']: # 'SpectrumRecalibration']:
        model.pars[block_name].release()

    # at first order, make sure that the constraints are respected
    model.pars['X1'].full -= model.pars['X1'].full.mean()
    model.pars['X1'].full /= model.pars['X1'].full.std()
    model.pars['col'].full -= model.pars['col'].full.mean()
    cons = SALT2LikeConstraints(model,
                                active={'M0': 10**(-0.4 * (30-19.5)),
                                        'dM0': 0.,
                                        'M1': 0.,
                                        'dM1': 0.,
                                        'col': 0.,
                                        'X1': 0.,
                                        'X1_var': 1.}, mu=1.E6)
    reg = NaClSplineRegularization(model, to_regularize=['M0', 'M1'],
                                   order=0, mu=1.)
    wres = minimize.WeightedResiduals(model)
    chi2 = minimize.LogLikelihood(wres, reg=[reg], cons=[cons])
    minz = minimize.Minimizer(chi2)
    res = minz.minimize(model.pars.free)

    res['cons'] = cons
    res['reg'] = reg
    res['chi2'] = chi2

    return res


def test_cons_dM0():
    cons = SALT2LikeConstraints(model,
                                active={'dM0': 0.},
                                mu=1.)
    pp = model.pars.copy()

    l = []
    for dx in [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]:
        M0 = pp['M0'].full.copy()
        M0 = np.roll(M0.reshape(-1, 129), dx, axis=0)
        model.pars['M0'].full[:] = M0.ravel()
        l.append((dx, float(cons.Jac @ model.pars.full)))
    l = np.rec.fromrecords(l, names=['dx', 'cons'])
    return l

def test_likelihood_derivatives(start_from_truth=False):
    """
    """
    model.pars.release()
    model.pars.full[:] = p_truth.full[:]

    if not start_from_truth:
        sz = len(model.pars['X0'].free)
        model.pars['X0'].free *= np.random.normal(size=sz, loc=1., scale=0.1)
        model.pars['X1'].free += np.random.normal(size=sz, scale=1.)
        model.pars['col'].free += np.random.normal(size=sz, scale=0.3)
        model.pars['tmax'].free += np.random.normal(size=sz, scale=1.)

    # fix everything but the SN parameters of interest
    # plus one block
    model.pars.fix()
    for block_name in ['X0', 'M0', 'X1', 'col', 'tmax']:
        model.pars[block_name].release()

    model.pars['X1'].full -= model.pars['X1'].full.mean()
    model.pars['X1'].full /= model.pars['X1'].full.std()
    model.pars['col'].full -= model.pars['col'].full.mean()

    cons = SALT2LikeConstraints(model,
                                active={'M0': 10**(-0.4 * (30-19.5)),
                                        'dM0': 0.,
                                        'M1': 0.,
                                        'dM1': 0.,
                                        'col': 0.,
                                        'X1': 0.,
                                        'X1_var': 1.
                                               },
                                mu=1.E6)
    # return cons
    reg = NaClSplineRegularization(model, to_regularize=['M0', 'M1'],
                                   order=0, mu=1.e-6)
    wres = minimize.WeightedResiduals(model)
    chi2 = minimize.LogLikelihood(wres)  # , reg=[reg], cons=[cons])

    Ja, Jn = helpers.check_deriv(chi2, p=model.pars.free)

    return Ja, Jn


