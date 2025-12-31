#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: gmcswain
M. Virginia McSwain
Lehigh University

ALMA images courtesy of the Disk Substructures at High Angular Resolution 
Project  (DSHARP; Andrews et al. 2018, ApJ, 869, L41).  They are available 
for download at https://bulk.cv.nrao.edu/almadata/lp/DSHARP/ .

Since the images are not easily accessible online from a python script, I 
saved them to my local hard drive.  Be sure to update the path to your own 
saved version of the images.
"""


import tkinter as tk
from tkinter import *
import datetime as dt
import numpy as np 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from astropy.io import fits



def set_star(option):
    global star
    star = starvar.get()
    plot_disk()
	
def set_colormap(option):
    global colormap
    colormap = colormapvar.get()
    plot_disk()
	
def set_rad(value):
	global rad	
	rad = slider_rad.get()
	plot_disk()
	
def set_xoff(value):
	global xoff	
	xoff = slider_xoff.get()
	plot_disk()
	
def set_yoff(value):
	global yoff	
	yoff = slider_yoff.get()
	plot_disk()

def set_inc(value):
	global inc	
	inc = slider_inc.get()
	plot_disk()
    
def set_pos_angle(value):
	global pos_angle
	pos_angle = slider_pos_angle.get()
	plot_disk()

def set_zoom(value):
	global zoom
	zoom = slider_zoom.get()
	plot_disk()	


def plot_disk():
	global star, zoom, rad, pos_angle, xoff, yoff
		

	# retrieve the image data
	dir = "/Users/gmcswain/Documents/Lehigh/Teaching/ASTR008/GUIs/Disks/"
	#dir = ""
	image_file = dir + star + '_continuum.fits'
	image_data, header = fits.getdata(image_file, header=True) 
	nx = header['NAXIS1']
	ny = header['NAXIS2']
	startx = np.int16(nx * 0.1*zoom/2)
	endx = np.int16(nx * (1 - 0.1*zoom/2))
	starty = np.int16(ny * 0.1*zoom/2)
	endy = np.int16(ny * (1 - 0.1*zoom/2))
	rows = image_data.shape[2]
	cols = image_data.shape[3]
	im = image_data.reshape(rows, cols) 
	f = Figure(figsize=(8,8), dpi=100)
	#f.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)  # sets boundary around image
	f.subplots_adjust(left=0, bottom=0, right=1, top=1)  # no boundary
	a = f.add_subplot(111)
	a.imshow(im[startx:endx, starty:endy], cmap='hot')
	a.axis('off')

	pixscale = header['CDELT2'] * 3600 * 1000   # units of milliarcsec
	#print (pixscale)
	
	# draw circle to measure disk, including inclination and position angle
	theta = np.arange(0, 2*np.pi, 2*np.pi/1000)
	xdisk = rad * np.cos(theta) 
	ydisk = rad * np.sin(theta) * np.cos(inc*np.pi/180) 
	xdisk_new = xdisk * np.cos(pos_angle*np.pi/180) + ydisk * np.sin(pos_angle*np.pi/180)
	ydisk_new = -xdisk * np.sin(pos_angle*np.pi/180) + ydisk * np.cos(pos_angle*np.pi/180)
	xdisk = xdisk_new
	ydisk = ydisk_new
	xcent = (endx - startx)/2 
	ycent = (endy - starty)/2
	xtool = xdisk + xcent + xoff
	ytool = ydisk + ycent - yoff
	
	# prevent the measuring tool from messing up the image frame when zoomed in
	tmp = np.where(xtool > 0, xtool, 0)
	xtool = tmp
	tmp = np.where(xtool < 2*xcent-1, xtool, 2*xcent-1)
	xtool = tmp
	tmp = np.where(ytool > 0, ytool, 0)
	ytool = tmp
	tmp = np.where(ytool < 2*ycent-1, ytool, 2*ycent-1)
	ytool = tmp
	
	if showtool.get() == 1:
		a.plot(xtool, ytool, 'w-', linewidth=1)

	plot = FigureCanvasTkAgg(f, master=imageframe)
	plot.draw()
	plot.get_tk_widget().place(relx=0, rely=0)


    
###########################################################


# create the master window
window = tk.Tk()
window.title("Protoplanetary Disks with ALMA")
frameheight = 800
framewidth = int(frameheight*1.5)
window.geometry(str(framewidth)+'x'+str(frameheight))


# frame to display menu options
menuframe = tk.Frame(window, width=framewidth/3, height=frameheight)
menuframe.grid_propagate(0)
menuframe.place(x=framewidth*2/3, y=0)


# frame to display images
imageframe = tk.Frame(window, width=framewidth*2/3, height=frameheight)
imageframe.grid_propagate(0)
imageframe.place(x=0, y=0)

row_pos = 0.1

# dropdown menu to select target star
starlist = ['AS205', 'AS209', 'DoAr25', 'DoAr33', 'Elias20', 'Elias24', \
			'Elias27', 'GWLup', 'HD142666', 'HD143006', 'HD163296', 'HTLup', \
			'IMLup', 'MYLup', 'RULup', 'SR4', 'Sz114', 'Sz129', 'WaOph6', \
			'WSB52']
starvar = tk.StringVar(menuframe)
starvar.set(starlist[0])   # default
star = starlist[0]   # default
starlbl = tk.Label(menuframe, text="Select a star to view its disk: ", \
				   font=("Ariel", 16))
starlbl.place(relx=0.1, rely=row_pos)
starmenu = tk.OptionMenu(menuframe, starvar, *starlist, command=set_star)
starmenu.place(relx=0.7, rely=row_pos+.002)


# add menu to select color map?
#colorlist = ['gray', 'hot']

# zoom in or out
zoom = tk.IntVar()
label_zoom = tk.Label(menuframe, text="Zoom factor: ", \
 				font=("Ariel", 14))
label_zoom.place(relx = 0.1, rely=row_pos+.05)
slider_zoom = tk.Scale(menuframe, variable=zoom, \
 					  orient=HORIZONTAL, showvalue=1, \
 					  from_=0, to=9, tickinterval=0, command=set_zoom)
slider_zoom.set(0)
slider_zoom.place(relx = 0.7, rely=row_pos+.03)
zoom = slider_zoom.get()


# option to draw measuring circle
row_pos = 0.3
showtool = tk.IntVar()
showtool.set(0)
showtoolbox = tk.Checkbutton(menuframe, text="Show Measuring Tool", \
							 font=("Ariel", 14), \
							 variable=showtool, onvalue=1, offvalue=0, \
							 command=plot_disk)
showtoolbox.place(relx = 0.1, rely = row_pos+0)

label_scale = tk.Label(menuframe, text="Image Scale: 1 pixel = 3 milliarcsec", \
					   font=("Ariel", 14))
label_scale.place(relx = 0.2, rely=row_pos+.05)

# size of measuring circle
rad = tk.IntVar()
label_rad = tk.Label(menuframe, text="Radius of Measuring Tool (pixels): ", \
 				font=("Ariel", 14))
label_rad.place(relx = 0.1, rely=row_pos+.1)
slider_rad = tk.Scale(menuframe, variable=rad, \
 					  orient=HORIZONTAL, showvalue=1, \
 					  from_=1, to=500, tickinterval=0, \
					  command=set_rad)
slider_rad.set(100)
slider_rad.place(relx = 0.7, rely=row_pos+.08)
rad = slider_rad.get()


# offset measuring circle
xoff = tk.IntVar()
label_xoff = tk.Label(menuframe, text="X-Offset (pixels): ", \
 				font=("Ariel", 14))
label_xoff.place(relx = 0.1, rely=row_pos+.15)
slider_xoff = tk.Scale(menuframe, variable=xoff, \
 					  orient=HORIZONTAL, showvalue=1, \
 					  from_=-500, to=500, tickinterval=0, \
					  command=set_xoff)
slider_xoff.set(0)
slider_xoff.place(relx = 0.7, rely=row_pos+.13)
xoff = slider_xoff.get()

yoff = tk.IntVar()
label_yoff = tk.Label(menuframe, text="Y-Offset (pixels): ", \
 				font=("Ariel", 14))
label_yoff.place(relx = 0.1, rely=row_pos+.2)
slider_yoff = tk.Scale(menuframe, variable=yoff, \
 					  orient=HORIZONTAL, showvalue=1, \
 					  from_=-500, to=500, tickinterval=0, \
					  command=set_yoff)
slider_yoff.set(0)
slider_yoff.place(relx = 0.7, rely=row_pos+.18)
yoff = slider_yoff.get()


# inclination angle
inc = tk.IntVar()
label_inc = tk.Label(menuframe, text="Inclination of Disk (degrees): ", \
 				font=("Ariel", 14))
label_inc.place(relx = 0.1, rely=row_pos+.25)
slider_inc = tk.Scale(menuframe, variable=inc, \
 					  orient=HORIZONTAL, showvalue=1, \
 					  from_=0, to=90, tickinterval=0, \
					  command=set_inc)
slider_inc.set(0)
slider_inc.place(relx = 0.7, rely=row_pos+.23)
inc = slider_inc.get()


# position angle
pos_angle = tk.IntVar()
label_pos_angle = tk.Label(menuframe, text="Position Angle (degrees): ", \
 				font=("Ariel", 14))
label_pos_angle.place(relx = 0.1, rely=row_pos+.3)
slider_pos_angle = tk.Scale(menuframe, variable=pos_angle, \
 					  orient=HORIZONTAL, showvalue=1, \
 					  from_=0, to=180, tickinterval=0, command=set_pos_angle)
slider_pos_angle.set(0)
slider_pos_angle.place(relx = 0.7, rely=row_pos+.28)
pos_angle = slider_pos_angle.get()





row_pos = 0.8

# place the data acknowledement labels
infolabel = tk.Label(menuframe, text="ALMA images courtesy of the Disk Substructures", \
                     font=("Ariel", 14))
infolabel2 = tk.Label(menuframe, text="at High Angular Resolution Project", \
                     font=("Ariel", 14))
infolabel3 = tk.Label(menuframe, text="(DSHARP; Andrews et al. 2018, ApJ, 869, L41)", \
                     font=("Ariel", 14))
infolabel.place(relx = 0.1, rely=row_pos)
infolabel2.place(relx = 0.1, rely=row_pos+.03)
infolabel3.place(relx = 0.1, rely=row_pos+.06)



plot_disk()



row_pos = 0.9
quit_button = tk.Button(menuframe, text="Quit Simulation")
quit_button.place(relwidth=0.7, relx=0.15, rely=row_pos)
quit_button['command'] = window.destroy


window.mainloop()