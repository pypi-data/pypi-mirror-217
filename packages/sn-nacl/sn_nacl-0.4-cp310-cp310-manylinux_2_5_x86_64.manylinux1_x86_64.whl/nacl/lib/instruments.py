""" Simple tools to read descriptions of instruments.

This module provides a python equivalent to the SNFIT "Instrument"
class.
"""

from ..util.io import NTuple
import os.path as op
import sys

from . import constants, atmosphericmodel, spectrum
from .interpolation import Func1D
from .indextools import first_two_cols
from ..util import saltpath
from warnings import warn
from glob import glob


import numpy as np

#import pdb
import re
from functools import reduce

#######################################
# Flux and units
#######################################
OVERHC = 1. / (constants.C_LIGHT * constants.H * 1e17)


#######################################
# Reader for config and data files
#######################################
def read_transmission_files(filename):
    """Read the transmission files following the snfit_data convention.

    Handle correctly the headers in snfit_data in particular WAVELENGTH_IN_NM trigger conversion to angstrom
    """
    with open(filename) as fid:
        lines = fid.readlines()
    keys = {}
    comments = []
    i = 0
    for line in lines:
        if line[0] not in ['@', '#']:
            break
        if line[0] == '@':
            k = line[1:].split()
            keys[k[0]] = ' '.join(k[1:])
        else:
            comments.append(line)
        i = i+1
    vals = np.genfromtxt(lines[i:])


    if 'WAVELENGTH_IN_NM' in keys:
        vals[:, 0] *= 10
    return vals

def read_filter_wheel_file(filename):
    """ Read the filter wheel description
    """
    fid = open(filename)
    lines = fid.readlines()
    fid.close()
    fwheel = {}
    for line in lines:
        if line[0] == '#':
            continue
        values = line.split()
        if len(values) == 2:
            fwheel[values[0]] = fwheel.get(values[0], []) + [values[1]]
        elif len(values) == 3:
            fwheel[values[0]] = fwheel.get(values[0], []) + [values[2]]
        else:
            print(("Warning: Strange line in file %s" % filename))
            print(line)
    return fwheel


