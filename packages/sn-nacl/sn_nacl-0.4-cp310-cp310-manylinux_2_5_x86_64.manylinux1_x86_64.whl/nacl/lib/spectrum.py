""" Implements a simple Spectrum class where: spec.x is the wavelength spec.y is
the flux spec.v is the variance

plus some methods deemed useful for SNe Ia (dereddening, deredshifting,
etc). Those methods are first implemented as functions working on arrays at the
namespace level so that they could be used more generally. They are then wrapped
into Spectrum class methods.

Also contains at the namespace level functions to read and create Spectrum
instances from files.

Note that for now, the only accepted file interface is the snfit ntuple format


Depends on croaks """


from . import interpolation, robuststat, constants
from ..util import saltpath, io

# temporary change, until pyfits is discontinued
try:
    import astropy.io.fits as pyfits
except:
    import pyfits
import numpy as np
import scipy
import scipy.signal
import copy
import pdb
import re
import sys
import os
import os.path as op
import glob
import math

def load_snf_std_fits(filename, verbose = False):
    """ Reads SNfactory reference
    spectra in fits format, as found in
    CVS_SNf/Tasks/Calibration/Reftables/Refflux/fits

    implementation stolen from
    CVS_SNf/Tasks/Calibration/Reftables/Refflux/tools/plot_refflux.py """

    t = pyfits.open(filename)
    tbdata = t[1].data
    
    # Get lambda and select proper range
    if 'WAVELENGTH' in t[1].columns.names:
        lbdaCol = 'WAVELENGTH'
    else:
        lbdaCol = 'LAMBDA'
    lbda = tbdata.field(lbdaCol).copy()
    lbdaUnits = t[1].columns.units[t[1].columns.names.index(lbdaCol) ]

    if verbose:
        print(" Wavelength from %s column: %.2f,%.2f '%s'" %  (lbdaCol, lbda[0], lbda[-1], lbdaUnits))
    
    flux = tbdata.field('FLUX').copy()
    fluxUnits = t[1].columns.units[t[1].columns.names.index('FLUX') ]
    if verbose:
        print(" Flux from FLUX column in '%s'" % fluxUnits)

    t.close()

    return Spectrum(lbda, flux)
    

def load_snf_fits(filename):
    """ Reads a spectrum object from an SNf fits file.
    Puts all the header information in a dictionnary s.keys

    Note that it should also work for all fits spectra, but in that case we
    can't be sure that the second extension is actually the variance.

    If no second extension is found, it doesn't crash, it simply doesn't read
    it.  """
    spec_fits = pyfits.open(filename)

    #- read the fits data +
    name = spec_fits[0].header.get('FILENAME')
    npts = spec_fits[0].header['NAXIS1']
    step = (spec_fits[0].header['CDELT1'])
    start = (spec_fits[0].header['CRVAL1'] - (spec_fits[0].header.get('CRPIX1', 1) -1) * step)
    end = start + (npts - 1) * step
    x = np.linspace(start, end,npts)
    y = spec_fits[0].data.astype('d')

    #- reads the variance, assumed to be
    #in the second fits hdu
    if len(spec_fits) == 2:
        v = spec_fits[1].data.astype('d')
    else: v = None

    s = Spectrum(x, y, v=v)
    s.keys = {}
    for key, value in spec_fits[0].header.items():
        s.keys[key] = value
        
    return s


def load_ntuple(filename, wavelength_key="WAVE", flux_key="FLUX", error_key="ERR"):
    """ Reads a spectrum from an snfit ntuple format file
    Keywords are: WAVE FLUX ERR VALID

    Note that the keys of the ntuple are propagates in s.keys for convenience
    """
    nt_s = io.NTuple.fromtxt(filename)

    if error_key in nt_s.dtype.names:
        s = Spectrum(nt_s[wavelength_key], nt_s[flux_key], v=nt_s[error_key] ** 2)
    else:
        s = Spectrum(nt_s[wavelength_key], nt_s[flux_key])
        
    s.keys = nt_s.keys

    return s


def read_ascii(filename):
    """
    Read ascii files and returns a list of lines.
    Empty lines and lines beginning with # are not returned.
    All comments starting with # in a line are dropped.
    All lines are stripped.
    """
    fh = open(filename, "r")
    line_list = []
    for line in fh.readlines():
        line = (re.sub("#.*$", "", line)).strip()        
        if len(line) == 0:
            continue
        line_list.append(line)
    return line_list


def load_ascii(filename):
    """
    Useful to read a reference spectrum, as pointed at by
    MagSys

    Reads a spectrum object from an ascii file, assuming the format:
    wavelength   flux   variance
    
    Variance being optional, and # delimitating comments.
    Empty lines ignored

    Since I am not sure if the third column is really variance, I skip it
    And since there can be more than 3 columns I just keep the 2 first ones
    """

    l_line = read_ascii(filename)

    x = []
    y = []
