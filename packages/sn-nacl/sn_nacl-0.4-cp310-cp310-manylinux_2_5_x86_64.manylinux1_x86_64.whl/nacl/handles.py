"""A set of utility classes to manipulate and view SNe, Spectra and Lightcurves
"""

import pathlib
from typing import List
import numpy as np
import logging
import pandas
import pylab as pl

from nacl.lib.dataproxy import DataProxy
from . import instruments
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)

# from numba import njit


class SNData:

    def __init__(self, sn_data):
        """constructor

        Parameters
        ----------
        sn_data : record
            a record that contains at least the following fields:
              - 'z', the SN redshift (float)
              - 'sn', a unique ID for the SN (int or str)
              - 'valid', int
        """
        self.data = sn_data
        self.lcs = {}
        self.spectra = []

    @property
    def z(self):
        return self.data.z

    @property
    def valid(self):
        return self.data.valid

    def kill(self):
        """invalidate the SN and all the associated follow-up data
        """
        self.data.valid = 0
        for lc in self.lcs.values():
            lc.data.valid[:] = 0
        for sp in self.spectra:
            sp.data.valid[:] = 0

    def plot(self):
        """standard plot to present the SN data"""
        pass


class LcData:
    """A class to access the light curve data."""

    def __init__(self, sn, band, slc, lc_data):
        """Constructor

        Parameters
        ----------
        sn : int
            Index of sn.
        band : str
            Name of the Filter.
        slc : slc
            Index of the Light Curve data in the full photometric data.
        lc_data : numpy.rec.array
            Photometric data.
        sne : numpy.recarray
            Information of all SNe (:math:`(z, X_0, X_1, c, t_{max})`)
        """
        self.sn = sn
        self.band = str(band) # .astype(str)
        self.slc = slc
        self.lc_data = lc_data

    def __len__(self):
        """number of light curve data points.
        """
        return len(self.lc_data[self.slc])

    @property
    def valid(self):
        return np.sum(self.data.valid) > 0

    @property
    def data(self):
        """
        Return numpy.rec.array data file.
        """
        return self.lc_data[self.slc]

    @property
    def z(self):
        """redshift"""
        return self.sn.z

    def kill(self):
        """invalidate all the light curve measurements"""
        self.data.valid[:] = 0

    def plot(self, ax=None):
        """standard light curve plot"""
        pl.figure()
        x, y, ey = self.data['mjd'], self.data['flux'], self.data['fluxerr']
        pl.errorbar(x, y, yerr=ey, ls='', color='k', marker='o')
        pl.xlabel('phase [days]')
        pl.ylabel('Flux')
        pl.title('SN#{} {} [$z={:5.3}]$'.format(self.sn_id, self.band, self.z))


class SpectrumData:
    """A class to access and plot spectra
    """
    def __init__(self, sn, spec, slc, sp_data):
        """Constructor

        Parameters
        ----------
        sn : SNData
            info about the SN
        spectrum : str or int
            Spectrum unique identifier
        slc : slc
            slice o
        sp_data : numpy.recarray or pandas.DataFrame
            spectral data
        """
        self.sn = sn
        self.spec = spec
        self.slc = slc
        self.sp_data = sp_data

    def __len__(self):
        """number of data points"""
        return len(self.data)

    @property
    def data(self):
        """the spectrum data itself"""
        return self.sp_data[self.slc]

    @property
    def z(self):
        """Sn redshift"""
        return self.sn.z

    def kill(self):
        self.data.valid[:] = 0

    def plot(self):
        """standard control plot
        """
        pl.figure()
        x, y, ey = self.data['wavelength'], self.data['flux'], self.data['fluxerr']
        pl.errorbar(x, y, yerr=ey, ls='', color='k')
        pl.xlabel(r'$\lambda [\AA]$')
        pl.ylabel('flux')
        pl.title('SN#{} [$z={:5.3}$]'.format(self.sn_id, self.z))

def _index_sne(tds):
    sne = dict([(r.sn, SNData(r)) for r in tds.sn_data.nt])
    return sne

def _index_lcs(tds, sne):
    """parse the lc_data and build the light curve index

    Parse the lc_data, build a LcData handle for each identified LC,
    and attach it to its SN

    Parameters
    ----------
    lc_data : nacl.lib.DataProxy
        the DataProxy that handles all the lightcurves
    sne : Dict[SNData]
        the index - each entry corresponds to a SN
    """
    lcs = []
    lc_data = tds.lc_data

    if not hasattr(lc_data, 'sn_index'):
        lc_data.make_index('sn')
    if not hasattr(lc_data, 'band_index'):
        lc_data.make_index('band')
    index = lc_data.sn_index * 100 + lc_data.band_index

    # detect the block edges
    i_slices = np.where(index[1:] - index[:-1])[0] + 1
    i_slices = np.hstack(([0], i_slices.repeat(2), [-1])).reshape((-1,2))

    # now comes the slow part -- we build the handles to each lightcurve
    # logging.info(f'building the LcData handles {i_slices.shape[0]} to build')
    lc_data_nt = lc_data.nt
    for i in range(i_slices.shape[0]):
        slc = slice(*i_slices[i])
        r = lc_data_nt[slc.start]
        lcdata = LcData(sne[r.sn], r.band, slc, lc_data.nt)
        lcs.append(lcdata)
        sne[r.sn].lcs[r.band] = lcdata
    return lcs

def _index_spectra(tds, sne):
    """parse the spec_data, identifies all the spectra

    Parameters
    ----------
    spec_data : _type_
        _description_
    sne : _type_
        _description_
    """
    spec_data = tds.spec_data
    spectra = []

    if not hasattr(spec_data, 'spec_index'):
        spec_data.make_index('spec')
    if not hasattr(spec_data, 'sn_index'):
        spec_data.make_index('sn')

    # logging.info('indexing the spectra')
    mjd = spec_data.mjd
    i_slices = np.where(mjd[1:] - mjd[:-1])[0] + 1
    i_slices = np.hstack([[0], i_slices.repeat(2), [-1]]).reshape((-1,2))

    # now, indexing
    spec_data_nt = spec_data.nt
    for i in range(i_slices.shape[0]):
        slc = slice(*i_slices[i])
        r = spec_data_nt[slc.start]
        spdata = SpectrumData(sne[r.sn], r.spec, slc, spec_data_nt)
        spectra.append(spdata)
        sne[r.sn].spectra.append(spdata)
        # logging.info('done.')
    return spectra

def build_index(tds):
    sne = _index_sne(tds)
    lcs = _index_lcs(tds, sne)
    spectra = _index_spectra(tds, sne)
    return sne, lcs, spectra