class Transmission(Func1D):
    """
    Special Func1D to handle filters
    
    Needed for them to know which Instrument they are from, and which Band they are
    """

    def __init__(self, *func_like, **kwargs):
        """
        By default the InstrumentName and Band are None
        InstrumentName: option to set the filter InstrumentName
        Band: option to set the filter Band
        """

        InstrumentName = kwargs.pop("InstrumentName", None)
        Band = kwargs.pop("Band", None)

        Func1D.__init__(self, *func_like, **kwargs)
        self.InstrumentName = InstrumentName
        self.Band = Band

    def __mul__(self, func2):
        """ Return a Func1D that will evaluate to the product of self
        and f2.
        """
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max

        InstrumentName = self.InstrumentName
        Band = self.Band
        
        if isinstance(func2, Func1D):
            x_min = max(self.x_min, func2.x_min)
            if func2.x_max != 0:
                x_max = min(self.x_max, func2.x_max)

        if  isinstance(func2, Transmission):
            x_min = max(self.x_min, func2.x_min)
            if func2.x_max != 0:
                x_max = min(self.x_max, func2.x_max)
            if func2.InstrumentName is not None:
                if InstrumentName is None:
                    InstrumentName = func2.InstrumentName
                else:
                    if func2.InstrumentName != InstrumentName:
                        raise ValueError("Multiplying transmissions from different instruments (%s, %s)" % (InstrumentName, func2.InstrumentName))

            if func2.Band is not None:
                if Band is None:
                    Band = func2.Band
                else:
                    if func2.Band != Band:
                        raise ValueError("Multiplying transmissions from different bands (%s, %s)" % (Band, func2.Band))
            
        return Transmission( lambda x: self.func(x) * Func1D( func2 ).func(x), x_min=x_min, x_max=x_max,
                             InstrumentName=InstrumentName,
                             Band=Band)

    #- Transmission multiplication is commutative and yields a Transmission
    __rmul__ = __mul__

    def __add__(self, func2):
        """ Return a Func1D that will evaluate to the sum of self
        and func2.
        """        
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max
        InstrumentName = self.InstrumentName
        Band = self.Band
        
        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        if  isinstance(func2, Transmission):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )
            if func2.InstrumentName is not None:
                if InstrumentName is None:
                    InstrumentName = func2.InstrumentName
                else:
                    if func2.InstrumentName != InstrumentName:
                        raise ValueError("Multiplying transmissions from different instruments (%s, %s)" % (InstrumentName, func2.InstrumentName))

            if func2.Band is not None:
                if Band is None:
                    Band = func2.Band
                else:
                    if func2.Band != Band:
                        raise ValueError("Multiplying transmissions from different bands (%s, %s)" % (Band, func2.Band))

        return Transmission( lambda x: self.func(x) + Func1D( func2 ).func(x), x_min=x_min, x_max=x_max,
                             InstrumentName=InstrumentName,
                             Band=Band)

    #- Transmission addition is commutative and yields a transmission
    __radd__ = __add__

    def __sub__(self, func2):
        """ Return a Func1D that will evaluate to the difference of self
        and func2.
        """        
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max
        InstrumentName = self.InstrumentName
        Band = self.Band
        
        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )


            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )
            if func2.InstrumentName is not None:
                if InstrumentName is None:
                    InstrumentName = func2.InstrumentName
                else:
                    if func2.InstrumentName != InstrumentName:
                        raise ValueError("Multiplying transmissions from different instruments (%s, %s)" % (InstrumentName, func2.InstrumentName))

            if func2.Band is not None:
                if Band is None:
                    Band = func2.Band
                else:
                    if func2.Band != Band:
                        raise ValueError("Multiplying transmissions from different bands (%s, %s)" % (Band, func2.Band))

        return Transmission( lambda x: self.func(x) - Func1D( func2 ).func(x), x_min=x_min, x_max=x_max,
                             InstrumentName=InstrumentName,
                             Band=Band)

    def __rsub__(self, func2):
        """ Return a Func1D that will evaluate to the difference of func2
        and self.
        """        
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max
        InstrumentName = self.InstrumentName
        Band = self.Band
        
        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        if  isinstance(func2, Transmission):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )
            if func2.InstrumentName is not None:
                if InstrumentName is None:
                    InstrumentName = func2.InstrumentName
                else:
                    if func2.InstrumentName != InstrumentName:
                        raise ValueError("Multiplying transmissions from different instruments (%s, %s)" % (InstrumentName, func2.InstrumentName))

            if func2.Band is not None:
                if Band is None:
                    Band = func2.Band
                else:
                    if func2.Band != Band:
                        raise ValueError("Multiplying transmissions from different bands (%s, %s)" % (Band, func2.Band))

        return Transmission( lambda x: Func1D( func2 ).func(x) - self.func(x), x_min=x_min, x_max=x_max,
                             InstrumentName=InstrumentName,
                             Band=Band)

    def __pow__(self, func2):
        """ Return a Func1D that will evaluates self ** func2
        """        
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max
        InstrumentName = self.InstrumentName
        Band = self.Band
        
        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        if  isinstance(func2, Transmission):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )
            if func2.InstrumentName is not None:
                if InstrumentName is None:
                    InstrumentName = func2.InstrumentName
                else:
                    if func2.InstrumentName != InstrumentName:
                        raise ValueError("Multiplying transmissions from different instruments (%s, %s)" % (InstrumentName, func2.InstrumentName))

            if func2.Band is not None:
                if Band is None:
                    Band = func2.Band
                else:
                    if func2.Band != Band:
                        raise ValueError("Multiplying transmissions from different bands (%s, %s)" % (Band, func2.Band))

        return Transmission( lambda x: self.func(x) ** (Func1D( func2 ).func(x)), x_min=x_min, x_max=x_max,
                             InstrumentName=InstrumentName,
                             Band=Band)

    def __rpow__(self, func2):
        """ Return a Func1D that will evaluates func2 ** self
        """        
        #- in this case, func2 would have default x_min and x_max 
        #- and 0 looses in the test just above
        x_min = self.x_min
        x_max = self.x_max
        InstrumentName = self.InstrumentName
        Band = self.Band
        
        if isinstance(func2, Func1D):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )

        if  isinstance(func2, Transmission):
            x_min = max( self.x_min, func2.x_min )
            if func2.x_max != 0:
                x_max = min( self.x_max, func2.x_max )
            if func2.InstrumentName is not None:
                if InstrumentName is None:
                    InstrumentName = func2.InstrumentName
                else:
                    if func2.InstrumentName != InstrumentName:
                        raise ValueError("Multiplying transmissions from different instruments (%s, %s)" % (InstrumentName, func2.InstrumentName))

            if func2.Band is not None:
                if Band is None:
                    Band = func2.Band
                else:
                    if func2.Band != Band:
                        raise ValueError("Multiplying transmissions from different bands (%s, %s)" % (Band, func2.Band))

        return Transmission( lambda x: (Func1D( func2 ).func(x)) ** self.func(x), x_min=x_min, x_max=x_max,
                             InstrumentName=InstrumentName,
                             Band=Band)
    
        
        
