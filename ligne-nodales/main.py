# -*- coding: utf-8 -*-
#!/usr/bin/python


# Victor Wetzel, UPMC, 2016, wetzel.victor@gmail.com
# Cinna Peyghamy, UPMC, 2016

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib as mtp


Lx = 1.
Ly = 1.
Nx = 100
Ny = 100
n = 3
m = 2

x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)

xx, yy = np.meshgrid(x,y)

tt = np.cos( (n*np.pi*xx)/Lx)*np.cos( (m*np.pi*yy)/Ly)

x0 = Lx/4.
y0 = Ly/4.

fig = plt.figure(figsize=(9.5, 7))

CS = plt.contour(x,y,tt)
plt.clabel(CS, inline = 1, fontsize = 12)
plt.suptitle('Representation des noeuds et ventres de pression pour le mode propre ({0},{1})'.format(n,m),
			fontsize=14, 
			fontweight='bold')
plt.xlabel('Longueur (m)', fontsize = 14)
plt.ylabel('Largeur (m)', fontsize = 14)
plt.show()