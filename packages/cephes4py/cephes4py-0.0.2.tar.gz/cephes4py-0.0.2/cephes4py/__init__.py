import _cephes4py
import logging

import numpy as np
from ._test import test

from _cephes4py.lib import hcephes_bdtr as bdtr
from _cephes4py.lib import hcephes_bdtrc as bdtrc
from _cephes4py.lib import hcephes_bdtri as bdtri
from _cephes4py.lib import hcephes_beta as beta
from _cephes4py.lib import hcephes_btdtr as btdtr
from _cephes4py.lib import hcephes_cabs as cabs
from _cephes4py.lib import hcephes_cbrt as cbrt
from _cephes4py.lib import hcephes_chbevl as chbevl
from _cephes4py.lib import hcephes_chdtr as chdtr
from _cephes4py.lib import hcephes_chdtrc as chdtrc
from _cephes4py.lib import hcephes_chdtri as chdtri
from _cephes4py.lib import hcephes_cosm1 as cosm1
from _cephes4py.lib import hcephes_dawsn as dawsn
from _cephes4py.lib import hcephes_ei as ei
from _cephes4py.lib import hcephes_ellie as ellie
from _cephes4py.lib import hcephes_ellik as ellik
from _cephes4py.lib import hcephes_ellpe as ellpe
from _cephes4py.lib import hcephes_ellpk as ellpk
from _cephes4py.lib import hcephes_erf as erf
from _cephes4py.lib import hcephes_erfc as erfc
from _cephes4py.lib import hcephes_erfce as erfce
from _cephes4py.lib import hcephes_euclid as euclid
from _cephes4py.lib import hcephes_expm1 as expm1
from _cephes4py.lib import hcephes_expn as expn
from _cephes4py.lib import hcephes_expx2 as expx2
from _cephes4py.lib import hcephes_fac as fac
from _cephes4py.lib import hcephes_fdtr as fdtr
from _cephes4py.lib import hcephes_fdtrc as fdtrc
from _cephes4py.lib import hcephes_fdtri as fdtri
from _cephes4py.lib import hcephes_gamma as gamma
from _cephes4py.lib import hcephes_gdtr as gdtr
from _cephes4py.lib import hcephes_gdtrc as gdtrc
from _cephes4py.lib import hcephes_hyp2f0 as hyp2f0
from _cephes4py.lib import hcephes_hyp2f1 as hyp2f1
from _cephes4py.lib import hcephes_hyperg as hyperg
from _cephes4py.lib import hcephes_hypot as hypot
from _cephes4py.lib import hcephes_i0 as i0
from _cephes4py.lib import hcephes_i0e as i0e
from _cephes4py.lib import hcephes_i1 as i1
from _cephes4py.lib import hcephes_i1e as i1e
from _cephes4py.lib import hcephes_igam as igam
from _cephes4py.lib import hcephes_igamc as igamc
from _cephes4py.lib import hcephes_igami as igami
from _cephes4py.lib import hcephes_incbet as incbet
from _cephes4py.lib import hcephes_incbi as incbi
from _cephes4py.lib import hcephes_iv as iv
from _cephes4py.lib import hcephes_j0 as j0
from _cephes4py.lib import hcephes_j1 as j1
from _cephes4py.lib import hcephes_jn as jn
from _cephes4py.lib import hcephes_jv as jv
from _cephes4py.lib import hcephes_k0 as k0
from _cephes4py.lib import hcephes_k0e as k0e
from _cephes4py.lib import hcephes_k1 as k1
from _cephes4py.lib import hcephes_k1e as k1e
from _cephes4py.lib import hcephes_kn as kn
from _cephes4py.lib import hcephes_kolmogi as kolmogi
from _cephes4py.lib import hcephes_kolmogorov as kolmogorov
from _cephes4py.lib import hcephes_lbeta as lbeta
from _cephes4py.lib import hcephes_lgam_sgn as lgam_sgn
from _cephes4py.lib import hcephes_lgam as lgam
from _cephes4py.lib import hcephes_log1p as log1p
from _cephes4py.lib import hcephes_nbdtr as nbdtr
from _cephes4py.lib import hcephes_nbdtrc as nbdtrc
from _cephes4py.lib import hcephes_nbdtri as nbdtri
from _cephes4py.lib import hcephes_ndtr as ndtr
from _cephes4py.lib import hcephes_ndtri as ndtri
from _cephes4py.lib import hcephes_onef2 as onef2
from _cephes4py.lib import hcephes_p1evl as p1evl
from _cephes4py.lib import hcephes_pdtr as pdtr
from _cephes4py.lib import hcephes_pdtrc as pdtrc
from _cephes4py.lib import hcephes_pdtri as pdtri
from _cephes4py.lib import hcephes_planckc as planckc
from _cephes4py.lib import hcephes_planckd as planckd
from _cephes4py.lib import hcephes_plancki as plancki
from _cephes4py.lib import hcephes_planckw as planckw
from _cephes4py.lib import hcephes_polevl as polevl
from _cephes4py.lib import hcephes_polylog as polylog
from _cephes4py.lib import hcephes_powi as powi
from _cephes4py.lib import hcephes_psi as psi
from _cephes4py.lib import hcephes_simpsn as simpsn
from _cephes4py.lib import hcephes_smirnov as smirnov
from _cephes4py.lib import hcephes_smirnovi as smirnovi
from _cephes4py.lib import hcephes_spence as spence
from _cephes4py.lib import hcephes_stdtr as stdtr
from _cephes4py.lib import hcephes_stdtri as stdtri
from _cephes4py.lib import hcephes_struve as struve
from _cephes4py.lib import hcephes_threef0 as threef0
from _cephes4py.lib import hcephes_y0 as y0
from _cephes4py.lib import hcephes_y1 as y1
from _cephes4py.lib import hcephes_yn as yn
from _cephes4py.lib import hcephes_yv as yv
from _cephes4py.lib import hcephes_zetac as zetac
from _cephes4py.lib import hcephes_airy as airy
from _cephes4py.lib import hcephes_drand as drand
from _cephes4py.lib import hcephes_fresnl as fresnl
from _cephes4py.lib import hcephes_mtherr as mtherr
from _cephes4py.lib import hcephes_poldiv as poldiv
from _cephes4py.lib import hcephes_polrt as polrt
from _cephes4py.lib import hcephes_shichi as shichi
from _cephes4py.lib import hcephes_sici as sici
from _cephes4py.lib import hcephes_cadd as cadd
from _cephes4py.lib import hcephes_cdiv as cdiv
from _cephes4py.lib import hcephes_cmov as cmov
from _cephes4py.lib import hcephes_cmul as cmul
from _cephes4py.lib import hcephes_cneg as cneg
from _cephes4py.lib import hcephes_csqrt as csqrt
from _cephes4py.lib import hcephes_csub as csub
from _cephes4py.lib import hcephes_poladd as poladd
from _cephes4py.lib import hcephes_polclr as polclr
from _cephes4py.lib import hcephes_polmov as polmov
from _cephes4py.lib import hcephes_polmul as polmul
from _cephes4py.lib import hcephes_polsbt as polsbt
from _cephes4py.lib import hcephes_polsub as polsub
from _cephes4py.lib import hcephes_radd as radd
from _cephes4py.lib import hcephes_rdiv as rdiv
from _cephes4py.lib import hcephes_revers as revers
from _cephes4py.lib import hcephes_rmul as rmul
from _cephes4py.lib import hcephes_rsub as rsub


