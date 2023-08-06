"""
Translated from https://github.com/flaport/sax or https://github.com/flaport/photontorch/tree/master
"""
import sax
from ....config import nso


def waveguide(wl=1.55, wl0=1.55, neff=2.34, ng=3.4, length=10.0, loss=0.0):
    dwl = wl - wl0
    dneff_dwl = (ng - neff) / wl0
    neff = neff - dwl * dneff_dwl
    phase = 2 * nso.pi * neff * length / wl
    amplitude = nso.asarray(10 ** (-loss * length / 20), dtype=complex)
    transmission = amplitude * nso.exp(1j * phase)
    sdict = sax.reciprocal({("o1", "o2"): transmission})
    return sdict


def simple_straight(length=10.0, width=0.5):
    S = {("o1", "o2"): 1.0}  # we'll improve this model later!
    return sax.reciprocal(S)


__all__ = ["waveguide", "simple_straight"]
