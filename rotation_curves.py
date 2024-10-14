#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 13:33:19 2023

@author: gmcswain
"""
import tkinter as tk
from tkinter import *
import numpy as np 

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
from imageio import imread

import astropy.units as u
from astropy import constants as const
from galpy.potential import MiyamotoNagaiPotential, NFWPotential, HernquistPotential
from galpy.potential import plotRotcurve


####################################################################

def set_gal():
	global gal, index
	gal = galvar.get()
	index = gallist[gal]
	#print (index)
	plot_rotcurve()	

def set_disk(value):
	global logStellarMass
	logStellarMass = slider_disk.get()
	#print (logStellarMass)
	plot_rotcurve()
	
def set_halo(value):
	global logHaloMass
	logHaloMass = slider_halo.get()
	#print (logHaloMass)
	plot_rotcurve()

def plot_rotcurve():
	global gal, index, logStellarMass, logHaloMass
	
	#print (logStellarMass, logHaloMass)
	
	good = np.where(j == index)
	Rmax = np.max(R[good]) * u.kpc
	#print (Rmax.value)
	Vlast = V_R[good][-1] * u.km / u.s
	#Mtot = Rmax * Vlast**2 / const.G
	#print (np.log10(Mtot.to(u.Msun).value))
	
	# set up potential models
	c = 1   # concentration parameter; setting to 1 for simplicity
	Ropt = ropt[good][0] * u.kpc    # optical radius from Dehghani+, 2020
	#Rvir = Ropt * c     	        # virial radius

	HaloMass = 10**logHaloMass * u.Msun
	A_NFW = np.log(1+c) - c/(1+c)
	amp_NFW = HaloMass / A_NFW

	stellar_mass = 10**logStellarMass * u.Msun
	disk_thickness = 300.*u.pc

	mp = MiyamotoNagaiPotential(amp=stellar_mass*const.G, a=Ropt/2, b=disk_thickness)  # stellar disk
	nfwp = NFWPotential(amp=amp_NFW, a=Rmax)  # dark matter halo
	Rmodel = np.linspace(0.1, Rmax.value, 1000)*u.kpc
	halo_vcirc = nfwp.vcirc(Rmodel) * u.km/u.s
	disk_vcirc = mp.vcirc(Rmodel) * u.km/u.s
	total_vcirc = np.sqrt(halo_vcirc**2 + disk_vcirc**2)


	f = Figure(figsize=(6,5), dpi=100)
	f.subplots_adjust(left=0.1, bottom=0.1)
	a = f.add_subplot(111)

	a.errorbar(R[good], V_R[good], yerr=eV_R[good], capsize=4, fmt='ko', label='Data')
	a.plot(Rmodel, disk_vcirc, 'b:', label='Stellar Disk')
	a.plot(Rmodel, halo_vcirc, 'r:', label='Dark Matter Halo')
	a.plot(Rmodel, total_vcirc, '-', color='purple', label='Total from Both')
	#a.mp.plotRotcurve(grid=1001,overplot=True, color='b', linestyle='dashed', label='Stellar Disk')
	#nfwp.plotRotcurve(grid=1001,overplot=True, color='r', linestyle='dashed', label='Dark Matter Halo')
	#plotRotcurve(mp+nfwp, overplot=True, color='purple', linestyle='dashed', label='Total')

	#a.set_ylim(0, np.max(V_R[good]+30))
	#a.set_xlim(0, np.max(R[good])+1)
	a.set_xlabel('R (kpc)')
	a.set_ylabel('V (km/s)')
	a.legend(loc='lower right')
	
	f.tight_layout()
	plot = FigureCanvasTkAgg(f, master=graphframe)
	plot.draw()
	plot.get_tk_widget().place(relx=0, rely=0)



####################################################################

# create the master window
window = tk.Tk()
window.title("Galaxy Rotation Curves")
framewidth = 900
frameheight = 500
window.geometry(str(framewidth)+'x'+str(frameheight))

# frame to display menu options
menuframe = tk.Frame(window, width=framewidth/3, height=frameheight)
menuframe.grid_propagate(0)
menuframe.place(x=0, y=0)
#menuframe.place(x=framewidth*2/3, y=0)

# frame to display graphs
graphframe = tk.Frame(window, width=framewidth*2/3, height=frameheight)
graphframe.grid_propagate(0)
graphframe.place(x=framewidth/3, y=0)
#graphframe.place(x=0, y=0)



# read the rotation curve data from Dehghani+, 2020
#dir = '/Users/gmcswain/Documents/Lehigh/Teaching/ASTR008/GUIs/Gal_Rot_Curves/'
#data = np.loadtxt(dir+'dehghani+2020.tsv', delimiter='|', skiprows=41)
data = np.loadtxt('dehghani+2020.tsv', delimiter='|', skiprows=41)
j = data[:, 0]
vopt = data[:, 1]
ropt = data[:, 2]
R = data[:, 4]
V_R = data[:, 5]
eV_R = data[:, 6]

# List of unknown galaxies
# index numbers correspond to the j values from Dehghani+, 2020
galnamelist = ['Galaxy A', 'Galaxy B', 'Galaxy C', 'Galaxy D', 'Galaxy E', \
			   'Galaxy F', 'Galaxy G', 'Galaxy H', 'Galaxy I', 'Galaxy J']
indexlist = [6, 7, 8, 9, 13, 14, 19, 20, 21, 22]
gallist = dict(zip(galnamelist, indexlist))


#  Fitting notes:
#  good/great fits using mp, nfwp models with indices 6, 7, 8, 9, 13, 14, 19, 20, 21, 22
#  ok fits with index 4, 5, 11, 23
#  poor fits with indices 1, 2, 3, 10, 12, 15, 16, 17, 18, 24, 25, 26


# Display menu of galaxy options
row_pos = 0.1
galvar = tk.StringVar(menuframe)
galvar.set(galnamelist[0])   # default 
gallbl = tk.Label(menuframe, text="Select a galaxy to investigate: ", \
				  font=("Ariel", 14))
gallbl.place(relx=0.1, rely=row_pos)
galmenu = tk.OptionMenu(menuframe, galvar, *galnamelist)
galmenu.place(relx=0.2, rely=row_pos+0.05)
setgalbtn = tk.Button(menuframe, text="Submit",  command=set_gal)
setgalbtn.place(relx=0.6, rely=row_pos+0.05)


# properties of galaxy stellar disk
row_pos = 0.3
label_disk = tk.Label(menuframe, text="Stellar Disk:", \
				font=("Ariel", 14))
label_disk.place(relx = 0.1, rely=row_pos)

mass_disk = tk.DoubleVar()
label_disk2 = tk.Label(menuframe, text="log(Mass) ", \
				font=("Ariel", 14))
label_disk2.place(relx = 0.2, rely=row_pos+.05)
slider_disk = tk.Scale(menuframe, orient=HORIZONTAL, \
					 variable=mass_disk, resolution=0.1, showvalue=1, \
					 from_=8, to=12, tickinterval=0, command=set_disk)
slider_disk.set(10)
slider_disk.place(relx = 0.5, rely=row_pos+.05)
logStellarMass = slider_disk.get()


# dark matter halo
row_pos = 0.5
label_halo = tk.Label(menuframe, text="Dark Matter Halo:", \
				font=("Ariel", 14))
label_halo.place(relx = 0.1, rely=row_pos)

mass_halo = tk.DoubleVar()
label_halo2 = tk.Label(menuframe, text="log(Mass): ", \
				font=("Ariel", 14))
label_halo2.place(relx = 0.2, rely=row_pos+.05)
slider_halo = tk.Scale(menuframe, orient=HORIZONTAL, \
					 variable=mass_halo, resolution=0.1, showvalue=1, \
					 from_=8, to=12, tickinterval=0, command=set_halo)
slider_halo.set(10)
slider_halo.place(relx = 0.5, rely=row_pos+.05)
logHaloMass = slider_halo.get()


row_pos = 0.9
quit_button = tk.Button(menuframe, text="Quit Simulation")
quit_button.place(relwidth=0.7, relx=0.15, rely=row_pos)
#quit_button['command'] = window.destroy
quit_button['command'] = window.quit


# plot the first galaxy by default
index=indexlist[0]
plot_rotcurve()

window.mainloop()

