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
Lx = 1. # m
Ly = 1.24 # m

# Constantes de discretisation:
Nx = 50. # Nombre de points sur x
Ny = 50. # Nombre de points sur y

# Limites des sommes sur les modes
M = 6
N = 6

# Paramètres de la source
F0 = 1  # Amplitude
f  =  0 # Fréquence d'oscillation - 150 marche bien
W  = 440 # Pulsation d'excitation



x0 = 0.64*Lx # Position (x,y) de la source
y0 = 0.42*Ly # Comment l'indiquer sur le graph? En blanc?

x0 = round(x0*Nx/Lx) - 1
y0 = round(y0*Ny/Ly) - 1

""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)

""" === EQUATIONS === """
X = repl.Xmn(x,y,Lx,Ly,N=N,M=M)
masse = repl.Masse_Modale(x,y,Lx,Ly,N=N,M=M)
w_mn = repl.Pulsations_Propres(Lx, Ly, N, M, c0)

N0, M0 = 4, 4
W = w_mn.get_w(N0,M0)

amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
resultat = repl.Modes_Forces(X, amp, M, N, Nx, Ny)


resultat.calcule_reponse(0, W)

""" === VISUALISATION === """
# Réponse de la cavité
title = 'Reponse d\'une cavite de dimension ({0},{1}) a une excitation harmonique de frequence w = {2} (rad/s)'.format(Lx, Ly, W)

clg.colorGraph(resultat.reponse, x0=x0, y0=y0 , title=title)

# Amplitude de chaque mode en fonction de la fréquence de la source

w_indm = []
mode_m = []

w_indn = []
mode_n = []

w_indnm = []
mode_nm = []

for n in xrange(1,N):
	for m in xrange(1,M):
		W = w_mn.get_w(n,m)

		print 'w({0},{1})={2}'.format(n,m,W)

		w_indnm.append(W)
		amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
		mode_nm.append(abs(amp.get_amp(n,m)))

for n in xrange(1,N):
	W = w_mn.get_w(n,0)

	print 'w({0},{1})={2}'.format(n,0,W)

	w_indn.append(W)
	amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
	mode_n.append(abs(amp.get_amp(n,0)))

for m in xrange(1,M):
	W = w_mn.get_w(0,m)

	print 'w({0},{1})={2}'.format(0,m,W)

	w_indm.append(W)
	amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
	mode_m.append(abs(amp.get_amp(0,m)))

# Normalisation
ref_min = np.min([np.min(mode_n), np.min(mode_m), np.min(mode_nm)])

fig = plt.figure(figsize = (16,6))
plt.bar(w_indnm,np.log(mode_nm/ref_min),color='r', width = 13)
plt.bar(w_indn, np.log(mode_n/ref_min), color='b', width = 13)
plt.bar(w_indm, np.log(mode_m/ref_min), color='g', width = 15)
plt.grid()
plt.suptitle('Amplitude de chaque mode en fonction de la pulsation d\'excitation', fontweight = 'bold', fontsize = 14)
plt.title("Amplitude de reference: {0}    Somme sur N*M = {1}*{2} = {3} modes    Lx = {4}  Ly = {5}   F0 = {6}".format(round(ref_min,2),N -1 ,M -1 , (N-1)*(M-1),Lx, Ly, F0))
plt.legend(['modes tangentiels', 'mode axial n', 'mode axial m'], fontsize = 12)
plt.xlabel('Pulsation d\'excitation de la source (rad/s)', fontsize = 14)
plt.ylabel('Amplitude modale (log)' ,fontsize = 14)
plt.show()
	

# Amplitude maximum en fonction de la position de la source (omega constant)
# --- t = 0,
amp_max = np.zeros((Ny,Nx))
W = w_mn.get_w(N0,M0)

for i in xrange(int(Nx)):
	for j in xrange(int(Ny)):
		x0 = i
		y0 = j

		amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
		resultat = repl.Modes_Forces(X, amp, M, N, Nx, Ny)
		resultat.calcule_reponse(0, W)

		amp_max[j][i] = np.max(resultat.reponse)

#clg.colorGraph(amp_max, x0=x0, y0=y0 , title=title)