""" Definition of the python side NTuple class.

These are mainly io routines. The idea is: if the file format is the
native numpy format, read of write directly, else pipe binary data
through ntcat.


"""

import numpy as np
from numpy.lib.utils import safe_eval
import re
import sys
import copy
from glob import glob
import os

def stringify(nt):
    '''Cast a record array so that byte fields become utf8 fields'''
    dt = [(f, t.replace('S', 'U')) for f, t in  nt.dtype.descr]
    return nt.astype(dt)

def read_header(fh):
    keys = {}
    names = []
    for i, line in enumerate(fh):
        if line.startswith('#'):
            if line[1:].strip() == "end":
                break
            else:
                names.append(line[1:].split(':')[0].strip())
        elif line.startswith('@'):
            l = line[1:].split()
            keys[l[0]] = convert(' '.join(l[1:]))
    return keys, names
    
def read_header_keys(filename):
    with open(filename) as fh:
        keys, names = read_header(fh)
    return keys, names

def select(ntuple, condition, vars=[], vars_rule="and"):
    """Provide an easier way to express condition on fields

    ga = nacl.util.io.select(nt_atmosphere, "(LAMBDA>5000.) & (LAMBDA<7000.) ")
    
    Works for more than one keyword

    vars is a list of  indexes over which to expand the condition string if 
    built like:
    condition = "field_%s < 1.", vars=["1", "3"]
    This will apply the condition on field_1 and field_3. Logical and.

    vars_rule is set to loop over vars with a & operator
    Set it to "or" "OR" or "|" to get an | operator. 
    Defaults to & for everything else

    Note that vars only loops is %s is provided.
    condition = "field_%d < 1" % (my_index)  works while providing my_index to vars won't work.


    In case of ntuple keys with a dot "target.name" for example,
    the field in the condition should be written with two underscores instead.

    "target__name == 'LSQ10vw'" will be understood as looking for the key target.name 
    (Actually, select() reads the keys with dots replacing them by __). 
    What this means is that if your key is target_name, things will also work
    fine.

    It is if and only if you have both target.name and target__name as keys, that
    you are screwed. But then, maybe that's also when you should start wondering
    if you are not asking for it a little bit, don't you agree ?

    """
    fields = dict([(k.replace(".", "__"), ntuple[k]) for k in ntuple.dtype.names])
    if not vars:
        index = eval(condition, globals(), fields)
    else:
        n = condition.count('%s')
        index = eval(condition % ((vars[0],) * n), globals(), fields)
        for var in vars[1:]:
            if vars_rule in ["or", "OR", "|"]:
                index |= eval(condition % ((var,) * n), globals(), fields)
            else:
                index &= eval(condition % ((var,) * n), globals(), fields)                
                
    return ntuple[index]

def sanitize(name):
    for s in '-*+/ ':
        name = name.replace(s, '_')
    return name

def eval_form(ntuple, formula, var=""):
    """ Provide an easier way to evaluate formula on fields

    For example, if the ntuple has fields named MAG_U and ZP_U
    we can do
    >>> nacl.util.io.eval_form(ntuple, "MAG_%s - ZP_%s", var="U")        
    """
    fields = dict([(sanitize(k), ntuple[k]) for k in ntuple.dtype.names])
    n = formula.count('%s')
    if n:
        formula = formula % ((var,) * n)
    return eval(formula, globals(), fields)


def read_matrix(lines):
    s = np.loadtxt(lines[0:1])
    m = np.loadtxt(lines[1:])
    assert m.shape == (s[0], s[1]), ('Unable to read matrix at'
                                     ' the end of the file')
    return m

# I want to be able to add a field to a NTuple without having to
# remember where those guys hid the method
from numpy.lib.recfunctions import append_fields, join_by, merge_arrays
from numpy.lib.recfunctions import rec_append_fields, rec_drop_fields


def rec_stack(*args, **keys):
    """ Easy concatenation of several record arrays into a single one

    Optionally rename the fields by adding a suffix or a prefix (or
    both) to the field names.

    Exemple:
    --------
    >>> nt0 = np.rec.fromarrays([range(3)], names=['a'])
    >>> nt1 = np.rec.fromarrays([range(3)], names=['a'])
    >>> rec_stack(nt0, nt1, suffix1="_1")
    array([(0, 0), (1, 1), (2, 2)],
          dtype=[('a', '<i8'), ('a_1', '<i8')])

    Recipes:
    --------
    + If you have a number of similar ntuples, for example in a dictionnary 
    >>> d{"label_1":{"nt_description":nt_1, "more info":stuff}, {"nt_description":nt_1, "more info":stuff}  }
    >>> l_nt = [ d[key]["nt_description"] for key in d.keys() ]
    >>> d_suffix = {"suffix%d"%(i) : "_"+label for i, label in enumerate(d.keys())}
    >>> nacl.util.io.rec_stack(*l_nt, **d_suffix)

    will create the NTuple where all the ntuple fields that would have had the same name are now of the form
    same-name_label, where label is the key that was used in the dictionnary.

    """
    merge_result = []
    for i, nt in enumerate(args):
        suffix = keys.pop('suffix%d' % i, "")
        prefix = keys.pop('prefix%d' % i, "")
        nt = nt.copy()
        # This ensure that a new dtype object is created and that the
        # change of field name is not going to affect the original
        # array
        nt.dtype = np.dtype(nt.dtype.descr)
        if suffix or prefix:
            nt.dtype.names = tuple([prefix + name + suffix
                                    for name in nt.dtype.names])
        merge_result.append(nt)
    return merge_arrays(merge_result, flatten=True)


