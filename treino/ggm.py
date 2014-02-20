# -*- coding: utf-8 -*-
import sys
from numpy import asarray,append,sign,mean,array
from pylab import figure,plot
from modelo import gradiente_N

class ggm:

    def __init__(self , lamb , beta_inicial , N , label):
        self.lambd = lamb # passo do algoritmo gradiente
        self.Bini = beta_inicial # chute inicial
        self.N = 1
        self.Bevol = asarray([self.Bini]) # evolução de beta
        self.Gevol = asarray([]) # evolução do gradiente
        self.beta = None
        self.label=label
        
    def estima_beta(self,inM,comp,maxit=3000,restr=-.8,limc=5e-1):
        Bnew = self.Bini
        for i in range(0,maxit): # maximo de iterações
            Bold = Bnew
            gradi = gradiente_N(array(inM),Bold)
            self.Gevol = append(self.Gevol,gradi) # salva evolução do gradiente
            Bnew = Bold + self.lambd*gradi # atualiza beta
            sys.stdout.write("\rComp:%s  It:%s   B:%.4f   Grad:%.4f" % (comp+1,i,Bnew,gradi))
            sys.stdout.flush()
            if Bold < restr: # restrição beta > [valor]
                Bold = restr
            self.Bevol = append(self.Bevol,Bnew)
            # escapa, se atender o limiar
            if abs(gradi)<limc: # limiar de convergência 
                break
        self.beta = self.Bevol[-1:][0]
        return self.beta

