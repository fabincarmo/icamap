# -*- coding: utf-8 -*-

from scipy.io import loadmat,savemat
from numpy import asarray,sqrt,reshape,size,log10,append,zeros,amax,shape,double,mean,where
from numpy.linalg import norm
from scipy import fft
    
def ler_dados(arquivo):
    dados = loadmat(arquivo,byte_order='=')
    beta = dados['beta'][:,0]
    W = dados['W']
    return W,beta
    
def normalizar(sinal1d,variancia):
    sinal1d = sinal1d - mean(sinal1d)
    out = asarray(sinal1d)
    out /= sqrt(variancia)
    return out
    
def divide_sinal(sinal,nvet,samples):
    sinal = asarray(sinal).copy()
    sinal = sinal[0:(nvet*samples)].copy()
    aux = reshape(sinal,(nvet,samples)).T
    return aux;

def calcSNR(limpo,ruido):
    limpo = asarray(limpo).copy()
    ruido = asarray(ruido).copy()
    snr = 10.*log10(sum(limpo**2.)/sum(ruido**2.))
    return snr
    
class TXT:
    
    def __init__(self,nome):
        self.arq = open(nome+'.txt',"a")
        
    def linha(self,texto):
        self.arq.write(texto+'\n')
    
    def fechar(self):
        self.arq.close()

def calcSD(sinal1,sinal2,N=64):
    s1= asarray(sinal1).copy()
    s2= asarray(sinal2).copy()
    s1 /= norm(asarray(s1))
    s2 /= norm(asarray(s2))
    s1 = divide_sinal(asarray(s1),size(s1)/N,N)
    s2 = divide_sinal(asarray(s2),size(s2)/N,N)
    s1 = append(s1,zeros([192,size(s1)/N]),axis=0)
    s2 = append(s2,zeros([192,size(s2)/N]),axis=0)
    S1 = fft(s1.T).T
    S2 = fft(s2.T).T
    lim = 1e-15
    S1 = where(abs(S1)<lim,lim,S1)
    S2 = where(abs(S2)<lim,lim,S2)
    SD = 0.
    for i in range(0,shape(S1)[1]):
        for k in range(0,256):
            SD += (10.*abs(log10(abs(S1[k,i])) - log10(abs(S2[k,i]))))**2
    SD = sqrt(SD)/shape(S1)[1]
    return SD