def convert(value):
    value = value.strip()
    if not value:
        value = "nan"
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            pass
    return value


def convert_format(value, format):
    value = value.strip()
    if format[0] == "I":
        if not value:
            value = -99
        else:
            value = int(value)
    elif format[0] in "FE":
        if not value:
            value = np.nan
        else:
            value = float(value)
    else:
        if not value:
            value = '_'
    return value



def find_closest(data, target, sorted=True):
    """
    Stolen from stakoverflow to find index closest to target from a sorted list A.

    If sorted is False, takes care of it
    """
    
    if not sorted:
        idx_sorted = np.argsort(data)
        A = data[idx_sorted]
    else:
        A = data
        idx_sorted = np.arange(len(data) - 1)
        
    idx = A.searchsorted(target)
    idx = np.clip(idx, 1, len(A)-1)
    left = A[idx-1]
    right = A[idx]
    idx -= target - left < right - target
    if idx > len(idx_sorted) -1:
        idx = -1
    return idx_sorted[idx]

class split_container:
    """
    This is a dummy class to create namespaces to contain the data provided by
    nacl.util.io.split method  
    
    >>>  c = croaks.croaks_split_namespace()
    >>> nacl.util.io.split(ntuple, c.__dict__)    
    """
    pass


def split(ntuple, d_output, two_D={}, field_output_suffix="_field"):
    """
    Parameters:
    -----------
    + ntuple:  a nacl.util.io.NTuple
    + d_output: is a dictionnary that will contain the splitted ntuple
    Note that d_output can be 
        - a genuine dictionnary
        - a class instance internal dictionnary c.__dict__
            This allows to access the splitted ntuple data via c.LAMBDA for
            example, if the ntuple has such a vector column
        - the global namespace dictionnary global()
            This allows to access the splitted ntuple data via LAMBDA for
            example if the ntuple has such a vector column
            WARNING: the ntuple should not have names that overwrite anything
                     in the global namespace. Ensuring this is of the user's
                     responsibility 
    + two_D: a dictionnary containing the 2D array names and the re regexp to
             do the grouping
             For example:
             two_D = {"Flux": "FLUX_.*"}
             will try to group all the columns with names matching the regexp
             in a 2D array that will be stored in d_output["Flux"].
             
             If the number of matching column names is N_col, and the NTuple
             length is N_row, the result will be an (N_row x N_col) array.

    + field_output_suffix: 

    Definition:
    -----------
    This method works on "horizontal" NTuples, i.e. of the form:
    LAMBDA  FLUX_label_1 FLUX_label_2 GA_label_1  GA_label_2 GA_3  V1  V2

    LAMBDA, V1 and V3 are different from FLUX_* and GA_* in that they are
    vectors that give a global information on FLUX_* and GA_*, while all FLUX_*
    for example are expected to be compatible (i.e., operations like calculating
    the mean make sense on them).
    
    nacl.util.io.split will by default return each column of the NTuple as a
    vector in d_output, of the form d_output[column_name] = colum_vector_value.

    In the case of our example:
    d["LAMBDA"] = wavelength_vector
    

    If two_D dictionnary is used, the fields corresponding to the regexp
    provided will be agregated in 2D arrays with the same orientation as what
    could be read in the NTuple ascii file.

    Examples:
    ---------
    For an NTuple ntuple  of the form:
    LAMBDA  FLUX_label_1 FLUX_label_2 GA_label_1  GA_label_2 GA_3  V1  V2
    
    with N_l lines

    >>> nacl.util.io.split(ntuple, globals(), two_D={"flux": "FLUX_.*"})
    will add in the global name space:
    
    >>> LAMBDA
    Which will be the vector ntuple["LAMBDA"]
    
    >>> flux
    Which will be the 2D array with
    
    >>> flux[:,0]
    corresponding to ntuple["FLUX_label_1"]

    >>> flux_field[0]
    corresponding to "FLUX_label_1"

    >>> flux[:, 0] - ntuple[flux_field[0]]
    should therefore return only zeroes. 
    

    It can also be useful to declare
    >>> class c:
    >>>    pass
    
    And then do
    >>> nacl.util.io.split(ntuple, globals(), two_D={"flux": "FLUX_.*"})

    This has the advantage of protecting the global namespace from polution. The
    data nacl.util.io.split from the NTuple being the accessible with things like

    >>> c.LAMBDA
    >>> c.flux[:,0]

    It is then easy to calculate sums, means and rms on the 2D arrays with
    things like
    >>> c.flux.mean(axis=1)
    to get the average flux spectrum
   
    """
    # list of ntuple fields, that will be consumed
    # as we deal with the fields
    l_ntuple_field = list(ntuple.dtype.names)

    # Looks for columns to group in 2D arrays:
    for key_two_D in list(two_D.keys()):
        l_field = []
        l_data = []        
        for ntuple_field in l_ntuple_field:
            if re.search(two_D[key_two_D], ntuple_field):
                # the ntuple_field is popped out in order to only leave vectors
                # once this loop is over
                l_data.append(ntuple[ntuple_field])
                l_field.append(ntuple_field)
            else:
                continue
        if len(l_field) != 0:
            # The .T is to inforce the Universal Matrix Convention
            d_output[key_two_D] = np.vstack(l_data).T
            d_output[key_two_D + field_output_suffix] = l_field

            # Update l_ntuple_field by popping out the used values:
            for field in l_field:
                l_ntuple_field.remove(field)
            
    for ntuple_field in l_ntuple_field:
        d_output[ntuple_field] = ntuple[ntuple_field]


