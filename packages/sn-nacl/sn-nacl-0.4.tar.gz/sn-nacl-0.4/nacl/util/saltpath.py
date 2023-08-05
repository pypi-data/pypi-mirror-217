"""
Tools to use snfit_data
"""

import os

SALTPATH = os.getenv("SALTPATH")

fitmodel_filename = os.path.join(SALTPATH, "fitmodel.card")

atmospheric_model_path = os.path.join(SALTPATH, "atmospheric_model")

stellar_libs_path = os.path.join(SALTPATH, "stellar_libs")

galaxy_template_path = os.path.join(SALTPATH, "galaxy_templates")

sn_template_path = os.path.join(SALTPATH, "sn_templates")

def reload_saltpath(saltpath=os.getenv("SALTPATH")):
    global SALTPATH
    global fitmodel_filename
    global atmospheric_model_path
    global stellar_libs_path
    global sn_template_path
    
    SALTPATH = saltpath

    fitmodel_filename = os.path.join(SALTPATH, "fitmodel.card")

    atmospheric_model_path = os.path.join(SALTPATH, "atmospheric_model")

    stellar_libs_path = os.path.join(SALTPATH, "stellar_libs")

    galaxy_template_path = os.path.join(SALTPATH, "galaxy_templates")

    sn_template_path = os.path.join(SALTPATH, "sn_templates")
    

def read_fitmodel_card(filename=None):
    """
    Reads $SALTPATH/fitmodel.cards or filename if filename is set
    """
    if filename is None:
        return read_card_file(fitmodel_filename)
    else:
        return read_card_file(filename)
        
def read_card_file(filename):
    """ Read a snfit "card" file into a dictionnary.

    Read all entries with the format:
    "@key1 value1
     @key2 ..."

    in file "filename.
    RETURN:
    ------
    a dictionnary: {key1: value1, key2: ...}
    """
    cards = {}
    fid = open(filename)
    lines = fid.readlines()
    fid.close()
    for line in lines:
        if not line.startswith('@'):
            continue
        else:
            key = line.split()
            value = " ".join(key[1:])
            key = key[0]
            cards[key[1:]] = value
    return cards