#    if len(l_line[0].split()) == 3:
#        v = []
#        for line in l_line:
#            w, f, variance = line.split()
#            x.append(float(w))
#            y.append(float(f))
#            v.append(float(variance))
#        return Spectrum(np.array(x), np.array(y), v=np.array(v))
#    else:
#        for line in l_line:
#            w, f = line.split()
#            x.append(float(w))
#            y.append(float(f))
#        return Spectrum(np.array(x), np.array(y))
    for line in l_line:
        if line[0] in ['@', '#']:
            continue
        line = line.split()
        x.append(float(line[0]))
        y.append(float(line[1]))
    return Spectrum(np.array(x), np.array(y))


def load_sn_template(phase, filename="snflux_1a_hsiao.dat"):
    """
    Reads a spectrum object from an ascii file, assuming the format:
    date  wavelength   flux
    
    It will return the spectrum corresponding to the phase asked for. If the phase doesn't exist, it will crash.


    If filename is a path, it will use the path. If is it just a basename
    it will look for it in 
    saltpath.sn_templates

    By default loads Hsiao template
    """
    if len(os.path.dirname(filename)) == 0:
        filename = os.path.join(saltpath.sn_template_path, filename)
        
    x = []
    y = []    
    for line in read_ascii(filename):
        p, w, f = line.split()
        if float(p) == phase:
            x.append(float(w))
            y.append(float(f))
    
    return Spectrum(np.array(x), np.array(y))


def load_galaxy_template(galaxy_type="S0", age=None, path=saltpath.galaxy_template_path, no_clip=False):
        """
        galaxy_type is 
           E
           S0
           Sa
           Sb
           Sc

        Age is from 2gy to 20gy by integer increments
        If age is provided will load a Pegase galaxy, otherwise will load a
        Kinney (check spelling) galaxy

        If no path towards the template directory given, will assume that they
        live in $SALTPATH/galaxy_templates/
        
        If no_clip is True returns the full template, otherwise clips it between
        2000 and 10000 AA
        """

        if age is None:
            filename = "galaxy_template_%s.dat" % (galaxy_type)
        else:
            filename = "gal_peg_%s_%s.dat" % (galaxy_type, age)

        s = load_ascii(os.path.join(path, filename))
        if not no_clip:
            s = s.clip(w_min=2000., w_max=10000.)
        return Spectrum(s.x, s.y)


def load_pickles(name=None, path=saltpath.stellar_libs_path, no_clip=False):
    """
    Load the Pickles library and return a dictionary of all the
    spectra, indexed by the stellar type names.
    
    We work directly from the original ASCII files, obtained from CDS.
    We read only the first two columns, which correspond to characters
    1-7 and 9-17 resp.
    
    Wavelengths are in Angstroems. 
    Fluxes are in [Energy/s/A/cm^2], normalized as: f(lambda)/f(5556 A)
    
    The third column (standard deviation, when several spectra are
    combined in ignored, as are all subsequent columns).
    
    """
    ret = []
    path = op.join(saltpath.stellar_libs_path, 'pickles')
    if name is not None:
        filenames = ['%s.dat' % name]
    else:
        filenames = glob.glob(op.join(path, '*.dat'))
    for fn in filenames:
        f = open(fn)
        wl, flx = [], []
        for l in f:
            wl.append(float(l[0:7]))
            flx.append(float(l[8:17]))
        s = Spectrum(np.array(wl), np.array(flx))
        stellar_type_name = op.basename(fn).split('.dat')[0]
        s.keys['name'] = stellar_type_name
        ret.append(s)
        f.close()
    return ret


