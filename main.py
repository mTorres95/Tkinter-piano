import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
else :
    print("Your python version is : ",major,minor)
    print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 
    from tkinter import messagebox
from math import pi,sin
#import collections
import subprocess
from observer import *
from piano import *
from signal_visualizer import *
from wave_generator import *

mw = tk.Tk()
height = mw.winfo_screenheight()
width = mw.winfo_screenwidth()
geometry = str(width) + "x" + str(height)
mw.geometry(geometry)
mw.title("Piano Lesson")
frame=tk.Frame(mw,borderwidth=5,width=360,height=300)
octaves=4
piano=Piano(frame,octaves)

view=View(frame)
view.grid(8)

waveGenerator=WaveGenerator(frame,view,piano)
waveGenerator.packing()

view.packing()
#view.update(waveGenerator)
frame.pack()


# create Menu
menubar = tk.Menu(mw)

# file dropdown menu
filemenu = tk.Menu(menubar, tearoff=0)
def onOpen():
    print(filedialog.askopenfilename(initialdir = "/",title = "Open file",filetypes = (("Python files","*.py;*.pyw"),("All files","*.*"))))

filemenu.add_command(label="Open", command=onOpen)
# filemenu.add_command(label="Save", command=hello)
# filemenu.add_separator()
def exit_application():
    answer = messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
    if answer == 'yes':
       mw.destroy()
    #else:
    #    tk.messagebox.showinfo('Return','You will now return to the application screen')
filemenu.add_command(label="Exit", command=exit_application)
menubar.add_cascade(label="File", menu=filemenu)

# help dropdown menu
helpmenu = tk.Menu(menubar, tearoff=0)
def lib_application():
    messagebox.showinfo("About","This application has:\n  a piano\n  a signal visualiser\n  and a wave generator"
                                "and each of them can be played individualy.\n\n"
                                "In this main application, you'll be able to generate the notes\n"
                                "you wish and play them either from the piano or the 'Play Note' button.\n"
                                "For the chords, you don't need to know how to form them, just chose the\n"
                                "note and whether the chord is Minor or Mayor! You can play them from the\n"
                                "'Play Chord' button or from the piano too.\n"
                                "You will also be able to see the signal the note you want to generate\n"
                                "produces at the lower part of the window.\n")
helpmenu.add_command(label="About", command=lib_application)
def about_application():
    messagebox.showinfo("Authors","Perez, Jeronimo\nMia Torres Lopez\nENIB - CAI\nProfessor: Alexis Nédélec")
helpmenu.add_command(label="Creators", command=about_application)
def lib_application():
    messagebox.showinfo("Libraries","TkInter\n   - wiki.python.org/moin/TkInter\n"
                                    "Winsound (sound in Windows)\n   - docs.python.org/2/library/winsound.html\n"
                                    "Aplay (sound in Linux)\n   - docs.python.org/2/library/winsound.html\n"
                                    "Format audio WAV:\n   - linux.die.net/man/1/aplay\n")
helpmenu.add_command(label="Libraries", command=lib_application)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
mw.config(menu=menubar)

mw.mainloop()
