import numpy as np
import pylab as pl
import scipy 
import os

ALPHA = 0.13
BETA = 3.0
M_B = -19.0906


class DistancesModulus(object):
    r"""
    Calculate distance modulus from parameter of a nacl.model.salt model.
    Given the parameters of the standardization laws (:math:`\alpha`, :math:`\beta` and :math:`M_B`)
    and the SN parameters from the models (:math:`X_0`, :math:`X_1` and :math:`c`), calculated
    the distance modulus :math:`\mu` :

    .. math::
        \mu = -2.5 \log_{10}(X_{0}) + \alpha X_{1} - \beta c - M_B

    Attributes
    ----------
    model : nacl.models.salt
        Model.
    beta0 : None or numpy.array
        Model initial parameters.
    nsn : int
        Number of SNe in data set.
    """
    def __init__(self, model, beta0=None):
        """
        Constructor.

        Parameters
        ----------
        model : nacl.models.salt
            Model.
        beta0 : numpy.array
            Model initial parameters [optional]
        """
        self.model = model
        self.beta0 = beta0
        self.nsn = model.training_dataset.nb_sne()

    def __call__(self, beta, jac=False):
        """
        Evaluate the distance with parameter :math:`\beta`.

        Parameters
        -------
        beta : numpy.array
            Vector containing the free parameters only.
        jac : bool
            Whether it return the jacobian matrix.

        Returns
        -------
        mu : numpy.array
            distance modulus
        """
        idxx0 = self.model.pars['X0'].indexof()
        idxx1 = self.model.pars['X1'].indexof()
        idxc = self.model.pars['c'].indexof()         
        x0, x1, c = beta[idxx0], beta[idxx1], beta[idxc]
        
        mu = - 2.5 * np.log10(x0) + ALPHA * x1 - BETA * c - M_B
        
        if jac:
            dmu_dx0 = -2.5 * 1/(x0 * np.log(10))
            dmu_dx1 = +ALPHA * np.ones_like(idxx1)
            dmu_dc = - BETA * np.ones_like(idxc)
            i, j, v = [], [], []
            # dx0
            i.append(np.arange(self.nsn))
            j.append(idxx0)
            v.append(dmu_dx0)
            # dx1
            i.append(np.arange(self.nsn))
            j.append(idxx1)
            v.append(dmu_dx1)
            # dc
            i.append(np.arange(self.nsn))
            j.append(idxc)
            v.append(dmu_dc)
            v, i, j = np.hstack(v), np.hstack(i), np.hstack(j)
            jacobian = scipy.sparse.coo_matrix((v, (i, j)), shape=(self.nsn, 3*self.nsn))
            return mu, jacobian
        return mu

    def plot(self, hessian, give_inv=False, save_dir=None):
        """
        Plot HD !

        Parameters
        -------
        hessian : numpy.ndarray
            Half of the hessian matrix given from minimizer or
            Inverse of half hessian matrix [if give_inv is True]
        give_inv : bool
            If the give hessian is already inversed.
        save_dir : None or str
            Saving directory of the plot.
        """
        #        from pycosmo import cosmo
        from astropy import cosmology
        import nacl.plotting.plots as plots
        from nacl.plotting.plots import hist
        #        cos = cosmo.Cosmo()
        cos = cosmology.FlatLambdaCDM(H0=70, Om=0.25)

        z, mu, dmu, var, inv_hessian = self.propagated_error(hessian, give_inv=give_inv)

        #        mu_th = cos.mu(z)
        mu_th = 5 * np.log10(np.array(cos.luminosity_distance(z))) + 25 # because pycosmo distances are in Mpc
        idx = z.argsort()

        plots.plot_HD(z, mu, dmu, mu_th, save_dir=save_dir)

        fig = pl.figure()
        chi2 = (mu - mu_th) / dmu
        ax = fig.add_subplot(111)
        hist(ax, chi2)
        ax.set_title(f'{(((mu - mu_th) / dmu) ** 2).sum()}')
        print('blue ', save_dir)
        if save_dir is not None:
            pl.savefig(save_dir + os.sep + f'distances_modulus_chi2.png')

        cov = var.copy()[idx].T[idx].T
        sig = np.sqrt(np.diag(cov))
        fig = pl.figure()
        ax0 = fig.add_subplot(121)
        m0 = ax0.matshow(cov, cmap=pl.matplotlib.cm.Blues)
        ax0.set_title('Distance covariance Matrix')
        pl.colorbar(m0)

        ax = fig.add_subplot(122)
        m = ax.matshow(cov / (sig.reshape(-1, 1) @ sig.reshape(-1, 1).T), cmap=pl.matplotlib.cm.Blues)
        ax.set_title('Distance correlation Matrix')
        pl.colorbar(m)
        if save_dir is not None:
            pl.savefig(save_dir + os.sep + f'distances_modulus_correlationMatrix.png')

    def propagated_error(self, hessian, give_inv=False):
        r"""
        From model fit, calculate distance modulus.

        The covariance matrix of the estimated parameters  (:math:`X_0`, :math:`X_1` and :math:`c`)
        can be obtained from the inverse of the hessian computed at the minimum.

        Let us note :math:`V^F = H^{-1}`, then the covariance matrix after marginalization on all the other
        parameters of the model is written~:


        .. math::
            V_{SN}= \begin{pmatrix}
            V^F_{X_0,X_0} & V^F_{X_0, X_1} & V^F_{X_0, c} \\
            V^F_{X_1, X_0} & V^F_{X_1, X_1} & V^F_{X_1, c} \\
            V^F_{c, X_0} & V^F_{c, X_1} & V^F_{c, c} \\
            \end{pmatrix}


        The covariance matrix of :math:`\mu` is deduced via the uncertainty propagation formula~:

        .. math::
            V_{\mu}^F(\mu) = J_{\mu} V_{SN} J_{\mu}^T

        where :math:`J_{\mu}} = (\frac{\partial }{partial X_0 },
        \frac{\partial }{partial X_1 }, \frac{\partial }{partial c})`
        is the matrix of derivatives of the distance modulus.

        Parameters
        -------
        hessian : numpy.array
            Half of the hessian matrix given from minimizer or
            Inverse of half hessian matrix [if give_inv is True]
        give_inv : bool
            If the give hessian is already inversed.

        Returns
        -------
        z : numpy.array
            SNe redshift.
        mu : numpy.array
            Distance modulus
        dmu : numpy.array
            Error on distance modulus from error on SNe parameters from fit.
        var : numpy.ndarray
            Covariance matrix.
        inv_hessian : numpy.ndarray
            Inverse of half of the hessian calculated at the minimum of the fit.
        """
        mu, jacobian = self(self.model.pars.free, jac=True)

        if give_inv:
            inv_hessian = hessian.copy()
        else:
            inv_hessian = np.linalg.inv(hessian)
        cov_matrix = inv_hessian[:3 * self.nsn, :3 * self.nsn]
        var = jacobian @ cov_matrix @ jacobian.T
        dmu = np.sqrt(np.diag(np.abs(var)))
        z = self.model.training_dataset.sne["z"]

        ret = [z, mu, dmu, var, inv_hessian]
        return ret
