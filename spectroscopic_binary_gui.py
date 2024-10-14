#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 09:01:33 2023

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
#from imageio import imread
import pandas as pd



####################################################

# solve the nonlinear kepler equation that relates time and angular position in orbit
def kepler_eqn(t, period, ecc):
    E = np.zeros(len(t))
    for i in range(len(t)):
        Etmp = 0
        for j in range(100):  # number of iterations to solve nonlinear eqn
            Etmp = 2*np.pi*t[i] / period + ecc*np.sin(Etmp)
        E[i] = Etmp
    return E
		

def solve_orbit():
	global Ntimes, period, ecc, inc, long, theta, t, \
		xA, yA, xB, yB, centercoord, scale, view
	
	Psec = period * 24*3600
	Ntimes = 1000
	t = np.linspace(0, period, Ntimes, endpoint=False)   # units of days
	E = kepler_eqn(t, period, ecc)
	theta = np.arctan( (1+ecc)/(1-ecc)**0.5 * np.tan(E/2) ) * 2
	
	G = 6.6743e-11  # SI
	atot = (KA*1000 + KB*1000)*Psec*np.sqrt(1-ecc**2) / (2*np.pi*np.sin(inc*np.pi/180))
	mtot = 4*np.pi**2 * atot**3 / (G*Psec**2)
	mratio = KA/KB
	aA = KA*period*np.sqrt(1-ecc**2) / (2*np.pi*np.sin(inc*np.pi/180))
	aB = KB*period*np.sqrt(1-ecc**2) / (2*np.pi*np.sin(inc*np.pi/180))
	rA = aA*(1 - ecc*np.cos(E))
	rB = aB*(1 - ecc*np.cos(E))
	
	centercoord = 200
	scale = centercoord / np.max([rA, rB]) * .9

	if view == 1:   #  observer's view
		xA = rA * np.cos(theta) * scale
		yA = rA * np.sin(theta) * np.cos(inc*np.pi/180) * scale
		xB = rB * np.cos(theta + np.pi) * scale 
		yB = rB * np.sin(theta + np.pi) * np.cos(inc*np.pi/180) * scale		
		
	if view == 2:   # top-down view
		xA = rA * np.cos(theta) * scale
		yA = rA * np.sin(theta) * scale
		xB = rB * np.cos(theta + np.pi) * scale
		yB = rB * np.sin(theta + np.pi) * scale

	# rotation due to longitude setting 
	xAnew = xA * np.cos(long*np.pi/180) + yA * np.sin(long*np.pi/180)
	yAnew = -xA * np.sin(long*np.pi/180) + yA * np.cos(long*np.pi/180)
	xA = xAnew
	yA = yAnew
	
	xBnew = xB * np.cos(long*np.pi/180) + yB * np.sin(long*np.pi/180)
	yBnew = -xB * np.sin(long*np.pi/180) + yB * np.cos(long*np.pi/180)
	xB = xBnew
	yB = yBnew


# plot the binary stars from observer's perspective
def plot_orbits():
	global Ntimes, centercoord, inc, orbitA, orbitB
	
	colorA = 'paleturquoise'
	colorB = 'orangered'

	Apoints = []
	Bpoints = []
	for i in range(Ntimes):
		Apoints.append(xA[i] + centercoord)
		Apoints.append(yA[i] + centercoord)
		Bpoints.append(xB[i] + centercoord)
		Bpoints.append(yB[i] + centercoord)	
		
	orbitA = sky.create_line(Apoints, width=2, dash=(5, 4), fill=colorA)
	orbitB = sky.create_line(Bpoints, width=2, dash=(5, 4), fill=colorB)
	
	centerofmass = sky.create_oval(-3+centercoord, -3+centercoord, \
									3+centercoord, 3+centercoord, \
									fill='white')
	