#- All the variance stuff will go in Variance_Spectrum
#- with its own factories, interpolators etc.
class Spectrum:
    def __init__(self, x, y, v=None, keys={}):
        """
        This is a very simple spectrum class, without safeguards of any kinds.
        
        self.x is the wavelength, assumed to be in AA
        self.y is the flux, assumed to be in ergs per sec per AA per cm^2
        self.v is the variance corresponding to self.x. Can be None.

        self.flux() is a interpolation Func1D that interpolates the flux
        self.photon() is a interpolation Func1D that interpolates the number
        of photons

        self.keys is a place holder for the keys of a spectrum nacl.util.io ntuple.
        It is initialized to None.

        WARNING: almost no method propagates the variance for now
        """

        self.x = x
        self.y = y
        self.v = v
        self.keys = keys

        #- The names here don't matter, they are lost in creating the Func1D
        self.flux = interpolation.Func1D(x, y)
        
        self.photon = interpolation.Func1D(x, flambda_to_fclambda(x, y))
        self.p = self.photon(self.x)

    
    def totxt(self, filename=None, comment=None, light=False, extra_light=False, wavelength_scale=1.):
        """
        Prints the spectrum to a file in NTuple format.
        If no filename is provided, prints to stdout.
        
        light: only prints wavelength flux and variance
        extra_light: only prints wavelength and flux

        wavelength_scale : multiplicator to wavelength, for example to get from AA to nm

        In order to comply with SALT2 idiosyncrasies, the keywords are:
        Keywords are:
        WAVE
        FLUX
        ERR
        VALID
        """
        
        if filename is None:
            fh = sys.stdout
        else:
            fh = open(filename, "w")

        if extra_light:
            light = True
            
        if light:
            if self.v is None or extra_light:
                for wave, flux in zip(self.x * wavelength_scale, self.y):
                    print("%-f    %-e" % (wave, flux), file=fh)
                return
            else:
                for wave, flux, v in zip(self.x * wavelength_scale, self.y, self.v):
                    print("%-f    %-e    %-e" % (wave, flux, v), file=fh)
                return


        if comment is not None:
            print("@generation_comment: %s" % (comment), file=fh)
        
        for key, value in self.keys.items():
            print("@%s : %s" % (key, str(value)), file=fh)
        
        if self.v is None:
            print("#WAVE:", file=fh)
            print("#FLUX:", file=fh)
            print("#VALID:", file=fh)
            print("#end", file=fh)
            
            for wave, flux in zip(self.x * wavelength_scale, self.y):
                print("%-f    %-e    1" % (wave, flux), file=fh)

        else:
            print("#WAVE:", file=fh)
            print("#FLUX:", file=fh)
            print("#ERR:", file=fh)
            print("#VALID:", file=fh)
            print("#end", file=fh)

            for wave, flux, variance in zip(self.x * wavelength_scale, self.y, self.v):
                err = np.sqrt(variance)
                print("%-f    %-e    %-e    1" % (wave, flux, err), file=fh)

    def clip(self, w_min=None, w_max=None):
        """
        returns a clipped spectrum with wavelength between the two bounds
        given in options.
        
        """
        
        if w_min is None:
            w_min = np.min(self.x)
        if w_max is None:
            w_max = np.max(self.x)

        i_ok = (self.x < w_max) & (self.x > w_min)
        if self.v is not None:
            v = self.v[i_ok]
        else:
            v = None
        return Spectrum(self.x[i_ok], self.y[i_ok], v=v, keys=self.keys)

    def noise_up(self, S_to_N = 10):
        """
        Returns a spectrum noised up to a S/N of S_to_N w.r.t the
        initial spectrum.
        This does *not* take into account the original noise of the spectrum.

        WARNING: assumes that the spectrum is flux calibrated
        """
        y_photon = flambda_to_fclambda(self.x, self.y)
        if S_to_N <= 0.:
            y_noise = y_photon
            v = copy.copy(self.v)
        else:
            mean_y_photon = np.mean(y_photon)
            y_noise = y_photon/mean_y_photon * S_to_N**2
            v = copy.copy(y_noise)
    
            y_noise = scipy.random.poisson(v)
    
            y_noise = y_noise *  mean_y_photon / S_to_N**2
            v = v * (mean_y_photon / S_to_N**2)**2
    
        y_noise = fclambda_to_flambda(self.x, y_noise)
        #- Twice for the variance
        v = fclambda_to_flambda(self.x, v)
        v = fclambda_to_flambda(self.x, v)
    
        return Spectrum(self.x, y_noise, v=v, keys=self.keys)



    def rescale_to_mag(self, mag_target, instrument="SWOPE", magsys="VEGA", current_filter="g"):
        """
        Returns a spectrum rescaled in ergs/cm^s/s/AA so that its magnitude in
        band [band] is equal to mag_target

        instrument and  magsys  can be either strings (and the saunerie
        equivalents will be loaded) or directly the saunerie equivalents.

        if current_filter is a Transmission instance, no need to provide
        instrument
        """

        if type(instrument) == str:
            instrument = instruments.InstrumentModel(instrument)
        if type(magsys) == str:
            magsys = instruments.MagSys(magsys)
        if type(current_filter) == str:
            current_filter = instrument.EffectiveFilterByBand(current_filter)


        mag_orig = magsys.mag(current_filter, self)[0][0]
        alpha = 10 ** (0.4 * (mag_orig - mag_target))
        return  spectrum.Spectrum(self.x, self.y * alpha, v=self.v, keys=self.keys)

    
                
    def deredden(self, ebmv=0., Rv=3.1):
        """
        deredden implementation as Spectrum method
        """        

        if self.v is not None:
            new_y, ccm_factor = deredden(self.x, self.y, ebmv=ebmv, Rv=Rv, return_ccm_factor=True)
            new_v = self.v * ccm_factor ** 2
            return Spectrum(self.x, new_y, v=new_v, keys=self.keys)
        else:
            new_y = deredden(self.x, self.y, ebmv=ebmv, Rv=Rv)
            return Spectrum(self.x, new_y, keys=self.keys)

    def redden(self, ebmv=0., Rv=3.1):
        """
        deredden implementation as Spectrum method

        Doesn't do anything to the variance
        """

        new_y = redden(self.x, self.y, ebmv=ebmv, Rv=Rv)
        return Spectrum(self.x, new_y, v=new_v, keys=self.keys)

    def rebin_simple(self, n):
        """
        Rebins the spectrum by averaging over n pixels.

        Also rebins the variance in the same way
        """
        if n <= 1:
            return Spectrum(self.x, self.y, v=self.v, keys=self.keys)
        
        x, y = rebin_simple(self.x, self.y, n)
        if self.v is not None:
            x, v = rebin_simple(self.x, self.v, n)
        else:
            v = None
        return Spectrum(x, y, v=v,  keys=self.keys)

    def SG_filter(self, n_bin, degree=3):
        """
        Uses the Savitzky_Golay implementation here to return a smoothed spectrum

        FIXME: need to implement the correct handling of variance
        """
        sg = Savitzky_Golay(n_bin, pol_degree=degree)

        if self.v is not None:
            print("WARNING: for now SG_filter drops the variance")
        
        return Spectrum(self.x, sg(self.y), keys=self.keys)

    def median_filter(self, kernel_size=30):
        """
        Uses scipy.signal.medfilter to median filter the spectrum
        """
        if self.v is not None:
            print("WARNING: for now  drops the variance")
        
        return Spectrum(self.x, scipy.signal.medfilt(self.y, kernel_size=kernel_size), keys=self.keys)        

    def slide_win(self,width=5, func=np.mean):
        """
        Applies np.mean on a sliding window of width 5 by default.
        func provides a differenc function to apply
        width changes the width on which the function is applied
        """
        if self.v is not None:
            print("Warning: for now slide_win drops the variance")

        return Spectrum(self.x, robuststat.slide_win(self.y, func=func, width=width), keys=self.keys)
            
    
    def deredshift_wavelength(self, z=0.):
        """
        Deredshifts only the wavelength axis (no change on flux)
        If z < 0 applies a blueshift
        """
        #- doppler_shift applies the redshift, therefore deredshifting has to go the other direction
        #- Thus the - sign
        new_x = doppler_shift(self.x, z=-z)
        return Spectrum(new_x, self.y, v=self.v, keys=self.keys)

    def redshift_wavelength(self, z=0.):
        """
        Deredshifts only the wavelength axis (no change on flux)
        If z < 0 applies a blueshift
        """
        #- doppler_shift applies the redshift, therefore deredshifting has to go the other direction
        #- Thus the - sign
        new_x = doppler_shift(self.x, z=z)
        return Spectrum(new_x, self.y, v=self.v, keys=self.keys)

    def to_rest_frame(self, z_helio=None, z_cmb=None, idr_restframe_scale=False):
        """
        Deredshifts the wavelength axis by z_cmb (or z_helio if z_cmb is not provided)
        and does *not* blueshift it back to z_ref, unless idr_restframe_scale is set to True
        
        """

        new_x = wavelength_to_rest_frame(self.x, z_helio=z_helio, z_cmb=z_cmb)
        new_y = flux_to_rest_frame(self.y, z_helio=z_helio, z_cmb=z_cmb, idr_restframe_scale=idr_restframe_scale)
            
        return Spectrum(new_x, new_y, v=self.v, keys=self.keys)

    def to_observer_frame(self, z_helio=None, z_cmb=None, idr_restframe_scale=False):
        """
        Redshifts the wavelength and the flux by z_cmb and z_helio.
        If only one is given, only uses it.        
        """
        new_x = wavelength_to_observer_frame(self.x, z_helio=z_helio, z_cmb=z_cmb)
        new_y = flux_to_observer_frame(self.y, z_helio=z_helio, z_cmb=z_cmb, idr_restframe_scale=idr_restframe_scale)

        return Spectrum(new_x, new_y, v=self.v, keys=self.keys)

    
    #- snfit IntegFlux considers the SN spectrum to be restframe but the filter to be
    #- observer frame. The z provided is meant to redshift the SN to there.
    #- If I have a SN spectrum observer frame, providing z=0 will yield 
    #- the observer frame magnitude of the SN at z.
    #-    number of photons = energy/(h*nu) = energy * wl/(2*pi*hbar*c)
    #-    2*pi* hbar*c = 2* pi * 197 eV nm = 6.28*197 * 1.60e-12 * 10 ergs angst
    #-    = 1.97946e-08
    #-    = 1/5.006909561e07
    def IntegFlux(self, effective_filter, z=0., wavelength_integration_step=5):
        """
        effective_filter is the filter transmission provided as Filter instance (defined in instruments.py derives from Func1D)
    
        This integration function follows snfit conventions:
    
        The spectrum flux is assumed to be in energy, i.e. in ergs/s/cm^2
    
        The filter transmission is assumed to be in pseudo_ADU/photon
    
        The redshift is the redshift between the observer frame and the spectrum
        frame. If the spectrum is observer frame then z=0 means an observer frame integral. 
    
        If the spectrum is restframe, z=0 means that restframe and observer frame are the 
        same. 
    
        The case z !=0 needs special attention. The spectrum is redshifted to redshift z
        and the filters remain in observer frame. The filters are thus blueshifted w.r.t 
        the spectrum. It is the typical case of observing a supernova at redshift z in 
        an observer frame filter F knowing its restframe spectrum S.
        A special warning: the spectrum is only redshifted as far as wavelength is concerned.
        The flux dillution due to the luminosity distance of the supernova is 
        NOT taken into account.
    
        wavelength_integration_step is kept as an option for convenience.
        To follow snfit it can be set looking for WAVELENGTH_INTEGRATION_STEP  
        in fitmodel.card
        snfit default, as this function default is an integration step of 5 AA.
    
    
        Note that in ALL CASES the spectrum wavelength axis and the filter wavelength
        axis are in the SAME FRAME.
        """
        
        spectrum_shifted = self.redshift_wavelength(z=z)
        
        nphot_l = spectrum_shifted.photon * effective_filter
        
        # Calculation of  the number of integration steps:
        n_steps = int((effective_filter.x_max - effective_filter.x_min) / wavelength_integration_step)
        
        # the wavelength integration step size is taken into account 
        # by Func1D integrator. 
        n_photon = nphot_l.integrate(effective_filter.x_min, effective_filter.x_max, n_steps)

        # This is to account for the flux dilution in a delta_lambda step, and to account for the fact
        # that snfit IntegFlux returns the flux in the blueshifted filter, not in restframe filters.
        n_photon /= (1. + z)**2
        
        # NB: hc for snfit and for saunerie are slightly different:    
        n_photon *= 5.006909561e7 * (constants.CLIGHT_A_s * constants.H_e_s)
        return n_photon

    
            
        

    
    
