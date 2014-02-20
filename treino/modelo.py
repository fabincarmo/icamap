# -*- coding: utf-8 -*-
from numpy import diff,size,asarray,abs,log,where
from scipy.special import gamma

def deriva(v1,v2):
    v1 = asarray(v1)
    v2 = asarray(v2)
    der = diff(v1)/diff(v2)
    return der

def fun_omega(ve):
    w = ((gamma(3.*(1.+ve)/2.))**(1./2.))/((1.+ve)*(gamma((1.+ve)/2.))**(3./2.))
    return w

def fun_c(ve):
    c = ((gamma(3.*(1.+ve)/2.))/(gamma((1.+ve)/2.)))**(1./(1.+ve))
    return c
    
def gradiente_N(xg,beta):
    if beta<-.8:
        beta = .8
    a=2.
    b=2.
    B2 = asarray([beta,beta+.001])
    w2 = fun_omega(B2)
    w = w2[0]
    c2 = fun_c(B2)
    c = c2[0]
    dw = deriva(w2,B2)[0]
    dc = deriva(c2,B2)[0]
    grad = 0.
    grad += (a-1.)/(beta+1.) - b
    grad += float(size(xg))*dw/w
    aux = where(xg==0.,1e-3,xg)
    gradv = ( -dc + (2.*c/(1+beta)**2.)*log(abs(aux)))*(abs(aux)**(2./(1+beta)))
    grad += sum(gradv)
    return grad