# plot the simulated radial velocity curve
def plot_radvel():
	global stvar, period, sysvel, sep, inc, ecc, long, theta, t, KA, KB

	period = slider_period.get()
	Psec = period * 24*3600
	vrA = KA * ( np.cos(theta + long*np.pi/180) + ecc*np.cos(long*np.pi/180) )
	vrB = -KB * ( np.cos(theta + long*np.pi/180) + ecc*np.cos(long*np.pi/180) )

	if KA > KB:
		vrmax = 40 + np.max(np.abs(vrA))
	else:
		vrmax = 40 + np.max(np.abs(vrB))
		
	colorA = 'paleturquoise'
	colorB = 'orangered'

	f = Figure(figsize=(4.2, 4.2), dpi=100)
	f.patch.set_facecolor('lightgray')
	f.subplots_adjust(left=0.2, bottom=0.2)

	a = f.add_subplot(111)
	a.plot(t, vrA + sysvel, color=colorA)
	a.plot(t, vrB + sysvel, color=colorB)
	a.text(t[5], vrA[5] + sysvel, '1', color=colorA, fontsize=14)
	a.text(t[5], vrB[5] + sysvel, '2', color=colorB, fontsize=14)
	a.plot(t, sysvel + np.zeros(len(t)), 'w:')
	a.set_xlabel('Time (days)')
	a.set_ylabel('Radial Velocity (km/s')
	a.set_ylim(-1*vrmax, vrmax)
	a.set_facecolor("dimgray")   # set color inside axes
	
	# plot SB2 data
	if stvar != '(none)':
		phA = pd.to_numeric(ds[stvar]['Phase_A'])
		phB = pd.to_numeric(ds[stvar]['Phase_B'])
		vA = pd.to_numeric(ds[stvar]['V_A (km/s)'])
		vB = pd.to_numeric(ds[stvar]['V_B (km/s)'])
		Pbinary = pd.to_numeric(ds[stvar]['Period'][0])
		tA = phA * Pbinary
		tB = phB * Pbinary
		a.plot(tA, vA, color=colorA, marker='o', linestyle='None')
		a.plot(tB, vB, color=colorB, marker='o', linestyle='None')
		a.text(.8, .9, 'P = '+str(np.round(Pbinary, 2))+' d', \
			   horizontalalignment='right', verticalalignment='top', \
			   transform=a.transAxes, color='white', fontsize=14)
	
	
	plot = FigureCanvasTkAgg(f, master=obsframe)
	plot.draw()
	plot.get_tk_widget().place(relx=0, rely=0)	
	
	
def set_period(value):
	global period
	period = slider_period.get()
	plot_all()

def set_sysvel(value):
	global sysvel
	sysvel = slider_sysvel.get()
	plot_all()

	
def set_ecc(value):
	global ecc
	ecc = slider_ecc.get()
	plot_all()

	
def set_long(value):
	global long
	long = slider_long.get()
	plot_all()

	
def set_inc(value):
	global inc
	inc = slider_inc.get()
	plot_all()
	

def set_KA(value):
	global KA
	KA = slider_KA.get()
	plot_all()
	

def set_KB(value):
	global KB
	KB = slider_KB.get()
	plot_all()	
	

def set_view(value):
	global view
	view = slider_view.get()
	plot_all()
	

def plot_all():
	global sysvel, ecc, long, inc, KA, KB, view, orbitA, orbitB
	period = slider_period.get()
	sysvel = slider_sysvel.get()
	ecc = slider_ecc.get()
	inc = slider_inc.get()
	long = slider_long.get()
	KA = slider_KA.get()
	KB = slider_KB.get()
	view = slider_view.get()
	
	sky.delete(orbitA)
	sky.delete(orbitB)
	#sky.delete(starA)
	#sky.delete(starB)

	#get_current_settings()
	solve_orbit()
	plot_orbits()
	plot_radvel()
	

def get_current_settings():
	global period, ecc, inc, long, KA, KB, view
	period = slider_period.get()
	ecc = slider_ecc.get()
	inc = slider_inc.get()
	long = slider_long.get()
	KA = slider_KA.get()
	KB = slider_KB.get()
	