#- Spectrum manipulation, implemented as array operations    
def rebin_simple(x, y, n):
    """ Bins up the spectrum by averaging the values of every n
    pixels.

    """
    remain = len(x) % n
    if remain > 0:
        x = x[:-remain].reshape(-1, n)
        y = y[:-remain].reshape(-1, n)
    else:
        x = x.reshape(-1, n)
        y = y.reshape(-1, n)

    n = float(n)
    x = np.nansum(x, axis=1) / n
    y = np.nansum(y, axis=1) / n
    
    return x, y


def deredden(x, y, ebmv=0., Rv=3.1, return_ccm_factor=False):
    """
    Deredden flux (y) using Cardelli,Clayton,Mathis law 
    
    x is the wavelength
    y is the flux

    ebmv is E(B-V)
    Rv is Rv, default value is 3.1

    """    
    ccm_factor = 1. / ccm(x, ebmv, Rv=Rv) 
    y_tmp = y * ccm_factor
    if return_ccm_factor:
        return y_tmp, ccm_factor
    else:
        return y_tmp
    


def redden(x, y, ebmv=0., Rv=3.1):
    """
    Redden flux (y) using Cardelli,Clayton,Mathis law 
    
    x is the wavelength
    y is the flux
    ebmv is E(B-V)
    Rv is Rv, default value is 3.1

    """    
    #- Only difference with deredden is ccm_factor == ccm instead of 1./ccm
    ccm_factor = ccm(x, ebmv, Rv=Rv) 
    y_tmp = y * ccm_factor
    return y_tmp


