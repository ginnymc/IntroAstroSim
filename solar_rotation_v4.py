#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 11:32:01 2022

@author: gmcswain
M. Virginia McSwain
Lehigh University

This tool is based upon the original CLEA exercise "The Period of Rotation of the Sun" (http://public.gettysburg.edu/~marschal/clea/Solarrotlab.html).

Images are pulled automatically from NASA's Solar Dynamics Observatory.  The latitude 
and longitude measurements are approximations that neglect the tilted orbit of the spacecraft
relative to the solar equator.  

2025-12-31:  v4 corrects a bug in the longitude calculation.
"""


import tkinter as tk
import datetime as dt
import numpy as np 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from imageio.v2 import imread



# this class allows Entry boxes to contain default text that disappears when entering new values
class LabeledEntry(tk.Entry):
    def __init__(self, master=None, label=" ", **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        self.label = label
        self.on_exit()
        self.bind('<FocusIn>', self.on_entry)
        self.bind('<FocusOut>', self.on_exit)

    def on_entry(self, event=None):
        if self.get() == self.label:
            self.delete(0, tk.END)

    def on_exit(self, event=None):
        if not self.get():
            self.insert(0, self.label)

            
def generate_url():
    global t, urlstring
    tstring = t.strftime('%Y%m%d')
    yearstring = t.strftime('%Y')
    monthstring = t.strftime('%m')
    daystring = t.strftime('%d')
    urlroot = 'http://jsoc.stanford.edu/data/hmi/images/'
    urlstring = urlroot + yearstring + '/' + monthstring + '/' + \
        daystring + '/' + tstring + '_000000_Ic_1k.jpg'


def setdate():
    global t
    if type(custommonth.get()) != 'MM' or type(customday.get()) != 'DD' or type(customyear.get()) != 'YYYY' :
        newmonth = int(custommonth.get())
        newday = int(customday.get())
        newyear = int(customyear.get())
        try:
            t = dt.datetime(newyear, newmonth, newday, 0, 0, 0, 0)
            datelbl.configure(text=t.strftime("%B %d, %Y"))
            generate_url()
            plot_sun()
            poslabel1.configure(text="Click a sunspot to measure its position!")
            poslabel2.configure(text="")
        except ValueError:
            datelbl.configure(text="Oops, that date isn't available!")

    else:
        datelbl.configure(text="Please enter a new date.")
    

def forwardclick():
    global t
    t += dt.timedelta(hours=24)
    datelbl.configure(text=t.strftime("%B %d, %Y"))
    try:
        generate_url()
        plot_sun()
        poslabel1.configure(text="Click a sunspot to measure its position!")
        poslabel2.configure(text="")
    except:
        datelbl.configure(text="Oops, that date isn't available!")

    
def backclick():
    global t
    t += dt.timedelta(hours=-24)
    datelbl.configure(text=t.strftime("%B %d, %Y"))
    try:
        generate_url()
        plot_sun()
        poslabel1.configure(text="Click a sunspot to measure its position!")
        poslabel2.configure(text="")
    except:
        datelbl.configure(text="Oops, that date isn't available!")


def resetclick():
    global t
    t = dt.date.today()
    datelbl.configure(text=t.strftime("%B %d, %Y"))
    generate_url()
    plot_sun()
    poslabel1.configure(text="Click a sunspot to measure its position!")
    poslabel2.configure(text="")    

    
def sunspot_coords(event):
    global pixrad, xcent, ycent
	
    try:
        x = event.xdata - xcent
        y = event.ydata - ycent
    except:
        x = 999
        y = 999
		
    spotr = np.sqrt(x**2 + y**2)/pixrad
    xsun = x/pixrad
    ysun = y/pixrad

    if spotr < 1:

        # calculate sunspot latitude & longitude here...
        z = np.sqrt(1 - xsun**2 - ysun**2)
        latitude = np.arcsin(ysun) * 180/np.pi
        longitude = np.arctan(xsun/z) * 180/np.pi
    
        # display values on the menuframe...
        latstr = "{:.2f}".format(latitude)
        lonstr = "{:.2f}".format(longitude)
        poslabel1.configure(text="Approx. Latitude (deg) = " + latstr)
        poslabel2.configure(text="Approx. Longitude (deg) = " + lonstr)

    else:
        poslabel1.configure(text="Click a sunspot to measure its position!")
        poslabel2.configure(text="")


def plot_sun():
    global urlstring, pixrad, xcent, ycent

    # this method works, but does not resize image
    #u = urllib.request.urlopen(urlstring)
    #raw_data = u.read()
    #u.close()
    #img = ImageTk.PhotoImage(data=raw_data)
    #label = tk.Label(imageframe, image=img)
    #label.image = img
    #label.pack()

    # this method works better for custom sizing and overplotting    
    im = imread(urlstring)
    f = Figure(figsize=(8,8), dpi=100)
    f.subplots_adjust(left=0.1, bottom=0.1)
    f.text(0.2, 0.07, "Courtesy of NASA/SDO and the AIA, EVE, and HMI science teams.")
    a = f.add_subplot(111)
    a.imshow(im)
    a.axis('off')


    # measure radius of sun image in pixel units (changes over time as satellite moves)
    # this method slices the image at the midpoint to find pixels where image is not black
    Npix = 1024
    xcent = int(Npix/2)
    ycent = int(Npix/2)
    tmp = np.zeros(Npix)
    for i in range(Npix):
        tmp[i] = im[i, int(Npix/2), :][0]
    high = np.where(tmp >= 10, 1, 0)
    pixrad = np.sum(high)/2
    
    # draw green circle at the limb to confirm image radius
    #theta = np.arange(0, 2*np.pi, 2*np.pi/1000)
    #xlimb = pixrad * np.cos(theta) + xcent
    #ylimb = pixrad * np.sin(theta) + ycent
    #a.plot(xlimb, ylimb, 'g-', linewidth=3)
    
    # draw the final image(s)
    plot = FigureCanvasTkAgg(f, master=imageframe)
    plot.draw()
    plot.get_tk_widget().place(relx=0, rely=0)
    
    
    # click on plot to get sunspot coords
    f.canvas.mpl_connect('button_press_event', sunspot_coords)

    
###########################################################


# create the master window
window = tk.Tk()
window.title("Rotation of the Sun")
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

    
# Get current date and image
t = dt.date.today()
try:
    generate_url()
except:
	t += dt.timedelta(hours=-24)
	generate_url()
	
plot_sun()


# place the data acknowledement labels
row_pos = 0.1
infolabel = tk.Label(menuframe, text="Data from NASA's Solar Dynamics Observatory", \
                     font=("Ariel", 16))
infolabel2 = tk.Label(menuframe, text="Helioseismic and Magnetic Imager (HMI)", \
                     font=("Ariel", 16))
infolabel.place(relx = 0.05, rely=row_pos)
infolabel2.place(relx = 0.05, rely=row_pos+.03)


# display sunspot position
row_pos = 0.3
poslabel1 = tk.Label(menuframe, text="Click a sunspot to measure its position!", \
                     font=("Ariel", 16))
poslabel1.place(relx = 0.05, rely = row_pos)
poslabel2 = tk.Label(menuframe, text="", font=("Ariel", 16))
poslabel2.place(relx = 0.05, rely = row_pos+.03)


# Display date and time within the menu frame
row_pos = 0.5
label1 = tk.Label(menuframe, text="Currently showing: ")
label1.place(relx = 0.05, rely=row_pos)
datelbl = tk.Label(menuframe, text=t.strftime("%B %d, %Y"))
datelbl.place(relx=0.4, rely=row_pos)


# buttons to fast-forward or rewind 24 hours
row_pos = 0.55
label3 = tk.Label(menuframe, text="Jump to previous/next day: ")
label3.place(relx=0.05, rely=row_pos)
forwardbtn = tk.Button(menuframe, text=">>", command=forwardclick)
backbtn = tk.Button(menuframe, text="<<", command=backclick)
backbtn.place(relx = 0.55, rely=row_pos)
forwardbtn.place(relx = 0.65, rely=row_pos)


# option to set a custom date
row_pos = 0.6
label4=tk.Label(menuframe, text="Set a custom date: ")
label4.place(relx=0.05, rely=row_pos)
custommonth = LabeledEntry(menuframe, label='MM', width=5)
customday = LabeledEntry(menuframe, label='DD', width=5)
customyear = LabeledEntry(menuframe, label='YYYY', width=7)
setdatebtn = tk.Button(menuframe, text="Change Date", command=setdate)
custommonth.place(relx=0.35, rely=row_pos)
customday.place(relx=0.43, rely=row_pos)
customyear.place(relx=0.51, rely=row_pos)
setdatebtn.place(relx=0.65, rely=row_pos)
label5=tk.Label(menuframe, text="(Most dates between May 1, 2010-present are available.)")
label5.place(relx=0.05, rely=row_pos+.05)


# button to reset to current date
row_pos = 0.7
resetbtn = tk.Button(menuframe, text="Reset to Current Date", command=resetclick)
resetbtn.place(relwidth=0.7, relx=0.15, rely=row_pos)


row_pos = 0.9
quit_button = tk.Button(menuframe, text="Quit Simulation")
quit_button.place(relwidth=0.7, relx=0.15, rely=row_pos)
quit_button['command'] = window.destroy


window.mainloop()