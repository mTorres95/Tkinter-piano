# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

import sys
import math
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 
from math import pi,sin,cos

class View :
    def __init__(self,parent,bg="white",width=800,height=500):
        self.canvas=tk.Canvas(parent,bg=bg,width=width,height=height)
        self.signal=[]
        self.width,self.height=width,height
        self.units=1
        self.canvas.bind("<Configure>",self.resize)
    def generate_signal(self,period=2,samples=100.0):
        del self.signal[0:]
        self.center = self.height/2
        self.canvas.create_line(0, self.center, self.width, self.center, fill='black')
        x_increment = 1   # increment
        
        # width stretch
        x_factor = self.f
        # height stretch
        y_amplitude = self.a

        # for i in range(self.h) :
        #     print(i)
        for x in range(self.width):
            #self.signal.append([t*Tech,self.vibration(t*Tech)])
            self.signal.append([x*x_increment , int(y_amplitude * math.sin(x * x_factor + self.p)) + int(y_amplitude * math.sin(x * x_factor * self.h + self.p)) + self.center])
        return self.signal
    def update(self,amplitude,frequency,phase,harmonic):
        print("View : update()")
        self.a=amplitude*127.5
        self.f=frequency/5000
        self.p=phase*math.pi/180
        self.h=harmonic+1
        print("Amp=",self.a,"\nFreq=",self.f,"\Phase=",self.p,"\Harmonic=",self.h)
        self.canvas.delete("all")
        self.grid()
        #self.canvas.create_line(0, self.center, self.width, self.center, fill='black')
        self.generate_signal()
        if self.signal :
            self.canvas.create_line(self.signal, fill='red')
    def grid(self,steps=6):
        self.units=steps
        tile_x=self.width/steps
        for t in range(1,steps+1):
            x =t*tile_x
            self.canvas.create_line(x,0,x,self.height,tags="grid")
            self.canvas.create_line(x,self.height/2-10,x,self.height/2+10,width=3,tags="grid")
        tile_y=self.height/steps
        for t in range(1,steps+1):
            y =t*tile_y
            self.canvas.create_line(0,y,self.width,y,tags="grid")
            self.canvas.create_line(self.width/2-10,y,self.width/2+10,y,width=3,tags="grid")
    def resize(self,event):
        if event:
            self.width,self.height=event.width,event.height
    def packing(self) :
        self.canvas.pack(expand=1,fill="both",padx=6)

if __name__ == "__main__" :
    mw = tk.Tk()

    width = 830
    height = 630

    mw.title("Visualisation de signal sonore")
    frame=tk.Frame(mw,borderwidth=5,width=width,height=height)
    frame.grid(row=0,column=0)

    frame2=tk.Frame(mw,borderwidth=5,width=width,height=height)
    frame2.grid(row=1,column=0)

    height = frame.winfo_screenheight()
    geometry = str(width) + "x" + str(height)
    print(geometry)
    mw.geometry(geometry)

    # amplitude
    amplitudeLabel = tk.Label(frame2, text="Amplitude")
    amplitudeLabel.grid(row=0, column=0, sticky="nsew")
    amplitudeSlider = tk.Scale(frame2, from_=20, to=200,orient="horizontal",resolution=0.1)
    amplitudeSlider.grid(row=0, column=1)

    # frequency
    frequencyLabel = tk.Label(frame2, text="Frequency")
    frequencyLabel.grid(row=1, column=0, sticky="nsew")
    frequencySlider = tk.Scale(frame2, from_=4, to=100,orient="horizontal",resolution=0.1)
    frequencySlider.grid(row=1, column=1)

    # harmonic
    harmonicLabel = tk.Label(frame2, text="Harmonic")
    harmonicLabel.grid(row=2, column=0, sticky="nsew")
    harmonicSlider = tk.Scale(frame2, from_=0, to=10,orient="horizontal",resolution=1)
    harmonicSlider.grid(row=2, column=1)

    # phase
    phaseLabel = tk.Label(frame2, text="Phase change")
    phaseLabel.grid(row=3, column=0, sticky="nsew")
    phaseSlider = tk.Scale(frame2, from_=0, to=180,orient="horizontal",resolution=0.1)
    phaseSlider.grid(row=3, column=1)

    # draw the signal
    view=View(frame)
    view.grid(6)
    view.packing()

    def update(self):
        amplitude = amplitudeSlider.get()
        amplitude = amplitude/100
        frequency = frequencySlider.get()
        frequency = frequency*10
        phase = phaseSlider.get()
        harmonic = harmonicSlider.get()
        view.update(amplitude,frequency, phase, harmonic)

    amplitudeSlider.bind("<ButtonRelease-1>", update)
    frequencySlider.bind("<ButtonRelease-1>", update) 
    phaseSlider.bind("<ButtonRelease-1>", update)
    harmonicSlider.bind("<ButtonRelease-1>", update)

    mw.mainloop()
