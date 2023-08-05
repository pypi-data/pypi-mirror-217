#!/usr/bin/env python
"""
Implements functions to describe and analyse atmospheric transmission.

In particular, re-implements the model of Buton et al. 2013, with code stolen from
CVS_SNf/Analysis/AtmosphericExtinction/Scripts/pyExtinction/AtmosphericExtinction.py


The anciliary data is to be found in $SALTPATH/atmospheric_model/

"""

import numpy
# temporary change, until pyfits is discontinued 
try:
    import astropy.io.fits as pyfits
except:
    import pyfits

import copy
    
from . import interpolation
from . import fitparameters
from ..util import saltpath

#- Utility I/O scripts to read atmospheric data parameters from SNf files

def read_snf_atmospheric_model(filename):
    """
    Reads the atmospheric transmission data from a file with FClass 625 and
    XFclass 610 (Non Photometric solution)
    of XFclass 600 (Photometric_transmission)
    """


    f_fits = pyfits.open(filename)
    header = f_fits[1].header

    atmospheric_transmission = atmosphericmodel.Buton_atmosphere(airmass=1.,
                                                                 pressure=header.get("PRESSURE"),
                                                                 ozone_column=header.get("OZ_INT"),
                                                                 aerosol_optical_depth=header.get("AE_TAU"),
                                                                 aerosol_exponent=header.get("AE_ANG"),
                                                                 ozone_template_path=None,
                                                                 keys=f_fits[1].header)

    return atmospheric_transmission


def read_snf_telluric_model(filename):
    """
    Reads the atmospheric telluric data and creates a telluric transmission model

    The file should be Fclass 620 XFclass 600

    """
    #- read the atmospheric transmission data

    f_fits = pyfits.open(filename)
    header = f_fits[1].header
    
    telluric_transmission = atmosphericmodel.Buton_telluric(airmass=1.,
                                                            H2Ow_power=header.get("TELLPOW0"),
                                                            H2Os_power=header.get("TELLPOW1"),
                                                            O2_power=header.get("TELLPOW2"),
                                                            H2Ow_intensity=header.get("TELLINT0"),
                                                            H2Os_intensity=header.get("TELLINT1"),
                                                            O2_intensity=header.get("TELLINT2"),                 
                                                            telluric_template_path=None,
                                                            keys=f_fits[1].header)        
    return telluric_transmission


def read_snf_full_model(atmospheric_filename, telluric_filename):
    """
    Reads a full atmospheric model from an atmospheric model file
    625_610 or 625_600
    and a telluric file
    620_600
    """
    f_fits_atmospheric = pyfits.open(atmospheric_filename)
    header_atmospheric = f_fits_atmospheric[1].header

    f_fits_telluric = pyfits.open(telluric_filename)
    header_telluric = f_fits_telluric[1].header


    keys = {}
    for item in list(f_fits_atmospheric[1].header.items()):
        keys[item[0]] = item[1]
    for item in list(f_fits_telluric[1].header.items()):
        keys[item[0]] = item[1]
    
    transmission_model = atmosphericmodel.Buton(airmass=1.,
                                                pressure=header_atmospheric.get("PRESSURE"),
                                                ozone_column=header_atmospheric.get("OZ_INT"),
                                                aerosol_optical_depth=header_atmospheric.get("AE_TAU"),
                                                aerosol_exponent=header_atmospheric.get("AE_ANG"),
                                                ozone_template_path=None,
                                                H2Ow_power=header_telluric.get("TELLPOW0"),
                                                H2Os_power=header_telluric.get("TELLPOW1"),
                                                O2_power=header_telluric.get("TELLPOW2"),
                                                H2Ow_intensity=header_telluric.get("TELLINT0"),
                                                H2Os_intensity=header_telluric.get("TELLINT1"),
                                                O2_intensity=header_telluric.get("TELLINT2"),                 
                                                telluric_template_path=None,
                                                keys=keys)        
    

    return transmission_model