class FortranDecription():
    """ Class to handle Fortran ReadMe files of the kind:
    
    --------------------------------------------------------------------------------
   Bytes Format  Units   Label    Explanations
--------------------------------------------------------------------------------
   1-  4  I4     ---     HR       [1/9110]+ Harvard Revised Number
                                    = Bright Star Number
   5- 14  A10    ---     Name     Name, generally Bayer and/or Flamsteed name
  15- 25  A11    ---     DM       Durchmusterung Identification (zone in
                                    bytes 17-19)
  26- 31  I6     ---     HD       [1/225300]? Henry Draper Catalog Number
  32- 37  I6     ---     SAO      [1/258997]? SAO Catalog Number
  38- 41  I4     ---     FK5      ? FK5 star Number
      42  A1     ---     IRflag   [I] I if infrared source
      43  A1     ---   r_IRflag  *[ ':] Coded reference for infrared source
      44  A1     ---    Multiple *[AWDIRS] Double or multiple-star code
  45- 49  A5     ---     ADS      Aitken's Double Star Catalog (ADS) designation
  50- 51  A2     ---     ADScomp  ADS number components
  52- 60  A9     ---     VarID    Variable star identification
  61- 62  I2     h       RAh1900  ?Hours RA, equinox B1900, epoch 1900.0 (1)
  63- 64  I2     min     RAm1900  ?Minutes RA, equinox B1900, epoch 1900.0 (1)
  65- 68  F4.1   s       RAs1900  ?Seconds RA, equinox B1900, epoch 1900.0 (1)
      69  A1     ---     DE-1900  ?Sign Dec, equinox B1900, epoch 1900.0 (1)
  70- 71  I2     deg     DEd1900  ?Degrees Dec, equinox B1900, epoch 1900.0 (1)
  72- 73  I2     arcmin  DEm1900  ?Minutes Dec, equinox B1900, epoch 1900.0 (1)
  74- 75  I2     arcsec  DEs1900  ?Seconds Dec, equinox B1900, epoch 1900.0 (1)
  76- 77  I2     h       RAh      ?Hours RA, equinox J2000, epoch 2000.0 (1)
  78- 79  I2     min     RAm      ?Minutes RA, equinox J2000, epoch 2000.0 (1)
  80- 83  F4.1   s       RAs      ?Seconds RA, equinox J2000, epoch 2000.0 (1)
      84  A1     ---     DE-      ?Sign Dec, equinox J2000, epoch 2000.0 (1)
  85- 86  I2     deg     DEd      ?Degrees Dec, equinox J2000, epoch 2000.0 (1)
  87- 88  I2     arcmin  DEm      ?Minutes Dec, equinox J2000, epoch 2000.0 (1)
  89- 90  I2     arcsec  DEs      ?Seconds Dec, equinox J2000, epoch 2000.0 (1)
  91- 96  F6.2   deg     GLON     ?Galactic longitude (1)
  97-102  F6.2   deg     GLAT     ?Galactic latitude (1)
 103-107  F5.2   mag     Vmag     ?Visual magnitude (1)
     108  A1     ---   n_Vmag    *[ HR] Visual magnitude code
     109  A1     ---   u_Vmag     [ :?] Uncertainty flag on V
 110-114  F5.2   mag     B-V      ? B-V color in the UBV system
     115  A1     ---   u_B-V      [ :?] Uncertainty flag on B-V
 116-120  F5.2   mag     U-B      ? U-B color in the UBV system
     121  A1     ---   u_U-B      [ :?] Uncertainty flag on U-B
 122-126  F5.2   mag     R-I      ? R-I   in system specified by n_R-I
     127  A1     ---   n_R-I      [CE:?D] Code for R-I system (Cousin, Eggen)
 128-147  A20    ---     SpType   Spectral type
     148  A1     ---   n_SpType   [evt] Spectral type code
 149-154  F6.3 arcsec/yr pmRA    *?Annual proper motion in RA J2000, FK5 system
 155-160  F6.3 arcsec/yr pmDE     ?Annual proper motion in Dec J2000, FK5 system
     161  A1     ---   n_Parallax [D] D indicates a dynamical parallax,
                                    otherwise a trigonometric parallax
 162-166  F5.3   arcsec  Parallax ? Trigonometric parallax (unless n_Parallax)
 167-170  I4     km/s    RadVel   ? Heliocentric Radial Velocity
 171-174  A4     ---   n_RadVel  *[V?SB123O ] Radial velocity comments
 175-176  A2     ---   l_RotVel   [<=> ] Rotational velocity limit characters
 177-179  I3     km/s    RotVel   ? Rotational velocity, v sin i
     180  A1     ---   u_RotVel   [ :v] uncertainty and variability flag on
                                    RotVel
 181-184  F4.1   mag     Dmag     ? Magnitude difference of double,
                                    or brightest multiple
 185-190  F6.1   arcsec  Sep      ? Separation of components in Dmag
                                    if occultation binary.
 191-194  A4     ---     MultID   Identifications of components in Dmag
 195-196  I2     ---     MultCnt  ? Number of components assigned to a multiple
     197  A1     ---     NoteFlag [*] a star indicates that there is a note
                                    (see file notes)
"""
    def __init__(self):
        self.fields = []
        self.bytes = []
        self.format = []
        self.unit = []
        self.Explanation = []
        
    def read_descr(self, description):
        for line in description.splitlines():
            if not line:
                continue
            entries = line.split()
            entries = [e.strip() for e in entries]
            if entries[0][0] not in "1234567890":
                continue
            entries.reverse()
            byterange = entries.pop().split('-')
            if len(byterange) == 1:
                self.bytes.append((int(byterange[0]) - 1, int(byterange[0])))
            elif len(byterange) == 2 and not byterange[1]:
                self.bytes.append((int(byterange[0]) - 1, int(entries.pop())))
            elif len(byterange) == 2 and byterange[1]:
                self.bytes.append((int(byterange[0]) - 1, int(byterange[1])))
            else:
                raise ValueError('Line not understood : ' + line)
            self.format.append(entries.pop())
            self.unit.append(entries.pop())
            self.fields.append(entries.pop())
            entries.reverse()
            self.Explanation.append(' '.join(entries))

    def read_file(self, fname):
        with open(fname) as fid:
            entries = []
            for line in fid:
                entries.append([convert_format(line[a:b], form) for (a, b), form in zip(self.bytes, self.format)])
        return entries

    def read_fid(self, fid):
        entries = []
        for line in fid:
            entries.append([convert_format(line[a:b], form) for (a, b), form in zip(self.bytes, self.format)])
        return entries

