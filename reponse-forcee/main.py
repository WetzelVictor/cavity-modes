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
Lx = 1 # m
Ly = 1 # m

# Constantes de discretisation:
Nx = 200*Lx # Nombre de points sur x
Ny = 200*Ly # Nombre de points sur y

# Limites des sommes sur les modes
M = 9
N = 9

# Paramètres de la source
F0 = 1  # Amplitude
W  = 440 # Pulsation d'excitation



x0 = 0*Lx # Position (x,y) de la source
y0 = 0*Ly # Comment l'indiquer sur le graph? En blanc?


""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)

""" === EQUATIONS === """
X = repl.Xmn(x,y,Lx,Ly,N=N,M=M)
masse = repl.Masse_Modale(x,y,Lx,Ly,N=N,M=M)
w_mn = repl.Pulsations_Propres(Lx, Ly, N, M, c0)

W = int(w_mn.get_w(1,1))

amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
resultat = repl.Modes_Forces(X, amp, M, N, Nx, Ny)


resultat.calcule_reponse(2.01, W)

""" === VISUALISATION === """
title = 'Reponse d\'une cavite de dimension ({0},{1}) a une excitation harmonique de frequence w = {2} (rad/s)'.format(Lx, Ly, W)

clg.colorGraph(resultat, x0=x0, y0=y0 , title=title)

"""
	w_indm = []
	mode_m = []
	
	w_indn = []
	mode_n = []
	
	w_indnm = []
	mode_nm = []
	
	for n in xrange(1,N):
		for m in xrange(1,M):
			W = w_mn.get_w(n,m)
			w_indnm.append(W)
			amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
			mode_nm.append(abs(amp.get_amp(n,m)))
	
	for n in xrange(N):
		W = w_mn.get_w(n,0)
		w_indn.append(W)
		amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
		mode_n.append(abs(amp.get_amp(n,0)))
	
	for m in xrange(M):
		W = w_mn.get_w(0,m)
		w_indm.append(W)
		amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
		mode_m.append(abs(amp.get_amp(0,m)))
	
	
	#fig = plt.scatter(index1, index2, marker='o', color = 'b')
	plt.bar(w_indnm, mode_nm,color='r', width = 20)
	plt.bar(w_indn, mode_n, color='b', width = 20)
	plt.bar(w_indm, mode_m, color='g', width = 20)
	plt.axis([0, 2500, 0, 50])
	plt.grid()
	plt.show()
		"""	
