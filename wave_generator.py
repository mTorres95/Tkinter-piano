# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

import sys
import wave
import math
import winsound
import subprocess

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

class WaveGenerator :

    def __init__(self,parent,view=None,piano=None):
        self.view = view
        self.piano = piano
        
        # dictionary for notes and its frequencies
        self.frequencies = { 'C' : 261.63,
                        'C#': 277.18,
                        'D' : 253.66,
                        'D#': 311.13,
                        'E' : 329.63,
                        'F' : 349.23,
                        'F#': 369.99,
                        'G' : 392.00,
                        'G#': 415.308,
                        'A' : 440.00,
                        'A#': 466.16,
                        'B' : 493.88    }
        # string for scales (repeated so it doesn't get out of ranges)
        self.chromatic = "C, C#, D, D#, E, F, F#, G, G#, A, A#, B, C, C#, D, D#, E, F, F#, G, G#, A, A#, B"
        self.chromaticArray = self.chromatic.split(", ")
        self.create_widgetd(parent)
        self.listNotes = []
        self.listChords = []

    def create_widgetd(self,parent):
        self.canvas=tk.Canvas(parent,width=600,height=300)
        #self.canvas.bind("<Configure>")  #The widget changed size. The new size is provided in the width and height attributes of the event object passed to the callback.

        #self.screen=tk.Frame(parent,borderwidth=5,width=500,height=160,bg="pink")
        # note and octave
        self.noteLabel = tk.Label(self.canvas, text="Note")
        #self.noteLabel.pack()
        self.noteLabel.grid(row=0, column=1, sticky="nsew")
        self.spinNote = tk.Spinbox(self.canvas, values=('C','C#','D','D#','E','F','F#','G','G#','A','A#','B'), wrap=True, command = self.update_signal)
        #self.spinNote.pack()
        self.spinNote.grid(row=0, column=2, sticky="nsew")
        


        self.octaveLabel = tk.Label(self.canvas, text="Octave")
        #self.octaveLabel.pack()
        self.octaveLabel.grid(row=1, column=1, sticky="nsew")
        self.spinOctave = tk.Spinbox(self.canvas, values=(4,5,6,7), command = self.update_signal)
        #self.spinOctave.pack()
        self.spinOctave.grid(row=1, column=2, sticky="nsew")
        

        # duration
        self.durationLabel = tk.Label(self.canvas, text="Duration")
        self.durationLabel.grid(row=2, column=2)
        #self.durationLabel.pack()
        self.durationSlider = tk.Scale(self.canvas, from_=0.5, to=4,orient="horizontal",resolution=0.1)
        self.durationSlider.grid(row=3, column=2)
        
        self.volumeLabel = tk.Label(self.canvas, text="Volume")
        self.volumeLabel.grid(row=2, column=0)
        self.volumeSlider = tk.Scale(self.canvas, from_=0.2, to=1,orient="horizontal",resolution=0.2, command = self.update_signal_slider)
        self.volumeSlider.grid(row=3, column=0)
        #self.durationSlider.pack()

        # single note
        self.singleNoteLabel = tk.Label(self.canvas, text="Generate single note")
        #self.singleNoteLabel.pack()
        self.singleNoteLabel.grid(row=0, column=0, sticky="nsew")
        self.buttonNote = tk.Button(self.canvas, text="Generate note .wav")
        #self.buttonNote.pack()
        self.buttonNote.grid(row=1, column=0, sticky="nsew")
        self.buttonNote.bind("<Button-1>", self.handle_click_note)

        # chord (major or minor)
        self.chordLabel = tk.Label(self.canvas, text="Generate Chord")
        self.chordLabel.grid(row=0, column=3, sticky="nsew")
        #self.chordLabel.pack()

        self.modeLabel = tk.Label(self.canvas, text="Major/Minor")
        #self.modeLabel.pack()
        self.modeLabel.grid(row=2, column=3, sticky="nsew")
        self.spinMode = tk.Spinbox(self.canvas, values=('Major', 'Minor'), wrap=True)
        #self.spinMode.pack()
        self.spinMode.grid(row=3, column=3, sticky="nsew")

        self.buttonMode = tk.Button(self.canvas, text="Generate chord .wav")
        #self.buttonMode.pack()
        self.buttonMode.grid(row=1, column=3, sticky="nsew")
        self.buttonMode.bind("<Button-1>", self.handle_click_mode) 

        self.view.update(self.volumeSlider.get(),float(self.frequencies[self.spinNote.get()])*(int(self.spinOctave.get())-3))

        # NOTE LIST
        
        self.NoteList_Label = tk.Label(self.canvas, text="Generated Notes").grid(row=0, column=4, sticky="nsew")
        self.ListBox= tk.Listbox(self.canvas,selectmode = 'SINGLE')
        self.scrollbar = tk.Scrollbar(self.canvas, orient='vertical')
        self.ListBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.ListBox.yview)
        self.ListBox.grid(row=1, column=4, sticky="nsew",rowspan = 3)
        self.scrollbar.grid(row=1, column=5, sticky="nsew",rowspan = 3)

        #PLAY NOTE FORM LIST
        self.buttonPlay_Note = tk.Button(self.canvas, text="Play Note")
        self.buttonPlay_Note.grid(row=2, column=6, sticky="nsew")
        self.buttonPlay_Note.bind("<Button-1>", self.play_Note) 

        #CHORDS LIST
        self.ChordsList_Label = tk.Label(self.canvas, text="Generated Chords").grid(row=0, column=7, sticky="nsew")
        self.ListBoxChords= tk.Listbox(self.canvas)
        self.scrollbarChords = tk.Scrollbar(self.canvas, orient='vertical')
        self.ListBoxChords.config(yscrollcommand=self.scrollbarChords.set)
        self.scrollbarChords.config(command=self.ListBoxChords.yview)
        self.ListBoxChords.grid(row=1, column=7, sticky="nsew",rowspan = 3)
        self.scrollbarChords.grid(row=1, column=8, sticky="nsew",rowspan = 3)
       
        #PLAY CHORD FORM LIST
        self.buttonPlay_Chord = tk.Button(self.canvas, text="Play Chord")
        self.buttonPlay_Chord.grid(row=2, column=9, sticky="nsew")
        self.buttonPlay_Chord.bind("<Button-1>", self.play_Chord) 
        #self.buttonPlay_Chord.bind("<ButtonRelease-1>", self.OriginalColor) 

    def play_Note(self,event):
        note = self.ListBox.get(self.ListBox.curselection())
        if sys.platform == 'win32':
            
            winsound.PlaySound(note, winsound.SND_FILENAME) # Change "A4.wav"
        elif sys.platform == 'linux':
            subprocess.call(["aplay",note]) # Change "A4.wav"
        else: 
            print("Your system is not compatible to play the sound")
    
    def play_Chord(self,event):
        chord = self.ListBoxChords.get(self.ListBoxChords.curselection())
        if 'Major' in chord :
            
            print('Major')
            if "#" in chord:
                note=chord[0:2]
            else:
                note=chord[0:1] 
            note=note.lower()
            print(note.lower())
            self.piano.control.button.nametowidget('.!frame.!frame.!frame2.'+ note).configure(bg = "red")

            
        else :
            print('Minor')
            note=chord[0:1]
            print(note.lower())



        if sys.platform == 'win32':
            
            winsound.PlaySound(chord, winsound.SND_FILENAME) # Change "A4.wav"
        elif sys.platform == 'linux':
            subprocess.call(["aplay",chord]) # Change "A4.wav"
        else: 
            print("Your system is not compatible to play the sound")
        
        self.piano.control.button.after(1000,self.OriginalColor)

    def OriginalColor(self):
        #self.piano.control.button.nametowidget('.!frame.!frame.!frame2.'+note).configure(bg = "white")
        chord=self.ListBoxChords.get(self.ListBoxChords.curselection())
        chord=chord.lower()
        print('entra')
        if("#" in chord):
            self.piano.control.button.nametowidget('.!frame.!frame.!frame2.'+chord[0:2]).configure(bg = "black")
        else:
            print('entra')
            self.piano.control.button.nametowidget('.!frame.!frame.!frame2.'+chord[0]).configure(bg = "white")



    def packing(self) :
        self.canvas.pack(expand=1,fill="both",padx=6)

    # handle of button: generates .wav of notes
    def handle_click_note(self, event):
        id = 0
        note = self.spinNote.get()
        octave = self.spinOctave.get()
        duration = self.durationSlider.get()
 
        fileName = note + octave + '.wav'
        sound = wave.open(fileName,'w') # instanciation de l'objet sound

        nbChannel = 2    # stéreo
        nbBit = 1    # taille d'un échantillon : 1 octet = 8 bits
        freqE = 44100   # fréquence d'échantillonnage

        L_level = 1*self.volumeSlider.get()
        R_level = 1*self.volumeSlider.get()

        nSamples = int(duration*freqE)
        print("Nombre d'échantillons :",nSamples)

        parametres = (nbChannel,nbBit,freqE,nSamples,'NONE','not compressed')# tuple
        sound.setparams(parametres)    # création de l'en-tête (44 octets)

        # niveau max dans l'onde positive : +1 -> 255 (0xFF)
        # niveau max dans l'onde négative : -1 ->   0 (0x00)
        # niveau sonore nul :                0 -> 127.5 (0x80 en valeur arrondi)

        amplitudeL = 127.5*L_level
        amplitudeR = 127.5*R_level

        frequenceR = float(self.frequencies[note])*(int(octave)-3)
        frequenceL = frequenceR

        print('Please wait...')
        for i in range(0,nSamples):
            # canal gauche
            # 127.5 + 0.5 pour arrondir à l'entier le plus proche
            valG = wave.struct.pack('B',int(128.0 + amplitudeL*math.sin(2.0*math.pi*frequenceL*i/freqE)))
            # canal droit
            valD = wave.struct.pack('B',int(128.0 + amplitudeR*math.sin(2.0*math.pi*frequenceR*i/freqE)))
            sound.writeframes(valG + valD) # écriture frame

        sound.close()
        print(fileName, 'created.')
        if not fileName in self.listNotes :
            self.listNotes.append(fileName) 
            self.ListBox.insert(id, fileName)
            id+=1
            print(self.listNotes)      

    def handle_click_mode(self, event):

        id = 0
        mode = self.spinMode.get()
        note = self.spinNote.get()
        octave = self.spinOctave.get() 
        duration = self.durationSlider.get()

        modalNoteIndex = self.chromaticArray.index(note)
        arrayFreq = []
        arrayFreq.append(self.frequencies[self.chromaticArray[modalNoteIndex]])
        fileName = note + octave + "_"

        if mode == 'Major':
            arrayFreq.append(self.frequencies[self.chromaticArray[modalNoteIndex + 5]])
            fileName+= "Major.wav"
        else:
            arrayFreq.append(self.frequencies[self.chromaticArray[modalNoteIndex + 4]])
            fileName+= "Minor.wav"
        
        arrayFreq.append(self.frequencies[self.chromaticArray[modalNoteIndex + 8]])
        print(fileName)

        sound = wave.open(fileName,'w') # instanciation de l'objet sound

        nbChannel = 2    # Stereo
        nbBit = 1    # taille d'un échantillon : 1 octet = 8 bits
        freqE = 44100   # fréquence d'échantillonnage

        L_level = 1
        R_level = 1

        nSamples = int(duration*freqE)
        print("Nombre d'échantillons :",nSamples)

        parametres = (nbChannel,nbBit,freqE,nSamples,'NONE','not compressed')# tuple
        sound.setparams(parametres)    # création de l'en-tête (44 octets)

        # niveau max dans l'onde positive : +1 -> 255 (0xFF)
        # niveau max dans l'onde négative : -1 ->   0 (0x00)
        # niveau sonore nul :                0 -> 127.5 (0x80 en valeur arrondi)

        amplitudeL = 127.5*L_level
        amplitudeR = 127.5*R_level

        print('Please wait...')
        # for freq in arrayFreq:
        #     for i in range(0,nSamples):
        #         # canal gauche
        #         # 127.5 + 0.5 pour arrondir à l'entier le plus proche
        #         valG = wave.struct.pack('B',int(128.0 + amplitudeL*math.sin(2.0*math.pi*freq*(int(octave)-3)*i/freqE)))
        #         # canal droit
        #         valD = wave.struct.pack('B',int(128.0 + amplitudeR*math.sin(2.0*math.pi*freq*(int(octave)-3)*i/freqE)))
        #         sound.writeframes(valG + valD) # écriture frame

        for i in range(0,nSamples):
            aux = int(128.0 + amplitudeR/3*math.sin(2.0*math.pi*float(arrayFreq[0])*(int(octave)-3)*i/freqE)
                            + amplitudeR/3*math.sin(2.0*math.pi*float(arrayFreq[1])*(int(octave)-3)*i/freqE)
                            + amplitudeR/3*math.sin(2.0*math.pi*float(arrayFreq[2])*(int(octave)-3)*i/freqE) )
            # canal gauche
            # 127.5 + 0.5 pour arrondir à l'entier le plus proche
            valG = wave.struct.pack('B', aux)
            # canal droit
            valD = wave.struct.pack('B', aux)
            sound.writeframes(valG + valD) # écriture frame
        sound.close()
        print(fileName, 'created.')
        if not fileName in self.listChords :
            self.listChords.append(fileName) 
            self.ListBoxChords.insert(id, fileName)
            id+=1
            print(self.listChords) 
              

    def update_signal(self):
        
        self.view.update(self.volumeSlider.get(),float(self.frequencies[self.spinNote.get()])*(int(self.spinOctave.get())-3))
        print(self.spinNote.get())

    def update_signal_slider(self,event):
        
        self.view.update(self.volumeSlider.get(),float(self.frequencies[self.spinNote.get()])*(int(self.spinOctave.get())-3))
        print(self.spinNote.get())

if __name__ == "__main__" :
    mw = tk.Tk()    #create window object
    #mw.geometry("360x300")   #window size
    mw.title("Generateur de fichier au format WAV")
    
    mw.rowconfigure(0, minsize=50, weight=1)
    mw.columnconfigure([0, 1, 2], minsize=50, weight=1)

    frame=tk.Frame(mw,borderwidth=5,width=360,height=300,bg="pink")
    frame.pack()

    waveGenerator = WaveGenerator(frame)
    waveGenerator.packing()
    #waveGenerator.get_screen().grid(column=3,row=1)
    mw.mainloop()  #run the Tkinter event loop. This method listens for events, such as button clicks or keypresses, and blocks any code that comes after it from running until the window it’s called on is closed
