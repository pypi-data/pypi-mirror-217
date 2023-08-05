#!/usr/bin/python
""" Define physical constants

All physical constants used in the code belongs to this module. We
also define conventionnal quantities here.
"""

import numpy as np


###############################################
# Definition of constants
###############################################
G = 6.67384e-11  # m^3/kg/s^2
C_LIGHT = 299792458.  # m/s
PARSEC = 3.08567758e16  # m
PROTON_MASS = 1.67262158e-27  # masse du proton kg
H = 6.62617e-34  # J.s
K_BOLTZ = 1.38066e-23  # J/K


#- unit transformation
CLIGHT_A_s  = 2.99792458e18         # [A/s]
CLIGHT_m_s  = 2.99792458e8         # [A/s]
CLIGHT_km_s  = 2.99792458e5         # [A/s]
H_e_s = 6.62606896e-27        # [erg s]

# Stefan-Boltzmann
SIGMA = 2 * np.core.umath.pi ** 5 * K_BOLTZ ** 4 / (15 * H ** 3 * C_LIGHT ** 2)
T_CMB = 2.7255  # Fixen (2009)
RHO_GAMMA = 4 * SIGMA * T_CMB ** 4 / C_LIGHT ** 3  # Energy density of CMB
# today in kg/m3

def hmstodeg(h, m=0, s=0):
    if isinstance(h, str):
        h, m, s = h.split(':')
        h, m, s = float(h), float(m), float(s)
    return h*15 + m*15/60.0 + s*15/3600.0

def dmstodeg(d, m=0, s=0, sign=0):
    if isinstance(d, str):
        d, m, s = d.split(':')
        sign = -1. if d[0] == '-' else 1.
        d, m, s = float(d), float(m), float(s)
    else:
        if not sign:
            if d == 0:
                print('Warning, sign may be ambiguous')
            sign = -1. if d < 0 else 1.
    return (abs(d) + m/60.0 + s/3600.0) * sign

def degtohms(deg):
    hh = deg / 15.0
    h = np.floor(hh)
    m = np.floor((hh - h)*60.0)
    s = (hh - h - m / 60)*3600.0
    return h, m, s

def degtodms(deg):
    si = np.sign(deg)
    hh = abs(deg)
    d = np.floor(hh)
    m = np.floor((hh - d)*60.0)
    s = (hh - d - m / 60)*3600.0
    return si*d, m, s


def flux_ab(wavelength):
    """ Compute AB reference SED at a given wavelength

    Parameters:
    -----------
    wavelength: in Angstrom

    Return:
    -------
    S_ab in erg/(s*cm2*A)
    """
    return 10 ** (-19.44) * C_LIGHT * 1e10 / wavelength ** 2

def hmstodeg(h, m=0, s=0):
    if isinstance(h, str):
        h, m, s = h.split(':')
        h, m, s = float(h), float(m), float(s)
    return h*15 + m*15/60.0 + s*15/3600.0

def dmstodeg(d, m=0, s=0, sign=0):
    if isinstance(d, str):
        d, m, s = d.split(':')
        sign = -1. if d[0] == '-' else 1.
        d, m, s = float(d), float(m), float(s)
    else:
        if not sign:
            if d == 0:
                print('Warning, sign may be ambiguous')
            sign = -1. if d < 0 else 1.
    return (abs(d) + m/60.0 + s/3600.0) * sign

def degtohms(deg):
    hh = deg / 15.0
    h = np.floor(hh)
    m = np.floor((hh - h)*60.0)
    s = (hh - h - m / 60)*3600.0
    return h, m, s

def degtodms(deg):
    si = np.sign(deg)
    hh = np.abs(deg)
    d = np.floor(hh)
    m = np.floor((hh - d)*60.0)
    s = (hh - d - m / 60)*3600.0
    return si*d, m, s
