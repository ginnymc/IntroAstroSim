#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 11:40:48 2025

@author: gmcswain
"""
import tkinter as tk
from tkinter import *
import numpy as np 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt
#from imageio import imread
import pandas as pd
import lightkurve as lk


def set_star(option):
	global star
	star = starvar.get()
	plot_lc()
	plot_folded()
	
def set_period(value): 
	global period
	period = slider_period.get()
	plot_folded()

def set_phshift(value): 
	global phshift
	phshift = slider_phshift.get()
	plot_folded()	


# plot the full lightcurve
def plot_lc():
	global star, time, Tmag
	#print ('LC plot coming soon')
	
	#search_result = lk.search_lightcurve(star, author="SPOC", exptime=120)
	search_result = lk.search_lightcurve(star, author="SPOC")
	lcf = search_result.download_all()
	
	flux = lcf[0].pdcsap_flux
	time = lcf[0].time
	good = np.isfinite(flux)
	time = np.array(time[good].value)  + 2457000.
	flux = np.array(flux[good].value)
	Tmag = -2.5*np.log10(flux) + 20.44
	
	f = Figure(figsize=(8, 3), dpi=100)
	f.patch.set_facecolor('aliceblue')
	f.subplots_adjust(left=0.11, bottom=0.16)

	a = f.add_subplot(111)
	a.plot(time, Tmag, '.', label=star)
	a.set_xlabel('Time as BJD (days)')
	a.set_ylabel('TESS Apparent Magnitude')
	a.invert_yaxis()
	a.set_title("Original Lightcurve from NASA's TESS Mission")
	a.legend(loc='upper right')
	
	#f.tight_layout()
	plot = FigureCanvasTkAgg(f, master=lc_frame)  # A tk.DrawingArea.
	plot.draw()
	plot.get_tk_widget().place(relx=0, rely=0)


	

# plot the folded lightcurve
def plot_folded():
	global star, period, time, Tmag, phshift
	
	phase = (time / period - phshift) % 1
	f2 = Figure(figsize=(4, 3), dpi=100)
	f2.patch.set_facecolor('lightsteelblue')
	f2.subplots_adjust(left=0.22, bottom=0.16)

	a = f2.add_subplot(111)
	a.plot(phase, Tmag, '.')
	a.set_xlabel('Phase')
	a.set_ylabel('TESS Apparent Magnitude')
	a.invert_yaxis()
	a.set_title('Folded Lightcurve')
		
	#f.tight_layout()
	plot = FigureCanvasTkAgg(f2, master=folded_frame)  # A tk.DrawingArea.
	plot.draw()
	plot.get_tk_widget().place(relx=0, rely=0)


##########################################################3

# create the master window
window = tk.Tk()
window.title("Variable Stars")
framewidth = 800
frameheight = 600
window.geometry(str(framewidth)+'x'+str(frameheight))

# create full lightcurve panel
lc_frame = tk.Frame(window, width=framewidth, height=frameheight/2)
lc_frame.grid_propagate(0)
lc_frame.place(x=0, y=0)

# create folded lightcurve panel
folded_frame = tk.Frame(window, width=framewidth/2, height=frameheight/2)
folded_frame.grid_propagate(0)
folded_frame.place(x=0, y=frameheight/2)

# create the control panel menu
menu_frame = tk.Frame(window, width=framewidth/2, height=frameheight/2)
menu_frame.grid_propagate(0)
menu_frame.place(x=framewidth/2, y=frameheight/2)

'''
# Cepheids in list:
V473 Lyr - P = 1.49
Y Sgr -  P = 5.77 d
AD Gem - P = 3.78
RZ CMa - P = 4.26
GH Car - P = 5.74
FR Car - P = 10.7
TW CMa - P = 7.00
WX Pup - P = 8.94
AA Gem - P = 11.31
AT Pup - P = 6.67
SS CMa - P = 12.3
DR Vel - P = 11.20
V Cen - P = 5.50
X Sgr - P = 7.00
ST Vel - P = 5.86
AC Mon - P = 8.01
VY Cyg - P = 7.86
WW Car - P = 4.68
RV Sco - P = 6.06
V339 Cen - P = 9.47
CY Car - 4.27
UZ Car - 5.20
V1344 Aql - 7.48
V440 Per - 7.57
MW Cyg - 5.95
GU Nor - 3.45
V659 Cen - 5.63
V378 Cen - 6.46
V402 Cyg - 4.36
V495 Cyg - 6.71
V1154 Cyg - 4.93
SX Car - 4.86
GH Lup - 9.28
ER Car - 7.72
26 Cir - 5.27
V419 Cen - 5.50
AP Pup - 5.08
GH Cyg - 7.82
V438 Cyg - 11.21
R Cru - 5.83
'''

# dropdown menu to select target star
row_pos = 0.1
starlist = ['R Cru', 'V438 Cyg', 'GH Cyg', 'AP Pup', 'V419 Cen', '26 Cir', \
			'ER Car', 'GH Lup', 'SX Car', 'V1154 Cyg', 'V495 Cyg', 'V402 Cyg', \
			'V378 Cen', 'V659 Cen', 'GU Nor', 'MW Cyg', 'V440 Per', 'V1344 Aql', \
			'UZ Car', 'CY Car', 'V339 Cen', 'RV Sco', 'WW Car', 'VY Cyg', \
			'AC Mon', 'ST Vel', 'X Sgr', 'V Cen', 'DR Vel', 'SS CMa', 'AT Pup', \
			'AS Per', 'V473 Lyr', 'Y Sgr', 'AD Gem', \
			'RZ CMa', 'GH Car', 'FR Car', 'TW CMa', 'WX Pup', 'AA Gem']
starvar = tk.StringVar(menu_frame)
starvar.set(starlist[0])   # default
star = starlist[0]   # default
starlbl = tk.Label(menu_frame, text="Select a star to view its lightcurve: ", \
				   font=("Ariel", 16))
starlbl.place(relx=0.1, rely=row_pos)
starmenu = tk.OptionMenu(menu_frame, starvar, *starlist, command=set_star)
starmenu.place(relx=0.15, rely=row_pos+.1)


# slider bar to test different periods
row_pos = 0.5
period = tk.IntVar()
label_period = tk.Label(menu_frame, text="Period (days): ", \
 				font=("Ariel", 14))
label_period.place(relx = 0.1, rely=row_pos)
slider_period = tk.Scale(menu_frame, variable=period, \
 					  orient=HORIZONTAL, showvalue=1, \
					  resolution=0.01, \
 					  from_=0.1, to=20, tickinterval=0, command=set_period)
slider_period.set(1)
slider_period.place(relx = 0.5, rely=row_pos-0.02)
period = slider_period.get()


# slider bar for phase shift
phshift = tk.IntVar()
label_phshift = tk.Label(menu_frame, text="Phase shift: ", \
 				font=("Ariel", 14))
label_phshift.place(relx = 0.1, rely=row_pos+.15)
slider_phshift = tk.Scale(menu_frame, variable=phshift, \
 					  orient=HORIZONTAL, showvalue=1, \
					  resolution=0.01, \
 					  from_=-0.5, to=0.5, tickinterval=0, command=set_phshift)
slider_phshift.set(0)
slider_phshift.place(relx = 0.5, rely=row_pos+.13)
phshift = slider_phshift.get()

# initial plots for the default star with default period, ph shift
plot_lc()
plot_folded()



# display the measured magnitude from folded lc



# place the data acknowledement labels
#row_pos = 0.7
#infolabel = tk.Label(menu_frame, text="Data from NASA's TESS Mission", \
#                     font=("Ariel", 14))
#infolabel.place(relx = 0.1, rely=row_pos)

row_pos = 0.8
quit_button = tk.Button(menu_frame, text="Quit Simulation")
quit_button.place(relwidth=0.7, relx=0.15, rely=row_pos)
quit_button['command'] = window.destroy


window.mainloop()