class FilterWheel(object):
    """ Handle the Filter transmissions

    The transmissions are Transmission instances
    """
    def __init__(self, path, filename, InstrumentName=None):
        # Filenames is a dictonnary with one key per band of the filterwheel
        filenames = read_filter_wheel_file(op.join(path, filename))
        self.transmissions = {}
        self.range = {}
        for band in filenames:
            transmission = read_transmission_files(op.join(path, filenames[band][0]))
            self.transmissions[band] = Transmission(transmission[:, 0], 
                                              transmission[:, 1],
                                              Band=band,
                                              InstrumentName=InstrumentName)
            self.range[band] = (self.transmissions[band].func.x.min(), 
                                self.transmissions[band].func.x.max())

    def __call__(self, band, **keys):
        """ Return the instrument transmission in band b

        Parameters:
        -----------
        band: string
              name of the photometric band

        focal_plane_position: not used in this class (see subclasses
                              such as RadiallyVariableFilterWheel for
                              position dependent Filters)
        """
        return self.transmissions[band]

    def get_filter_bandpass(self, band):
        """ Give the wavelength range covered by a filter

        Parameters:
        -----------
        band: string
              name of the photometric band
        """
        return self.range[band]


class RadiallyVariableFilterWheel(FilterWheel):
    """ Handle radially variable filters such as MegaCam filters.

    """
    def __init__(self, path, filename, InstrumentName=None):
        filenames = read_filter_wheel_file(op.join(path, filename))
        self.transmissions = {}
        self.range = {}
        self.radii = {}
#        for band in 'ugriyz':
        for band in filenames:
            self.transmissions[band] = [NTuple.fromtxt(
                op.join(path, f)) for f in filenames[band]]
            self.radii[band] = [float(nt.keys['MEASUREMENT_RADIUS'].replace('cm', '')) for nt in self.transmissions[band]]
            self.transmissions[band] = [Transmission(*first_two_cols(t),
                                               Band=band,
                                               InstrumentName=InstrumentName) for t in self.transmissions[band]]
            self.range[band] = (self.transmissions[band][0].func.x.min(),
                                self.transmissions[band][0].func.x.max())
            
    def _get_rad(self, rad, band):
        radii = self.radii[band]
        i = np.digitize([rad], radii)[0]
        imax = len(radii)-1
        if i > imax:
            i = imax
        i = i - 1
        r1, r2 = radii[i], radii[i + 1]
        w = (rad - r1) / (r2 - r1)
        if w < 0 or w > 1:
            raise ValueError('Radius %f is outside the focal plane' % rad)
        return i, w
    
    def __call__(self, band, focal_plane_position=0.):
        """ Return the instrument transmission in band b

        Parameters:
        -----------
        band: string
              name of the photometric band

        focal_plane_position: radius in cm
        """
        i, w = self._get_rad(focal_plane_position, band)
        return (self.transmissions[band][i + 1] * w) + (self.transmissions[band][i] * (1 - w))