def doppler_shift(x, z=0.):
    """
    Shifts a wavelength array by 
       * (1.+z) if  z > 0.
       / (1.-z) if z < 0.
    """
    if (z == 0.) or (z is None):
        return x
    if z > 0.:
        return x * (1.0 + z)
    if z < 0.:
        return x / (1.0 - z)

    
def wavelength_to_rest_frame(x, z_helio=None, z_cmb=None):
    """
    Deredshifts the wavelengths using z_cmb is it is provided, z_helio otherwise.
    If both are none, returns the wavelength unchanged.
    This is supposed to be used together with flux_to_rest_frame
    """
    if z_cmb is None:
        if z_helio is not None:
            new_x = doppler_shift(x, - z_helio)
        else:
            new_x = x
    else:
        new_x = doppler_shift(x, - z_cmb)

    return new_x


def flux_to_rest_frame(y, z_helio=None, z_cmb=None, idr_restframe_scale=False):
    """
    Deredshifts the flux accounting for the luminosity distance dillution as calculated in
    luminosity_distance

    If only one of z_helio or z_cmb are provided, both are assumed to be the same
    The restframe is considered to be at 10pc, where 
    absolute magnitudes are defined.
    """
    if (z_helio is None) and (z_cmb is None):
        return y
    if z_helio is not None:
        if z_cmb is None:
            z_cmb = z_helio

    if z_cmb is not None:
        if z_helio is None:
            z_helio = z_cmb

    #- Reference redshift is restframe at 10pc
    if idr_restframe_scale:
        z_ref = 0.05    
        d_r = luminosity_distance(z_helio=z_ref, z_cmb=z_ref)
        factor = 1.e15
    else:
        z_ref = 0.    
        #- 10 pc = 10.e-6 Mpc
        d_r = 10.e-6  
        factor = 1.

    #- Luminosity distance
    d_z = luminosity_distance(z_helio=z_helio, z_cmb=z_cmb)

    factor *= (1.0 + z_helio) / (1.0 + z_ref) * d_z * d_z / (d_r * d_r)
    new_y = y * factor

    return new_y