__all__ = [
    "__version__",
    "bdtr",
    "bdtrc",
    "bdtri",
    "beta",
    "btdtr",
    "cabs",
    "cbrt",
    "chbevl",
    "chdtr",
    "chdtrc",
    "chdtri",
    "cosm1",
    "dawsn",
    "ei",
    "ellie",
    "ellik",
    "ellpe",
    "ellpk",
    "erf",
    "erfc",
    "erfce",
    "euclid",
    "expm1",
    "expn",
    "expx2",
    "fac",
    "fdtr",
    "fdtrc",
    "fdtri",
    "gamma",
    "gdtr",
    "gdtrc",
    "hyp2f0",
    "hyp2f1",
    "hyperg",
    "hypot",
    "i0",
    "i0e",
    "i1",
    "i1e",
    "igam",
    "igamc",
    "igami",
    "incbet",
    "incbi",
    "iv",
    "j0",
    "j1",
    "jn",
    "jv",
    "k0",
    "k0e",
    "k1",
    "k1e",
    "kn",
    "kolmogi",
    "kolmogorov",
    "lbeta",
    "lgam_sgn",
    "lgam",
    "log1p",
    "nbdtr",
    "nbdtrc",
    "nbdtri",
    "ndtr",
    "ndtri",
    "onef2",
    "p1evl",
    "pdtr",
    "pdtrc",
    "pdtri",
    "planckc",
    "planckd",
    "plancki",
    "planckw",
    "polevl",
    "polylog",
    "powi",
    "psi",
    "simpsn",
    "smirnov",
    "smirnovi",
    "spence",
    "stdtr",
    "stdtri",
    "struve",
    "threef0",
    "y0",
    "y1",
    "yn",
    "yv",
    "zetac",
    "airy",
    "drand",
    "fresnl",
    "mtherr",
    "poldiv",
    "polrt",
    "shichi",
    "sici",
    "cadd",
    "cdiv",
    "cmov",
    "cmul",
    "cneg",
    "csqrt",
    "csub",
    "poladd",
    "polclr",
    "polmov",
    "polmul",
    "polsbt",
    "polsub",
    "radd",
    "rdiv",
    "revers",
    "rmul",
    "rsub",
]


# Register with Numba
numba_installed = False
try:
    import numba
    numba_installed = True
except ModuleNotFoundError as _:
    pass

if numba_installed:
    try:
        from numba.core.typing.cffi_utils import register_module as _register_module
        _register_module(_cephes4py)
    except ModuleNotFoundError as _:
        logging.warn("Failed to register Cephes bindings to Numba. You will be unable to call the bindings in Numba-jitted functions in nopython mode.")


def np_from_buf(a: np.array):
    """ 
    Utility function to automatically get the C type and call FFI().from_buffer().
    Very primitive. Example:
    >> array = np.zeros(29, dtype=np.float_)
    >> array[:] = -8
    >> cephes4py.chbevl(2, cephes4py.to_buf(array), 32)
    """
    t = a.dtype.name
    if t.startswith('float'):
        ct = 'double[]'
    elif t.startswith('int'):
        ct = 'long[]'
    else:
        raise ValueError("Numpy array can only have type float or integer.")
    return _cephes4py.ffi.from_buffer(ct, a)
    

def from_buffer(type, array):
    return _cephes4py.ffi.from_buffer(type, array)