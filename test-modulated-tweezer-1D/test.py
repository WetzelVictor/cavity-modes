#!/usr/bin/env python

import matplotlib as plt
plt.use('TkAgg')
from plt.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from plt.backend_bases import key_press_handler


import numpy as np

from plt.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Embedding in TK")


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
dph = 0
x = np.linspace(0,Lx,1000)
A = 1.

y = A * (np.cos(4*PI*x/Lx + ph) + np.cos(4*PI*x/Lx)  )*np.cos(W*t)

fig, ax = plt.subplots()


for i in range(500):
    if t == 0:
        points, = ax.plot(x, y)
        ax.set_xlim(0, 10) 
        ax.set_ylim(-1, 1) 
        t += dt
    else:
    	t += dt
    	ph += dph
        y = np.sin(4*PI*x/Lx + ph)*np.cos(W*t)
        points.set_data(x,y)

    plt.pause(0.008)


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.