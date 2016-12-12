import pylab as plt
import numpy as np

def colorGraph1(data, p=None, title=''):

	fig = plt.figure(figsize=(6, 3))
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
	plt.show()