def wavelength_to_observer_frame(x, z_helio=None, z_cmb=None):
    """
    Redshifts the wavelengths using z_cmb is it is provided, z_helio otherwise.
    If both are none, returns the wavelength unchanged.
    This is supposed to be used together with flux_to_rest_frame
    """
    if z_cmb is None:
        if z_helio is not None:
            new_x = doppler_shift(x, z_helio)
        else:
            new_x = x
    else:
        new_x = doppler_shift(x, z_cmb)

    return new_x


def flux_to_observer_frame(y, z_helio=None, z_cmb=None, idr_restframe_scale=False):
    """
    Redshifts the flux accounting for the luminosity distance dillution as calculated in
    luminosity_distance.
    It assumes that the SN flux was given for a supernova at z_ref. 
    By default, it assumes that the original flux is given at 10pc

    If only one of z_helio or z_cmb are provided, both are assumed to be the same
    If no z_ref is provided, the restframe will be considered to be at 10pc, where 
    absolute magnitudes are defined.
    """

    if (z_helio is None) and (z_cmb is None):
        return y

    if z_helio is not None:
        if z_cmb is None:
            z_cmb = z_helio

    if z_cmb is not None:
        if z_helio is None:
            z_helio = z_cmb

    #- Reference redshift is restframe at 10pc
    #- Reference redshift is restframe at 10pc
    if idr_restframe_scale:
        z_ref = 0.05    
        d_r = luminosity_distance(z_helio=z_ref, z_cmb=z_ref)
        factor = 1.e15
    else:
        z_ref = 0.   
        #- 10 pc = 10.e-6 Mpc 
        d_r = 10.e-6 
        factor = 1

    #- Luminosity distance
    d_z = luminosity_distance(z_helio=z_helio, z_cmb=z_cmb)

    factor *= (1.0 + z_helio) / (1.0 + z_ref) * d_z * d_z / (d_r * d_r)

    new_y = y / factor
    return new_y
    
#--- Tools
def locate(w, w_min=None, w_max=None, method="range"):
    """
    Finds index for which w is between w_min and w_max.
    If either w_min or w_max are None, they are taken as the extremes of the array.

    If method is "range" returns all the indexes.
    If method is min, max or mean, returns respectively the min, the max or the median
    of all the indexes
    """
    if w_min is None:
        w_min = min(w)
    if w_max is None:
        w_max = max(w)

    i_ok = np.where((w < w_max) & (w >w_min))
    i_ok = i_ok[0]
    
    if method == "min":
        return np.min(i_ok)
    elif method == "max":
        return np.max(i_ok)
    elif method == "median":
        return int(np.median(i_ok))
    elif method == "range":
        return i_ok
    else:
        return list(range(len(w) - 1))
        print("Method not implemented, returning the full range")

#- Astronomy

#- unit transformation
CLIGHT_A_s = 2.99792458e18         # [A/s]
CLIGHT_m_s = 2.99792458e8         # [A/s]
CLIGHT_km_s = 2.99792458e5         # [A/s]
HPLANCK = 6.62606896e-27        # [erg s]


def lambda_to_nu(x):
    """
    Transforms wavelength in AA in Hertz
    """    
    return CLIGHT_A_s / x


def nu_to_lambda(x):
    """
    Transforms Hertz in AA 
    """
    return CLIGHT_A_s / x


def flambda_to_fclambda(x, y):
    """
    Transforms a flux in erg/s/cm^2/AA in flux in photons/s/cm^2
    x in AA

    n_l*d_l = f_l*d_l / (h*nu)
    n_l*d_l = f_l*d_l * l/h*c
    """    
    return y * x / (CLIGHT_A_s * HPLANCK)


def fclambda_to_flambda(x, y):
    """
    Transforms a flux in erg/s/cm^2/AA in flux in erg/s/cm^2/photons
    x in AA

    n_l*d_l = f_l*d_l * l/(h*c)
    f_l*dl = h*c/l * n_l*d_l
    """
    
    return y * CLIGHT_A_s * HPLANCK / x


def fnu_to_flambda(frequency, flux):
    """
    Returns flambda that corresponds to nu_to_lambda(frequency) wavelength array
    
    f_l = f_nu c/lambda^2
    """
    
    wavelength = nu_to_lambda(frequency)
    return flux * CLIGHT_A_s / wavelength ** 2
    