def set_star(value):
	global stvar
	stvar = str(starvar.get())
	plot_all()


####################################################

# create the master window
window = tk.Tk()
window.title("Spectroscopic Binary Simulator")
frameheight = 800
framewidth = frameheight
window.geometry(str(framewidth)+'x'+str(frameheight))


# frame to display menu options
menuframe = tk.Frame(window, width=framewidth/2, height=frameheight)
menuframe.grid_propagate(0)
menuframe.place(x=framewidth*1/2, y=0)


# upper frame to display binary star positions
posframe = tk.Frame(window, width=framewidth*1/2 + 3, height=frameheight*1/2)
posframe.grid_propagate(0)
posframe.place(x=-3, y=0)


# create canvas for posframe
sky = tk.Canvas(posframe, width=framewidth/2, height=frameheight/2)
sky.config(bg="dimgray")
sky.place(relx=0, rely=0)



# lower frame to display rad vel curve
obsframe = tk.Frame(window, width=framewidth*1/2, height=frameheight*1/2)
obsframe.grid_propagate(0)
obsframe.place(x=0, y=400)


# place the menu options...

# initialize the orbital parameters
row_pos = 0.1
label_section1 = tk.Label(menuframe, text="Vizualize Spectroscopic Binary System:", \
				font=("Ariel", 14))
label_section1.place(relx = 0.05, rely=row_pos)

# period slider bar
period = tk.DoubleVar()
label_period = tk.Label(menuframe, text="Orbital period (days): ", \
				font=("Ariel", 12))
label_period.place(relx = 0.1, rely=row_pos+.05)
slider_period = tk.Scale(menuframe, variable=period, \
						 orient=HORIZONTAL, showvalue=1, \
						 resolution=0.01, \
						 from_=1, to=30, tickinterval=0, command=set_period)  
slider_period.set(5)
slider_period.place(relx = 0.6, rely=row_pos+.03)



# eccentricity slider bar
ecc = tk.DoubleVar()
label_ecc = tk.Label(menuframe, text="Eccentricity of orbit: ", \
				font=("Ariel", 12))
label_ecc.place(relx = 0.1, rely=row_pos+.1)
slider_ecc = tk.Scale(menuframe, variable=ecc, \
					  resolution=0.05, \
					  orient=HORIZONTAL, showvalue=1, \
					  from_=0, to=0.9, tickinterval=0, command=set_ecc)
slider_ecc.set(0)
slider_ecc.place(relx = 0.6, rely=row_pos+.08)
ecc = slider_ecc.get()


# longitude of periastron
long = tk.DoubleVar()
label_long = tk.Label(menuframe, text="Longitude (degrees): ", \
					 font=("Ariel", 12))
label_long.place(relx = 0.1, rely=row_pos+.15)
slider_long = tk.Scale(menuframe, variable=long, \
						 orient=HORIZONTAL, showvalue=1, \
						 from_=0, to=360, tickinterval=0, command=set_long)  
slider_long.set(0)
slider_long.place(relx = 0.6, rely=row_pos+.13)
long = slider_long.get()


# inclination
inc = IntVar()
label_inc = tk.Label(menuframe, text="Inclination of orbit (degrees): ", \
				font=("Ariel", 12))
label_inc.place(relx = 0.1, rely=row_pos+.2)
label_inc2 = tk.Label(menuframe, text="(For visualization only.  Does not affect rad vel curve.)", \
				font=("Ariel", 10))
label_inc2.place(relx = 0.1, rely=row_pos+0.23)
slider_inc = tk.Scale(menuframe, variable=inc, \
					  orient=HORIZONTAL, showvalue=1, \
					  from_=1, to=90, tickinterval=0, command=set_inc)
slider_inc.set(90)
slider_inc.place(relx = 0.6, rely=row_pos+.18)
inc = slider_inc.get()


