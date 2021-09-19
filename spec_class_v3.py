#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 13:14:56 2020

@author: gmcswain
M. Virginia McSwain
Lehigh University

All spectra are from the Indo-U.S. Library of Coude Feed Stellar Spectra 
(Valdes et al. 2004, ApJS, vol. 152, issue 2, pp. 251-259); 
https://ui.adsabs.harvard.edu/abs/2004ApJS..152..251V/abstract)

This version of the simulation accesses the spectral library directly from the 
noao.edu website.  Note that the URL may need updating in the near future to 
reflect the name change from NOAO to NSF's NOIR Lab.

Consider adding more stars of different spectral types.  Full list is available here:
https://iopscience.iop.org/article/10.1086/386343/fulltext/59155.html?doi=10.1086/386343

Cross references for stellar names:
https://iopscience.iop.org/article/10.1086/386343/fulltext/59155.tables.html?doi=10.1086/386343

"""

import tkinter as tk
import pandas as pd
import numpy as np 
import urllib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from astropy.io import fits
from scipy import stats




###########################################################

def set_star():
    global star
    star = starvar.get()
    plot_spectra()
    
def set_sptype():
    global sptype
    sptype = sptypevar.get()
    plot_spectra()
    
def plot_spectra():
    global star, sptype, HIvar, HeIvar
    f1 = urllib.request.urlopen(url+stdlist[sptype]+'.txt')
    f2 = urllib.request.urlopen(url+starlist[star]+'.txt')

    # read file 1
    for i in range(32):
        header = f1.readline()
    w1 = []
    s1 = []
    for line in f1:
        line = line.strip()
        columns = line.split()
        w1.append(float(columns[0]))
        s1.append(float(columns[1]))
        
    # read file 2
    for i in range(32):
        header = f2.readline()
    w2 = []
    s2 = []
    for line in f2:
        line = line.strip()
        columns = line.split()
        w2.append(float(columns[0]))
        s2.append(float(columns[1]))
    
    # bin spectra to lower resolution
    w_binned = np.arange(3900, 7100, 4)
    s1_binned, w_binned, bin_number = stats.binned_statistic(w1, s1, statistic='mean', bins=w_binned)
    s2_binned, w_binned, bin_number = stats.binned_statistic(w2, s2, statistic='mean', bins=w_binned)
    
    # plot star, spectral standard, and difference spectra
    f = Figure(figsize=(5,4.5), dpi=100)
    f.subplots_adjust(left=0.1, bottom=0.1)
    a = f.add_subplot(111)
    if showunk.get() == 1:
        a.plot(w_binned[:-1]/10, s2_binned, 'b-', label=star)
    if showstd.get() == 1:
        a.plot(w_binned[:-1]/10, s1_binned, 'r-', label=sptype)
    if showdiff.get() == 1:
        a.plot(w_binned[:-1]/10, s1_binned-s2_binned, 'g-', label='Difference')
    a.legend(loc='upper right')
    a.set_xlabel('Wavelength (nm)')
    a.set_ylabel('Relative Intensity')
    a.set_xlim([390, 710])
    a.set_ylim([-0.5, 4])
    
    # mark spectral lines
    if HIvar.get() == 1: 
        a.plot([397.0, 397.0], [-10,10], 'c:')
        a.plot([410.2, 410.2], [-10,10], 'c:')
        a.plot([434.0, 434.0], [-10,10], 'c:')
        a.plot([486.1, 486.1], [-10,10], 'c:')
        a.plot([656.3, 656.3], [-10,10], 'c:')
        a.text(660, -0.3, 'H I', fontsize=12, color='c')
        
    if HeIvar.get() == 1:
        a.plot([400.9, 400.9], [-10,10], 'm:')
        a.plot([402.6, 402.6], [-10,10], 'm:')
        a.plot([414.4, 414.4], [-10,10], 'm:')
        a.plot([438.7, 438/7], [-10,10], 'm:')
        a.plot([447.1, 447.1], [-10,10], 'm:')
        a.plot([471.3, 471.3], [-10,10], 'm:')
        a.plot([492.1, 492.1], [-10,10], 'm:')
        a.plot([501.6, 501.6], [-10,10], 'm:')
        a.plot([504.7, 504.7], [-10,10], 'm:')
        a.plot([587.6, 587.6], [-10,10], 'm:')
        a.plot([706.5, 706.5], [-10,10], 'm:')
        a.text(590, -0.3, 'He I', fontsize=12, color='m')
        
    if CaIIvar.get() == 1:
        a.plot([396.9, 396.9], [-10,10], ':', color='limegreen')
        a.plot([393.4, 393.4], [-10,10], ':', color='limegreen')
        a.text(400, -0.3, 'Ca II', fontsize=12, color='limegreen')
    
    if NaIvar.get() == 1:
        a.plot([589.0, 589.0], [-10,10], ':', color='teal')
        a.text(595, -0.3, 'Na I', fontsize=12, color='teal')
    
    if FeIvar.get() == 1:  # not an exhaustive list of Fe lines in the optical range!
        a.plot([400.524, 400.524], [-10,10], ':', color='orange')
        a.plot([404.581, 404.581], [-10,10], ':', color='orange')
        a.plot([406.359, 406.359], [-10,10], ':', color='orange')
        a.plot([407.173, 407.173], [-10,10], ':', color='orange')
        a.plot([413.205, 413.205], [-10,10], ':', color='orange')
        a.plot([414.386, 414.386], [-10,10], ':', color='orange')
        a.plot([419.909, 419.909], [-10,10], ':', color='orange')
        a.plot([420.202, 420.202], [-10,10], ':', color='orange')
        a.plot([425.078, 425.078], [-10,10], ':', color='orange')
        a.plot([426.047, 426.047], [-10,10], ':', color='orange')
        a.plot([427.176, 427.176], [-10,10], ':', color='orange')
        a.plot([430.790, 430.790], [-10,10], ':', color='orange')
        a.plot([432.576, 432.576], [-10,10], ':', color='orange')
        a.plot([437.592, 437.592], [-10,10], ':', color='orange')
        a.plot([440.475, 440.475], [-10,10], ':', color='orange')
        a.plot([441.512, 441.512], [-10,10], ':', color='orange')
        a.plot([442.730, 442.730], [-10,10], ':', color='orange')
        a.plot([487.131, 487.131], [-10,10], ':', color='orange')
        a.plot([489.149, 489.149], [-10,10], ':', color='orange')
        a.plot([492.050, 492.050], [-10,10], ':', color='orange')
        a.plot([495.759, 495.759], [-10,10], ':', color='orange')
        a.plot([516.748, 516.748], [-10,10], ':', color='orange')
        a.plot([517.159, 517.159], [-10,10], ':', color='orange')
        a.plot([522.718, 522.718], [-10,10], ':', color='orange')
        a.plot([523.294, 523.294], [-10,10], ':', color='orange')
        a.plot([526.953, 526.953], [-10,10], ':', color='orange')
        a.plot([527.035, 527.035], [-10,10], ':', color='orange')
        a.plot([532.803, 532.803], [-10,10], ':', color='orange')
        a.plot([537.148, 537.148], [-10,10], ':', color='orange')
        a.plot([539.712, 539.712], [-10,10], ':', color='orange')
        a.plot([540.577, 540.577], [-10,10], ':', color='orange')
        a.plot([544.691, 544.691], [-10,10], ':', color='orange')
        a.plot([606.548, 606.548], [-10,10], ':', color='orange')
        a.plot([613.769, 613.769], [-10,10], ':', color='orange')
        a.plot([619.155, 619.155], [-10,10], ':', color='orange')
        a.plot([623.072, 623.072], [-10,10], ':', color='orange')
        a.plot([625.255, 625.255], [-10,10], ':', color='orange')
        a.plot([630.150, 630.150], [-10,10], ':', color='orange')
        a.plot([631.801, 631.801], [-10,10], ':', color='orange')
        a.plot([633.682, 633.682], [-10,10], ':', color='orange')
        a.plot([639.360, 639.360], [-10,10], ':', color='orange')
        a.plot([640.000, 640.000], [-10,10], ':', color='orange')
        a.plot([641.164, 641.164], [-10,10], ':', color='orange')
        a.plot([642.135, 642.135], [-10,10], ':', color='orange')
        a.plot([643.084, 643.084], [-10,10], ':', color='orange')
        a.plot([649.498, 649.498], [-10,10], ':', color='orange')
        a.plot([654.623, 654.623], [-10,10], ':', color='orange')
        a.plot([659.291, 659.291], [-10,10], ':', color='orange')
        a.plot([667.798, 667.798], [-10,10], ':', color='orange')
        a.text(670, -0.3, 'Fe I', fontsize=12, color='orange')
 
    #f.tight_layout()
    plot = FigureCanvasTkAgg(f, master=graphframe)  # A tk.DrawingArea.
    plot.draw()
    plot.get_tk_widget().place(relx=0.2, rely=0)



###########################################################

# create the master window
window = tk.Tk()
window.title("Classification of Stellar Spectra")
framewidth = 900
frameheight = 500
window.geometry(str(framewidth)+'x'+str(frameheight))

# frame to display menu options
menuframe = tk.Frame(window, width=framewidth/3, height=frameheight)
menuframe.grid_propagate(0)
menuframe.place(x=0, y=0)


# frame to display graphs
graphframe = tk.Frame(window, width=framewidth*2/3, height=frameheight)
graphframe.grid_propagate(0)
graphframe.place(x=framewidth/3, y=0)


# List of unknown stars and their filenames
url = "https://www.noao.edu/cflib/V1/TEXT/"
starfilelist = ['11636', '15335', '16673', '16895', '28099', '40136', \
                '58946', '65900', '70110', '78558', '87822', '91752', \
                '111721', '116656', '130109', '136729', '149630', \
                '151431', '153653', '154445', '158352', '173087', \
                '173936', '177817', '186307', '189944', '190993', \
                '193322', '207516', '212978']
starnamelist = []
for star in starfilelist:
    starnamelist.append('HD ' + star)
starlist = dict(zip(starnamelist, starfilelist))


# Display menu of unknown stars
row_pos = 0.1
starvar = tk.StringVar(menuframe)
starvar.set(starnamelist[0])   # default
star = starnamelist[0]   # default
starlbl = tk.Label(menuframe, text="Select a star to classify: ")
starlbl.place(relx=0.1, rely=row_pos)
starmenu = tk.OptionMenu(menuframe, starvar, *starnamelist)
starmenu.place(relx=0.2, rely=row_pos+0.05)
setstarbtn = tk.Button(menuframe, text="Submit", command=set_star)
setstarbtn.place(relx=0.6, rely=row_pos+0.05)

showunk = tk.IntVar()
showunk.set(1)
showunkbox = tk.Checkbutton(menuframe, text="Show unknown star", variable=showunk, onvalue=1, offvalue=0, command=plot_spectra)
showunkbox.place(relx = 0.2, rely = row_pos+0.1)


# List of spectral standards filenames and their spec types
sptypelist = ['O9', 'B2', 'B5', 'B8', 'A0', 'A3', \
            'A6', 'A8', 'F2', 'F5', 'F8', 'G1', \
            'G4', 'G8']
stdfilelist = ['149757', '193536', '158148', '172958', '103287', '106591', \
            '186307', '155514', '33256', '11592', '11007', '89707', \
            '32923', '10700']
stdlist = dict(zip(sptypelist, stdfilelist))


# Display menu of known spectral types
row_pos = 0.3
sptypevar = tk.StringVar(menuframe)
sptypevar.set(sptypelist[0])
sptype = 'O9'
sptypelbl = tk.Label(menuframe, text="Select a spectral type to compare: ")
sptypelbl.place(relx=0.1, rely=row_pos)
sptypemenu = tk.OptionMenu(menuframe, sptypevar, *sptypelist)
sptypemenu.place(relx=0.2, rely=row_pos+0.05)
setsptypebtn = tk.Button(menuframe, text="Submit", command=set_sptype)
setsptypebtn.place(relx=0.6, rely=row_pos+0.05)

showstd = tk.IntVar()
showstd.set(0)
showstdbox = tk.Checkbutton(menuframe, text="Show spectral standard", variable=showstd, onvalue=1, offvalue=0, command=plot_spectra)
showstdbox.place(relx = 0.2, rely = row_pos+0.1)
showdiff = tk.IntVar()
showdiff.set(0)
showdiffbox = tk.Checkbutton(menuframe, text="Show difference spectrum", variable=showdiff, onvalue=1, offvalue=0, command=plot_spectra)
showdiffbox.place(relx = 0.2, rely = row_pos+0.15)


# Checkboxes for different atomic species
row_pos = 0.6
atomlbl = tk.Label(menuframe, text="Mark positions of atomic spectral lines: ")
atomlbl.place(relx=0.1, rely=row_pos)
HIvar = tk.IntVar()
HIvar.set(0)
HI = tk.Checkbutton(menuframe, text="H I", variable=HIvar, onvalue=1, offvalue=0, command=plot_spectra)
HI.place(relx = 0.2, rely = row_pos+0.05)
HeIvar = tk.IntVar()
HeIvar.set(0)
HeI = tk.Checkbutton(menuframe, text="He I", variable=HeIvar, onvalue=1, offvalue=0, command=plot_spectra)
HeI.place(relx = 0.2, rely = row_pos+0.1)
CaIIvar = tk.IntVar()
CaIIvar.set(0)
CaII = tk.Checkbutton(menuframe, text="Ca II", variable=CaIIvar, onvalue=1, offvalue=0, command=plot_spectra)
CaII.place(relx = 0.2, rely = row_pos+0.15)
NaIvar = tk.IntVar()
NaIvar.set(0)
NaI = tk.Checkbutton(menuframe, text="Na I", variable=NaIvar, onvalue=1, offvalue=0, command=plot_spectra)
NaI.place(relx = 0.6, rely = row_pos+0.05)
FeIvar = tk.IntVar()
FeIvar.set(0)
FeI = tk.Checkbutton(menuframe, text="Fe I", variable=FeIvar, onvalue=1, offvalue=0, command=plot_spectra)
FeI.place(relx = 0.6, rely = row_pos+0.1)


row_pos = 0.9
quit_button = tk.Button(menuframe, text="Quit Simulation")
quit_button.place(relwidth=0.7, relx=0.15, rely=row_pos)
#quit_button['command'] = window.destroy
quit_button['command'] = window.quit

plot_spectra()


window.mainloop()
