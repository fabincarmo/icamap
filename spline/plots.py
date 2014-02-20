# -*- coding: utf-8 -*-

from numpy import linspace,size
from graf_tex import *

def espectrograma(sinal,arquivo,fs=8000.,jan=256,sobrepos=128):
    figure()
    subplot(211)
    plot(linspace(0,size(sinal)/fs,size(sinal)),sinal,'k')
    axis([0, size(sinal)/fs, -10, 10])
    subplot(212)
    Pxx,freqs,bins,im = specgram(sinal,Fs=fs,NFFT=jan,noverlap=sobrepos)
    axis([0.,size(Pxx)/fs,None,None])
    salvagraf(arquivo)
    return True

def plotc(s1,s2,s3,pasta):
    font = {'size' : 6}
    rc('font', **font)
    figure(figsize=(4,6))
    subplot(311)
    plot(linspace(0,size(s1)/8000.,size(s1)),s1,lw=.5,c='k')
    axis([0,size(s1)/8000.,-10,10])
    subplot(312)
    plot(linspace(0,size(s2)/8000.,size(s2)),s2,lw=.5,c='k')
    axis([0,size(s2)/8000.,-10,10])
    subplot(313)
    plot(linspace(0,size(s3)/8000.,size(s3)),s3,lw=.5,c='k')
    axis([0,size(s3)/8000.,-10,10])
    salvagraf(pasta+'/x_.pdf')