def find_fortran_description(filename, tablename):
    with open(filename) as fid:
        for line in fid:
            if line.startswith('Byte-by-byte Description of file: %s' % tablename):
                break
        descr = []
        for line in fid:
            if line.startswith('Byte-by-byte Description of file'):
                break
            descr.append(line)
    return ''.join(descr)

def readdescription(fid):
    descr = []
    sep = 0
    while (sep < 4):
        descr.append(fid.readline())
        if descr[-1].startswith("--"):
            sep += 1
    return "".join(descr)


class NTuple(np.ndarray):
    """ Add Toads-like file formatting to np record arrays

    Exemples
    --------
    >>> nt = NTuple.fromfile('filename.ntuple')
    >>> nt['col2'] += 1
    >>> nt.keys['modified'] = "by me"
    >>> nt.tofile('newfilename.ntuple')

    One may convert a classic np record array to benefit from the
    io function using the view mecanism:
    >>> a = array(zip(randn(10), randn(10)), {'names':['x','y'],'formats':('float',)*2})
    >>> b = a.view(NTuple)
    >>> b.tofile('filename.ntuple')
    """
    def __new__(subtype, shape, dtype=float, buffer=None, offset=0,
                strides=None, order=None, keys={}):
        obj = np.ndarray.__new__(subtype, shape, dtype, buffer,
                                    offset, strides, order)
        obj.keys = keys
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.keys = getattr(obj, 'keys', {})

    def __call__(self, *args, **keys):
        return select(self, *args, **keys)
        
    @classmethod
    def fromfile(cls, f, mmap_mode=None):
        own_fid = False
        if isinstance(f, str):
            fid = open(f, "rb")
            own_fid = True
        else:
            fid = f

        try:
            # try to distinguish from Np binary files and txt files.
            N = len(np.lib.format.MAGIC_PREFIX)
            magic = fid.read(N)
            fid.seek(-N, 1)  # back-up
            if magic == np.lib.format.MAGIC_PREFIX:
                if mmap_mode:
                    return open_memmap(f, mode=mmap_mode)
                else:
                    a, keys = read_array(fid)
                    a = a.view(NTuple)
                    a.keys = keys
                    return a
            else:
                if mmap_mode:
                    raise IOError("mmap mode not supported for txt files")
                if not own_fid:
                    raise IOError("f must be a filename, cannot read ascii"
                                  " data from existing file handle")
                import subprocess
                p = subprocess.Popen(['ntcat', '-b', f],
                                     stdout=subprocess.PIPE, bufsize=4096)
                a, keys = read_array(p.stdout)
                a = a.view(NTuple)
                a.keys = keys
                p.wait()
                return a
        finally:
            if own_fid:
                fid.close()

    def tofile(self, f, format=None):
        own_fid = False
        if isinstance(f, str):
            fid = open(f, "wb")
            own_fid = True
            if format is None:
                if f.endswith('.npy') or f.endswith('.nxt'):
                    format = "binary"
                else:
                    format = "txt"
        else:
            fid = f
            if format is None:
                format = "binary"
        try:
            if format == "binary":
                write_array(fid, self)
            else:
                import subprocess
                p = subprocess.Popen(['ntcat', '-'], stdout=fid,
                                     stdin=subprocess.PIPE, bufsize=4096)
                write_array(p.stdin, self)
                p.stdin.close()
                p.wait()
        finally:
            if own_fid:
                fid.close()
                
    def keys_to_list(self, key_string, dtype=None):
        key_string = self.keys[key_string]
        key_string = key_string.replace("[", "")
        key_string = key_string.replace("]", "")
        
        key_string = key_string.strip()
        l_key = key_string.split(",")
        
        if dtype is None:
            return np.array(l_key)
        else:
            return np.array(l_key, dtype=dtype)

                
    def totxt(self, filename=None):
        """
        Write the tuple to a *.list fileformat, with values that can
        be something else than doubles

        If filename is not provided, will write to stdout

        @key1 value
        @key2 value
        #value_name_1: description
        #value_name_2: description
        #end
        value1 value2
        value1 value2        
        """

        if filename is None:
            fh = sys.stdout
        else:
            fh = open(filename, "w")

        for key, value in self.keys.items():
            print("@%s %s" % (key, str(value)), file=fh)

        for name in self.dtype.names:
            print("#%s:" % (name), file=fh)
        print("#end", file=fh)

        tmp_line = ""
        for t_line in self:
            for name in self.dtype.names:
                tmp_line += "%-s  " % (str(t_line[name]))
            tmp_line += "\n"
        print(tmp_line, file=fh)
        if hasattr(self, 'm'):
            print("#MATRIX", file=fh)
            print("%d %d" % self.m.shape, file=fh)
            np.savetxt(fh, self.m)

    @classmethod
    def fromtxt(self, filename):
        comments = set(['#', '\n'])
        with open(filename, "r") as fid:
            keys, names = read_header(fid)
            records = []
            for line in fid:
                if line[0] in comments:
                    continue
                vals = line.split()
                records.append([convert(v) for v in vals])
        nt = np.rec.fromrecords(records, names=names).view(NTuple)
        nt.keys = keys
        return nt
    
    @classmethod
    def fromtxtslow(self, filename):
        """
        Read the tuple from a *.list fileformat, with values that can
        be something else than doubles

        @key1 value
        @key2 value
        #value_name_1: description
        #value_name_2: description
        #end
        value1 value2
        value1 value2
        """
        fh = open(filename, "r")

        d_key = {}
        l_name = []

        hasm = False
        l_line = []
        lines = fh.readlines()
        for i, line in enumerate(lines):
            if line.startswith('#MATRIX'):
                m = read_matrix(lines[i + 1:])
                hasm = True
                break
            if re.search("^#", line):
                if re.search(":", line):
                    line = line.split(":")[0]
                    line = re.sub("#", "", line)
                    line = re.sub("\s*", "", line)
                    line = line.strip()
                    if line == "end":
                        continue
                    else:
                        l_name.append(line)
                else:
                    #- a # without : means a comment
                    continue
            elif re.search("^@", line):
                group = re.search("@(.+?)\s+(.+)", line)
                group = group.groups()
                try:
                    d_key[group[0]] = float(group[1])
                except:
                    d_key[group[0]] = group[1]
            else:
                l_line.append(line)
        fh.close()

        l_value = []
        #- Check that the file contains actual data, not only a header
        if len(l_line) != 0:
            for line in l_line:
                #- remove comments
                line = line.split("#")[0]
                #- skip empty lines
                if re.search("^\s+$", line):
                    continue
                else:
                    line = line.strip()
                    line = re.sub("\s+", " ", line)
                    tmp_l_value = re.split("\s", line)
                    for (i_v, value) in enumerate(tmp_l_value):
                        try:
                            tmp_l_value[i_v] = int(value)
                        except ValueError:
                            try:
                                tmp_l_value[i_v] = float(value)
                            except ValueError:
                                continue
                    l_value.append(tmp_l_value)
            l_value = np.rec.fromrecords(l_value, names=l_name)
            l_value = l_value.view(NTuple)
            l_value.keys = d_key
            if hasm:
                l_value.m = m
        else:  # If the file has no actual data, we make a dummy empty recarray
            l_value = np.recarray((0,),
                                     dtype=[(name, "S1") for name in l_name])
            l_value = l_value.view(NTuple)
            l_value.keys = d_key
        return l_value

    @classmethod
    def fromsnana(self, filename):
        """Read the tuple from a *.dat snana format file.

        KEY1: value
        KEY2: value
        VARLIST: name1 name2 ...
        OBS: value1 value2
        OBS: value1 value2
        END:
        """
        fh = open(filename, "r")

        d_key = {}
        names = []
        hasm = False
        records = []
        
        for i, line in enumerate(fh):
            entries = line.split()
            if entries[0] == 'VARLIST:':
                names = entries[1:]
            elif entries[0] == "OBS:":
                records.append([convert(v) for v in entries[1:]])
            elif entries[0] == "END:":
                break
            else:
                d_key[entries[0][:-1]] = " ".join(entries[1:])
        fh.close()
        nt = np.rec.fromrecords(records, names=names)
        nt = nt.view(NTuple)
        nt.keys = d_key
        return nt

    @classmethod
    def fromorg(self, filename):
        fh = open(filename, "r")

        d_key = {}
        names = []
        records = []
        first = True        
        header_expr = re.compile(':\s*(.+)\s*:\s*(.+)\s*')
        
        lines = fh.readlines()
        fh.close()
        for i, line in enumerate(lines):
            if line.startswith(':'):
                try:
                    key, val = header_expr.match(line).groups()
                except:
                    raise ValueError('Line not understood : ' + line)
                try:
                    val = float(val)
                except:
                    pass
                d_key[key] = val
            if line.startswith('|-'):
                continue
            if line.startswith('|'):
                vals = line.split('|')[1:-1]
                if first:
                    names = [v.strip() for v in vals]
                    first = False
                else:
                    records.append([convert(v) for v in vals])

        nt = np.rec.fromrecords(records, names=names)
        nt = nt.view(NTuple)
        nt.keys = d_key
        return nt

    def toorg(self, filename=None):
        """
        Write the tuple to a .org file. 

        Parameters
        ----------
          - filename [str]: output file name 
                            if None, write to stdout instead

        """
        if filename is None:
            fh = sys.stdout
        else:
            fh = open(filename, 'w')
            
        # global keys 
        for key, value in self.keys.items():
            print(":%s: %s" % (key, str(value)), file=fh)
        
        # header 
        ncols = len(self.keys)
        line_sep = "|" + "-+"*(ncols-1) + "-|"
        print(line_sep, file=fh) 
        s = "| "
        for key in self.dtype.names:
            s += key ; s += " | "
        print(s, file=fh)
        print(line_sep, file=fh)
        
        # data 
        tmp_line = ""
        for t_line in self:
            for name in self.dtype.names:
                tmp_line += '| %-s ' % (str(t_line[name]))
            tmp_line += '|\n'
        print(tmp_line[:-1], file=fh)
        print(line_sep, file=fh) 
    
    @classmethod
    def fromcsv(self, filename):
        fh = open(filename, "r")

        d_key = {}
        names = []
        records = []
        first = True

        lines = fh.readlines()
        fh.close()
        for i, line in enumerate(lines):
            if line.startswith('%'):
                continue
            vals = line.split(',')
            if first:
                names = [v.strip() for v in vals]
                first = False
            else:
                records.append([convert(v) for v in vals])

        nt = np.rec.fromrecords(records, names=names)
        nt = nt.view(NTuple)
        nt.keys = d_key
        return nt

    @classmethod
    def fromfortran(self, filename, description):
        f = FortranDecription()
        f.read_descr(description)
        if isinstance(filename, str):
            nt = f.read_file(filename)
        else:
            nt = f.read_fid(filename)
        nt = np.rec.fromrecords(nt, names=f.fields)
        nt = nt.view(NTuple)
        nt.keys = {}
        return nt

