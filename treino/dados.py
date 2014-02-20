# -*- coding: utf-8 -*-
import sys
from scipy.io import savemat
from numpy import asarray,mean,sqrt,size,array,append,reshape
    
def gravar_dados(arquivo,W,beta):
    dicionario = {'W' : W , 'beta': beta }
    savemat(arquivo,dicionario)
    return True
    
def normalizar(sinal1d,variancia):
    sinal1d = sinal1d - mean(sinal1d)
    out = asarray(sinal1d)
    out /= sqrt(variancia)
    return out
    
class TXT:
    
    def __init__(self,nome):
        self.arq = open(nome+'.txt',"w")
        
    def linha(self,texto):
        self.arq.write(texto+'\n')
    
    def fechar(self):
        self.arq.close()
        
### monta a matriz a partir de um vetor:
### vetor vy(t) = [y(t), y(t-1), ... , y(t-N+1)]
### matriz Y = [vy(0), vy(1), ... vy(T-1)]
def v2m(v,N):
    TAM = size(v)
    m = array([])
    for i in range(0,N):
        m = append(m,v[i:i+TAM-N+1])
    return reshape(m,(N,TAM-N+1))[::-1]

