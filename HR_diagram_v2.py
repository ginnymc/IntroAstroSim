#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 12:01:57 2019

@author: gmcswain
M. Virginia McSwain
Lehigh University

This HR Diagram simulation relies upon the data stored in the accompanying 
spreadsheet  file "stardata.xlsx".  Real photometric data for the open clusters 
Pleiades and M34, and 8 simulated datasets can be used as unknowns in a 
classroom lab activity.  The spreadsheet can be modified easily by the user to 
include other datasets or simulations.

Data for the Pleiades are from Simbad. 

Data for M34 are from the NOMAD Catalog (2004AAS...205.4815Z).

Simulated open cluster data rely upon magnitudes generated from the PARSEC 
isochrones with the web interface CMD 3.5 (http://stev.oapd.inaf.it/cgi-bin/cmd). 
Random positions, cluster distance modulus, and photometric noise are added 
within the HR Diagram simulation to ensure a unique dataset.  Reddening is not included.


"""

import tkinter as tk
import pandas as pd
import numpy as np 


def read_stars():
    global clustervar, ds, starid, x, y, Bmag, Vmag, Rmag, framewidth, frameheight

    # read in magnitude data for the cluster.  For simulated clusters, these are absolute mags.
    Bmag = pd.to_numeric(ds[clustervar]['B mag'])
    Vmag = pd.to_numeric(ds[clustervar]['V mag'])
    Rmag = pd.to_numeric(ds[clustervar]['R mag'])    
    N = len(Vmag)
   
    try:   # get star ID numbers, if available
        starid = ds[clustervar]['Star ID']
    except:   # no ID numbers available for simulated clusters
        starid = np.arange(0, N, 1)

    
    try:  # first look for x+y coordinates on pre-determined scale (values between 0-600)
        x = pd.to_numeric(ds[clustervar]['X'])
        y = pd.to_numeric(ds[clustervar]['Y'])
    
    except:  
        try:  # if x+y not available, look for ra+dec coordinates
            ra = pd.to_numeric(ds[clustervar]['RA (J2000)'])
            dec = pd.to_numeric(ds[clustervar]['Dec (J2000)'])
            xscale = (max(ra) - min(ra) ) * 1.1 / framewidth
            yscale = (max(dec) - min(dec) ) *  1.1 / frameheight
            scale = max([xscale, yscale])
            x = framewidth - (ra - min(ra) ) / scale + (framewidth - framewidth/1.1)/2
            y = frameheight - (dec - min(dec)) / scale  + (frameheight - frameheight/1.1)/2
        
        except:  # For simulated clusters, generate random positions
            mu, sigma = 0, frameheight/4
            r = np.random.normal(mu, sigma, N)
            theta = np.random.uniform(0, 2*np.pi, N)
            x = r*np.cos(theta)+ framewidth/2
            y = r*np.sin(theta)+frameheight/2
 
            # also for simulated clusters, add random distance modulus
            distmod = np.random.uniform(0.5, 10, 1)
            Bmag = Bmag + distmod[0]
            Vmag = Vmag + distmod[0]
            Rmag = Rmag + distmod[0]


def draw_stars():
    global starid, x, y, Bmag, Vmag, Rmag, filtervar, fillvar, stars
    sky.bind("<Button-1>", starcoords)

    # see more color options at 
    # http://cs111.wellesley.edu/~cs111/archive/cs111_spring15/public_html/labs/lab12/tkintercolor.html
    if filtervar == '(none)': 
        fillvar = 'white'
        mag = Vmag
    if filtervar == 'B': 
        fillvar = 'dodger blue'
        mag = Bmag
    if filtervar == 'V': 
        fillvar = 'green yellow'
        mag = Vmag
    if filtervar == 'R': 
        fillvar = 'red'
        mag = Rmag

    # create star's graphics in simulation
    # size is assigned based on dynamic range of magnitudes
    # random noise included with logarithmic dependence on magnitude
    stars = []
    stepsize = (max(mag)-min(mag))/6
    for i in range(len(starid)):
        noise = np.random.uniform(-np.log(1 + (mag[i]-min(mag))*.03), np.log(1 + (mag[i]-min(mag))*.03), 1)
        mag[i] = mag[i]+noise[0]
        radius=2  
        if mag[i] <= min(mag)+stepsize*5: radius=3
        if mag[i] <= min(mag)+stepsize*4: radius=4
        if mag[i] <= min(mag)+stepsize*3: radius=5
        if mag[i] <= min(mag)+stepsize*2: radius=6
        if mag[i] <= min(mag)+stepsize: radius=7
       
        tmp = sky.create_oval(x[i]-radius, y[i]-radius, x[i]+radius, y[i]+radius, \
            fill=fillvar, \
            tags = (str(starid[i]),  f"{mag[i]:.2f}") )
        stars.append(tmp)
        

def delete_stars():
    global starid, x, y, Bmag, Vmag, Rmag, filtervar, stars
    for i in range(len(starid)): sky.delete(stars[i])


# get star coords and magnitudes when clicked
# still bugs when 2 objects overlap  :(
def starcoords(event):
    cursorx = event.x
    cursory = event.y
    #item = sky.find_overlapping(cursorx-3, cursory-3, cursorx+3, cursory+3)
    item = sky.find_closest(cursorx, cursory, halo=2)
    if sky.gettags(item) != ():
        starlabel.configure(text="Star ID: "+sky.gettags(item)[0], \
                            font=("Ariel", 16))
        maglabel.configure(text="Apparent magnitude in filter " + filtervar + " = " + \
                           sky.gettags(item)[1], \
                           font=("Ariel", 16))
    else:
        starlabel.configure(text="No star at this location.", \
                            font=("Ariel", 16))
        maglabel.configure(text=" ")
    

def set_filter():
    global filtervar
    filtervar = str(fvar.get())
    delete_stars()
    draw_stars()
    starlabel.configure(text="Click a star to measure its apparent magnitude!", \
                            font=("Ariel", 16))
    maglabel.configure(text=" ")
 
    
def set_cluster():
    global clustervar
    clustervar = str(clvar.get())
    #print ('Changing to cluster '+clustervar)
    delete_stars()
    read_stars()
    draw_stars()
    starlabel.configure(text="Click a star to measure its apparent magnitude!", \
                            font=("Ariel", 16))
    maglabel.configure(text=" ")


################################################


# create the master window
window = tk.Tk()
window.title("Hertzsprung-Russell Diagram of a Star Cluster")
framewidth = 600
frameheight = 600
window.geometry(str(framewidth*2)+'x'+str(frameheight))


# create control panel frame
controlframe = tk.Frame(window, width=framewidth, height=frameheight)
controlframe.grid_propagate(0)
controlframe.place(x=framewidth, y=0)


# read in star data; get list of available clusters from the data file
dir = '/Users/gmcswain/Documents/Lehigh/Teaching/ASTR008/GUIs/HR_Diagram/'
ds = pd.read_excel(dir+'stardata.xlsx', sheet_name=None)
clusterlist = []
for sheet_name in ds.keys():
    clusterlist.append(sheet_name)


# initialize the default star cluster in control panel
row_pos = 0.2
clvar = tk.StringVar(controlframe)
clvar.set(clusterlist[0])
cluster = 'Pleiades'   # default
clusterlbl = tk.Label(controlframe, text="Select a star cluster: ")
clusterlbl.place(relx=0.1, rely=row_pos)
clustermenu = tk.OptionMenu(controlframe, clvar, *clusterlist)
clustermenu.place(relx=0.35, rely=row_pos)
setclusterbtn = tk.Button(controlframe, text="Change Cluster", command=set_cluster)
setclusterbtn.place(relx=0.7, rely=row_pos)


# display default cluster data - necessary before set_cluster() is run
starid = ds[cluster]['Star ID']
try: 
    x = pd.to_numeric(ds[cluster]['X'])
    y = pd.to_numeric(ds[cluster]['Y'])
except:
    ra = pd.to_numeric(ds[cluster]['RA (J2000)'])
    dec = pd.to_numeric(ds[cluster]['Dec (J2000)'])
    xscale = (max(ra) - min(ra) ) * 1.1 / framewidth
    yscale = (max(dec) - min(dec) ) *  1.1 / frameheight
    scale = max([xscale, yscale])
    x = framewidth - (ra - min(ra) ) / scale + (framewidth - framewidth/1.1)/2
    y = frameheight - (dec - min(dec)) / scale  + (frameheight - frameheight/1.1)/2
Bmag = pd.to_numeric(ds[cluster]['B mag'])
Vmag = pd.to_numeric(ds[cluster]['V mag'])
Rmag = pd.to_numeric(ds[cluster]['R mag'])


# option to change filter in control panel
row_pos = 0.4
filterlist = ['B', 'V', 'R', '(none)']
fvar = tk.StringVar(controlframe)
fvar.set(filterlist[3])
filtervar = '(none)'
filterlbl = tk.Label(controlframe, text="Select a filter: ")
filterlbl.place(relx=0.1, rely=row_pos)
filtermenu = tk.OptionMenu(controlframe, fvar, *filterlist)
filtermenu.place(relx=0.35, rely=row_pos)
setfilterbtn = tk.Button(controlframe, text="Change Filter", command=set_filter)
setfilterbtn.place(relx=0.7, rely=row_pos)


# space to display current star or instructions
row_pos = 0.6
starlabel = tk.Label(controlframe, text="Click a star to measure its apparent magnitude!", \
                     font=("Ariel", 16))
starlabel.place(relx = 0.1, rely = row_pos)


# display magnitude in control panel
row_pos = 0.7
maglabel = tk.Label(controlframe, text="")
maglabel.place(relx = 0.1, rely = row_pos)


# Quit button in control panel
row_pos = 0.9
quit_button = tk.Button(controlframe, text="Quit Simulation")
quit_button.place(relwidth=0.7, relx=0.15, rely=row_pos)
quit_button['command'] = window.destroy


##################################3


# create sky frame
skyframe = tk.Frame(window, width=framewidth, height=frameheight)
skyframe.grid_propagate(0)
skyframe.place(x=0, y=0)


# draw sky and stars
sky = tk.Canvas(skyframe, width=framewidth, height=frameheight)
sky.config(bg="black")
sky.place(relx=0, rely=0)
sky.bind("<Button-1>", starcoords)
draw_stars()


window.mainloop()
