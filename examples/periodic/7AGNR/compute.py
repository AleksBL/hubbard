import Hubbard.hamiltonian as hh
import Hubbard.plot as plot
import numpy as np
import sys

fn = sys.argv[1]
U = float(sys.argv[2])
eB = float(sys.argv[3])

H = hh.HubbardHamiltonian(fn, t1=2.7, t2=0.2, t3=.18, U=U, eB=eB, nsc=[3, 1, 1], kmesh=[51, 1, 1], what='xyz')
if U < 0.1:
    H.converge(premix=1.0)
else:
    H.converge()
H.save()

# Spin polarization plot
p = plot.SpinPolarization(H, colorbar=True, vmax=0.1)
p.set_title(r'$\varepsilon_\mathrm{B}=%.2f$ eV, $U=%.2f$ eV'%(eB, U))
fo = fn.replace('.XV', '-pol-U%.2f-eB%.2f.pdf'%(U, eB))
p.savefig('summary/'+fo)

# Bandstructure plot
ymax = 2
ev = H.eigh(k=[0, 0, 0])
batoms = list(np.where(H.geom.atoms.Z == 5)[0])
p = plot.Bandstructure(H, scale=2, ymax=ymax, projection=batoms)
p.set_title(r'$\varepsilon_\mathrm{B}=%.2f$ eV, $U=%.2f$ eV'%(eB, U))
for i, evi in enumerate(ev):
    if abs(evi-H.midgap) < ymax:
        zak_open = H.get_Zak_phase_open_contour(Nx=100, sub=i)
        zak = H.get_Zak_phase(Nx=100, sub=i)
        print 'Zak phase for band %i : %.4f rad closed loop, %.4f rad (open loop): ' % (i, zak, zak_open)
        p.axes.annotate('\#%i: %.4f'%(i, zak), (0.13*(i%2), evi-H.midgap), size=8)

# Sum over filled bands:
zak = H.get_Zak_phase(Nx=100)
p.axes.annotate(r'$\gamma=%.4f$'%zak, (0.4, 0.50), size=22, backgroundcolor='w')
z2 = int(round(np.abs(1-np.exp(1j*zak))/2))
tol = 0.05
if np.abs(zak) < tol or np.abs(np.abs(zak)-np.pi) < tol:
    # Only append Z2 when appropriate:
    p.axes.annotate(r'$\mathbf{Z_2=%i}$'%z2, (0., 0.9*ymax), size=22, backgroundcolor='k', color='w')
fo = fn.replace('.XV', '-zak-U%.2f-eB%.2f.pdf'%(U, eB))
p.savefig('summary/'+fo)