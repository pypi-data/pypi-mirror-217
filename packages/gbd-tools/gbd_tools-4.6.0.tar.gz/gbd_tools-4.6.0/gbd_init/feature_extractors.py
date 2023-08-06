
# MIT License

# Copyright (c) 2023 Markus Iser, Karlsruhe Institute of Technology (KIT)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

import pandas as pd
import os
import glob

from gbd_core.contexts import suffix_list, identify
from gbd_core.api import GBD, GBDException
from gbd_core.util import eprint, confirm
from gbd_init.initializer import Initializer, InitializerException

try:
    from gbdc import extract_base_features, extract_gate_features, isohash
except ImportError:
    def extract_base_features(path, tlim, mlim):
        return [ ]

    def extract_gate_features(path, tlim, mlim):
        return [ ]
    
    def isohash(path):
        return [ ]


## GBDHash
def compute_hash(hash, path, limits):
    eprint('Hashing {}'.format(path))
    hash = identify(path)
    return [ ("local", hash, path), ("filename", hash, os.path.basename(path)) ]

## ISOHash
def compute_isohash(hash, path, limits):
    eprint('Computing ISOHash for {}'.format(path))
    ihash = isohash(path)
    return [ ('isohash', hash, ihash) ]

## Base Features
def compute_base_features(hash, path, limits):
    eprint('Extracting base features from {} {}'.format(hash, path))
    rec = extract_base_features(path, limits['tlim'], limits['mlim'])
    return [ (key, hash, int(value) if isinstance(value, float) and value.is_integer() else value) for key, value in rec.items() ]

## Gate Features
def compute_gate_features(hash, path, limits):
    eprint('Extracting gate features from {} {}'.format(hash, path))
    rec = extract_gate_features(path, limits['tlim'], limits['mlim'])
    return [ (key, hash, int(value) if isinstance(value, float) and value.is_integer() else value) for key, value in rec.items() ]   


