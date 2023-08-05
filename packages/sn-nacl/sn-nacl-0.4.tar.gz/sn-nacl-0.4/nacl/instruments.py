"""Access point to the instrument models.

At the moment, the module is still connected to
`saunerie.instruments`.  We will change that and probably stick to the
I/O system implemented in sncosmo.

"""

import numpy as np
from sksparse.cholmod import cholesky_AAt

import logging
import os
# TODO: import saunerie.instruments here
# TODO: maybe make it compatible with sncosmo I/O's
from .lib.instruments import InstrumentModel

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)


ZP_ERROR = {'MEGACAMPSF::g': 3,
            'MEGACAMPSF::i': 4,
            'MEGACAMPSF::r': 6,
            'MEGACAMPSF::z': 8,
            'SDSS::g': 4,
            'SDSS::i': 3,
            'SDSS::r': 2,
            'SDSS::u': 8,
            'SDSS::z': 5,
            'SWOPE::B': 8,
            'SWOPE::V': 8,
            'SWOPE::r': 8,
            'SWOPE::u': 23,
            '4SHOOTER2::B': 11,
            '4SHOOTER2::I': 20,
            '4SHOOTER2::R': 8,
            '4SHOOTER2::Us': 70,
            '4SHOOTER2::V': 7,
            'KEPLERCAM::B': 11,
            'KEPLERCAM::Us': 31,
            'KEPLERCAM::V': 7,
            'KEPLERCAM::i': 8,
            'KEPLERCAM::r': 25,
            'STANDARD::B': 15,
            'STANDARD::I': 15,
            'STANDARD::R': 15,
            'STANDARD::U': 100,
            'STANDARD::V': 15,
            'SWOPE2::B': 8,
            'SWOPE2::V': 8,
            'SWOPE2::g': 9,
            'SWOPE2::i': 8,
            'SWOPE2::r': 8,
            'SWOPE2::u': 23}

_instrument_repository = {}  # 'data/SALT3_training_sample/filters'}


def load_instrument(name, path=None):
    """
    Search for the requested instrument in a global dictionary.  If
    not found, load the instrument and return it (and update the
    cache).

    Parameters
        -------
        name : str
            Name of the instrument.
        path : None or str
            Whether instrument file should be specified.

        Returns
        -------
        ret : nacl.lib.instruments.InstrumentModel
            Instrument model.
    """
    global _instrument_repository
    ret = _instrument_repository.get(name, None)
    if ret is None:
        if path is None:
            ret = InstrumentModel(name)
        else:
            ret = InstrumentModel(name, path=path + os.sep + name)
        _instrument_repository[name] = ret
    return ret


_transmission_repository = {}


def load_transmission(instrument_name, passband_name, path=None):
    """
    Search for the specifier instrument and then the specified filter
    in their respective caches.  If not found, load, update the caches
    and return the passband.

    Parameters
    -------
    instrument_name : str
        Name of the instrument.
    passband_name : str
        Name of the desired band.
    path : None or str
        Whether instrument file should be specified.

    Returns
    -------
    ret : nacl.lib.instruments.InstrumentModel
        Filter transmission.

    """
    global _transmission_repository
    full_name = instrument_name + '::' + passband_name
    ret = _transmission_repository.get(full_name)
    if ret is None:
        try:

            instr = load_instrument(instrument_name, path=path)
            ret = instr.EffectiveFilterByBand(passband_name)
            #print('FLux in e not ADU')
            #ret = instr.get_efficiency_at_airmass(passband_name)
            _transmission_repository[full_name] = ret
        except KeyError:
            raise KeyError
    return ret


def load(full_name, path=None):
    """
    Transmission loader.

    Parameters
    -------
    full_name : str
        Names of the instrument & band such as 'INSTRUMENT::BAND'
    path : None or str
        Whether instrument file should be specified.

    Returns
    -------
    numpy.array
        Filter transmission.
    """
    instrument_name, passband_name = full_name.split('::')

    return load_transmission(instrument_name, passband_name, path=path)


