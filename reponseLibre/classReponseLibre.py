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

		self.w_index = [np.zeros(N)]*M

		self.compute_w()

	def compute_w(self):
		for n in xrange(self.M):
			for m in xrange(self.N):
				
				w = self.c0 * np.sqrt( (float(n)/self.Lx)**2 + (float(m)/self.Ly)**2)
				print w

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

		self.empty_mode = np.matrix([np.zeros(self.Nx)]*self.Ny) 

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

		self.mass_index = [np.zeros(N)]*M

		self.compute_masses()



	def compute_masses(self):
		for n in xrange(self.M):
			for m in xrange(self.N):
				X_x_p2 = np.cos(n*PI*self.x/self.Lx)**2
				Y_y_p2 = np.cos(m*PI*self.y/self.Ly)**2
				
				mass = self.rho * np.trapz(X_x_p2, x =self.x) * np.trapz(Y_y_p2, x =self.y)
				

				self.mass_index[m][n] = mass

	def get_mass(self, n, m):
		return self.mass_index[m][n]



""" === CONDITIONS INITIALES === """

class Conditions_Initiales:
	def __init__(self, x0, y0, F0,Nx, Ny):

		self.phi_0 = np.matrix([np.zeros(Nx)] *Ny)
		self.phi_0.itemset((x0,y0),F0)

		#clg.colorGraph(self.phi_0)




""" === CONTRIBUTIONS DES MODES === """

class Anm:
	def __init__(self,  x, y, Lx, Ly, M_mn,CI, N =1 , M =1, rho =1):

		self.N = N # Upper limit x
		self.M = M # Upper limit y

		self.x = x
		self.y = y

		self.Lx = float(Lx)
		self.Ly = float(Ly)

		self.Nx = len(self.x) - 1 
		self.Ny = len(self.y) - 1

		self.CI = CI
		self.M_mn = M_mn
		self.rho = rho

		self.A_index = [np.zeros(N)]*M

		self.compute_A()


	def compute_A(self):
		for n in xrange(self.M):
			for m in xrange(self.N):
				X_x_p2 = np.cos(n*PI*self.x/self.Lx)**2 # Créations des modes propres au carré
				Y_y_p2 = np.cos(m*PI*self.y/self.Ly)**2

				XY_p2 = np.multiply(X_x_p2.reshape(len(X_x_p2),1) ,Y_y_p2)  # Multiplication des matrices

				CIXY = np.multiply(XY_p2, self.CI.phi_0) # Multiplication des matrices

				A = np.trapz(CIXY, axis = 0, x =self.x) #deux intégrales successives en x et y
				A = np.trapz(A, axis = 0, x = self.y)

				A = (self.rho / self.M_mn.get_mass(m,n))*A

				self.A_index[m][n] = A


	def get_A(self, n, m):
		return self.A_index[m][n]

class Bnm:
	def __init__(self,  x, y, Lx, Ly, M_mn, CI, w_mn, N =1, M =1, rho =1):

		self.N = N # Upper limit x
		self.M = M # Upper limit y

		self.x = x
		self.y = y

		self.Lx = float(Lx)
		self.Ly = float(Ly)

		self.Nx = len(self.x) - 1 
		self.Ny = len(self.y) - 1

		self.CI = CI
		self.M_mn = M_mn
		self.rho = rho
		self.w_mn = w_mn

		self.B_index = [np.zeros(N)]*M

		self.compute_B()

	def compute_B(self):
		for n in xrange(self.M):
			for m in xrange(self.N):
				X_x_p2 = np.cos(n*PI*self.x/self.Lx)**2 # Créations des modes propres au carré
				Y_y_p2 = np.cos(m*PI*self.y/self.Ly)**2

				XY_p2 = np.multiply(X_x_p2.reshape(len(X_x_p2),1) ,Y_y_p2)  # Multiplication des matrices

				CIXY = np.multiply(XY_p2, self.CI.phi_0) # Multiplication des matrices

				B = np.trapz(CIXY, axis = 0, x =self.x) #deux intégrales successives en x et y
				B = np.trapz(B, axis = 0, x = self.y)

				B = (self.rho**2 / (self.M_mn.get_mass(m,n) *self.w_mn.get_w(m,n) )   *B

				self.B_index[m][n] = B


	def get_B(self, n, m):
		return self.B_index[m][n]

""" === MODES REPONSES LIBRES === """

class Modes_Libres:
	def __init__(self, X, A, B,w_mn, Nx, Ny, M, N):
		
		self.Nx = Nx
		self.Ny = Ny

		self.M = M
		self.N = N

		self.empty_reponse = np.matrix([np.zeros(self.Nx)]*self.Ny) 
		self.reponse = self.empty_reponse

		self.X = X
		self.A = A
		self.B = B 
		self.w_mn = w_mn

	def calcul_reponse(self,t):
		reponse = self.empty_reponse

		for n in xrange(self.N):
			for m in xrange(self.M):

				PHI = self.A.get_A(n,m)*np.cos(self.w_mn.get_w(n,m)*t) + self.B.get_B(n,m)*np.sin(self.w_mn.get_w(n,m)*t)

				reponse += self.X.get_mode(n,m)*PHI
				

		self.reponse = reponse












		