generic_extractors = {
    "base" : {
        "contexts" : [ "cnf" ],
        "features" : [ ("base_features_runtime", "empty"), ("clauses", "empty"), ("variables", "empty"), ("clause_size_1", "empty"), ("clause_size_2", "empty"), ("clause_size_3", "empty"), 
            ("clause_size_4", "empty"), ("clause_size_5", "empty"), ("clause_size_6", "empty"), ("clause_size_7", "empty"), ("clause_size_8", "empty"), ("clause_size_9", "empty"), 
            ("horn_clauses", "empty"), ("inv_horn_clauses", "empty"), ("positive_clauses", "empty"), ("negative_clauses", "empty"),
            ("horn_vars_mean", "empty"), ("horn_vars_variance", "empty"), ("horn_vars_min", "empty"), ("horn_vars_max", "empty"), ("horn_vars_entropy", "empty"),
            ("inv_horn_vars_mean", "empty"), ("inv_horn_vars_variance", "empty"), ("inv_horn_vars_min", "empty"), ("inv_horn_vars_max", "empty"), ("inv_horn_vars_entropy", "empty"),
            ("vg_degrees_mean", "empty"), ("vg_degrees_variance", "empty"), ("vg_degrees_min", "empty"), ("vg_degrees_max", "empty"), ("vg_degrees_entropy", "empty"),
            ("balance_clause_mean", "empty"), ("balance_clause_variance", "empty"), ("balance_clause_min", "empty"), ("balance_clause_max", "empty"), ("balance_clause_entropy", "empty"),
            ("balance_vars_mean", "empty"), ("balance_vars_variance", "empty"), ("balance_vars_min", "empty"), ("balance_vars_max", "empty"), ("balance_vars_entropy", "empty"),
            ("vcg_vdegrees_mean", "empty"), ("vcg_vdegrees_variance", "empty"), ("vcg_vdegrees_min", "empty"), ("vcg_vdegrees_max", "empty"), ("vcg_vdegrees_entropy", "empty"),
            ("vcg_cdegrees_mean", "empty"), ("vcg_cdegrees_variance", "empty"), ("vcg_cdegrees_min", "empty"), ("vcg_cdegrees_max", "empty"), ("vcg_cdegrees_entropy", "empty"),
            ("cg_degrees_mean", "empty"), ("cg_degrees_variance", "empty"), ("cg_degrees_min", "empty"), ("cg_degrees_max", "empty"), ("cg_degrees_entropy", "empty") ],
        "compute" : compute_base_features,
    },
    "gate" : {
        "contexts" : [ "cnf" ],
        "features" : [ ("gate_features_runtime", "empty"), ("n_vars", "empty"), ("n_gates", "empty"), ("n_roots", "empty"),
            ("n_none", "empty"), ("n_generic", "empty"), ("n_mono", "empty"), ("n_and", "empty"), ("n_or", "empty"), ("n_triv", "empty"), ("n_equiv", "empty"), ("n_full", "empty"),
            ("levels_mean", "empty"), ("levels_variance", "empty"), ("levels_min", "empty"), ("levels_max", "empty"), ("levels_entropy", "empty"),
            ("levels_none_mean", "empty"), ("levels_none_variance", "empty"), ("levels_none_min", "empty"), ("levels_none_max", "empty"), ("levels_none_entropy", "empty"),
            ("levels_generic_mean", "empty"), ("levels_generic_variance", "empty"), ("levels_generic_min", "empty"), ("levels_generic_max", "empty"), ("levels_generic_entropy", "empty"),
            ("levels_mono_mean", "empty"), ("levels_mono_variance", "empty"), ("levels_mono_min", "empty"), ("levels_mono_max", "empty"), ("levels_mono_entropy", "empty"),
            ("levels_and_mean", "empty"), ("levels_and_variance", "empty"), ("levels_and_min", "empty"), ("levels_and_max", "empty"), ("levels_and_entropy", "empty"),
            ("levels_or_mean", "empty"), ("levels_or_variance", "empty"), ("levels_or_min", "empty"), ("levels_or_max", "empty"), ("levels_or_entropy", "empty"),
            ("levels_triv_mean", "empty"), ("levels_triv_variance", "empty"), ("levels_triv_min", "empty"), ("levels_triv_max", "empty"), ("levels_triv_entropy", "empty"),
            ("levels_equiv_mean", "empty"), ("levels_equiv_variance", "empty"), ("levels_equiv_min", "empty"), ("levels_equiv_max", "empty"), ("levels_equiv_entropy", "empty"),
            ("levels_full_mean", "empty"), ("levels_full_variance", "empty"), ("levels_full_min", "empty"), ("levels_full_max", "empty"), ("levels_full_entropy", "empty") ],
        "compute" : compute_gate_features,
    },
    "isohash" : {
        "contexts" : [ "cnf" ],
        "features" : [ ("isohash", "empty") ],
        "compute" : compute_isohash,
    },
}


def init_features_generic(key: str, api: GBD, rlimits, df, target_db):
    einfo = generic_extractors[key]
    context = api.database.dcontext(target_db)
    if not context in einfo["contexts"]:
        raise InitializerException("Target database context must be in {}".format(einfo["contexts"]))
    extractor = Initializer(api, rlimits, target_db, einfo["features"], einfo["compute"])
    extractor.create_features()
    extractor.run(df)


def init_local(api: GBD, rlimits, root, target_db):
    context = api.database.dcontext(target_db)
    
    features = [ ("local", None), ("filename", None) ]
    extractor = Initializer(api, rlimits, target_db, features, compute_hash)
    extractor.create_features()

    # Cleanup stale entries
    df = api.query(group_by=context + ":local")
    dfilter = df["local"].apply(lambda x: not x or not os.path.isfile(x))
    missing = df[dfilter]
    if len(missing) and api.verbose:
        for path in missing["local"].tolist():
            eprint(path)
    if len(missing) and confirm("{} files not found. Remove stale entries from local table?".format(len(missing))):
        api.reset_values("local", values=missing["local"].tolist())

    # Create df with paths not yet in local table
    paths = [ path for suffix in suffix_list(context) for path in glob.iglob(root + "/**/*" + suffix, recursive=True) ]
    df2 = pd.DataFrame([(None, path) for path in paths if not path in df["local"].to_list()], columns=["hash", "local"])
    
    extractor.run(df2)