#!/usr/bin/python-2.7
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings('ignore')

import sys
from treino import *
from dados import gravar_dados,TXT
from Tkinter import *
from tkFileDialog import askopenfilename

Tk().withdraw()
arquivo = askopenfilename().encode('utf-8')
nome = (arquivo.split('/')[-1]).split('.')[0]
sys.stdout.write('Arquivo selecionado: %s\n' % arquivo)
bini_ = float(input('Escolha um beta inicial [ex.: 3]: '))
N = (input('Tamanho do frame [ex.: 64]: '))

#N = 64
#arquivo="/home/fabio/Dropbox/mestrado/dissertação/scripts/ICA-MAP/final/icamapgen/versao final/treino/teste.flac"
#nome="teste"
#bini_=3


W,beta = treinar(   arquivo , \
                    Bini = bini_ , \
                    label=nome , \
                    N=N)


gravar_dados(nome+'/'+nome+'.mat',W,beta)

wd = TXT(nome+'/'+nome)
wd.linha('betas =\n'+str(beta))
wd.linha('W = ' )
for i in range(N):
	wd.linha(str(W[i]))
wd.fechar()

sys.stdout.write("\rTreino realizado! Dados gravados em %s/%s.mat\n" % (nome,nome))
sys.stdout.flush()

