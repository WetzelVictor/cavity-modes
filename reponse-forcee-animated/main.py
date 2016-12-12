#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import matplotlib.animation as animation

""" === CONSTANTES === """
PI = np.pi

# Parametres physiques:
c0  = 440. # Celerite [m/s}
rho = 1   # Masse Volumique [kg/m^3]

# Dimensions de la piece:
Lx = 1 # m
Ly = 1 # m

# Constantes de discretisation:
Nx = 150*Lx # Nombre de points sur x
Ny = 150*Ly # Nombre de points sur y

# Limites des sommes sur les modes
M = 15
N = 15

# Paramètres de la source
F0 = 100  # Amplitude
f  =  0 # Fréquence d'oscillation - 150 marche bien
W = 6000 # Pulsation d'excitation

x0 = 123*Lx # Position (x,y) de la source
y0 = 50*Ly # Comment l'indiquer sur le graph? En blanc?


""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)

""" === EQUATIONS === """
X = repl.Xmn(x,y,Lx,Ly,N=N,M=M)
masse = repl.Masse_Modale(x,y,Lx,Ly,N=N,M=M)
w_mn = repl.Pulsations_Propres(Lx, Ly, N, M, c0)
amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)

resultat = repl.Modes_Forces(X, amp, M, N, Nx, Ny)


""" === VISUALISATION : ANIMATION=== """
dt = 0.0001
t = 0

title = 'Reponse d\'une cavite de dimension ({0},{1}) a une excitation harmonique de frequence w = {2} (rad/s)'.format(Lx, Ly, W)

fig = plt.figure()

im = plt.imshow(resultat.calcule_reponse(W,t), animated=True, interpolation='nearest')

def update_fig(*args):
	global t
	t += dt
	im.set_array(resultat.calcule_reponse(W,t))
	return im,

ani = animation.FuncAnimation(fig,update_fig,interval=60, blit=True)
plt.show()