class VariableFilterWheel(FilterWheel):
    """ Handle variable filters such as MegaCam filters.
    """
    def __init__(self, path, filename, InstrumentName=None):
        filenames = read_filter_wheel_file(op.join(path, filename))
        self.transmissions = {}
        self.range = {}
        self.pos = {}
        self.x = {}
        self.y = {}
        self.grid = {}
        for band in filenames:
            transmissions = [NTuple.fromfile(
                f) for f in glob(op.join(path, filenames[band][0]))]
            x = np.array([float(nt.keys['MEASUREMENT_X']) for nt in transmissions])
            y = np.array([float(nt.keys['MEASUREMENT_Y']) for nt in transmissions])
            self.pos[band] = np.rec.fromarrays([x,y], names=['x', 'y'])
            s = np.argsort(self.pos[band], order=['x', 'y'])
            self.pos[band] = self.pos[band][s]
            self.transmissions[band] = np.array([Transmission(*first_two_cols(transmissions[i]),
                                                     Band=band,
                                                     InstrumentName=InstrumentName) for i in s])
            self.x[band] = np.unique(self.pos[band]['x'])
            self.y[band] = np.unique(self.pos[band]['y'])
            self.range[band] = (self.transmissions[band][0].func.x.min(),
                                self.transmissions[band][0].func.x.max())
            self.transmissions[band] = self.transmissions[band].reshape((len(self.x[band]), len(self.y[band])))
            
    def _2D_interp(self, pos, band):
        i = np.digitize(pos[0], self.x[band]) - 1
        j = np.digitize(pos[1], self.y[band]) - 1
        x = self.x[band]
        y = self.y[band]
        if i > len(x) or i < 0 or j > len(y) or j < 0:
            raise ValueError('Radius %f, %f is outside the focal plane' % (pos[0], pos[1]))
        a, b = x[i], x[i+1]
        c, d = y[j], y[j+1]
        w_x = (pos[0] - a) / (b - a)
        w_y = (pos[1] - c) / (d - c)
        return i, j, w_x, w_y
    
    def __call__(self, band, focal_plane_position=(0.,0.)):
        """ Return the instrument transmission in band b

        Parameters:
        -----------
        band: string
              name of the photometric band

        focal_plane_position: radius in cm
        """
        i, j, w_x, w_y = self._2D_interp(focal_plane_position, band)
        r = self.transmissions[band]
        return ((r[i, j] * ((1 - w_x) * (1 - w_y))) +
                (r[i+1, j] * ((1 - w_y) * w_x)) + 
                (r[i, j + 1] * ((1 - w_x) * w_y)) +
                (r[i+1, j+1] * (w_x * w_y)))



