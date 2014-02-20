# -*- coding: utf-8 -*-
from numpy import diff,size,asarray,abs,log,arange,exp,sqrt,sign,where
from scipy.special import gamma

def fun_c(ve):
    c = ((gamma(3.*(1.+ve)/2.))/(gamma((1.+ve)/2.)))**(1./(1.+ve))
    return c
    
import math
def derivfun(vari,beta,arg):
    signMs = sign(arg)
    s = (2.*fun_c(beta)/((1.+beta)*sqrt(vari)))*((abs(arg.copy())/sqrt(vari))**((1.-beta)/(1.+beta)))
    s = where(s==float('inf'),0.,s)
    out =   s * signMs
    #out = where(abs(out)>500.,sign(out)*500.,out)
    return out

#def derivfun2(vari,beta,arg,lim,params):
#    signMs = sign(arg)
#    s = (2.*fun_c(beta)/((1.+beta)*sqrt(vari)))*((abs(arg.copy())/sqrt(vari))**((1.-beta)/(1.+beta)))
#    s1 =   s * signMs
#    p0,m0,p1,m1 = params
#    arg2 = (arg + lim)/(2*lim)
#    h00 = 2*arg2**3 - 3*arg2**2 + 1 
#    h10 = arg2**3 - 2*arg2**2 + arg2
#    h01 = -2*arg2**3 + 3*arg2**2
#    h11 = arg2**3 - arg2**2
#    s2 = h00*p0 + h10*2*lim*m0 + h01*p1 + h11*2*lim*m1
#    out = where(abs(arg)<lim,s2,s1)
#    return out


