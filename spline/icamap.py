# -*- coding: utf-8 -*- 

# USAGE: python2.7 icamap.py <voz> <ruido> <iterations> <lambda> <SNR inicial>

from numpy import asarray,shape,size,linspace,argwhere,max,sqrt,array
import sys
import dggm
from modelo import derivfun,fun_c
from numpy import zeros
from pylab import *
from graf_tex import *

class icamapgen:

    def __init__(self,Wx,betax,Wv=None,betav=None,lamb = .01, maxits=8000,ruido=1.,limiar=0.,glim=100):
        self.Wx = array(Wx,order='F')
        self.betax = array(betax,order='F')
        self.Wv = asarray(Wv,order='F')
        self.betav = array(betav,order='F')
        self.N = shape(Wx)[0]
        self.maxits = maxits
        self.lamb = lamb
        self.ruido = ruido
        self.limiar = limiar
        self.glim=glim
        self.jang = 64

    def seta_lim(self):
        self.splinex = array([])
        self.splinev = array([])
        self.paramsx = array([])
        self.paramsv = array([])
        t = linspace(-.1,.1,1000000)
        for w in range(64):
            fx = derivfun(self.ruido,self.betax[w],t)
            limx = abs(t[argwhere(abs(fx)>self.glim)[0][0]])
            fv = derivfun(self.ruido,self.betav[w],t)
            if any(abs(fv>self.glim)):
                limv = abs(t[argwhere(abs(fv)>self.glim)[0][0]])
            else:
                limv = 0.
            self.splinex = append(self.splinex,limx)
            self.splinev = append(self.splinev,limv)
            p0x = -(2.*fun_c(max(self.betax[w]))/((1.+max(self.betax[w]))*sqrt(1.)))*((limx/sqrt(1.))**((1.-max(self.betax[w]))/(1.+max(self.betax[w]))))
            p1x = -p0x.copy()
            m0x = (2./(1.+max(self.betax[w]))-1.)*(2.*fun_c(max(self.betax[w]))/(1.+max(self.betax[w]))/sqrt(1.))*((limx/sqrt(1.))**(-2.*max(self.betax[w])/(1.+max(self.betax[w]))))
            m1x = m0x.copy()
            self.paramsx = append(self.paramsx,array([p0x,m0x,p1x,m1x]))
            p0v = -(2.*fun_c(max(self.betav[w]))/((1.+max(self.betav[w]))*sqrt(self.ruido)))*((limv/sqrt(self.ruido))**((1.-max(self.betav[w]))/(1.+max(self.betav[w]))))
            p1v = -p0v.copy()
            m0v = (2./(1.+max(self.betav[w]))-1.)*(2.*fun_c(max(self.betav[w]))/(1.+max(self.betav[w]))/sqrt(self.ruido))*((limv/sqrt(self.ruido))**(-2.*max(self.betav[w])/(1.+max(self.betav[w]))))
            m1v = m0v.copy()
            self.paramsv = append(self.paramsv,array([p0v,m0v,p1v,m1v]))
        self.paramsx = reshape(self.paramsx,(64,4))
        self.paramsv = reshape(self.paramsv,(64,4))

    def gen(self,sinal):
        T=size(sinal)
        sinal = concatenate((zeros(63),sinal))
        self.seta_lim()
        saida = array(sinal.copy() * .9,order='F')
        sys.stdout.write("\rExecutando...                                     ")
        sys.stdout.flush()
        dggm.alggrad(saida,
                     sinal,
                     self.betax,
                     self.betav,
                     self.Wx,
                     self.Wv,
                     self.ruido,
                     self.lamb,
                     self.maxits,
                     self.splinex,
                     self.splinev,
                     self.paramsx,
                     self.paramsv
						)
        return sinal[-T:],saida[-T:]

        
    def aplicar(self,sinal):
        self.entrada = sinal
        s = self.gen(sinal)
        return s





