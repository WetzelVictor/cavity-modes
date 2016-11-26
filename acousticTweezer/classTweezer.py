# -*- coding: utf-8 -*-
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
		self.rep_pression = self.empty_reponse
		self.rep_potentiel = self.empty_reponse

		self.X = X
		self.amp = amp


	def calcule_reponse(self, t, W):
		reponse = self.empty_reponse
		rho_f = 1

		for n in xrange(self.N):
			for m in xrange(self.M):
				
				rep_pot = self.X.get_mode(n,m)*self.amp.get_amp(n,m)
				rep_pression = rho_f*rep_pot
				
				self.rep_pression += rep_pression.transpose()
				self.rep_potentiel += rep_pot.transpose()

		self.rep_potentiel = self.rep_potentiel * np.cos(W*t)
		self.rep_pression  = self.rep_pression  * np.sin(W*t)


""" === PARTICULE === """

class particule:
	def __init__(self, v0=[0.,0.], x0=0., y0=0., acContFact = 1., rho=10., diam= 0.01):
		
		# Conditions Initiales
		self.v0 = v0
		self.x0, self.y0 = float(x0), float(y0)

		# Attributs
		self.v = [0,0]
		self.xy= [0,0]

		# Caractéristiques physiques
		self.PHI, self.rho, self.volume = acContFact, rhop, 4./3.*PI*(diam**2)/4.
		self.m = self.rho * self.volume

	def compute_position(self,t):
		return

	def compute_speed(self,p):
		return

	def compute_Frad(self,pressure_field, speed_field):
		return


""" === SOURCE === """
# Source plane située en x=0 ou x=Lx

class source_paroi_gd:

	def __init__(self, X_mn, masse_modale, w_mn, x, y, Lx, Ly, Nx, Ny, N, M, F0=1, W=0, amor = 0.01):
		
		self.F0 = F0
		self.W = W

		self.X = X_mn
		self.w_mn = w_mn
		self.masse_modale = masse_modale
		self.amor = amor

		self.N, self.M = N , M
		self.x, self.y = x, y
		self.Lx, self.Ly = Lx, Ly
		self.Nx, self.Ny = Nx, Ny

		self.amp_index = np.zeros((M,N))

		# --- Computations 
		self.compute_amps()

		# --- Responses Initialisation
		self.speed = speed(self, self.x, self.y, self.Lx, self.Ly, self.Nx, self.Ny, self.N, self.M)
		self.response = Modes_Forces(self.X, self, self.M, self.N, self.Nx, self.Ny)

	def compute_amps(self):
		self.amp_index *=0

		for m in xrange(self.M):
				amp = self.F0 / \
				(self.masse_modale.get_mass(0,m)*(self.w_mn.get_w(0,m)**2 - self.W**2 +self.amor)) # dernier flottant est l'amortissement
				
				self.amp_index[m][0] = amp

	def get_amp(self, n, m):
		return self.amp_index[m][n]

	def calcule_reponse(self, t):
		self.response.calcule_reponse(t, self.W)


# --- Source plane située en y=0 ou y=Lx
class source_paroi_hb:

	def __init__(self, X_mn, masse_modale, w_mn, x, y, Lx, Ly, Nx, Ny, N, M, F0=1, W=0, amor= 0.01):
		
		self.F0 = F0
		self.W = W

		self.X = X_mn
		self.w_mn = w_mn
		self.masse_modale = masse_modale
		self.amor = amor

		self.N, self.M = N , M
		self.x, self.y = x, y
		self.Lx, self.Ly = Lx, Ly
		self.Nx, self.Ny = Nx, Ny

		self.amp_index = np.zeros((M,N))

		# --- Computations 
		self.compute_amps()

		# --- Responses Initialisation
		self.speed = speed(self, self.x, self.y, self.Lx, self.Ly, self.Nx, self.Ny, self.N, self.M)
		self.response = Modes_Forces(self.X, self, self.M, self.N, self.Nx, self.Ny)

	def compute_amps(self):
		self.amp_index *=0

		for n in xrange(self.N):
				amp = self.F0 / \
				(self.masse_modale.get_mass(n,0)*(self.w_mn.get_w(n,0)**2 - self.W**2 + self.amor)) # dernier flottant est l'amortissement
				
				self.amp_index[0][n] = amp

	def get_amp(self, n, m):
		return self.amp_index[m][n]

	def calcule_reponse(self, t):
		self.response.calcule_reponse(t, self.W)


# === SPEED ===

class speed:
	def __init__(self,amp, x, y, Lx, Ly, Nx, Ny, N = 1 , M = 1):

		self.N = N # Upper limit x
		self.M = M # Upper limit y

		self.x = x
		self.y = y

		self.Nx, self. Ny = Nx, Ny

		self.Lx = float(Lx)
		self.Ly = float(Ly)

		self.amp = amp

		self.empty_reponse = np.zeros((self.Ny,self.Nx))



		self.U = self.empty_reponse
		self.V = self.empty_reponse

		

	def calcule_vitesse(self,t,W):

		for n in xrange(self.N):
			for m in xrange(self.M):
				cosx = np.cos(n*PI*self.x/self.Lx)
				sinx = np.sin(n*PI*self.x/self.Lx)

				cosy = np.cos(m*PI*self.y/self.Ly)
				siny = np.sin(m*PI*self.y/self.Ly)

				U = ((-n*PI)/self.Lx) * np.multiply( sinx.reshape(len(sinx),1),cosy) * self.amp.get_amp(n,m)
				V = ((-m*PI)/self.Ly) * np.multiply( cosx.reshape(len(cosx),1),siny) * self.amp.get_amp(n,m)

				self.U += U
				self.V += V

		self.U *= np.cos(W*t)
		self.V *= np.cos(W*t)

		













		