import numpy as np 
from matplotlib import pyplot as plt

PI = np.pi
f = 0.05
c = 440
lamb = c / f
k = 2*PI/lamb
W = 2*PI*f
t = 0
mod = 0.2
dt = 0.1
Lx = 10.
B = 0.0001
ph = 1.507
dph = 0.01
x = np.linspace(0,Lx,1000)
A = 1.

y = A * (np.cos(4*PI*x/Lx + ph))*np.cos(W*t)

fig, ax = plt.subplots()
x0 = (7.*PI/2. - ph)*Lx/(4*PI)
y0 = 0.
dx, dy = 0.01, 0

for i in range(800):
    if t == 0:
        curve, = ax.plot(x, y)
        points, = ax.plot(x0, y0, marker ='o', linestyle = 'None')

        ax.set_xlim(0, 10) 
        ax.set_ylim(-1, 1) 
        t += dt
    if i <=550:
    	t += dt
    	y0 += dy
    	ph += dph
    	x0 = (7.*PI/2. - ph)*Lx/(4*PI)
        y = np.cos(4*PI*x/Lx + ph)*np.cos(W*t)
        curve.set_data(x,y)
        points.set_data(x0, y0)
    else:
    	t += dt
    	y = np.cos(4*PI*x/Lx + ph)*np.cos(W*t)
        curve.set_data(x,y)

    plt.pause(0.008)