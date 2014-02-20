# -*- coding: utf-8 -*- 

from numpy import asarray,shape,size
import sys
import dggm

class icamapgen:
    
    def __init__(self,Wx,betax,Wv=None,betav=None,lamb = .01, maxits=8000,ruido=1.,limg=100):
        self.Wx = asarray(Wx)
        self.betax = betax
        self.Wv = asarray(Wv)
        self.betav = betav
        self.N = shape(Wx)[0]
        self.maxits = maxits
        self.lamb = lamb
        self.ruido = ruido
        self.limg = limg
        self.jang = 64 # tamanho da janela do gradiente para cálculo da média

    def gen(self,sinal):
        T = size(sinal)
        #sinal = concatenate((zeros(self.N-1),sinal))
        #saida = randn(size(sinal)) 
        saida = sinal.copy() * .9 # estimativa inicial do sinal limpo
        sys.stdout.write("\rExecutando...                                     ")
        sys.stdout.flush()
		# chama o código em Fortran
        dggm.alggrad(saida,
                     sinal,
                     self.betax,
                     self.betav,
                     self.Wx,
                     self.Wv,
                     self.ruido,
                     self.lamb,
                     self.maxits,
                     self.limg
						)
        return sinal[-T:],saida[-T:]
        
        
    def aplicar(self,sinal):
        self.entrada = sinal
        s = self.gen(sinal)
        return s



