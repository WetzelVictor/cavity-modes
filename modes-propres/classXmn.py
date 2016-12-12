import numpy as np
import colorGraph as clg
PI = np.pi


# Victor Wetzel, UPMC, 2016, wetzel.victor@gmail.com
# Cinna Peyghamy, UPMC, 2016


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






		