#- Atmospheric model from Buton et al.
#- Directly usable with SNf fits keywords

def buton_base_rayleigh(wavelength):
    """Rayleigh extinction from Hansen & Travis (1974).

    Implementation stolen from CVS_SNf/Analysis/AtmosphericExtinction/Scripts/pyExtinction/AtmosphericExtinction.py

    wavelength: wavelength vector [AA]
    
    return: Rayleigh extinction [mag/airmass] without the pressure term
            pressure: effective surface pressure [mbar]

    """
    EXT2OPT = .92103403719761834  # LOG10/2.5 = Extinction to opt. thickness
    
    lm = wavelength * 1e-4                # Wavelength from A to microns
    
    # Optical depth
    tau = 0.008569 / lm ** 4 * (1 + 0.0113 / lm ** 2 + 0.00013 / lm ** 4)
    tau *= 1. / (1013.25 * EXT2OPT) 
    
    return tau


class Buton_atmosphere(object):
    def __init__(self, airmass=1.,
                 pressure=616.,
                 ozone_column=257.,
                 aerosol_optical_depth=0.0076,
                 aerosol_exponent=1.26,
                 ozone_template_path=None,
                 keys={}):
        """
        Creates an atmospheric extinction model based on Buton et al.

        By default looks for the ozone template in 
        saltpath.atmospheric_model_path+"/Buton/ozoneTemplate.fits"
        which should be
        $SALTPATH/atmospheric_model/Buton/ozoneTemplate.fits


        If no parameters are provided, the airmass will be set to 1. and the other parameters to the
        average values given by Buton et al 2013:
        are adapted to mean Mauna-Kea summit conditions.

        The ozone template can be provided by hand, but by default it is assumed to live in
        $SALTPATH/atmospheric_model/Buton/ozoneTemplate.fits

        =================================  =================
        Parameter                          Value ± Error
        =================================  =================
        *Mauna Kea*
        ----------------------------------------------------
        Pressure                           616 ± 2 mbar
        Ozone column                       257 ± 23 DU
        Aerosols optical depth @ 1 micron  0.0076 ± 0.0014
        Aerosols angstrom exponent         1.26 ± 1.33
        =================================  =================

        The parameters are stored in a fitparemeters.FitParameters() instance
        
        The ozone template is read in a Func1D() stored in self.ozone_template

        There is a keys dictionnary member, {} by default, to store metadata

        Examples:
        >>> mauna_kea_average_atmosphere = atmosphericmodel.Buton()
        >>> mauna_kea_average_atmosphere.parameter
        pressure: array([ 616.])
        ozone_column: array([ 257.])
        airmass: array([ 1.])
        aerosol_optical_depth: array([ 0.0076])
        aerosol_exponent: array([ 1.26])
        
        >>> wavelength = numpy.linspace(3000., 10000., 200)
        >>> pylab.plot(wavelength, mauna_kea_average_atmosphere(wavelength))
        >>> mauna_kea_average_atmosphere.parameter
        >>> mauna_kea_average_atmosphere.parameter["airmass"] = 2.
        >>> mauna_kea_average_atmosphere.parameter
        pressure: array([ 616.])
        ozone_column: array([ 257.])
        airmass: array([ 2.])
        aerosol_optical_depth: array([ 0.0076])
        aerosol_exponent: array([ 1.26])

        >>> pylab.plot(wavelength, mauna_kea_average_atmosphere(wavelength))


        To plot single components:
        >>> x = np.linspace(2500., 10000., 100)
        >>> plt.plot(x, b(x), "r-")
        >>> plt.plot(x, b.rayleigh_transmission(x), "g-")
        >>> plt.plot(x, b.ozone_transmission(x), "b-")
        >>> plt.plot(x, b.aerosol_transmission(x), "k-")
        >>> p = b.parameter.copy()
        >>> p["aerosol_exponent"] = 3.
        >>> plt.plot(x, b.aerosol_transmission(x, p=p), "k--")

        Changing parameters:
        >>> p = b.parameter
        >>> p["pressure"] = 500.
        This changes what b(x) will return

        To get the parameters:
        >>> 
        """
        self.parameter = fitparameters.FitParameters(["airmass",
                                                      "pressure",
                                                      "ozone_column",
                                                      "aerosol_optical_depth",
                                                      "aerosol_exponent"])

        self.parameter["airmass"][0] = airmass
        self.parameter["pressure"][0] = pressure
        self.parameter["ozone_column"][0] = ozone_column
        self.parameter["aerosol_optical_depth"][0] = aerosol_optical_depth
        self.parameter["aerosol_exponent"][0] = aerosol_exponent

        # By default assumes that the ozone template is in snfit_data
        if ozone_template_path is None:
            ozone_template_path = saltpath.atmospheric_model_path + "/Buton/ozoneTemplate.fits"
        self.read_ozone_template(ozone_template_path)

        self.keys = keys
        
    def get_parameter(self):
        """
        Returns a copy of the parameters

        >>> p = b.parameter
        >>> p["pressure"] = 500.
        Changes b(x)

        >>> p = b.get_parameter()
        >>> p["pressure"] = 500.
        Doesn't change b(x)
        To get the new b(x) do
        >>> b(x, parameter=p)

        NB: you could also do b.parameter.copy()
        """        
        return self.parameter.copy()
    
    def func1d_rayleigh(self, parameter=None):
        """
        pressure is in [mbar]

        sets self.rayleigh to be  Rayleigh extinction in [mag/airmass]
        as a Func1D that will change when self.pressure changes
        """

        if parameter is None:
            parameter = self.parameter

        return parameter["pressure"].full[0] * interpolation.Func1D(buton_base_rayleigh)
                
    def read_ozone_template(self, ozone_template_path):
        """
        Reads the ozone template and puts it in 
        self.ozone_template as a Func1D instance
        """
        # Read wavelength and transmission columns
        ext = 1
        colLbda = "LAMBDA"
        colTrans = "OZONE"
        
        ffile = pyfits.open(ozone_template_path)
        x = ffile[ext].data.field(colLbda)   # Wavelength
        y = ffile[ext].data.field(colTrans)  # Transmission    
        refO3col = ffile[ext].header["REFO3COL"]
        ffile.close()

        self.ozone_template_path = ozone_template_path
        self.ozone_template = interpolation.Func1D(x, numpy.absolute(-2.5 * numpy.log10(y)) / refO3col)
        
    def func1d_ozone(self, parameter=None):
        """
        Sets self.ozone to be the Func1D that calculates the ozone component of the atmospheric transmission
        """
        if parameter is None:
            parameter = self.parameter
        return parameter["ozone_column"].full[0] * self.ozone_template

    def func1d_transmission(self, transmission, parameter=None):
        """
        Returns a func1d that calculates the transmission corresponding to an extinction func1d
        """
        if parameter is None:
            parameter = self.parameter
        return 10 ** (-0.4 * (parameter["airmass"].full[0] * transmission))
    
    def func1d_aerosol(self, parameter=None):
        """
        Sets self.aerosol to be the Func1D that calculates the aerosol component of the atmospheric transmission
        """
        EXT2OPT = .92103403719761834  # LOG10/2.5 = Extinction to opt. thickness
        wavelength_reference = 1.e4
        if parameter is None:
            parameter = self.parameter

        return interpolation.Func1D(lambda x:
                                             parameter["aerosol_optical_depth"].full[0] / EXT2OPT *
                                             (x / wavelength_reference) **
                                             - parameter["aerosol_exponent"].full[0])

    def func1d_atmospheric_extinction(self, parameter=None):
        """
        Returns the Func1D that calculates the atmospheric extiction in [mag/airmass]       
        """
        if parameter is None:
            parameter = self.parameter
            
        return self.func1d_rayleigh(parameter=parameter) + self.func1d_ozone(parameter=parameter) + self.func1d_aerosol(parameter=parameter)

    
    def func1d_atmospheric_transmission(self, parameter=None):
        """
        Returns the atmospheric transmission curve for a given airmass in photons     
        See Buton et al eq.5

        call self(x) to get its values along axis x
        """
        atmospheric_extinction = self.func1d_atmospheric_extinction(parameter=parameter)
        if parameter is None:
            parameter = self.parameter
        return 10 ** (-0.4 * (parameter["airmass"].full[0] * atmospheric_extinction))

    def rayleigh_extinction(self, x, parameter=None, jac=False):
        """
        Convenience function to plot the raileght component of the atmospheric
        extinction corresponding to the parameters of the Buton instance.
        
        If parameter is set, will plot with these parameters instead.
        """
        rayleigh = self.func1d_rayleigh(parameter=parameter)

        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return rayleigh(x)

    def ozone_extinction(self, x, parameter=None, jac=False):
        """
        Convenience function to plot the ozone component of the atmospheric
        extinction corresponding to the parameters of the Buton instance.
        
        If p is set, will plot with these parameters instead.
        """
        ozone = self.func1d_ozone(parameter=parameter)

        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return ozone(x)

    def aerosol_extinction(self, x, parameter=None, jac=False):
        """
        Convenience function to plot the aerosol component of the atmospheric
        extinction corresponding to the parameters of the Buton instance.
        
        If p is set, will plot with these parameters instead.
        """
        aerosol = self.func1d_aerosol(parameter=parameter)

        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return aerosol(x)

    def atmospheric_extinction(self, x, parameter=None, jac=False):
        """
        A convenience function to be able to plot the atmospheric extinction corresponding to the parameters
        of the Buton instance
        """
        atmospheric_extinction = self.func1d_atmospheric_extinction(parameter=parameter)

        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return atmospheric_extinction(x)

        
    def rayleigh_transmission(self, x, parameter=None):
        """
        Convenience function to plot the raileght component of the atmospheric
        transmission corresponding to the parameters of the Buton instance.
        
        If parameter is set, will plot with these parameters instead.
        """
        rayleigh = self.func1d_rayleigh(parameter=parameter)

        if parameter is None:
            parameter = self.parameter
        return 10 ** (-0.4 * (parameter["airmass"].full[0] * rayleigh(x)))

    def ozone_transmission(self, x, parameter=None):
        """
        Convenience function to plot the raileght component of the atmospheric
        transmission corresponding to the parameters of the Buton instance.
        
        If parameter is set, will plot with these parameters instead.
        """
        ozone = self.func1d_ozone(parameter=parameter)

        if parameter is None:
            parameter = self.parameter
        return 10 ** (-0.4 * (parameter["airmass"].full[0] * ozone(x)))


    def aerosol_transmission(self, x, parameter=None):
        """
        Convenience function to plot the raileght component of the atmospheric
        transmission corresponding to the parameters of the Buton instance.
        
        If p is set, will plot with these parameters instead.
        """
        aerosol = self.func1d_aerosol(parameter=parameter)

        if parameter is None:
            parameter = self.parameter
        return 10 ** (-0.4 * (parameter["airmass"].full[0] * aerosol(x)))
                          
        
    def __call__(self, x, parameter=None, jac=False):
        atmospheric_transmission = self.func1d_atmospheric_transmission(parameter=parameter)

        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return atmospheric_transmission(x)
        

