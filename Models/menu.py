from tkinter import *
from tkinter import ttk
from Models.audio import Audio
from Models.graphic import Graphic
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
                self.audio_name = self.en.get()
                self.nameText = os.getcwd() + '/Audios/' + self.en.get() + '.wav'
                self.sampling_rate, self.data_array = read(self.nameText)
                self.dimension = self.data_array[0].size
                self.otherWindows()
            except FileNotFoundError:
                self.variable.set("*Archivo no encontrado")

    def otherWindows(self):
        self.raiz2 = Tk()
        self.variable2 = StringVar()
        self.raiz2.title('avance 1')
        self.raiz2.resizable(width=False, height=False)

        row = Frame(self.raiz2)
        lab = Label(row, width=35, text="Introduzca la frecuencia de filtro bajo (Hz):", anchor='w')
        self.low_cutoff = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        self.low_cutoff.pack(side=RIGHT, expand=YES, fill=X)

        row2 = Frame(self.raiz2)
        lab2 = Label(row2, width=35, text="Introduzca la frecuencia de filtro alto (Hz):", anchor='w')
        self.high_cutoff = Entry(row2)
        row2.pack(side=TOP, fill=X, padx=5, pady=5)
        lab2.pack(side=LEFT)
        self.high_cutoff.pack(side=RIGHT, expand=YES, fill=X)

        row3 = Frame(self.raiz2)
        lab3 = Label(row3, width=35, text="Introduzca el orden deseado para el filtro (N):", anchor='w')
        self.order = Entry(row3)
        row3.pack(side=TOP, fill=X, padx=5, pady=5)
        lab3.pack(side=LEFT)
        self.order.pack(side=RIGHT, expand=YES, fill=X)

        row4 = Frame(self.raiz2)
        lab4 = Label(row4, width=18, textvariable=self.variable2,fg="red", anchor='w')
        row4.pack(side=TOP, fill=X, padx=180, pady=5)
        lab4.pack(side=LEFT)

        self.mostrar = Button(self.raiz2, text='Aceptar', command=self.showgraphic())
        self.mostrar.pack(side=LEFT, padx=180, pady=5)
        #self.raiz2.mainloop()

    def showgraphic(self):
        print("Funciona")
        self.variable2.set("")
        if (self.low_cutoff.get() == "" or self.high_cutoff.get() == "" or self.order.get() == ""):
            self.variable2.set("*Campo(s) vacio")
        else:
            if self.dimension == 1:
                data = self.data_array
            else:
                data = self.data_array[:, self.dimension - 1]

            time = len(data) / self.sampling_rate
            originalAudio = Audio(self.sampling_rate, self.dimension, self.data, self.time,self.audio_name, self.low_cutoff.get(), self.high_cutoff.get(), self.order.get())
            grafic = Graphic()
            grafic.createGraphics(originalAudio, self.low_cutoff.get(), self.high_cutoff.get(), self.order.get())

