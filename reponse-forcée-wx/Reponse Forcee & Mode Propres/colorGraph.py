import pylab as plt

def graphReponseForcee(obj, x0=None, y0=None, title='Reponse Forcee'):


	fig = plt.figure(figsize=(6, 3.2))
	fig.canvas.set_window_title(title)
	ax = fig.add_subplot(111)
	#txt = fig.add_subplot(222)
	if not x0==None or not y0==None:
		plt.scatter(x0, y0 , s=70, color ='black')
		plt.scatter(x0, y0 , s=40, color ='white')
	ax.set_title('Reponse Forcee')
	plt.imshow(obj.reponse, interpolation='nearest')
	ax.set_aspect('equal')
	cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
	cax.get_xaxis().set_visible(False)
	cax.get_yaxis().set_visible(False)
	cax.patch.set_alpha(255)
	cax.set_frame_on(False)
	plt.colorbar(orientation='vertical')
	plt.show()



def graphModesPropres(obj, n=None, m=None, title='Reponse Forcee'):

	fig = plt.figure(figsize=(6, 3.2))
	fig.canvas.set_window_title(title)
	ax = fig.add_subplot(111)
	ax.set_title('Mode Propre')
	plt.imshow(obj.get_mode(n,m), interpolation='nearest')
	ax.set_aspect('equal')
	cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
	cax.get_xaxis().set_visible(False)
	cax.get_yaxis().set_visible(False)
	cax.patch.set_alpha(255)
	cax.set_frame_on(False)
	plt.colorbar(orientation='vertical')
	plt.show()

