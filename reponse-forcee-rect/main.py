#!/usr/bin/python
# -*- coding: utf-8 -*-


# Victor Wetzel, UPMC, 2016, wetzel.victor@gmail.com
# Cinna Peyghamy, UPMC, 2016


"""
Modelisation et visualisation de la réponse acoustique
d'une cavité parallèlepipédique 2D parfaitement régléchissante
"""

""" === BIBLIOTHEQUES === """
import numpy as np 
from matplotlib import pyplot as plt
import math 

import classReponseForcee as repl
import colorGraph as clg

""" === CONSTANTES === """
PI = np.pi

# Parametres physiques:
c0  = 440. # Celerite [m/s}
rho = 1   # Masse Volumique [kg/m^3]

# Dimensions de la piece:
Lx = 1. # m
Ly = 1.24 # m

# Constantes de discretisation:
Nx = 200 # Nombre de points sur x
Ny = 200 # Nombre de points sur y

# Limites des sommes sur les modes
M = 7
N = 7

# Paramètres de la source
F0 = 1  # Amplitude
f  =  0 # Fréquence d'oscillation - 150 marche bien
W  = 440 # Pulsation d'excitation



x0 = 0.5*Lx # Position (x,y) de la source
y0 = 0.5*Ly # Comment l'indiquer sur le graph? En blanc?

x0 = round(x0*Nx/Lx) - 1
y0 = round(y0*Ny/Ly) - 1

""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)

""" === EQUATIONS === """
X = repl.Xmn(x,y,Lx,Ly,N=N,M=M)
masse = repl.Masse_Modale(x,y,Lx,Ly,N=N,M=M)
w_mn = repl.Pulsations_Propres(Lx, Ly, N, M, c0)


# -- ax1
N1, M1 = 1, 1
x01, y01 = 0.25*Lx, 0.35*Ly
x0_1, y0_1 = round(x01*Nx/Lx) - 1, round(y01*Ny/Ly) - 1

W1 = 321

amp1 = repl.Amplitude_forcee(X, masse, w_mn, x0_1, y0_1, F0, W1, N, M)
res1 = repl.Modes_Forces(X, amp1, N, M, Nx, Ny)
res1.calcule_reponse(0, W)

# -- ax2
N2, M2 = 2, 0
W2 = w_mn.get_w(N2,M2)

x02, y02 = 0.25*Lx, 0.262*Ly
x0_2, y0_2 = round(x02*Nx/Lx) - 1, round(y02*Ny/Ly) - 1


amp2 = repl.Amplitude_forcee(X, masse, w_mn, x0_2, y0_2, F0, W2, N, M)
res2 = repl.Modes_Forces(X, amp2, N, M, Nx, Ny)
res2.calcule_reponse(0, W)

# -- ax3
N3, M3 = 4, 5
W3 = w_mn.get_w(N3,M3)

x03, y03 = 0.25*Lx, 0.35*Ly
x0_3, y0_3 = round(x03*Nx/Lx) - 1, round(y03*Ny/Ly) - 1

amp3 = repl.Amplitude_forcee(X, masse, w_mn, x0_3, y0_3, F0, W3, N, M)
res3 = repl.Modes_Forces(X, amp3, N, M, Nx, Ny)
res3.calcule_reponse(0, W)

# -- ax4
N4, M4 = 5, 0
W4 = w_mn.get_w(N4,M4)

x04, y04 = 0.25*Lx, 0.35*Ly
x0_4, y0_4 = round(x04*Nx/Lx) - 1, round(y04*Ny/Ly) - 1

amp4 = repl.Amplitude_forcee(X, masse, w_mn, x0_4, y0_4, F0, W4, N, M)
res4 = repl.Modes_Forces(X, amp4, N, M, Nx, Ny)
res4.calcule_reponse(0, W)


""" === VISUALISATION === """

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, sharey=False, figsize = (24,8))

fig.suptitle('Champ de pression de plusieurs cavites en regime force\nLx = {0}m, Ly = {1}m, F0 = {2}N/m'.format(Lx, Ly, F0),fontsize = 16, fontweight = 'bold')


ax1.imshow(res1.reponse, interpolation ='nearest')
ax1.scatter(x0_1, y0_1, color = 'k', s = 100)
ax1.scatter(x0_1, y0_1, color = 'w', s = 30)
ax1.axis([0,Nx-1,0,Ny-1])
ax1.set_title('Pulsation d\'excitation quelconque\nW = {0}\nPosition source: x ={1}m , y = {2}m'.format(round(W1), x01, y01), fontsize = 16)


ax2.imshow(res2.reponse, interpolation ='nearest')
ax2.scatter(x0_2, y0_2, color = 'k', s = 100)
ax2.scatter(x0_2, y0_2, color = 'w', s = 30)
ax2.axis([0,Nx-1,0,Ny-1])
ax2.set_title('Pulsation d\'excitation particuliere\nW = {0} = w({1},{2}),\nPosition source: x ={3}m , y = {4}m'.format(round(W2),N2, M2, x02, y02), fontsize = 16)


ax3.imshow(res3.reponse, interpolation ='nearest')
ax3.scatter(x0_3, y0_3, color = 'k', s = 100)
ax3.scatter(x0_3, y0_3, color = 'w', s = 30)
ax3.axis([0,Nx-1,0,Ny-1])
ax3.set_title('Pulsation d\'excitation:\nW = {0} = w({1},{2}),\nPosition source: x ={3}m , y = {4}m'.format(round(W3),N3, M3, x03, y03), fontsize = 16)


ax4.imshow(res4.reponse, interpolation ='nearest')
ax4.scatter(x0_4, y0_4, color = 'k', s = 100)
ax4.scatter(x0_4, y0_4, color = 'w', s = 30)
ax4.axis([0,Nx-1,0,Ny-1])
ax4.set_title('Pulsation d\'excitation:\nW = {0} = w({1},{2}),\nPosition source: x ={3}m , y = {4}m'.format(round(W4),N4, M4, x04, y04), fontsize = 16)

plt.show()

