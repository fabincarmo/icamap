# -*- coding: utf-8 -*-

from scikits.audiolab import flacread
from numpy import asarray

def carregar_audio(arquivo):
    sinal, fs, enc = flacread(arquivo)
    return asarray(sinal)