class Buton_telluric(object):
    def __init__(self, airmass=1.,
                 H2Ow_power=0.6,
                 H2Os_power=0.6,
                 O2_power=0.58,
                 H2Ow_intensity=1.,
                 H2Os_intensity=1.,
                 O2_intensity=1.,                 
                 telluric_template_path=None,
                 keys={}):
        """Creates a telluric line absorption model based on Buton et al.

        By default looks for the telluric template in 
        saltpath.atmospheric_model_path+"/Buton/SNIFS_extinction.fits"
        which should be
        $SALTPATH/atmospheric_model/Buton/SNIFS_extinction.fits

        The telluric data is in the 2nd extension. Note that the first extension
        contains the average Mauna Kea extinction as implemented in class Buton.
        
        If no parameters are provided, the airmass will be set to 1. and the other parameters to the
        average values given by Buton et al 2013.

        The telluric template can be provided by hand

        The parameters are stored in a fitparameters.FitParameters() instance
        
        The telluric template is read in 3 different Func1D() stored in 
        self.H2Ow_template
        self.H2Os_template
        self.O2_template
        
        Those are telluric extinctions in mmags
        There is a keys dictionnary member, {} by default, to store metadata        

        Examples:
        >>> mauna_kea_telluric = atmosphericmodel.Buton_telluric()
        >>> mauna_kea_telluric.parameter
        H2Os_power: array([ 0.6])
        O2_intensity: array([ 1.])
        airmass: array([ 1.])
        O2_power: array([ 0.58])
        H2Ow_intensity: array([ 1.])
        H2Os_intensity: array([ 1.])
        H2Ow_power: array([ 0.6])

        >>> wavelength = numpy.linspace(3000., 10000., 200)
        >>> pylab.plot(wavelength, mauna_kea_telluric(wavelength))
        >>> H2Ow_transmission = mauna_kea_telluric.func1d_H2Ow_transmission() # This function will NOT change when mauna_kea_telluric.parameter is changed
        >>> pylab.plot(wavelength, H2Ow_transmission(wavelength))

        >>> pylab.plot(wavelength, mauna_kea_telluric.H2Ow_transmission(wavelength))
        >>> mauna_kea_telluric.parameter["H2Ow_intensity"] = 2.
        >>> pylab.plot(wavelength, mauna_kea_telluric.H2Ow_transmission(wavelength))

        """
        self.parameter = fitparameters.FitParameters(["airmass",
                                                      "H2Ow_power",
                                                      "H2Os_power",
                                                      "O2_power",
                                                      "H2Ow_intensity",
                                                      "H2Os_intensity",
                                                      "O2_intensity"])        

        self.parameter["airmass"][0] = airmass
        self.parameter["H2Ow_power"][0] = H2Ow_power
        self.parameter["H2Os_power"][0] = H2Os_power
        self.parameter["O2_power"][0] = O2_power
        
        self.parameter["H2Ow_intensity"][0] = H2Ow_intensity
        self.parameter["H2Os_intensity"][0] = H2Os_intensity
        self.parameter["O2_intensity"][0] = O2_intensity

        # By default assumes that the telluric template is in snfit_data
        if telluric_template_path is None:
            telluric_template_path = saltpath.atmospheric_model_path + "/Buton/SNIFS_extinction.fits"
        self.read_telluric_template(telluric_template_path)

        self.keys = keys
        
    def get_parameter(self):
        """
        Returns a copy of the parameters
        
        Warning:
        >>> p = b.parameter
        >>> p["pressure"] = 500.
        Changes b(x)

        NB: you could also do b.parameter.copy()
        """
        return self.parameter.copy()
        
    def read_telluric_template(self, telluric_template_path):
        """
        Reads the telluric template and puts it in 
        self.H2Ow_template
        self.H2Os_template
        self.O2_template
        as a Func1D instances

        The templates are extinctions in mmags
        """
        # Read wavelength and transmission columns
        ext = 2
        
        fh = pyfits.open(telluric_template_path)
        wavelength = fh[ext].data.field("LAMBDA")  # Wavelength
        H2Ow = fh[ext].data.field('H2Ow    ')
        H2Os = fh[ext].data.field('H2Os    ')
        O2 = fh[ext].data.field('O2      ') 
        fh.close()

        self.telluric_template_path = telluric_template_path
        self.H2Ow_template = interpolation.Func1D(wavelength, H2Ow)
        self.H2Os_template = interpolation.Func1D(wavelength, H2Os)
        self.O2_template = interpolation.Func1D(wavelength, O2)
        
    def func1d_H2Ow_extinction(self, parameter=None):
        """
        Returns the Func1D that calculates the H2Ow component of the telluric
        extinction accounting for intensity, airmass and power
        
        """
        if parameter is None:
            parameter = self.parameter

        return parameter["airmass"].full[0] ** parameter["H2Ow_power"].full[0] * parameter["H2Ow_intensity"].full[0] * self.H2Ow_template 

    def func1d_H2Ow_transmission(self, parameter=None):
        """
        Returns the transmission of the H2Ow component accounting for the
        airmass and intensity of the component
        """
        H2Ow_extinction = self.func1d_H2Ow_extinction(parameter=parameter)
        return 10 ** (-0.4 * H2Ow_extinction)
    
    def func1d_H2Os_extinction(self, parameter=None):
        """
        Returns the Func1D that calculates the H2Ow component of the telluric
        extinction accounting for intensity, airmass and power
        
        """
        if parameter is None:
            parameter = self.parameter

        return parameter["airmass"].full[0] ** parameter["H2Os_power"].full[0] * parameter["H2Os_intensity"].full[0] * self.H2Os_template 

    def func1d_H2Os_transmission(self, parameter=None):
        """
        Returns the transmission of the H2Os component accounting for the
        airmass and intensity of the component
        """
        H2Os_extinction = self.func1d_H2Os_extinction(parameter=parameter)
        return 10 ** (-0.4 * H2Os_extinction)    
    
    def func1d_O2_extinction(self, parameter=None):
        """
        Returns the Func1D that calculates the H2Ow component of the telluric
        extinction accounting for intensity, airmass and power
        
        """
        if parameter is None:
            parameter = self.parameter

        return parameter["airmass"].full[0] ** parameter["O2_power"].full[0] * parameter["O2_intensity"].full[0] * self.O2_template 
    
    def func1d_O2_transmission(self, parameter=None):
        """
        Returns the transmission of the O2 component accounting for the
        airmass and intensity of the component
        """
        O2_extinction = self.func1d_O2_extinction(parameter=parameter)
        return 10 ** (-0.4 * O2_extinction)

    def func1d_telluric_extinction(self, parameter=None):
        """
        Returns the Func1D that calculates the telluric extiction 
        
        Note that since each component has a different airmass power, the
        airmass dependence is already included.  
        """
        extinction = self.func1d_H2Ow_extinction(parameter=parameter) + \
                     self.func1d_H2Os_extinction(parameter=parameter) + \
                     self.func1d_O2_extinction(parameter=parameter)
        
        return extinction
    
    def func1d_telluric_transmission(self, parameter=None):
        """
        Returns the full telluric transmission curve including airmass
        dependence and relative intensity of the components     
        """
        telluric_extinction = self.func1d_telluric_extinction(parameter=parameter)
        return 10 ** (-0.4 * telluric_extinction)

    def H2Ow_transmission(self, x, parameter=None, jac=False):
        """
        Convenience function that evaluates the H20w transmission 
       
        Also usable to fit only the H2Ow component
        """
        H2Ow_transmission = self.func1d_H2Ow_transmission(parameter=parameter)

        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return H2Ow_transmission(x)

    def H2Os_transmission(self, x, parameter=None, jac=False):
        """
        Convenience function that evaluates the H20w transmission 
       
        Also usable to fit only the H2Os component
        """
        H2Os_transmission = self.func1d_H2Os_transmission(parameter=parameter)

        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return H2Os_transmission(x)

    def O2_transmission(self, x, parameter=None, jac=False):
        """
        Convenience function that evaluates the H20w transmission 
       
        Also usable to fit only the O2 component
        """
        O2_transmission = self.func1d_O2_transmission(parameter=parameter)

        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return O2_transmission(x)

    def telluric_extinction(self, x, parameter=None, jac=False):
        """
        Facility method to easily access the full telluric extinction
        """
        telluric_extinction = self.func1d_telluric_extinction(parameter=parameter)

        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return telluric_extinction(x)

        
    def __call__(self, x, parameter=None, jac=False):
        telluric_transmission = self.func1d_telluric_transmission(parameter=parameter)

        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return telluric_transmission(x)