# change observer's view
view = IntVar()
label_view1 = tk.Label(menuframe, text="Observer's View", font=("Ariel", 12))
label_view1.place(relx = 0.15, rely=row_pos+.3)
label_view2 = tk.Label(menuframe, text="Top-Down View", font=("Ariel", 12))
label_view2.place(relx = 0.55, rely=row_pos+.3)
slider_view = tk.Scale(menuframe, orient=HORIZONTAL, length=50, \
					 variable=view, resolution=1, showvalue=0, \
					 from_=1, to=2, tickinterval=0, command=set_view )
slider_view.set(1)   # default to Observer's view
slider_view.place(relx = 0.41, rely=row_pos+.305)
view = slider_view.get()



# fitting radial velocity curve
row_pos = 0.6
label_section2 = tk.Label(menuframe, text="Additional Radial Velocity Parameters:", \
				font=("Ariel", 14))
label_section2.place(relx = 0.05, rely=row_pos)

# systemic velocity
sysvel = tk.DoubleVar()
label_sysvel = tk.Label(menuframe, text="C.O.M. velocity (km/s): ", \
					 font=("Ariel", 12))
label_sysvel.place(relx = 0.1, rely=row_pos+.05)
slider_sysvel = tk.Scale(menuframe, variable=sysvel, \
						 orient=HORIZONTAL, showvalue=1, \
						 resolution=0.1, \
						 from_=-40, to=40, tickinterval=0, command=set_sysvel)  
slider_sysvel.set(0)
slider_sysvel.place(relx = 0.6, rely=row_pos+.03)
sysvel = slider_sysvel.get()


KA = tk.DoubleVar()
label_KA = tk.Label(menuframe, text="K_1 (km/s): ", \
					 font=("Ariel", 12))
label_KA.place(relx = 0.1, rely=row_pos+.1)
slider_KA = tk.Scale(menuframe, variable=KA, \
						 orient=HORIZONTAL, showvalue=1, \
						 resolution=1, \
						 from_=1, to=300, tickinterval=0, command=set_KA)  
slider_KA.set(100)
slider_KA.place(relx = 0.6, rely=row_pos+.08)
KA = slider_KA.get()


KB = tk.DoubleVar()
label_KB = tk.Label(menuframe, text="K_2 (km/s)): ", \
					 font=("Ariel", 12))
label_KB.place(relx = 0.1, rely=row_pos+.15)
slider_KB = tk.Scale(menuframe, variable=KB, \
						 orient=HORIZONTAL, showvalue=1, \
						 resolution=1, \
						 from_=1, to=300, tickinterval=0, command=set_KB)  
slider_KB.set(100)
slider_KB.place(relx = 0.6, rely=row_pos+.13)
KB = slider_KB.get()


# read in stellar data; get list of available stars from the data file
#dir = '/Users/gmcswain/Documents/Lehigh/Teaching/ASTR008/GUIs/Binary Stars/'
ds = pd.read_excel('SB2 data.xlsx', sheet_name=None)
starlist = ['(none)']
for sheet_name in ds.keys():
    starlist.append(sheet_name)


# choose a binary star data set to include
row_pos = 0.85
starvar = tk.StringVar(menuframe)
starvar.set(starlist[0])
starlbl = tk.Label(menuframe, text="Select a dataset to include: ", \
				   font=("Ariel", 14))
starlbl.place(relx=0.05, rely=row_pos)
starmenu = tk.OptionMenu(menuframe, starvar, *starlist, command=set_star)
starmenu.place(relx=0.6, rely=row_pos)
stvar = '(none)'


# initiate plots with default settings
get_current_settings()
solve_orbit()
plot_orbits()
plot_radvel()



row_pos = 0.95
quit_button = tk.Button(menuframe, text="Quit Simulation")
quit_button.place(relwidth=0.7, relx=0.15, rely=row_pos)
quit_button['command'] = window.destroy



window.mainloop()