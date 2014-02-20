from matplotlib.pyplot import *
from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family':'serif', 'serif':['Computer Modern Roman'], 
        'monospace': ['Computer Modern Typewriter']})


# USO: from graf_tex import *
def salvagraf(arquivo):
    savefig(arquivo,bbox_inches="tight")
    return 


#from numpy import linspace, pi, sin, arange, size
##edit: with an example of marking an arbitrary subset of points, as requested in the comments:
##
#xs = linspace(-pi, pi, 100)
#ys = sin(xs)
#markers_on = arange(0,size(xs),10)
#plot(xs, ys, 'g-')
#plot(xs[markers_on], ys[markers_on], 'r', label="Teste")
#legend(loc=4)
#show()