class MagSys(object):
    """
    Handles the MagSys description
    """
    
    #+ Rajouter le truc de Marc de instmodel ici
    def __init__(self, magsys_name):
        """
        Read the magsys description from an snfit_data directory

        The reference spectrum is loaded in a spectrum under
        self.reference_spectrum

        Note that self.ZP is not the ZeroPoint as implemented in snfit/src/magsys.cc
        but the magnitude of the reference star in the filter.

        In order to get the ZeroPoint needed to calculate the magnitude, it is necessary
        to invoke self.ZeroPoint(ObserverFilter) where ObserverFilter is a Transmission instance.
        
        It can NOT be a simple Func1D instance, for it needs to know its InstrumentName and Band


        Parameters:
        -----------
        magsys_name should be described in fitmodel.cards pointed
        at by $SALTPATH
        """
        fitmodel_card = saltpath.read_fitmodel_card()
        if magsys_name == 'AB':
            self.pure_ab = True
            return
        else:
            self.pure_ab = False
        if not (magsys_name in fitmodel_card):
            raise ValueError("Couldn't find MagSys %s in your SALTPATH (%s)" % (magsys_name, saltpath.SALTPATH))

        magsys_filename = saltpath.SALTPATH + "/" + fitmodel_card[magsys_name]
            
        self.ZP = {}

        fh = open(magsys_filename, "r")
        for line in fh.readlines():
            #- remove comments and empty lines
            line = (re.sub("#.*$", "", line)).strip()        
            if len(line) == 0:
                continue
            if line.startswith("@"):
                group = re.search("^@(.+?)\s+(.+)", line)
                group = group.groups()
                if group[0] == "SPECTRUM":
                    self.reference_spectrum_path = saltpath.SALTPATH + "/" + group[1]
                    self.reference_spectrum = spectrum.load_ascii(self.reference_spectrum_path)
            #- This assumes that the magsys file is not exotic:
            #- if it is not a comment, an @ or an empty line, it is an instrument ZP
            else:
                data = line.split()
                if not (data[0] in list(self.ZP.keys())):
                    self.ZP[data[0]] = {}
                self.ZP[data[0]][data[1]] = float(data[2])

    def ZeroPoint(self, ObserverFilter):
        """
        Same implementation as snfit/src/magsys.cc
        
        ObserverFilter needs to be a Transmission instance 
        """
        if self.pure_ab:
            wl = np.linspace(ObserverFilter.x_min, ObserverFilter.x_max)
            reference_spectrum = spectrum.Spectrum(wl, constants.flux_ab(wl))
            return 2.5 * np.log10(reference_spectrum.IntegFlux(ObserverFilter, 0.))
        else:
            flux = self.reference_spectrum.IntegFlux(ObserverFilter, 0.)
            return 2.5 * np.log10(flux) + self.ZP[ObserverFilter.InstrumentName][ObserverFilter.Band]

    def mag(self, ObserverFilter, spectrum_list, spectrum_loader=lambda x : x):
        """
        Calculates the magnitude of spectra using an ObserverFilter that has to be
        a Transmission instance.

        If spectrum_loader is provided, uses it to read the data. Otherwise, assumes that 
        spectrum_list is a list of spectrum.Spectrum instance

        ObserverFilter is expected to be a list of ObserverFilters

        Examples:
        ---------
        load the spectra (if you run in test, where PTF09dnl data lives)
        >>> sn_name = "PTF09dnl"
        >>> sn_path = os.path.join("./", sn_name)
        >>> nt_sn = nacl.util.NTuple.fromtxt(os.path.join(sn_path, "%s_spec_merged.list" %  (sn_name)))
        >>> l_spectrum = []
        >>> for filename in nt_sn["filename"]:
               tmp_spectrum = spectrum.load_ntuple(os.path.join(sn_path, filename))
               l_spectrum.append(tmp_spectrum)

        Load the instrument and magsys
        >>> instrument = instruments.InstrumentModel("SWOPE")
        >>> magsys = instruments.MagSys("VEGA")
        >>> observer_filter = instrument.EffectiveFilterByBand("g")


        Possible to use only one filter and spectrum
        >>> magsys.mag(observer_filter, l_spectrum[3])
        array([(-19.94143291159957,)],
              dtype=[('g', '<f8')])

        Possible to calculate the mags of the full spectrum list
        >>> magsys.mag(observer_filter, l_spectrum)
            array([(-19.829897425083587,), (-19.920241486850074,),
                   (-19.932614171822166,), (-19.94143291159957,),
                   (-19.88517517546827,), (-19.889984971628934,),
                   (-19.84623774750333,), (-19.835170085307567,),
                   (-19.69677647212223,), (-19.560002435004172,),
                   (-19.357319526502515,), (-18.99707016591549,),
                   (-18.905751902417677,), (-18.895062900516358,),
                   (-18.823659018820486,), (-18.82680933234854,),
                   (-18.59134345034653,), (-18.275082295370318,),
                   (-18.106126338432183,), (-18.0919526101773,),
                   (-17.823886134044365,), (-17.787802645726963,), (-17.516200221607,),
                   (-17.37836748599415,), (-17.38841134403154,),
                   (-17.363730161058008,), (-17.3197802772009,),
                   (-17.263928780299743,), (-17.207123524932392,),
                   (-17.19225272676723,)],
                  dtype=[('g', '<f8')])

        Possible to load the spectra inside of the mag calculation, with a spectrum_loader       
        >>> os.chdir(sn_path)
        >>> magsys.mag(observer_filter, nt_sn["filename"], spectrum_loader=spectrum.load_ntuple)
            array([(16.01232254417715,), (15.92860061849749,), (15.921179105837751,),
                   (15.913653784190643,), (15.977232537932833,), (15.971919469595042,),
                   (16.022310674641226,), (16.033430436507768,), (16.19766767411273,),
                   (16.343111225705233,), (16.534715100013916,), (16.948693007225014,),
                   (17.053167003173723,), (17.066288834748185,), (17.15258042408282,),
                   (17.14327408888971,), (17.414470723339335,), (17.764370290920283,),
                   (17.95434843068567,), (17.971541356898307,), (18.211643011663316,),
                   (18.21272014546581,), (18.52436971411903,), (18.650500460393452,),
                   (18.639698400983757,), (18.651509477256596,), (18.622885337729812,),
                   (18.746686051787446,), (18.82050490149692,), (18.763722405091343,)],
                  dtype=[('g', '<f8')])

        And also possible to loop over filters instances:
        
        """
        # Syntaxic sugar to allow the easy use of mag on only one spectrum or only one transmission
        if isinstance(spectrum_list, spectrum.Spectrum):
            spectrum_list = [spectrum_list]
        if isinstance(ObserverFilter, Transmission):
            ObserverFilter = [ObserverFilter]

            
        res = np.zeros(len(spectrum_list), dtype=[(of.Band, float) for of in ObserverFilter])
        for _sp, sp in enumerate(spectrum_list):
            s = spectrum_loader(sp)
            res[_sp] = tuple(s.IntegFlux(of, 0.) for of in ObserverFilter)
        for of in ObserverFilter:
            Zp = self.ZeroPoint(of)
            res[of.Band] = -2.5 * np.log10(res[of.Band]) + Zp
        return res
        

