from __future__ import print_function

import matplotlib.pyplot as plt
from Hubbard.plot import GeometryPlot
import sisl
import numpy as np


class Wavefunction(GeometryPlot):

    def __init__(self, HubbardHamiltonian, wf, **keywords):

        # Set default keywords
        if 'realspace' in keywords:
            if 'facecolor' not in keywords:
                keywords['facecolor'] = 'None'
            if 'cmap' not in keywords:
                keywords['cmap'] = 'Greys'
        else:
            if 'cmap' not in keywords:
                keywords['cmap'] = plt.cm.bwr

        GeometryPlot.__init__(self, HubbardHamiltonian, **keywords)

        if 'realspace' in keywords:
            self.__realspace__(HubbardHamiltonian, wf, **keywords)

        else:
            self.__orbitals__(HubbardHamiltonian, wf, **keywords)

    def __orbitals__(self, HubbardHamiltonian, wf, **keywords):    

        x = HubbardHamiltonian.geom[:, 0]
        y = HubbardHamiltonian.geom[:, 1]

        assert len(x) == len(wf)

        self.axes.scatter(x, y, wf.real, 'r') # pos. part, marker AREA is proportional to data
        self.axes.scatter(x, y, -wf.real, 'g') # neg. part
    
    def __realspace__(self, HubbardHamiltonian, wf, z=1.1, vmax=0.006, grid_unit=0.05, **keywords):
        # Set new sc to create real-space grid
        sc = sisl.SuperCell([self.xmax-self.xmin, self.ymax-self.ymin, 3.2])
        H = HubbardHamiltonian.H.move([-self.xmin, -self.ymin, 0])
        H.xyz[np.where(np.abs(H.xyz[:, 2]) < 1e-3), 2] = 0
        H.set_sc(sc)

        # Create the real-space grid
        grid = sisl.Grid(grid_unit, sc=H.sc, geometry=H)
        sisl.electron.wavefunction(wf, grid, geometry=H)
        index = grid.index([0, 0, z])

        # Create custom map to differenciate it from polarization cmap
        import matplotlib.colors as mcolors
        custom_map = mcolors.LinearSegmentedColormap.from_list(name='custom_map', colors =['g', 'white', 'red'], N=100)
        
        # Plot only the real part
        ax = self.axes.imshow(grid.grid[:, :, index[2]].T.real, cmap=custom_map, origin='lower',
                              vmax=vmax, vmin=-vmax, extent=self.extent)
        # Colorbars
        if 'colorbar' in keywords:
            if keywords['colorbar'] != False:
                # Charge density per unit of length in the z-direction
                plt.colorbar(ax, label=r'$q_\uparrow+q_\downarrow$ ($e/$\AA)')