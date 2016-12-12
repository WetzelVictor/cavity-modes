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
import classTweezer as twe
import colorGraph as clg

""" === CONSTANTES === """
PI = np.pi

# Parametres physiques:
c0  = 440. # Celerite [m/s}
rho_f = 1   # Masse Volumique [kg/m^3]

# Dimensions de la piece:
Lx = 1 # m
Ly = 1 # m

# Constantes de discretisation:
Nx = 200 # Nombre de points sur x
Ny = 200 # Nombre de points sur y

# Limites des sommes sur les modes
M = 15
N = 15

""" === VARIABLES D'ESPACE === """
x = np.linspace(0,Lx,Nx)
y = np.linspace(0,Ly,Ny)

""" === EQUATIONS === """
X_mn = twe.Xmn(x,y,Lx,Ly,N=N,M=M)
masse = twe.Masse_Modale(x,y,Lx,Ly,N=N,M=M)
w_mn = twe.Pulsations_Propres(Lx, Ly, N, M, c0)

W0 = 440
W1 = 230


""" === INSTANCIATIONS DES SOURCES """
t = 0.001

# === Source 1 ===
source_gd = twe.source_paroi_gd(X_mn, masse, w_mn, x, y, Lx, Ly, Nx, Ny, N, M, F0=1, W=440, amor = 0.01)
source_gd.calcule_reponse(t)

# === Source 2 ===
source_hb = twe.source_paroi_hb(X_mn, masse, w_mn, x, y, Lx, Ly, Nx, Ny, N, M, F0=1, W=440, amor = 0.01)
source_hb.calcule_reponse(t)

ultime = source_hb.response.rep_pression + source_gd.response.rep_pression

table1 = w_mn.get_table()


""" === FENETRE WX === """

class MyFrame(wx.Frame):
    
	def __init__(self, parent, title, pos, size):

		global ultime
		global source_hb
		global source_gd
		global t
		global table1
		

		# The Frame
		wx.Frame.__init__(self, parent, id=-1, title=title, pos=pos, size=size)
		self.panel = wx.Panel(self)
		self.panel.SetBackgroundColour("Pink")

		# The Boxes
		self.boxReponseForcee = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(5, 2), size=(350, 260))
		self.subboxTitre = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(120, 2), size=(160, 50))
		self.subboxTitre = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(120, 2), size=(160, 50))
		self.boxYX = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(5, 2), size=(115, 50))
		self.boxTable = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(5, 100), size=(350, 162))

		# The Textes
		self.textTweezers = wx.StaticText(self.panel, id=-1, label="ACOUSTIC TWEEZERS", pos=(130, 23), size=wx.DefaultSize)
		self.textTweezers.SetForegroundColour((130, 140, 10))
		self.AmpText = wx.StaticText(self.panel, id=-1, label="Amplitudes", pos=(180, 70), size=wx.DefaultSize)
		# The First Table
		self.firstTable = wx.StaticText(self.panel, id=-1, label=table1[0], pos=(50, 110), size=wx.DefaultSize)
		self.secondTable = wx.StaticText(self.panel, id=-1, label=table1[1], pos=(200, 110), size=wx.DefaultSize)

		# The Pos Text
		self.XFreqText = wx.StaticText(self.panel, id=-1, label="100", pos=(10, 20), size=wx.DefaultSize)
		self.virguleText = wx.StaticText(self.panel, id=-1, label=",", pos=(55, 20), size=wx.DefaultSize)
		self.YFreqText = wx.StaticText(self.panel, id=-1, label="100", pos=(65, 20), size=wx.DefaultSize)

		#-------------------------------

		# The X Amp Slider
		self.Xslider = wx.Slider(self.panel, id=-1, value=100, minValue=0, maxValue=100, pos=(100, 53), size=(250, -1))
		self.Xslider.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.changeXAmp)

		# The Y Amp Slider
		self.Yslider = wx.Slider(self.panel, id=-1, value=100, minValue=0, maxValue=100, pos=(100, 83), size=(250,-1))
		self.Yslider.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.changeYAmp)

		# The Enter X Bouton
		self.enterXBouton = wx.Button(self.panel, id=-1, label="X FREQ", pos=(5, 50))
		self.enterXBouton.Bind(wx.EVT_BUTTON, self.enterXPulse)

		# The Enter Y Bouton
		self.enterYBouton = wx.Button(self.panel, id=-1, label="Y FREQ", pos=(5, 80))
		self.enterYBouton.Bind(wx.EVT_BUTTON, self.enterYPulse)

		# The Exit Bouton
		self.exitBouton = wx.Button(self.panel, id=-1, label="QUITTER", pos=(250, 400))
		self.exitBouton.Bind(wx.EVT_BUTTON, self.exit)

	def updateColorGraph(self):
		plt.clf()
		plt.close()
		ultime = source_hb.response.rep_pression + source_gd.response.rep_pression
		clg.colorGraph1(ultime, title="Acoustic Tweezers")

	def changeFreqX(self, x):
		new = float(x)
		self.XFreqText.SetLabel("%d" %new)
		#source_hb.setPulse(2*PI*x)
		source_hb.W = new
		source_hb.compute_amps()
		source_hb.calcule_reponse(t)
		self.updateColorGraph()

	def changeFreqY(self, y):
		new = float(y)
		self.YFreqText.SetLabel("%d" %new)
		#source_hb.setPulse(2*PI*x)
		source_gd.W = new
		source_gd.compute_amps()
		source_gd.calcule_reponse(t)
		self.updateColorGraph()

	def enterXPulse(self, evt):
		x = evt.GetInt()
		saveBox = wx.TextEntryDialog(None, "Pulsation en X ?", "", "440")
		if saveBox.ShowModal()==wx.ID_OK:
			saveX = saveBox.GetValue()
			self.changeFreqX(saveX)

	def enterYPulse(self, evt):
		y = evt.GetInt()
		saveBox = wx.TextEntryDialog(None, "Pulsation en Y ?", "", "440")
		if saveBox.ShowModal()==wx.ID_OK:
			saveY = saveBox.GetValue()
			self.changeFreqY(saveY)

	def changeXAmp(self, evt):
		source_hb.F0 = evt.GetInt() * 0.01
		source_hb.compute_amps()
		source_hb.calcule_reponse(t)
		self.updateColorGraph()

	def changeYAmp(self, evt):
		source_gd.F0 = evt.GetInt() * 0.01
		source_gd.compute_amps()
		source_gd.calcule_reponse(t)
		self.updateColorGraph()

	#-------------------------------

	def exit(self, evt):
		sys.exit(0)


""" === VISUALISATION === """

if __name__ =='__main__':
	
	app = wx.App()
	mainFrame = MyFrame(None, title=NAME + " " + VERSION, pos=(700, 400), size=(360, 460))
	mainFrame.Show()
	MyFrame.updateColorGraph(mainFrame)	
	app.MainLoop()