# from numpy.lib.format
def _wrap_header(header, version):
    """
    Takes a stringified header, and attaches the prefix and padding to it
    """
    _header_size_info = {(1, 0): ('<H', 'latin1'), (2, 0): ('<I', 'latin1'), (3, 0): ('<I', 'utf8')}
    import struct
    assert version is not None
    fmt, encoding = _header_size_info[version]
    if not isinstance(header, bytes):  # always true on python 3
        header = header.encode(encoding)
    hlen = len(header) + 1
    padlen = np.lib.format.ARRAY_ALIGN - ((np.lib.format.MAGIC_LEN + struct.calcsize(fmt) + hlen) % np.lib.format.ARRAY_ALIGN)
    try:
        header_prefix = np.lib.format.magic(*version) + struct.pack(fmt, hlen + padlen)
    except struct.error:
        msg = "Header length {} too big for version={}".format(hlen, version)
        raise ValueError(msg)

    # Pad the header with spaces and a final newline such that the magic
    # string, the header-length short and the header are aligned on a
    # ARRAY_ALIGN byte boundary.  This supports memory mapping of dtypes
    # aligned up to ARRAY_ALIGN on systems like Linux where mmap()
    # offset must be page-aligned (i.e. the beginning of the file).
    return header_prefix + header + b' '*padlen + b'\n'

    
