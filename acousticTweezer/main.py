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

import classTweezer as twe
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

""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)

""" === EQUATIONS === """
X_mn = twe.Xmn(x,y,Lx,Ly,N=N,M=M)
masse = twe.Masse_Modale(x,y,Lx,Ly,N=N,M=M)
w_mn = twe.Pulsations_Propres(Lx, Ly, N, M, c0)



""" === INSTANCIATIONS DES SOURCES """
t1 = 0.001
t2 = t1 + PI

# === Source 1 ===
y0 = 100
source_gd = twe.source_paroi_gd( X_mn, masse, w_mn, y0, x, y, Lx, Ly, Nx, Ny, N, M, F0=1, W=w_mn.get_w(0,3), amor = 0.1)
source_gd.calcule_reponse(t1)

# === Source 2 ===
source_hb = twe.source_paroi_hb( X_mn, masse, w_mn, x, y, Lx, Ly, Nx, Ny, N, M, F0=0, W=w_mn.get_w(0,4), amor = 0.1)
source_hb.calcule_reponse(t2)


""" === VISUALISATION === """

title1 =  'Réponse d\'une cavité a une excitation harmonique de pulsation {0} (rad/s)'.format(int(source_gd.W))
#clg.colorGraph1(source_gd.response.rep_pression, source_gd.W, title=title1)

title2 =  'Réponse d\'une cavité a une excitation harmonique de pulsation {0} (rad/s)'.format(int(source_hb.W))
#clg.colorGraph1(source_hb.response.rep_pression, source_gd.W, title=title2)

ultime = source_hb.response.rep_pression + source_gd.response.rep_pression
title3 =  'Acoustic tweezer'
clg.colorGraph1(ultime, source_gd.W, title=title3)

