# -*- coding: utf-8 -*-

from scikits.audiolab import flacread,flacwrite
from numpy import asarray

def carregar_audio(arquivo):
    sinal, fs, enc = flacread(arquivo)
    return asarray(sinal)

def gravar_audio(sinal,arquivo,fs=8000,enc='pcm16'):
    sinal = asarray(sinal)
    sinal /= max (abs(sinal))
    flacwrite(sinal,arquivo,fs,enc)
    return True