class InstrumentModel(object):
    """Handle instrument description.

    The way we handle transmissions needs some convention to be clearly stated out here.

    A transmission is a value that describes how a given quantity (say photons)
    is transfered, without changing the nature of the quantity (i.e. yielding photons in this case).
    It is a ratio between 0 and 1. 

    An efficiency is a value that describes how a given quantity is transformed
    into an other quantity. For example how a filter+detector transforms photons
    in electrons. Or in ADUs.

    Since photons are the correct way to deal with flux in cosmology analysis,
    we decide to only consider transmissions in photons per photons, and
    efficiencies in electrons per photons. An option will be made available for
    transforming photons in ADUs in order prevent the mistake inherent to the
    fact that a gain is in e/ADUs (one thus has to *divide* the efficiency in
    electrons per photons by the gain in order to get ADUs per photons)

    We expect the spectra to be in photons/A/cm^2, but they are usually provided
    in ergs/A/cm^2, which is why the Spectrum class implements a
    s.photon method that provides the Func1D giving the spectrum of the object
    in photons/A/cm^2
    

    The functions that provide those different values are:

    self.filters(band, focal_plane_position): the pure filter transmission in photons per photons

    get_transmission(band): provides the instrument transmission (between 0 and 1) in photons per photons 
                            includes mirror reflectivity and optics transmission

    get_efficiency(band): provides the efficiency of transformation between
                          photons and electrons includes the instrument
                          transmission, the quantum efficiency of the detector
                          and the area of the mirror

    get_efficiency(band, unit="ADU"): provides the efficiency of transformation between photons and electrons

    EffectiveFilterByBand(band): for similarity with snfit. Provides the
    "transmission" in ADUs/photons, or using the semantic defined above, the
    efficiency in ADUs per photons

    """
    def __init__(self, name=None, path=None):
        """ Read the instrument description from an snfit_data
        directory.

        Parameters:
        -----------
        name: the name of an instrument described in fitmodels.card in the
        $SALTPATH

        path: The path to an instrument directory. This is for convenience.
              if a name is provided, the filter will have this name, otherwise, 
              it will have the default name "default_name"

        """
        if path is not None:
            #- here we are in a special case, where the user knows what he is doing
            #- he is trying to access a special instrument file directly, for testing
            if name is None:
                #- We need a name for the InstrumentModel instance, no matter what
                name = "default_name"                
            instrument_path = path
        else:
            #- here no special path is provided. Name should be provided
            #- Follwoing the Instrument file system, we should have a 
            #- directory labelled by the instrument name
            if name is None:
                raise ValueError("Could not create instrument without name")            
            fitmodels = saltpath.read_fitmodel_card()            
            try:
                instrument_path = fitmodels[name]
            except KeyError:
                raise ValueError('Unknown instrument %s' % name)
            instrument_path = op.join(saltpath.SALTPATH, instrument_path)

        instrument_file = op.join(instrument_path, 'instrument.cards')

        self.name = name
        self.path = instrument_path
        self.cards = saltpath.read_card_file(instrument_file)

        self.mirror_reflectivity = self._load('MIRROR_REFLECTIVITY')
        self.optics_transmission = self._load('OPTICS_TRANS')
        self.ccd_qe = self._load('QE')
        
        self.area = float(self.cards['MIRROR_AREA'])  # in cm^2

        if 'GAIN' in self.cards:
            self.gain = float(self.cards['GAIN'])
        else:
            self.gain = 1.
        