def write_array_header_1_0(fp, d):
    """ Write the header for an array using the 1.0 format.

    Parameters
    ----------
    fp : filelike object
    d : dict
        This has the appropriate entries for writing its string representation
        to the header of the file.
    """
    import struct
    header = ["{"]
    for key, value in sorted(d.items()):
        # Need to use repr here, since we eval these when reading
        header.append("'%s': %s, " % (key, repr(value)))
    header.append("}")
    header = "".join(header)
    header = _wrap_header(header, version=(1,0))
    fp.write(header)

def write_array(fp, array, version=(1, 0)):
    """
    Write an array to an NPY file, including a header.

    If the array is neither C-contiguous nor Fortran-contiguous AND the
    file_like object is not a real file object, this function will have to
    copy data in memory.

    Parameters
    ----------
    fp : file_like object
        An open, writable file object, or similar object with a ``.write()``
        method.
    array : ndarray
        The array to write to disk.
    version : (int, int), optional
        The version number of the format.  Default: (1, 0)

    Raises
    ------
    ValueError
        If the array cannot be persisted.
    Various other errors
        If the array contains Python objects as part of its dtype, the
        process of pickling them may raise various errors if the objects
        are not picklable.

    """
    if version != (1, 0):
        msg = "we only support format version (1,0), not %s"
        raise ValueError(msg % (version,))
    # magic number now handled in write_array_header_1_0
    #    fp.write(np.lib.format.magic(*version))
    write_array_header_1_0(fp, header_data_from_ntuple_1_0(array))
    array = np.asarray(array)
    if array.dtype.hasobject:
        # We contain Python objects so we cannot write out the data directly.
        # Instead, we will pickle it out with version 2 of the pickle protocol.
        cPickle.dump(array, fp, protocol=2)
    elif array.flags.f_contiguous and not array.flags.c_contiguous:
        if isinstance(fp, str):#file):
            fp.write(array.T.tostring('C'))
        else:
            array.T.tofile(fp)

    else:
        if isinstance(fp, str):
            fp.write(array.tostring('C'))
        else:
            # XXX: We could probably chunk this using something like
            # arrayterator.
            array.tofile(fp)


