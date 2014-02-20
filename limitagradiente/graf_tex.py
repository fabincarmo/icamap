from matplotlib.pyplot import *
from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family':'serif', 'serif':['Computer Modern Roman'], 
        'monospace': ['Computer Modern Typewriter']})


# USO: from graf_tex import *
def salvagraf(arquivo):
    savefig(arquivo,bbox_inches="tight")
    return 