# deprecated
#        conv = self.area
#        self.open_transmission = (self.mirror_reflectivity *
#                                  self.optics_transmission *
#                                  self.ccd_qe * conv)
        if "RADIALLY_VARIABLE_FILTERS" in self.cards:
            self.filters = RadiallyVariableFilterWheel(
                self.path, self.cards['RADIALLY_VARIABLE_FILTERS'], InstrumentName=self.name)
        elif "VARIABLE_FILTERS" in self.cards:
            self.filters = VariableFilterWheel(
                self.path, self.cards['VARIABLE_FILTERS'], InstrumentName=self.name)
        elif "FILTERS" in self.cards:
            self.filters = FilterWheel(self.path, self.cards['FILTERS'], InstrumentName=self.name)

        self.atm_trans = None
        self.atm_model = None
        if "ATMOSPHERIC_TRANS" in self.cards:
            self.atm_trans = self._load("ATMOSPHERIC_TRANS")
        elif "ATMOSPHERIC_MODEL" in self.cards:
            self.atm_model = getattr(atmosphericmodel, self.cards['ATMOSPHERIC_MODEL'])
            

    def _load(self, key):
        """ Load component of the instrument

        Parameters:
        -----------
        key: string
             The name of the component in the card file
        Return:
        -------
        A Transmission with the transmission of the component (or 1 if the
        component is not found in the card file)
        """
        trans = Transmission(1.)
        if key in self.cards:
            try:
                trans = Transmission(float(self.cards[key]))
            except ValueError:
                tr = []
                for path in self.cards[key].split():
                    data = read_transmission_files(op.join(self.path, path))
                    tr.append(Transmission(data[:, 0], data[:, 1]))
                trans = reduce(lambda x, y: x*y, tr)
        return trans

    def get_transmission(self, band, **keys):
        """ Return the instrument transmission in photons per photons
        as a Transmission (derived from Func1D) instance

        It should be in the interval [0., 1.]
        
        This accounts for:
            the filter transmission : accessible via self.filters(band, focal_plane_position)
            the mirror reflectivity : in self. mirror_reflectivity
            the optic transmission  : in self.optics_transmission

        Parameters:
        -----------
        band: string
              The name of the photometric band 

        focal_plane_position: parameter to be passed to filterwheel.
        """