class FilterDb:
    """
    Utility class that projects a set of filters on B-splines
    and stores the projection coefficients.

    The class is given a default projection basis, but it is always
    possible to define one (adapted) basis per filter.

    Attributes
    ----------
    basis : nacl.lib.bspline.BSpline
        Spline basis.
    _grid : np.array
        Grid, spline evaluation
    _J : scipy.sparse.csr_matrix
        Jacobian matrix.
    _factor : sksparse.cholmod.Factor
        Result of cholesky decomposition.
    filterpath : None or str
        Whether filter files should be specified.
    transmission_db : dict
        Transmission filters data base
    db : dict
        Data base of transmission project on basis is corrected from redshift.
    """

    def __init__(self, basis, tds=None, additional_band=None, filterpath=None):
        """
        Constructor - initialize the class, build a default projector.

        Parameters
        ----------
        basis : nacl.lib.bspline.BSpline
            Default BSpline basis on which to decompose the filters
        tds : nacl.dataset.TrainingDataset
            if present, load all the transmissions which
            are used in the training dataset and insert them in the database. [optional]
        """
        self.basis = basis
        self._grid, self._J, self._factor = self._projector(self.basis)
        self.filterpath = filterpath
        # I leave a trace of the factor that the FilterSet did actually
        # include the possibility of adding an external atmosphere model
        # Never used in practice -> I got rid of that.
        # self._atm = np.ones_like(self._grid)

        self.transmission_db = {}
        self.db = {}

        # if a tds is given, load all the transmissions
        # which appear in it.
        if tds is not None and tds.get_all_transmissions() is not None:
            for tr in tds.get_all_transmissions().values():
                self.insert(tr)
        if additional_band is not None:
            for bd in additional_band:
                self.insert(load(bd))

    def __len__(self):
        """
        Given number of filter stored in database.
        """
        return len(self.db)

    @staticmethod
    def _projector(basis):
        r"""
        Precompute the elements and factorization of the fit matrix

        .. math:: (J^T J)^{-1} J^T

        this saves repeated calls to cholesky_AAt when processing
        other filters.

        Parameters
        ----------
        basis : nacl.lib.bspline.BSpline
            Spline basis.

        Returns
        -------
        gxx : np.array
            Grid, spline evaluation
        jacobian : scipy.sparse.csr_matrix
            Jacobian matrix.
        factor : sksparse.cholmod.Factor
            Result of cholesky decomposition.
        """
        # refine the basis grid
        gx = basis.grid
        gxx = np.hstack((gx, 0.5*(gx[1:]+gx[:-1])))
        gxx.sort()
        # precompute the projector
        # (will save repeated calls to cholesky_AAt)
        jacobian = basis.eval(gxx).tocsr()
        factor = cholesky_AAt(jacobian.T)
        return gxx, jacobian, factor

    def insert(self, tr, z=0., basis=None):
        """
        Project the transmission `tr` on the spline basis and insert it
        into the database.

        If basis is None (which should be almost always the case) we
        use the default projector. Otherwise, we recompute a projector
        and use it.

        Parameters
        ----------
        tr :
            Filter transmission.
        z : float
            SN redshift.
        basis : nacl.lib.bspline.BSpline
            Spline basis.

        Returns
        -------
        tq : numpy.array
            Transmission for grid of wavelength redshift corrected.
        b : nacl.lib.bspline.BSpline
            Spline basis.
        """
        if basis is None:  # then, use the default basis
            grid, jacobian, factor = self._grid, self._J, self._factor
            b = self.basis
        else:
            grid, jacobian, factor = self._projector(basis)
            b = basis

        y = tr(grid * (1.+z))  # * atm
        tq = self._factor(self._J.T * y)

        full_name = tr.InstrumentName + '::' + tr.Band
        self.transmission_db[full_name] = tr
        self.db[(full_name, z)] = (tq, b)
        if z == 0.:
            self.db[full_name] = (tq, b)
        return tq, b

    def __getitem__(self, key):
        """
        Retrieve the coefficients and basis for the requested filter.
        """
        if key not in self.db:
            raise KeyError
        return self.db[key]

    def plot(self, key):
        pass

