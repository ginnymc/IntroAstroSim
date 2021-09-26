#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 15:03:34 2019

@author: gmcswain
M. Virginia McSwain
Lehigh University

This simulation of the moons of Jupiter is based on the original CLEA exercise,
"The Revolution of the Moons of Jupiter"  
(http://www3.gettysburg.edu/~marschal/clea/juplab.html).

This simulation relies upon the Skyfield package written by Brandon Rhodes 
(https://rhodesmill.org/skyfield/, 2019ascl.soft07024R).

It requires NASA's ephemeris file 'jup365.bsp', last updated 2021-03-14 08:29.	
This code is set up to rely upon a local installation of this file to the 
directory of your choice.  The file can be downloaded from 
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/.

For instructions on using the ephemeris file, see 
https://rhodesmill.org/skyfield/planets.html .


"""

import tkinter as tk
import datetime as dt
from astropy.time import Time, TimezoneInfo
import astropy.units as u
from skyfield.api import load, load_file




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

def select_interval():
    global deltat
    deltat = interval.get()
    
def forwardclick():
    global t, deltat, ttemp, tzone, utc_offset
    ttemp+=dt.timedelta(hours=deltat)
    t = Time(ttemp)
    datelbl.configure(text=t.to_datetime(timezone=utc_offset).strftime("%B %d, %Y at %H:%M "+ tzone))
    jdlbl.configure(text="JD "+str('% 11.3f' % t.jd))
    deletemoons()
    updatemoons()
    moonlabel.configure(text="Click a moon to measure its position!")
    poslabel.configure(text="")

    
def backclick():
    global t, deltat, ttemp, tzone, utc_offset
    ttemp += dt.timedelta(hours=-deltat)
    t = Time(ttemp)
    datelbl.configure(text=t.to_datetime(timezone=utc_offset).strftime("%B %d, %Y at %H:%M "+ tzone))
    jdlbl.configure(text="JD "+str('% 11.3f' % t.jd))
    deletemoons()
    updatemoons()
    moonlabel.configure(text="Click a moon to measure its position!")
    poslabel.configure(text="")

def resetclick():
    global t, ttemp, tzone, utc_offset
    ttemp = dt.datetime.now(tz=utc_offset)
    t = Time(ttemp)
    datelbl.configure(text=t.to_datetime(timezone=utc_offset).strftime("%B %d, %Y at %H:%M "+ tzone))
    jdlbl.configure(text="JD "+str('% 11.3f' % t.jd))
    deletemoons()
    updatemoons()
    moonlabel.configure(text="Click a moon to measure its position!")
    poslabel.configure(text="")    
    
def setdate():
    global t, ttemp, tzone, utc_offset
    if type(custommonth.get()) != 'MM' or type(customday.get()) != 'DD' or type(customyear.get()) != 'YYYY' :
        newmonth = int(custommonth.get())
        newday = int(customday.get())
        newyear = int(customyear.get())
        try:
            ttemp = dt.datetime(newyear, newmonth, newday, 0, 0, 0, 0, tzinfo=utc_offset)
            t = Time(ttemp)
            datelbl.configure(text=t.to_datetime(timezone=utc_offset).strftime("%B %d, %Y at %H:%M "+ tzone))
            jdlbl.configure(text="JD "+str('% 11.3f' % t.jd))
            deletemoons()
            updatemoons()
            moonlabel.configure(text="Click a moon to measure its position!")
            poslabel.configure(text="")
        except ValueError:
            datelbl.configure(text='Please select a valid date')
            jdlbl.configure(text=' ')
    else:
        datelbl.configure(text='Please select a valid date')
        jdlbl.configure(text=' ')

        
def settzone():
    global t, ttemp, tzone, utc_offset
    tzone = str(tvar.get())
    if tzone == 'EST':
        utc_offset = TimezoneInfo(utc_offset=-5*u.hour)  # EST
    if tzone == 'EDT':
        utc_offset = TimezoneInfo(utc_offset=-4*u.hour)  # EDT
    if tzone == 'UTC':
        utc_offset = TimezoneInfo(utc_offset=-0*u.hour)  # UTC

    datelbl.configure(text=t.to_datetime(timezone=utc_offset).strftime("%B %d, %Y at %H:%M "+ tzone))
    jdlbl.configure(text="JD "+str('% 11.3f' % t.jd))
    deletemoons()
    updatemoons()
    moonlabel.configure(text="Click a moon to measure its position!")
    poslabel.configure(text="")
    

def updatecolors():
    global io_ball, eu_ball, ga_ball, ca_ball, colored
    if colored.get() == False:
        io_fill = eu_fill = ga_fill = ca_fill = "white"
    elif colored.get() == True:
        io_fill = "#FBF608"  # Gold
        eu_fill = "#FF5412"  # Red-orange
        ga_fill = "#FF66E9"  # Hot pink
        ca_fill = "#01DEE6"  # Teal
    sky.itemconfig(io_ball, fill=io_fill)
    sky.itemconfig(eu_ball, fill=eu_fill)
    sky.itemconfig(ga_ball, fill=ga_fill)
    sky.itemconfig(ca_ball, fill=ca_fill)

def updatemoons():
    global ttemp, io_ball, eu_ball, ga_ball, ca_ball, framewidth, frameheight
    sky.bind("<Button-1>", mooncoords)
    tmoon = ts.utc(ttemp)
    jupdiam = 139822.
    ju_x, ju_z = [framewidth/2, frameheight/8]
    #io_x, io_y, io_z = jupiter.at(tmoon).observe(io).position.km / jupdiam
    io_x, io_y, io_z = jupiter.at(tmoon).observe(io).ecliptic_position().km / jupdiam
    eu_x, eu_y, eu_z = jupiter.at(tmoon).observe(europa).ecliptic_position().km / jupdiam
    ga_x, ga_y, ga_z = jupiter.at(tmoon).observe(ganymede).ecliptic_position().km / jupdiam
    ca_x, ca_y, ca_z = jupiter.at(tmoon).observe(callisto).ecliptic_position().km / jupdiam
    moonrad = 3
    juprad = 13
    xscale = juprad*2
    zscale = xscale
    io_ball = sky.create_oval(ju_x + io_x*xscale - moonrad, ju_z + io_z*zscale - moonrad, \
                              ju_x + io_x*xscale + moonrad, ju_z + io_z*zscale + moonrad, \
                              fill="white", tags=("Io", str('% 5.2f' % io_x) ) )
    eu_ball = sky.create_oval(ju_x + eu_x*xscale - moonrad, ju_z + eu_z*zscale - moonrad, \
                              ju_x + eu_x*xscale + moonrad, ju_z + eu_z*zscale + moonrad, \
                              fill="white", tags=("Europa", str('% 5.2f' % eu_x) ) )
    ga_ball = sky.create_oval(ju_x + ga_x*xscale - moonrad, ju_z + ga_z*zscale - moonrad, \
                              ju_x + ga_x*xscale + moonrad, ju_z + ga_z*zscale + moonrad, \
                              fill="white", tags=("Ganymede", str('% 4.2f' % ga_x) ) )
    ca_ball = sky.create_oval(ju_x + ca_x*xscale - moonrad, ju_z + ca_z*zscale - moonrad, \
                              ju_x + ca_x*xscale + moonrad, ju_z + ca_z*zscale + moonrad, \
                              fill="white", tags=("Callisto", str('% 4.2f' % ca_x) ))
    ju_ball = sky.create_oval(ju_x - juprad, ju_z -juprad, ju_x + juprad, ju_z + juprad, \
                              fill="gray", tags=("Jupiter", "0" ) )
    updatecolors()
    if io_y < 0: sky.tag_raise(io_ball)
    if eu_y < 0: sky.tag_raise(eu_ball)
    if ga_y < 0: sky.tag_raise(ga_ball)
    if ca_y < 0: sky.tag_raise(ca_ball)



def deletemoons():
    global io_ball, eu_ball, ga_ball, ca_ball
    sky.delete(io_ball)
    sky.delete(eu_ball)
    sky.delete(ga_ball)
    sky.delete(ca_ball)

    
def mooncoords(event):
    #print ("clicked at", event.x, event.y)
    x = event.x
    y = event.y
    #item= sky.find_overlapping(x-1, y-1, x+1, y+1)
    item = sky.find_closest(x, y, halo=2)
    if sky.gettags(item) != ():
        #print (sky.gettags(item)[0])
        moonlabel.configure(text=sky.gettags(item)[0], font=("Ariel", 16))
        poslabel.configure(text="x = "+ sky.gettags(item)[1] + " Jup. diameters", \
                           font=("Ariel", 16))
    else:
        moonlabel.configure(text="No moon at this location.", \
                            font=("Ariel", 16))
        poslabel.configure(text="")
    

# create the master window
window = tk.Tk()
window.title("Moons of Jupiter Simulation")
framewidth = 800
frameheight = 600
colored = tk.BooleanVar(False)
window.geometry(str(framewidth)+'x'+str(frameheight))

# create moon animation frame
moonframe = tk.Frame(window, width=framewidth, height=frameheight/4)
moonframe.grid_propagate(0)
moonframe.place(x=0, y=0)


# create time control frame
timeframe = tk.Frame(window, width=framewidth, height=frameheight*3/4)
timeframe.grid_propagate(0)
timeframe.place(x=0, y=frameheight/4)



# Get current time.  Default timezone set to EST.
tzonelist = ['UTC', 'EST', 'EDT', 'Others coming soon']
tvar = tk.StringVar(timeframe)
tvar.set(tzonelist[0])
tzone = 'EST'
utc_offset = TimezoneInfo(utc_offset=-5*u.hour)  # EST by default
ttemp = dt.datetime.now(tz=utc_offset)
t = Time(ttemp)


# plot the moons
directory = './'
moons = load_file(directory+'jup365.bsp')
io = moons['IO']
europa = moons['EUROPA']
ganymede = moons['GANYMEDE']
callisto = moons['CALLISTO']
jupiter = moons['JUPITER BARYCENTER']
#ts = load.timescale()
ts = load.timescale(builtin=True)
sky = tk.Canvas(moonframe, width=framewidth, height=frameheight/4)
sky.config(bg="black")
sky.place(relx=0, rely=0)
sky.bind("<Button-1>", mooncoords)
updatemoons()


# display current moon and its position
row_pos = 0.1
poslabel = tk.Label(timeframe, text="")
poslabel.place(relx = 0.5, rely = row_pos)
moonlabel = tk.Label(timeframe, text="Click a moon to measure its position!", \
                     font=("Ariel", 16))
moonlabel.place(relx = 0.1, rely = row_pos)


# Display date and time within the time window
row_pos = 0.2
label1 = tk.Label(timeframe, text="Currently showing: ")
label1.place(relx = 0.1, rely=row_pos)
datelbl = tk.Label(timeframe, text=t.to_datetime(timezone=utc_offset).strftime("%B %d, %Y at %H:%M "+ tzone))
datelbl.place(relx=0.5, rely=row_pos)
jdlbl = tk.Label(timeframe, text="JD "+str('% 11.3f' % t.jd))
jdlbl.place(relx=0.5, rely=row_pos+0.08)

# option to change time zone
row_pos = 0.4
label5 = tk.Label(timeframe, text="Change the time zone: ")
label5.place(relx=0.1, rely=row_pos)
timezonemenu = tk.OptionMenu(timeframe, tvar, *tzonelist)
timezonemenu.place(relx=0.5, rely=row_pos)
settzonebtn = tk.Button(timeframe, text="Change Time Zone", command=settzone)
settzonebtn.place(relx=0.7, rely=row_pos)

# option to set a custom date
row_pos = 0.5
label4=tk.Label(timeframe, text="Set a custom date: ")
label4.place(relx=0.1, rely=row_pos)
custommonth = LabeledEntry(timeframe, label='MM', width=4)
customday = LabeledEntry(timeframe, label='DD', width=4)
customyear = LabeledEntry(timeframe, label='YYYY', width=5)
setdatebtn = tk.Button(timeframe, text="Change Date", command=setdate)
custommonth.place(relx=0.5, rely=row_pos)
customday.place(relx=0.57, rely=row_pos)
customyear.place(relx=0.64, rely=row_pos)
setdatebtn.place(relx=0.75, rely=row_pos)


# select observation interval
row_pos= 0.6
interval = tk.IntVar()
R1 = tk.Radiobutton(timeframe, text='2 hours', variable=interval, value=2, \
                    command=select_interval)
R2 = tk.Radiobutton(timeframe, text='12 hours', variable=interval, value=12, \
                    command=select_interval)
label2 = tk.Label(timeframe, text="Select observation interval: ")
label2.place(relx = 0.1, rely=row_pos)
R1.place(relx = 0.5, rely=row_pos)
R2.place(relx = 0.7, rely=row_pos)


# buttons to fast-forward or rewind 2 hours
row_pos = 0.7
label3 = tk.Label(timeframe, text="Jump to previous/next observation: ")
label3.place(relx=0.1, rely=row_pos)
forwardbtn = tk.Button(timeframe, text=">>", command=forwardclick)
backbtn = tk.Button(timeframe, text="<<", command=backclick)
backbtn.place(relx = 0.6, rely=row_pos)
forwardbtn.place(relx = 0.7, rely=row_pos)


# button to reset to current time
row_pos = 0.8
resetbtn = tk.Button(timeframe, text="Reset to Current Local Time", command=resetclick)
resetbtn.place(relwidth=0.7, relx=0.15, rely=row_pos)


row_pos = 0.9
quit_button = tk.Button(timeframe, text="Quit Simulation")
quit_button.place(relwidth=0.7, relx=0.15, rely=row_pos)
quit_button['command'] = window.destroy

# menubar with extra features
menubar = tk.Menu(window)
featuremenu = tk.Menu(menubar, tearoff=0)
featuremenu.add_checkbutton(label="ID by color", variable=colored, onvalue=True, offvalue=False, command=updatecolors)
menubar.add_cascade(label="Features", menu=featuremenu)

window.config(menu=menubar)
window.mainloop()



