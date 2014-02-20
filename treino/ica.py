# -*- coding: utf-8 -*-

import mdp

class ica:
    def __init__(self):
        self.ica = mdp.nodes.FastICANode( 
                whitened=True,
                verbose=False
                )
        
    def realiza_ica(self,sinais):
        out2 = self.ica(sinais.T) # ----->>> formato dos dados deve ser (T,N) onde N é o número de componentes
        return out2.T
    
    def obter_W(self):
        ## retorna a matriz de desmistura
        return self.ica.filters.T
    
    def obter_V(self):
        ## retorna a matriz de projeção do branqueamento
        return self.ica.white.v.T

