#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modelisation et visualisation des modes propres
d'un cavite parallapipedique de dimensions Lx*Ly*Lz
aux parois parfaitement reflechissantes.
"""

""" === BIBLIOTHEQUES === """
import numpy as np 
from matplotlib import pyplot as plt

import classReponseLibre as repl
import colorGraph as clg


""" === CONSTANTES === """
PI = np.pi

# Parametres physiques:
c0  = 440. # Celerite [m/s}
rho = 1.   # Masse Volumique [kg/m^3]

# Dimensions de la piece:
Lx = 1 # m
Ly = 1 # m

# Constantes de discretisation:
Nx = 200*Lx # Nombre de points sur x
Ny = 200*Ly # Nombre de points sur y

# Placement de la condition initiale
x0 =200 -1
y0 =200 -1

F0 = 1

""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)

# Chaque mode est defini par les entiers: (m,n,p)
M = 3
N = 3


""" === EQUATIONS === """
X = repl.Xmn(x,y,Lx,Ly,N=N,M=M)
masse = repl.Masse_Modale(x,y,Lx,Ly,N=N,M=M)
w = repl.Pulsations_Propres(Lx, Ly, N, M, c0)
CI = repl.Conditions_Initiales(x0, y0, F0, Nx, Ny)

A = repl.Anm(x, y, Lx, Ly, masse, CI, N, M, rho)
B = repl.Bnm(x, y, Lx, Ly, masse, CI, w, N, M, rho)

"""print w.w_index
print

print A.A_index
print
print B.B_index
"""
resultat = repl.Modes_Libres(X, A, B, w, Nx, Ny, M, N)

resultat.calcul_reponse(2)


""" === VISUALISATION === """
clg.colorGraph(resultat.reponse)