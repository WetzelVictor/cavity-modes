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

""" === CONSTANTES === """
PI = np.pi

# Parametres physiques:
c0  = 440. # Celerite [m/s}
rho = 1   # Masse Volumique [kg/m^3]

# Dimensions de la piece:
Lx = 1 # m
Ly = 1 # m

# Constantes de discretisation:
Nx = 200*Lx # Nombre de points sur x
Ny = 200*Ly # Nombre de points sur y

# Limites des sommes sur les modes
M = 15
N = 15

# Paramètres de la source
F0 = 100  # Amplitude
f  =  0 # Fréquence d'oscillation - 150 marche bien
W  = 440 # Pulsation d'excitation



x0 = 18*Lx # Position (x,y) de la source
y0 = 20*Ly # Comment l'indiquer sur le graph? En blanc?


""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)

""" === EQUATIONS === """
X = repl.Xmn(x,y,Lx,Ly,N=N,M=M)
masse = repl.Masse_Modale(x,y,Lx,Ly,N=N,M=M)
w_mn = repl.Pulsations_Propres(Lx, Ly, N, M, c0)

W = int(w_mn.get_w(4,0))

amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
resultat = repl.Modes_Forces(X, amp, M, N, Nx, Ny)


resultat.calcule_reponse(2.01, W)

""" === VISUALISATION === """
title = 'Reponse d\'une cavite de dimension ({0},{1}) a une excitation harmonique de frequence w = {2} (rad/s)'.format(Lx, Ly, W)

clg.colorGraph(resultat, x0=x0, y0=y0 , title=title)
