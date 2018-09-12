import Hubbard.hubbard as HH
import sys
import numpy as np

# Density tolerance for quitting the iterations
tol = 1e-10

# 3NN tight-binding model
H = HH.Hubbard('junction-2-2.XV', t1=2.7, t2=0.2, t3=.18)

# Output file to collect the energy difference between
# FM and AFM solutions
f = open('FM-AFM.dat','w')

for u in np.linspace(0.0, 1.4, 15):
    # We approach the solutions from above, starting at U=4eV
    H.U = 4.4-u 
    H.read() # Try reading, if we already have density on file       

    # AFM case first
    deltaN = 1.
    i = 0
    while deltaN > tol:
        if deltaN > 0.1:
            # precondition
            deltaN, eAFM = H.iterate(mix=.1)
        else:
            deltaN, eAFM = H.iterate(mix=1)
        i += 1
        if i%100 == 0:
            print "   AFM iteration %i: deltaN = %.8f" %(i, deltaN)
    print "   Converged in %i iterations" %i
    H.save() # Computed density to file
    
    # Now FM case
    H.Nup += 1 # change to two more up-electrons than down
    H.Ndn -= 1
    H.read()
    deltaN = 1.
    i = 0 # Reset
    while deltaN > tol:
        if deltaN > 0.1:
            # precondition
            deltaN, eFM = H.iterate(mix=.1)
        else:
            deltaN, eFM = H.iterate(mix=1)
        i += 1
        if i%100 == 0:
            print "   FM iteration %i: deltaN = %.8f" %(i, deltaN)
    print "   Converged in %i iterations" %i
    H.save()

    # Revert the imbalance for next loop
    H.Nup -= 1
    H.Ndn += 1

    f.write('%.4f %.8f\n'%(H.U, eFM-eAFM))

f.close()