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

import classSources as twe
import colorGraph as clg

""" === CONSTANTES === """
PI = np.pi

# Parametres physiques:
c0  = 440. # Celerite [m/s}
rho_f = 1   # Masse Volumique [kg/m^3]

# Dimensions de la piece:
Lx = 1 # m
Ly = 1 # m

# Constantes de discretisation:
Nx = 200 # Nombre de points sur x
Ny = 200 # Nombre de points sur y

# Limites des sommes sur les modes
M = 15
N = 15

# Paramètres de la source
exc_1 = twe.source(x0=50, y0=99, F0=2, W=0)
exc_2 = twe.source(x0=50, y0=0, F0=2, W=0)


""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)

""" === EQUATIONS === """
X = twe.Xmn(x,y,Lx,Ly,N=N,M=M)
masse = twe.Masse_Modale(x,y,Lx,Ly,N=N,M=M)
w_mn = twe.Pulsations_Propres(Lx, Ly, N, M, c0)



""" === INSTANCIATIONS DES SOURCES """
t = 0.001

# === Source 1 ===
exc_1.W = w_mn.get_w(14,14) # Fréquence d'excitation source 1

amp_1 = twe.Amplitude_forcee(X, masse, w_mn, exc_1.x0, exc_1.y0, exc_1.F0, exc_1.W, N, M)

vit_1 = twe.speed(amp_1, x, y, Lx, Ly, Nx, Ny, N , M )
source_1 = twe.Modes_Forces(X, amp_1, M, N, Nx, Ny)

vit_1.calcule_vitesse(t, exc_1.W)
source_1.calcule_reponse(t, exc_1.W)

# === Source 2 ===
exc_2.W = w_mn.get_w(14,14) # Fréquence d'excitation source 1

amp_2 = twe.Amplitude_forcee(X, masse, w_mn, exc_2.x0, exc_2.y0, exc_2.F0, exc_2.W, N, M)

vit_2 = twe.speed(amp_2, x, y, Lx, Ly, Nx, Ny, N , M )
source_2 = twe.Modes_Forces(X, amp_2, M, N, Nx, Ny)

vit_2.calcule_vitesse(t, exc_2.W)
source_2.calcule_reponse(t, exc_2.W)




""" === VISUALISATION === """

title1 =  'Réponse d\'une cavité a une excitation harmonique de pulsation {0} (rad/s)'.format(int(exc_1.W))
#clg.colorGraph1(source_1.rep_pression, exc_1.W, p=[exc_1.x0,exc_1.y0], title=title1)


title2 = 'Réponse d\'une cavité de dimension ({0},{1}) a deux excitations harmoniques de pulsation {2} et {3} (rad/s)'.format(Lx, Ly, int(exc_1.W), int(exc_2.W))

clg.colorGraph2(source_2.rep_pression + source_1.rep_pression, 
					data_2 = [exc_1.W, exc_2.W], 
					p1=[exc_1.x0,exc_1.y0], 
					p2=[exc_2.x0,exc_2.y0], 
					title=title2)

#clg.quiver(x, y, vit.U, vit.V,1)