class Buton(Buton_atmosphere, Buton_telluric):
    def __init__(self, airmass=1.,
                 pressure=616.,
                 ozone_column=257.,
                 aerosol_optical_depth=0.0076,
                 aerosol_exponent=1.26,
                 ozone_template_path=None,
                 H2Ow_power=0.6,
                 H2Os_power=0.6,
                 O2_power=0.58,
                 H2Ow_intensity=1.,
                 H2Os_intensity=1.,
                 O2_intensity=1.,                 
                 telluric_template_path=None,
                 keys={}):
        """
        This is an object whose purpose is to provide a way to handle simultaneously
        Buton_atmosphere and Buton_telluric into a single instance.
        
        """
        
        # Initialize the parameters
        self.parameter = fitparameters.FitParameters(["airmass",
                                                      "pressure",
                                                      "ozone_column",
                                                      "aerosol_optical_depth",
                                                      "aerosol_exponent",
                                                      "H2Ow_power",
                                                      "H2Os_power",
                                                      "O2_power",
                                                      "H2Ow_intensity",
                                                      "H2Os_intensity",
                                                      "O2_intensity"])        
        
        self.parameter["airmass"][0] = airmass
        self.parameter["pressure"][0] = pressure
        self.parameter["ozone_column"][0] = ozone_column
        self.parameter["aerosol_optical_depth"][0] = aerosol_optical_depth
        self.parameter["aerosol_exponent"][0] = aerosol_exponent
        
        self.parameter["H2Ow_power"][0] = H2Ow_power
        self.parameter["H2Os_power"][0] = H2Os_power
        self.parameter["O2_power"][0] = O2_power
        
        self.parameter["H2Ow_intensity"][0] = H2Ow_intensity
        self.parameter["H2Os_intensity"][0] = H2Os_intensity
        self.parameter["O2_intensity"][0] = O2_intensity

        
        # Create the two components of the model and have them use the same
        # parameter vector
        self.atmosphere = Buton_atmosphere()
        self.atmosphere.parameter = self.parameter
        self.ozone_template_path = self.atmosphere.ozone_template_path
        self.ozone_template = self.atmosphere.ozone_template
         
        
        self.telluric = Buton_telluric()
        self.telluric.parameter = self.parameter
        self.telluric_template_path = self.telluric.telluric_template_path
        self.H2Ow_template = self.telluric.H2Ow_template
        self.H2Os_template = self.telluric.H2Os_template
        self.O2_template = self.telluric.O2_template

        self.keys = keys

    def get_parameter(self):
        """
        Returns a copy of the parameters

        Warning: p = b.parameter 
        Changing p will change what b(x) returns

        NB: you could also do b.parameter.copy()
        """
        return self.parameter.copy()
        

    def func1d_total_transmission(self, parameter=None):
        """
        Returns the atmospheric transmission curve for a given airmass in photons     
        See Buton et al eq.5
        
        And including the telluric lines

        call self(x) to get its values along axis x
        """
        telluric_transmission = self.func1d_telluric_transmission(parameter=parameter)
        atmospheric_transmission = self.func1d_atmospheric_transmission(parameter=parameter)

        total_transmission = telluric_transmission * atmospheric_transmission
        return total_transmission

        
    def __call__(self, x, parameter=None, jac=False):
        """
        Evaluates the total transmission (atmospheric + telluric) on the
        wavelength grid x
        """
        
        total_transmission = self.func1d_total_transmission(parameter=parameter)
        
        if jac:
            raise NotImplemented("Jacobian calculation not implemented")
        else:
            return total_transmission(x)
        
    
