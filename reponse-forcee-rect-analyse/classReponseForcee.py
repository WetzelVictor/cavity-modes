# -*- coding: utf-8 -*-


# Victor Wetzel, UPMC, 2016, wetzel.victor@gmail.com
# Cinna Peyghamy, UPMC, 2016


import colorGraph as clg
import numpy as np
import pylab as plt
PI = np.pi

""" === PULSATIONS PROPRES === """
class Pulsations_Propres:
	def __init__(self, Lx, Ly, N, M, c0):
		
		self.N = N # Upper limit x
		self.M = M # Upper limit y

		self.Lx = float(Lx)
		self.Ly = float(Ly)

		self.c0 = c0

		self.w_index = np.zeros((M,N))

		self.compute_w()

	def compute_w(self):
		for n in xrange(self.M):
			for m in xrange(self.N):
				
				w = self.c0 * np.sqrt( (float(n)/self.Lx)**2 + (float(m)/self.Ly)**2)

				self.w_index[m][n] = w


	def get_w(self, n, m):
		return self.w_index[m][n]


""" === MODES PROPRES === """
class Xmn:
	def __init__(self,  x, y, Lx, Ly, N = 1 , M = 1):

		self.N = N # Upper limit x
		self.M = M # Upper limit y

		self.x = x
		self.y = y

		self.Lx = float(Lx)
		self.Ly = float(Ly)

		self.Nx = len(self.x) - 1 
		self.Ny = len(self.y) - 1

		self.empty_mode = np.zeros((self.Ny,self.Nx)) 

		self.mode_index = []

		self.compute_modes()


	def compute_modes(self):
		X = self.empty_mode

		for n in xrange(self.M):
			for m in xrange(self.N):
				a = np.cos(n*PI*self.x/self.Lx)
				b = np.cos(m*PI*self.y/self.Ly)
				
				X = np.multiply( a.reshape(len(a),1) ,b)

				self.mode_index.append(X)

	def get_mode(self, n, m):
		return self.mode_index[n + m*(self.N)]



""" === MASSE MODALE === """
class Masse_Modale:
	def __init__(self,  x, y, Lx, Ly, N = 1 , M = 1, rho=1):
		
		self.N = N # Upper limit x
		self.M = M # Upper limit y

		self.x = x
		self.y = y

		self.Lx = float(Lx)
		self.Ly = float(Ly)

		self.Nx = len(self.x) - 1 
		self.Ny = len(self.y) - 1

		self.rho = rho

		self.mass_index = np.zeros((M,N))

		self.compute_masses()




	def compute_masses(self):
		for m in xrange(self.M):
			for n in xrange(self.N):
				X_x_p2 = np.cos(n*PI*self.x/self.Lx)**2
				Y_y_p2 = np.cos(m*PI*self.y/self.Ly)**2
				
				mass = self.rho * np.trapz(X_x_p2, x =self.x) * np.trapz(Y_y_p2, x =self.y)
				

				self.mass_index[m][n] = mass

	def get_mass(self, n, m):
		return self.mass_index[m][n]


""" === RÉPONSE FORCÉE === """

class Modes_Forces:
	def __init__(self, X, amp, M, N, Nx, Ny):

		self.M = M
		self.N = N

		self.Nx, self. Ny = Nx, Ny

		self.empty_reponse = np.zeros((self.Ny,self.Nx))
		self.reponse = self.empty_reponse
		self.reponse_index = []

		self.X = X
		self.amp = amp
	
	def calcule_reponse(self, t, W):
		reponse = self.empty_reponse

		for n in xrange(self.N):
			for m in xrange(self.M):
				reponse = self.X.get_mode(n,m)*self.amp.get_amp(n,m)*np.cos(W*t)
				#self.reponse_index.append(reponse)
				#print 'n = {0}, m = {1}'.format{n,m}

				self.reponse = self.reponse +  reponse.transpose()


	def sum_response(self):
		# Sommer tous les éléments de self.reponse_index dans reponse
		self.reponse = np.sum(self.reponse_index)

class Amplitude_forcee:
	def __init__(self, X, masse_modale, w_mn, x0, y0, F0, W, N, M):

		self.X = X
		self.w_mn = w_mn
		self.masse_modale = masse_modale

		self.x0 = x0
		self.y0 = y0

		self.F0 = F0

		self.N, self.M = N , M

		self.amp_index = np.zeros((M,N))

		self.W =W

		self.compute_amps()

		self.amp_index

	def compute_amps(self):
		for n in xrange(self.M):
			for m in xrange(self.N):
				amp = ( self.X.get_mode(n,m).item((self.x0,self.y0)) *self.F0) / \
					  (self.masse_modale.get_mass(n,m)*(self.w_mn.get_w(n,m)**2 - self.W**2 +0.1))
				
				self.amp_index[m][n] = amp

				#print 'AMP mn ({0},{1}) ==== {2} w({0},{1}) = {3}'.format(n,m,amp,self.w_mn.get_w(n,m))


	def get_amp(self, n, m):
		return self.amp_index[m][n]














		