# deprecated        
#        if band == 'open':
#            return self.open_transmission
#        else:
#            return (self.filters(band, focal_plane_position) *
#                    self.open_transmission)
        return self.filters(band, **keys) * self.mirror_reflectivity * self.optics_transmission

    def get_efficiency(self, band, unit="e-", **keys):
        """
        Returns the instrument efficiency in e- per photons.
        
        This accounts for 
            the instrument transmission: provided by get_transmission (includes filter transmission, mirror reflectivity and optics transmission)
            the quantum efficiency : in self.qe
            the mirror area : in self.area        
         
        if unit="e-", the default that's all.
        if unit="ADU", it also includes the gain
        """

        instrument_transmission = self.get_transmission(band, **keys)
        electron_efficiency = instrument_transmission * self.ccd_qe * self.area
        
        if unit == "e-":
            return electron_efficiency
        elif unit == "ADU":
            return electron_efficiency * (1./self.gain)
        else:
            print(("unit %s not implemented" % (unit)))
            raise NotImplementedError
 
    def get_efficiency_at_airmass(self, band, airmass=1.25, reference_airmass=1.25, **keys):
        """
        Calculates the instrument efficiency in e- per photons, in cluding the atmospheric transmission

        This needs the instrument description to provide an atmospheric effective transmission curve.
        """
        
        efficiency = self.get_efficiency(band, **keys)
        if self.atm_trans is not None:
            return efficiency * self.atm_trans ** (airmass / reference_airmass)
        elif self.atm_model is not None:
            return efficiency * self.atm_model(airmass=airmass)
        else:
            warn(Warning("Instrument has no separate atmospheric transmission curve"))
            return efficiency
        
    def EffectiveFilterByBand(self, band, **keys):
        """
        For easy comparison with snfit: returns the effective transmission (i.e. efficiency) in ADUs 
        of a given filter.

        This is snfit idiosyncratic, and therefore also includes airmass at
        airmass 1.25 when available, as well as the gain.
        """        

        return  self.get_efficiency_at_airmass(band, unit="ADU", **keys)



if __name__ == "__main__":
    #- Implements few tests that I feel better if I can run from time to time
    '''
    x = Transmission(np.arange(1., 10., 0.1), np.arange(1., 10., 0.1))
    y = Transmission(np.arange(1., 10., 0.1), np.arange(1., 10., 0.1)+10.)    
    
    print "x(4.) + 1.    = %f     (should be 5.)" % ((x + 1.)(4.))
    print "1.    + x(4.) = %f     (should be 5.)" % ((1. + x)(4.))

    print "x(4.) - 1.    = %f     (should be 3.)" % ((x - 1.)(4.))
    print "1.    - x(4.) = %f     (shoudld be -3.)" % ((1. - x)(4.))


    print "x(4.) * 2.    = %f     (should be 8.)" % ((x * 2.)(4.))
    print "2.    * x(4.) = %f     (should be 8.)" % ((2. * x)(4.))
    
    print "x(4.) ** 2.    = %f     (should be 16.)" % ((x ** 2.)(4.))
    print "2.    ** x(4.) = %f     (should be 16.)" % ((2. ** x)(4.))

    print "(x + y)(2.)    = %f     (should be 14.)" % ((x + y)(2.))
    print "(y + x)(2.)    = %f     (should be 14.)" % ((y + x)(2.))
    print "(x * y)(2.)    = %f     (should be 24.)" % ((x * y)(2.))
    print "(y * x)(2.)    = %f     (should be 24.)" % ((y * x)(2.))
    print "(x ** y)(2.)   = %f     (should be 4096.)" % ((x ** y)(2.))
    print "(y ** x)(2.)   = %f     (should be 144.)" % ((y ** x)(2.))    
    '''
    instrument = InstrumentModel('MEGACAM6')
    
