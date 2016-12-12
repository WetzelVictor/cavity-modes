#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename : 'modespropres\main.py'
"""
MODES PROPRES
Visualisation des modes propres d'une cavité rectangulaire
aux parois parfaitement réfléchissantes
"""

""" === BIBLIOTHEQUES === """
import numpy as np 
import pylab as plt

import classXmn as indModes
import colorGraph as clg



""" === CONSTANTES === """
PI = np.pi

# Parametres physiques:
c0  = 440 # Celerite [m/s}
rho = 1   # Masse Volumique [kg/m^3]

# Dimensions de la piece:
Lx = 1 # m
Ly = 1 # m

# Constantes de discretisation:
Nx = 1000*Lx # Nombre de points sur x
Ny = 1000*Ly # Nombre de points sur y

""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)

# Chaque mode est defini par les entiers: (m,n)
M = 5
N = 5

# Classe de modes
modes = indModes.Xmn(x,y,Lx,Ly,N=N,M=M)

clg.colorGraph(modes.get_mode(4,4))