def header_data_from_ntuple_1_0(array):
    """ Get the dictionary of header metadata from a np.ndarray.

    Parameters
    ----------
    array : np.ndarray

    Returns
    -------
    d : dict
        This has the appropriate entries for writing its string representation
        to the header of the file.
    """
    d = {}
    d['shape'] = array.shape
    if array.flags.c_contiguous:
        d['fortran_order'] = False
    elif array.flags.f_contiguous:
        d['fortran_order'] = True
    else:
        # Totally non-contiguous data. We will have to make it C-contiguous
        # before writing. Note that we need to test for C_CONTIGUOUS first
        # because a 1-D array is both C_CONTIGUOUS and F_CONTIGUOUS.
        d['fortran_order'] = False

    d['descr'] = np.lib.format.dtype_to_descr(array.dtype)
    d['keys'] = array.keys
    for k in d['keys']:
        d['keys'][k] = str(d['keys'][k])

    return d


def read_array(fp):
    """
    Read an array from an NPY file.

    Parameters
    ----------
    fp : file_like object
        If this is not a real file object, then this may take extra memory
        and time.

    Returns
    -------
    array : ndarray
        The array from the data on disk.

    Raises
    ------
    ValueError
        If the data is invalid.

    """
    version = np.lib.format.read_magic(fp)
    if version != (1, 0):
        msg = "only support version (1,0) of file format, not %r"
        raise ValueError(msg % (version,))
    shape, fortran_order, dtype, keys = read_array_header_1_0(fp)
    if len(shape) == 0:
        count = 1
    else:
        count = np.multiply.reduce(shape)

    # Now read the actual data.
    if dtype.hasobject:
        # The array contained Python objects. We need to unpickle the data.
        array = cPickle.load(fp)
    else:
        try:
            # We can use the fast fromfile() function.
            array = np.fromfile(fp, dtype=dtype, count=count)
        except TypeError:
            # This is not a real file. We have to read it the memory-intensive
            # way.
            # XXX: we can probably chunk this to avoid the memory hit.
            data = fp.read(int(count * dtype.itemsize))
            array = np.fromstring(data, dtype=dtype, count=count)

        if fortran_order:
            array.shape = shape[::-1]
            array = array.transpose()
        else:
            array.shape = shape

    return array, keys


def read_array_header_1_0(fp):
    """
    Read an array header from a filelike object using the 1.0 file format
    version.

    This will leave the file object located just after the header.

    Parameters
    ----------
    fp : filelike object
        A file object or something with a `.read()` method like a file.

    Returns
    -------
    shape : tuple of int
        The shape of the array.
    fortran_order : bool
        The array data will be written out directly if it is either
        C-contiguous or Fortran-contiguous. Otherwise, it will be made
        contiguous before writing it out.
    dtype : dtype
        The dtype of the file's data.

    Raises
    ------
    ValueError :
        If the data is invalid.

    """
    # Read an unsigned, little-endian short int which has the length of the
    # header.
    import struct
    hlength_str = fp.read(2)
    if len(hlength_str) != 2:
        msg = "EOF at %s before reading array header length"
        raise ValueError(msg % fp.tell())
    header_length = struct.unpack('<H', hlength_str)[0]
    header = fp.read(header_length)
    if len(header) != header_length:
        raise ValueError("EOF at %s before reading array header" % fp.tell())

    # The header is a pretty-printed string representation of a literal Python
    # dictionary with trailing newlines padded to a 16-byte boundary. The keys
    # are strings.
    #   "shape" : tuple of int
    #   "fortran_order" : bool
    #   "descr" : dtype.descr
    #   "keys" : datacards
    try:
        d = safe_eval(header.decode())
    except SyntaxError as e:
        msg = "Cannot parse header: %r\nException: %r"
        raise ValueError(msg % (header, e))
    if not isinstance(d, dict):
        msg = "Header is not a dictionary: %r"
        raise ValueError(msg % d)
    keys = list(d.keys())
    keys.sort()
    if keys != ['descr', 'fortran_order', 'keys', 'shape']:
        if keys != ['descr', 'fortran_order', 'shape']:
            msg = "Header does not contain the correct keys: %r"
            raise ValueError(msg % (keys,))
        else:
            d['keys'] = {}

    # Sanity-check the values.
    if (not isinstance(d['shape'], tuple) or
        not np.all([isinstance(x, int) for x in d['shape']])):
        msg = "shape is not valid: %r"
        raise ValueError(msg % (d['shape'],))
    if not isinstance(d['fortran_order'], bool):
        msg = "fortran_order is not a valid bool: %r"
        raise ValueError(msg % (d['fortran_order'],))
    try:
        dtype = np.dtype(d['descr'])
    except TypeError as e:
        msg = "descr is not a valid dtype descriptor: %r"
        raise ValueError(msg % (d['descr'],))

    return d['shape'], d['fortran_order'], dtype, d['keys']


