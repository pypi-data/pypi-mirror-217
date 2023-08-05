# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/99_init.ipynb (unless otherwise specified).


from __future__ import annotations


__all__ = []

# Internal Cell
#nbdev_comment from __future__ import annotations

__author__ = "Floris Laporte"
__version__ = "0.8.8"

# Cell
from functools import partial as partial
from math import pi as pi

from scipy.constants import c as c

try:
    from flax.core.frozen_dict import FrozenDict as FrozenDict
except ImportError:
    FrozenDict = dict

# Cell

from sax import typing_ as typing
from .typing_ import (
    Array as Array,
    ComplexFloat as ComplexFloat,
    Float as Float,
    Model as Model,
    ModelFactory as ModelFactory,
    Models as Models,
    SCoo as SCoo,
    SDense as SDense,
    SDict as SDict,
    Settings as Settings,
    SType as SType,
    is_complex as is_complex,
    is_complex_float as is_complex_float,
    is_float as is_float,
    is_mixedmode as is_mixedmode,
    is_model as is_model,
    is_model_factory as is_model_factory,
    is_multimode as is_multimode,
    is_scoo as is_scoo,
    is_sdense as is_sdense,
    is_sdict as is_sdict,
    is_singlemode as is_singlemode,
    modelfactory as modelfactory,
    scoo as scoo,
    sdense as sdense,
    sdict as sdict,
    validate_model as validate_model,
)

# Cell

from sax import utils as utils
from .utils import (
    block_diag as block_diag,
    clean_string as clean_string,
    copy_settings as copy_settings,
    flatten_dict as flatten_dict,
    get_inputs_outputs as get_inputs_outputs,
    get_port_combinations as get_port_combinations,
    get_ports as get_ports,
    get_settings as get_settings,
    grouped_interp as grouped_interp,
    merge_dicts as merge_dicts,
    mode_combinations as mode_combinations,
    reciprocal as reciprocal,
    rename_params as rename_params,
    rename_ports as rename_ports,
    try_float as try_float,
    unflatten_dict as unflatten_dict,
    update_settings as update_settings,
    validate_multimode as validate_multimode,
    validate_not_mixedmode as validate_not_mixedmode,
    validate_sdict as validate_sdict,
    validate_settings as validate_settings,
)

# Cell

from sax import multimode as multimode
from .multimode import (
    multimode as multimode,
    singlemode as singlemode,
)

# Cell

from sax import models as models
from .models import get_models as get_models, passthru as passthru

# Cell

from .netlist import netlist as netlist
from .netlist import load_netlist as load_netlist
from .netlist import load_recursive_netlist as load_recursive_netlist

# Cell

from .circuit import circuit as circuit
from .circuit import get_required_circuit_models as get_required_circuit_models

# Cell

from sax import backends as backends

# Cell

from sax import patched as _patched