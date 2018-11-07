from tkinter import *
from tkinter import ttk
import os
from scipy.io.wavfile import read

class Menu:
    #CONSTRUCTOR///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def __init__(self):
        self.raiz = Tk()
        self.variable = StringVar()
        self.row = Frame(self.raiz)
        self.row2 = Frame(self.raiz)
        #self.raiz.geometry('300x200')
        self.raiz.resizable(width=False, height=False)
        self.raiz.title('avance 1')
        self.lab = Label(self.row, width = 20, text="Ingrese nombre del audio:", anchor = 'w')
        self.en = Entry(self.row)
        self.lab2 = Label(self.row2, width=18, textvariable=self.variable,fg="red", anchor = 'w')
        self.row.pack(side=TOP, fill=X, padx=5, pady=10)
        self.lab.pack(side=LEFT)
        self.en.pack(side=RIGHT, expand=YES, fill=X)
        self.row2.pack(side=TOP, fill=X, padx=5, pady=5)
        self.lab2.pack(side=RIGHT, padx= 160, pady = 0)
        self.aceptar = Button(self.raiz, text='Aceptar',command=self.readAudio)
        self.aceptar.pack(side=LEFT, padx=200, pady=5)
        self.raiz.mainloop()

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: readAudio
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:
    def readAudio(self):
        self.variable.set("")
        if (self.en.get() == ""):
            self.variable.set("*Campo vacio")
        else:
            try:
                nameText = os.getcwd() + '/Audios/' +self.en.get()+ '.wav'
                sampling_rate, data_array = read(nameText)
                dimension = data_array[0].size
            except FileNotFoundError:
                self.variable.set("*Archivo no encontrado")