def open_memmap(filename, mode='r+', dtype=None, shape=None,
                fortran_order=False, version=(1, 0)):
    """
    Open a .npy file as a memory-mapped array.

    This may be used to read an existing file or create a new one.

    Parameters
    ----------
    filename : str
        The name of the file on disk.  This may *not* be a file-like
        object.
    mode : str, optional
        The mode in which to open the file; the default is 'r+'.  In
        addition to the standard file modes, 'c' is also accepted to
        mean "copy on write."  See `memmap` for the available mode strings.
    dtype : data-type, optional
        The data type of the array if we are creating a new file in "write"
        mode, if not, `dtype` is ignored.  The default value is None,
        which results in a data-type of `float64`.
    shape : tuple of int
        The shape of the array if we are creating a new file in "write"
        mode, in which case this parameter is required.  Otherwise, this
        parameter is ignored and is thus optional.
    fortran_order : bool, optional
        Whether the array should be Fortran-contiguous (True) or
        C-contiguous (False, the default) if we are creating a new file
        in "write" mode.
    version : tuple of int (major, minor)
        If the mode is a "write" mode, then this is the version of the file
        format used to create the file.  Default: (1,0)
    Returns
    -------
    marray : memmap
        The memory-mapped array.

    Raises
    ------
    ValueError
        If the data or the mode is invalid.
    IOError
        If the file is not found or cannot be opened correctly.

    See Also
    --------
    memmap

    """
    if not isinstance(filename, str):
        raise ValueError("Filename must be a string.  Memmap cannot use"
                         " existing file handles.")

    if 'w' in mode:
        # We are creating the file, not reading it.
        # Check if we ought to create the file.
        if version != (1, 0):
            msg = "only support version (1,0) of file format, not %r"
            raise ValueError(msg % (version,))
        # Ensure that the given dtype is an authentic dtype object rather than
        # just something that can be interpreted as a dtype object.
        dtype = np.dtype(dtype)
        if dtype.hasobject:
            msg = "Array can't be memory-mapped: Python objects in dtype."
            raise ValueError(msg)
        d = dict(
            descr=dtype_to_descr(dtype),
            fortran_order=fortran_order,
            shape=shape,
        )
        # If we got here, then it should be safe to create the file.
        fp = open(filename, mode + 'b')
        try:
            fp.write(magic(*version))
            write_array_header_1_0(fp, d)
            offset = fp.tell()
        finally:
            fp.close()
    else:
        # Read the header of the file first.
        fp = open(filename, 'rb')
        try:
            version = np.lib.format.read_magic(fp)
            if version != (1, 0):
                msg = "only support version (1,0) of file format, not %r"
                raise ValueError(msg % (version,))
            shape, fortran_order, dtype, keys = read_array_header_1_0(fp)
            if dtype.hasobject:
                msg = "Array can't be memory-mapped: Python objects in dtype."
                raise ValueError(msg)
            offset = fp.tell()
        finally:
            fp.close()

    if fortran_order:
        order = 'F'
    else:
        order = 'C'

    # We need to change a write-only mode to a read-write mode since we've
    # already written data to the file.
    if mode == 'w+':
        mode = 'r+'

    marray = np.memmap(filename, dtype=dtype, shape=shape, order=order,
                          mode=mode, offset=offset)

    return marray, keys


def find_odometer(template):
    existing_files = glob(template +'*.npy')
    existing_files = [int(f.replace('.npy', '').replace(template, '')) for f in existing_files]
    if not existing_files:
        print('Warning: first file in the serie')
        odometer = 0
    else:
        odometer = np.max(existing_files) + 1
    return odometer

class IFile(object):
    def __init__(self, names, filename=None, template='datafile_', freq=10, append=True):
        self.names = names
        self.res = []
        if filename is None:
            odometer = find_odometer(template)
            self.filename = '%s%04d.npy' % (template, odometer)
        else:
            self.filename = filename
            if os.path.exists(filename):
                if append:
                    print('File already exists, appending')
                    tab = np.load(filename)
                    self.res = [[t[n] for n in self.names] for t in tab]
                else:
                    print('Warning: File already exists, it will be overwriten')
        print('Data will be registered in ' + self.filename)
        self.freq = freq
        self.i = 0

    def __enter__(self):
        return self
    
    def __exit__(self, *exec_details):
        self.res = self._write()
                
    def _write(self):
        if self.res:
            tab = np.rec.fromrecords(self.res, names=self.names)
            np.save(self.filename, tab)
            self.i = 0
            return tab
    
    def append(self, *args):
        if len(args) != len(self.names):
            raise ValueError("Incorrect number of arguments. Append should be provided with %s" % str(self.names))
        self.i += 1
        self.res.append(args)
        if self.i == self.freq:
            self._write()
        
