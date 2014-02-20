# -*- coding: utf-8 -*-

from numpy import floor,size,var,dot,array,append
from flac import carregar_audio
from dados import normalizar, v2m
from ica import ica
from ggm import ggm
import os
import sys

def kurtnorm(dados):
	return ((1./(size(dados)-1.))*sum((dados-mean(dados))**4.))/(var(dados)**2.)

def treinar(arquivo , Bini , label , N):
    pasta = label
    if not(os.path.exists(pasta)): # verifica se a pasta existe
        os.makedirs(pasta) # se não existe, cria
    
    # carrega arquivo de audio
    sys.stdout.write("\rCarregando arquivo...                   ")
    sys.stdout.flush()
    sinal = carregar_audio(arquivo)
    
    T = size(sinal) # numero de amostras do sinal
    sinal = normalizar(sinal,var(sinal)) # normaliza variancia do sinal para 1
    
    # coloca o sinal no formato matricial
    sinalM = v2m(sinal,N)

    # realiza o ICA nas realizações e obtem a matriz de desmistura
    sys.stdout.write("\rRealizando ICA...                   ")
    sys.stdout.flush()
    ica_ = ica()
    ica_.realiza_ica(sinalM)
    W = ica_.obter_W()
    
    # Transforma as realizações para o espaço ICA
    fontes = dot(W,sinalM)

    # Realiza a estimação do parametro beta do modelo GGM
    sys.stdout.write("\rEstimando parâmetros...                   ")
    sys.stdout.flush()
    betas = array([])
    for b in range(0,N):
        aggm = ggm(beta_inicial=Bini,N=N,lamb=5./T,label=label)
        beta = aggm.estima_beta(fontes[b,:],comp=b)
        betas = append(betas,beta)

    return W,betas

