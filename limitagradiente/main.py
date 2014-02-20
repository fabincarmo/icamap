# -*- coding: utf-8 -*- 

import warnings
warnings.filterwarnings('ignore')
import os
import sys
#from time import time,sleep

from numpy import zeros,var,size
from scipy import randn
from flac import carregar_audio,gravar_audio
from dados import ler_dados,normalizar,calcSNR,calcSD,TXT
from icamap import icamapgen
from plots import plotc,espectrograma
from Tkinter import *
from tkFileDialog import askopenfilename

os.system('clear')

N = float(input('Tamanho do frame [64]:'))
genero = raw_input('Gênero [homem/mulher]:')
Tk().withdraw()
s_voz = askopenfilename().encode('utf-8')
ruido = raw_input('Tipo de ruído: ')
Tk().withdraw()
s_ruido = askopenfilename().encode('utf-8')
its_ = float(input('Número máximo de iterações: '))
lamb_ = float(input('Valor do passo: '))
limg = float(input('Limitação do gradiente: '))
snrini_ = float(input('SNR inicial: '))

# cria pasta onde serão salvos os resultados
pasta = genero+'_'+s_voz.split('/')[-1:][0]+'_'+ruido+'_'+s_ruido.split('/')[-1:][0]
if os.path.exists(pasta):
    os.system('rm '+pasta+'/*')
else:
    os.system('mkdir '+pasta)

sys.stdout.write("\rLendo arquivos MAT...                                     ")
sys.stdout.flush()

# lê os dados treinados
Wx,betax = ler_dados('../treino/'+genero+'/'+genero+'.mat')
if s_ruido=='gaussiano':
	Wv=Wx.copy()
	betav=zeros(N)
else:
	Wv,betav = ler_dados('../treino/'+ruido+'/'+ruido+'.mat')

snrini = snrini_
numits = its_
passolambda = lamb_

sys.stdout.write("\rCarregando arquivos de áudio...                                     ")
sys.stdout.flush()

# carrega os arquivos de áudio
x = carregar_audio(s_voz)
if s_ruido=='gaussiano':
    v = randn(x.size)	
else:
    v = carregar_audio(s_ruido)
    v=v[0:size(x)]

sys.stdout.write("\rConfigurando...                                     ")
sys.stdout.flush()

if size(x)>size(v):
    x = x[0:size(v)]
else:
    v = v[0:size(x)]

varv = 1./(10.**(snrini/10.)) # variância do ruído
x = normalizar(x,var(x))
v = normalizar(v,var(v)/varv)

y = x.copy()+v.copy() # cria sinal ruidoso

# calcula SNR e SD dos sinais limpo e ruidoso
snr1 = calcSNR(x,v) # deve ser igual a SNR inicial escolhida
sd1 = calcSD(x,y)

# cria arquivo de texto onde serão escritos os resultado de SNR e SD
arquivo = TXT(pasta+'/icamapgen')
arquivo.linha('SNR sinal sujo: '+str(snr1))
arquivo.linha('Input SD: '+str(sd1))

sys.stdout.write("\rIniciando...                                     ")
sys.stdout.flush()

teste = icamapgen(Wx,
                  betax,
                  Wv,
                  betav,
                  ruido=varv,
                  maxits=numits,
                  lamb=passolambda,
                  limg=limg)
y, xest = teste.aplicar(y.copy())

sys.stdout.write("\rTerminando...                                     ")
sys.stdout.flush()

## Original ###############################################################
snr2 = calcSNR(x,x-xest)
sd2 = calcSD(x,xest)

espectrograma(x,arquivo=pasta+'/spec_limpo.pdf')
espectrograma(y,arquivo=pasta+'/spec_sujo.pdf')
espectrograma(xest,arquivo=pasta+'/spec_xestimado.pdf')

# grava os sinais de áudio em FLAC
xaudio = x/abs(max(x))
gravar_audio(xaudio,pasta+'/original.flac',)
yaudio = y/abs(max(y))
gravar_audio(yaudio,pasta+'/sujo.flac',)
xestaudio = xest/abs(max(xest))
gravar_audio(xestaudio,pasta+'/estimado.flac',)

arquivo.linha('SNR com ICAMAPgen: '+str(snr2))
arquivo.linha('SD com ICAMAPgen: '+str(sd2))
arquivo.linha('\n')

plotc(x,y,xest,pasta)

arquivo.fechar()
sys.stdout.write("\n")
sys.stdout.flush()
