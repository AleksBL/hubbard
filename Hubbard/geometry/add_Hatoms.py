"""

:mod:`Hubbard.geometry`
==========================

Function to generate graphene-based geometries

.. currentmodule:: Hubbard.geometry

"""

from __future__ import print_function
import numpy as np
import sisl

def add_Hatoms(geom, d=1.1, sp3=[]):
    ''' Function to saturate edge C atoms with Hydrogen'''
    Hxyz = []
    for ia in geom:
        idx = geom.close(ia, R=(0.1, 1.43))
        if len(idx[1]) == 2:
            a, b = idx[1]
            v1 = geom.axyz(a) - geom.xyz[ia,:]
            v2 = geom.axyz(b) - geom.xyz[ia,:]
            p = -1*(v1 + v2)
            p = p * d / ( (p**2).sum() )**0.5
            Hxyz.append(p+geom.xyz[ia, :])
            if ia in sp3:
                Hxyz[-1][2] -= 0.9
                p = Hxyz[-1]-geom.xyz[ia, :]
                p = p * d / ( (p**2).sum() )**0.5
                Hxyz[-1] = p + geom.xyz[ia, :]
                Hxyz.append(Hxyz[-1]*1.0)
                Hxyz[-1][2] -= 2*Hxyz[-1][2]
    Hgeom = sisl.Geometry(Hxyz, atom=sisl.Atom(Z=1, R=d), sc=geom.sc)
    return geom.add(Hgeom)