#- Flux to magnitude:
def magnitude(fx, dfx, m0=48.59, zp=0.):
    """
    Calculates a magnitude from a flux and its error
    """
    if fx <= 0 or np.isnan(fx):  # Nothing we can do about negative flux!
        return np.nan, np.nan
    else:
        m = -2.5 * np.log10(fx) + zp - m0

    if dfx > 0:
        dm = 2.5 / np.log(10) / fx * dfx
    else:
        dm = 0

    return m, dm



#- CCM reddening law 
#- Stolen from Prospect/Util.py and updated from O'Donnell
def ccm(wavelength, ebmv, Rv=3.1):
    """
    Given a wavelength in angstroms, calculate the
    extinction A(w) according to the CCM model.
    c.f. Cardelli, Clayton, Mathis 1989: ApJ 345:245
    with optical/NIR part updated from
    O'Donnell (1994ApJ...422..158O).

    :Parameters:
        `wavelength` : np.array
            Array of wavelength values at which you which to
            find warp values
         `ebmv` : float
         `Rv` : float, default is 3.1


    :return: np.array
    """
    # change variables from angstroms to microns
    ang_to_micron = 1.0e-4
    # cardelli's parameter x = 1/(wavelength in microns)
    x = 1.0 / (wavelength * ang_to_micron)

    # version to deal with arrays
    ex1 = (x < 1.1) * __ccm_ir(x, Rv)
#    ex2 = (1.1 <= x  ) * (x < 3.3) * __ccm_optical(x, Rv)
    ex2 = (1.1 <= x) * (x < 3.3) * __odonnell_optical(x, Rv)
    ex3 = (3.3 <= x) * (x < 8.0) * __ccm_uv1(x, Rv)
    ex4 = (x >= 8.0) * __ccm_uv2(x, Rv)
    extinction = ex1 + ex2 + ex3 + ex4

    # get flux multiplicative factor from the extinction
    return 10.0 ** (-0.4 * extinction * ebmv)


def __ccm_ir(x, rv):
    # for x < 1.1
    a0 = 0.574
    b0 = -0.527
    c0 = rv * a0 + b0
    return c0 * (x ** 1.61)


def __ccm_optical(x, rv):
    # for 1.1 < x < 3.3
    y = x - 1.82
    # a coeffs
    a0 = 1.0
    a1 = 0.17699
    a2 = -0.50447
    a3 = -0.02427
    a4 = 0.72085
    a5 = 0.01979
    a6 = -0.77530
    a7 = 0.32999
    # b coeffs
    b0 = 0.0
    b1 = 1.41338
    b2 = 2.28305
    b3 = 1.07233
    b4 = -5.38434
    b5 = -0.62251
    b6 = 5.30260
    b7 = -2.09002
    # total coeffs
    c0 = rv * a0 + b0
    c1 = rv * a1 + b1
    c2 = rv * a2 + b2
    c3 = rv * a3 + b3
    c4 = rv * a4 + b4
    c5 = rv * a5 + b5
    c6 = rv * a6 + b6
    c7 = rv * a7 + b7
    # finally result
    return (c0
             + c1 * y
             + c2 * (y ** 2)
             + c3 * (y ** 3)
             + c4 * (y ** 4)
             + c5 * (y ** 5)
             + c6 * (y ** 6)
             + c7 * (y ** 7))


def __odonnell_optical(x, rv):
    """A/Av in Optical/Near IR: 1.1-3.3 micron^-1"""
    y = x - 1.82
    pa = [-0.505, +1.647, -0.827, -1.718, +1.137, +0.701, -0.609, +0.104, 1]
    pb = [+3.347, -10.805, +5.491, +11.102, -7.985, -3.989, +2.908, +1.952, 0]
    a = np.polyval(pa, y)
    b = np.polyval(pb, y)
    return a * rv + b


def __ccm_uv1(x, rv):
    # for 3.3 < x < 8.0
    y = x - 5.90
    fa = (x >= 5.90) * (-0.04473 * (y ** 2) - 0.009779 * (y ** 3))
    fb = (x >= 5.90) * (0.21300 * (y ** 2) + 0.120700 * (y ** 3))
    aa = 1.752 - 0.316 * x - 0.104 / ((x - 4.67) ** 2 + 0.341) + fa
    bb = -3.09 + 1.825 * x + 1.206 / ((x - 4.62) ** 2 + 0.263) + fb
    return rv * aa + bb


def __ccm_uv2(x, rv):
    # for x>8.0
    y = x - 8.0
    # a coeffs
    a0 = -1.073
    a1 = -0.628
    a2 = 0.137
    a3 = -0.070
    # b coeffs
    b0 = 13.670
    b1 = 4.257
    b2 = -0.420
    b3 = 0.374
    # total coeffs
    c0 = rv * a0 + b0
    c1 = rv * a1 + b1
    c2 = rv * a2 + b2
    c3 = rv * a3 + b3
    return (c0
             + c1 * y
             + c2 * (y ** 2)
             + c3 * (y ** 3))


