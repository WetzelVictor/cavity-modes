import pylab as plt
import numpy as np

def colorGraph1(data, data_2, p=None, title=''):

	fig = plt.figure(figsize=(9, 5))
	fig.canvas.set_window_title(title)

	ax = fig.add_subplot(111)

	#txt = fig.add_subplot(222)


	if not p==None:
		plt.scatter(p[0], p[1] , s=70, color ='black')
		plt.scatter(p[0], p[1] , s=40, color ='white')


	ax.set_title('')
	
	plt.imshow(data, interpolation='nearest')
	
	ax.set_aspect('equal')

	cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
	cax.get_xaxis().set_visible(False)
	cax.get_yaxis().set_visible(False)
	cax.patch.set_alpha(255)
	cax.set_frame_on(False)


	plt.colorbar(orientation='vertical')
	plt.title(('       W = {0}(rad/s)'.format(data_2) ))
	plt.show()

def colorGraph2(data, data_2, p1=None, p2=None, title=''):

	fig = plt.figure(figsize=(9, 5))
	fig.canvas.set_window_title(title)

	ax = fig.add_subplot(111)

	#txt = fig.add_subplot(222)

	if not p1==None or not p2==None:
		plt.scatter(p1[0], p1[1] , s=70, color ='black')
		plt.scatter(p1[0], p1[1] , s=40, color ='white')

		plt.scatter(p2[0], p2[1] , s=70, color ='black')
		plt.scatter(p2[0], p2[1] , s=40, color ='white')



	ax.set_title('')
	
	plt.imshow(data, interpolation='nearest')
	
	ax.set_aspect('equal')

	cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
	cax.get_xaxis().set_visible(False)
	cax.get_yaxis().set_visible(False)
	cax.patch.set_alpha(255)
	cax.set_frame_on(False)


	plt.colorbar(orientation='vertical')
	plt.title(('   W1 = {0},    W2 = {1}(rad/s)'.format(int(data_2[0]), int(data_2[1]) )))
	plt.show()


def stream(X, Y, U, V):
	fig0, ax0 = plt.subplots()
	strm = ax0.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=plt.cm.autumn)
	fig0.colorbar(strm.lines)

	plt.show()



def quiver(X,Y, U, V, pas=2):

	fig = plt.figure(figsize=(10,10))

	U = U[::pas]
	V = V[::pas]
	X = X[::pas]
	Y = Y[::pas]

	M = np.hypot(U, V)
	Q = plt.quiver(X, Y, U, V, M,
               units='x',
               pivot='tip',
               width = 0.005)

	plt.axis([0, 1., 0, 1.])
	plt.show()

