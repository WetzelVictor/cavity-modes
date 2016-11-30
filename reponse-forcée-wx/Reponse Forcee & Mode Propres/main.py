#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modelisation et visualisation de la réponse acoustique
d'une cavité parallèlepipédique 2D parfaitement régléchissante
"""

NAME = "Projet acoustique"
VERSION = "1.0"


""" === BIBLIOTHEQUES === """
import numpy as np 
from matplotlib import pyplot as plt
import math 
import wx
import sys
import classReponseForcee as repl
import colorGraph as clg
import threading




""" === CONSTANTES === """
PI = np.pi

# Parametres physiques:
c0  = 440 # Celerite [m/s}
rho = 1   # Masse Volumique [kg/m^3]

# Dimensions de la piece:
Lx = 1 # m
Ly = 1 # m

# Constantes de discretisation:
Nx = 200*Lx # Nombre de points sur x
Ny = 200*Ly # Nombre de points sur y

# Limites des sommes sur les modes
M = 15
N = 15

# Paramètres de la source
F0 = 100  # Amplitude
W  = 440 # Pulsation d'excitation

x0 = 100*Lx # Position (x,y) de la source
y0 = 100*Ly # Comment l'indiquer sur le graph? En blanc?




""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)




""" === EQUATIONS === """
X = repl.Xmn(x,y,Lx,Ly,N=N,M=M)
masse = repl.Masse_Modale(x,y,Lx,Ly,N=N,M=M)
w_mn = repl.Pulsations_Propres(Lx, Ly, N, M, c0)

W = int(w_mn.get_w(4,0))

amp = repl.Amplitude_forcee(X, masse, w_mn, x0, y0, F0, W, N, M)
resultat = repl.Modes_Forces(X, amp, M, N, Nx, Ny)






""" === FENETRE WX === """

class MyFrame(wx.Frame):
    
	def __init__(self, parent, title, pos, size):

		global resultat
		global amp	
		global X

		self.graphN = 0
		self.graphM = 0
		self.f = 0
		self.W = 0
		self.t = 2.01

        # The Frame
		wx.Frame.__init__(self, parent, id=-1, title=title, pos=pos, size=size)
		self.panel = wx.Panel(self)
		self.panel.SetBackgroundColour("gray")

		# The Boxes
		self.boxReponseForcee = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(5, 2), size=(350, 260))
		self.subboxReponseForcee1 = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(80, 120), size=(135, 50))
		self.subboxReponseForcee2 = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(80, 120), size=(135, 50))

		self.boxModesPropres = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(5, 250), size=(350, 150))
		self.subboxModesPropres1 = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(90, 280), size=(127, 50))
		self.subboxModesPropres2 = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(90, 280), size=(127, 50))
		self.boxYX = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(5, 2), size=(90, 50))

		# The Textes
		self.textReponseForcee = wx.StaticText(self.panel, id=-1, label="REPONSE FORCEE", pos=(90, 140), size=wx.DefaultSize)
		self.textReponseForcee.SetForegroundColour((0, 40, 254))

		self.textModesPropres = wx.StaticText(self.panel, id=-1, label="MODES PROPRES", pos=(100, 300), size=wx.DefaultSize)
		self.textModesPropres.SetForegroundColour((0, 40, 254))


		#-------------------------------

		# The Pos Text
		self.XposText = wx.StaticText(self.panel, id=-1, label="100", pos=(10, 20), size=wx.DefaultSize)
		self.virguleText = wx.StaticText(self.panel, id=-1, label=",", pos=(43, 20), size=wx.DefaultSize)
		self.YposText = wx.StaticText(self.panel, id=-1, label="100", pos=(55, 20), size=wx.DefaultSize)

        # The X Slider
		self.XsliderText = wx.StaticText(self.panel, id=-1, label="Position en X", pos=(20, 230), size=wx.DefaultSize)
		self.Xslider = wx.Slider(self.panel, id=-1, value=x0, minValue=0, maxValue=(Nx-1), pos=(20, 210), size=(250, -1))
		self.Xslider.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.changeXPos)
        
        # The Y Slider
		self.YsliderText = wx.StaticText(self.panel, id=-1, label="Position en Y", pos=(235, 20), size=wx.DefaultSize)
		self.Yslider = wx.Slider(self.panel, id=-1, value=y0, minValue=0, maxValue=(Ny-1), pos=(270, 40), size=(-1,200), style=wx.SL_VERTICAL)
		self.Yslider.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.changeYPos)

		# The Frequency Slider
		self.frequencyText = wx.StaticText(self.panel, id=-1, label="Frequence : 150", pos=(20, 80), size=wx.DefaultSize)
		self.frequency = wx.Slider(self.panel, id=-1, value=150, minValue=20, maxValue=1000, pos=(20, 60), size=(250, -1))
		self.frequency.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.changeFrequency)

		# The Center Bouton
		self.centerBouton = wx.Button(self.panel, id=-1, label="CENTRER", pos=(100, 17))
		self.centerBouton.Bind(wx.EVT_BUTTON, self.doCenter)

		#-------------------------------

		# The Modes Text
		self.modesText1 = wx.StaticText(self.panel, id=-1, label="Modes  	(", pos=(30, 353), size=wx.DefaultSize)
		self.modesText2 = wx.StaticText(self.panel, id=-1, label=",", pos=(180, 353), size=wx.DefaultSize)
		self.modesText3 = wx.StaticText(self.panel, id=-1, label=")", pos=(275, 353), size=wx.DefaultSize)

		# The Mode N Boxe
		self.modeNChoice = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
		self.modeN = wx.Choice(self.panel, id=-1, pos=(100, 350), size=wx.DefaultSize, choices=self.modeNChoice)
		self.modeN.Bind(wx.EVT_CHOICE, self.changeModeN)

		# The Mode M Boxe
		self.modeMChoice = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
		self.modeM = wx.Choice(self.panel, id=-1, pos=(200, 350), size=wx.DefaultSize, choices=self.modeMChoice)
		self.modeM.Bind(wx.EVT_CHOICE, self.changeModeM)

		#-------------------------------

		# The Exit Bouton
		self.exitBouton = wx.Button(self.panel, id=-1, label="QUITTER", pos=(250, 400))
		self.exitBouton.Bind(wx.EVT_BUTTON, self.exit)

	#-------------------------------

	def updateReponseForcee(self):
		amp.W = self.W
		amp.compute_amps()
		resultat.calcule_reponse(self.t, self.W)
		plt.clf()
		plt.close()
		clg.graphReponseForcee(resultat, x0=amp.x0, y0=amp.y0 , title="Reponse Forcee")

	def closeReponseForcee(self):
		plt.clf()
		plt.close()

	def changeXPos(self, evt):
		x = evt.GetInt()
		amp.set_XPos(x)
		self.XposText.SetLabel("%d" %x)
		self.updateReponseForcee()

	def changeYPos(self, evt):
		y = evt.GetInt()
		amp.set_YPos(y)
		self.YposText.SetLabel("%d" %y)
		self.updateReponseForcee()

	def changeFrequency(self, evt):
		self.f = evt.GetInt()
		self.frequencyText.SetLabel("Frequence : %d" %self.f)
		self.W = 2*PI*self.f
		self.updateReponseForcee()

	#-------------------------------

	def updateModePropres(self):
		plt.clf()
		plt.close()
		clg.graphModesPropres(X, self.graphN, self.graphM)

	def changeModeN(self, evt):
		n = evt.GetInt() 
		self.graphN = n
		self.updateModePropres()

	def changeModeM(self, evt):
		m = evt.GetInt()
		self.graphM = m
		self.updateModePropres()

	def doCenter(self, evt):
		amp.set_XPos(100)
		self.XposText.SetLabel("100")
		self.Xslider.SetValue(100)
		amp.set_YPos(100)
		self.YposText.SetLabel("100")
		self.Yslider.SetValue(100)
		self.updateReponseForcee()

	#-------------------------------

	def exit(self, evt):
		sys.exit(0)



""" === VISUALISATION === """
title = 'Reponse d\'une cavite de dimension ({0},{1}) a une excitation harmonique de frequence w = {2} (rad/s)'.format(Lx, Ly, W)

if __name__ =='__main__':
	
	app = wx.App()
	mainFrame = MyFrame(None, title=NAME + " " + VERSION, pos=(700, 400), size=(360, 460))
	mainFrame.Show()
	MyFrame.updateReponseForcee(mainFrame)	
	app.MainLoop()
	
	

