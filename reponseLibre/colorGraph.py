import pylab as plt

def colorGraph(obj):

	fig = plt.figure(figsize=(6, 3.2))

	ax = fig.add_subplot(111)
	ax.set_title('colorMap')
	
	plt.imshow(obj, interpolation='nearest')

	ax.set_aspect('equal')

	cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
	cax.get_xaxis().set_visible(False)
	cax.get_yaxis().set_visible(False)
	cax.patch.set_alpha(255)
	cax.set_frame_on(False)
	plt.colorbar(orientation='vertical')
	plt.show()