#- Luminosity distance
def luminosity_distance(z_helio, z_cmb, hubble=70.0, omega_m=0.28):
    """
    Returns luminosity distance using equation (16) of Kantowski
    & Thomas (2001), ApJ, 561, 491 with the CMB redshift used in the
    integral but heliocentric redshift used everywhere else.

    Luminosity distance returned in Mpc
    """
    import math

    hubble = 70.0
    omega_m = 0.28
    sol = 299792.458
    front = 2.0 * (1.0 + z_helio) * sol / hubble / math.pow(omega_m, 1.0 / 3.0)  # note z_helio here
    a = 1.0 / 6.0
    b = 2.0 / 3.0
    c = 7.0 / 6.0
    omom = 1.0 - omega_m
    arg = 1.0 + omega_m * z_cmb * (3.0 + z_cmb * (3.0 + z_cmb))  # note z_cmb here
    return front * (scipy.special.hyp2f1(a, b, c, omom) - math.pow(arg, - a) * scipy.special.hyp2f1(a, b, c, omom / arg))


#- Stolen from SJB EMPCA:
class Savitzky_Golay(object):
    """
    Utility class for performing Savitzky Golay smoothing
    
    Code adapted from http://public.procoders.net/sg_filter/sg_filter.py
    """
    def __init__(self, width, pol_degree=3, diff_order=0):
        self._width = width
        self._pol_degree = pol_degree
        self._diff_order = diff_order
        self._coeff = self._calc_coeff(width//2, pol_degree, diff_order) 

    def _calc_coeff(self, num_points, pol_degree, diff_order=0):
    
        """
        Calculates filter coefficients for symmetric savitzky-golay filter.
        see: http://www.nrbook.com/a/bookcpdf/c14-8.pdf
    
        num_points   means that 2*num_points+1 values contribute to the
                     smoother.
    
        pol_degree   is degree of fitting polynomial
    
        diff_order   is degree of implicit differentiation.
                     0 means that filter results in smoothing of function
                     1 means that filter results in smoothing the first 
                                                 derivative of function.
                     and so on ...
        """
    
        # setup interpolation matrix
        # ... you might use other interpolation points
        # and maybe other functions than monomials ....
    
        x = np.arange(-num_points, num_points+1, dtype=int)
        monom = lambda x, deg : math.pow(x, deg)
    
        A = np.zeros((2*num_points+1, pol_degree+1), float)
        for i in range(2*num_points+1):
            for j in range(pol_degree+1):
                A[i,j] = monom(x[i], j)
            
        # calculate diff_order-th row of inv(A^T A)
        ATA = np.dot(A.transpose(), A)
        rhs = np.zeros((pol_degree+1,), float)
        rhs[diff_order] = (-1)**diff_order
        wvec = np.linalg.solve(ATA, rhs)
    
        # calculate filter-coefficients
        coeff = np.dot(A, wvec)
    
        return coeff
    
    def __call__(self, signal):
        """
        Applies Savitsky-Golay filtering
        """
        n = np.size(self._coeff-1)/2
        res = np.convolve(signal, self._coeff)
        return res[n:-n]

#- SN template class
class SnTemplate(object):
    @classmethod
    def load_ascii(self, filename, names=["phase", "wavelength", "flux"], **keyargs):
        """
        Uses np.genfromtxt to load

        usecols=(1,3,5) to select which columns to use
        names = ["a", "flux", "wavelength", "b", "phase","d"]
        or
        names = ["flux", "wavelength", "phase"] 

        By default, assumes that phase comes first, then wavelength then flux
        """

        nt = np.genfromtxt(filename, names=names, **keyargs)
        nt = nt.view(io.NTuple)

        return SnTemplate(nt["phase"], nt["wavelength"], nt["flux"])
    
    def __init__(self, phase, wavelength, flux):
        """
        Assumes that the phase is in days
                     wavelength is in AA
                     flux is in energy, and ergs/s/cm^2/AA even. But as long as you don't use the photon conversion, you are probably fine 
        """
        nt = np.rec.fromarrays([phase, wavelength,flux], names=["phase", "wavelength", "flux"])
        self.nt = nt.view(io.NTuple)
        self.dp = croaks.DataProxy(self.nt, p="phase", w="wavelength", f="flux")
        self.dp.make_index("p", intmap=True)

        

    def __call__(self, phase, method="nearest"):
        """
        Returns the Spectrum instance corresponding to the phase selected by the method
        
        nearest: the phase nearest to the phase asked for
        key "SnTemplate.phase" contains the phase
        """

        p_index = croaks.find_closest(self.dp.p_set, phase)
        i_ok = self.dp.p_index == p_index
        
        s = Spectrum(self.dp.w[i_ok], self.dp.f[i_ok])
        s.keys["SnTemplate.phase"] = self.dp.p_set[p_index]

        return s
        
