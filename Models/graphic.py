from numpy import linspace
from scipy import fft
import matplotlib.pyplot as plt
import os
import numpy as np

    #Clase que se encarga de tener los distintos graficos necesarios
class Graphic:

    def __init__(self):
        super(Graphic, self).__init__()

    def makeGraphic(self, title, xlabel, xdata, ylabel, ydata):
        plt.title(title, fontsize = 16, color = 'blue')
        plt.xlabel(xlabel, color = 'red')
        plt.ylabel(ylabel, color = 'orange')
        plt.plot(xdata, ydata)
        plt.savefig( os.getcwd()+ "/Salida/" + title + ".png")
        return

    def timeGraphic(self, data, duration,nameAudio):
        t = linspace(0, duration, len(data))
        self.makeGraphic("Sonido: " + nameAudio + " original", "Tiempo [s]", t, "Amplitud [dB]", data)
        plt.show()
        return

    def frequencyGraphic(self, data, frequency, nameAudio):
        sampleLength = len(data)
        #Calcula la tranformada de fourier unidimensional (matriz de data) y luego divide por el largo de la muestra
        newData = fft(data) / sampleLength
        # Funcion que retorna los resultados aplicando fourier y crea una matriz con el resultado
        fftFrequency = np.fft.fftfreq(sampleLength, 1 / frequency)
        self.makeGraphic("Sonido: " + nameAudio + " aplicando T.Fourier", "Frecuencia [Hz]", fftFrequency, "Amplitud [dB]", abs(newData))
        plt.show()
        return newData
    def spectrogramGraphic(self, data, frequency, nameAudio):
        plt.specgram(data, NFFT=1024, Fs=frequency)
        plt.xlabel('Tiempo[s]')
        plt.ylabel('Frecuencia[Hz]')
        plt.title(nameAudio, fontsize=16, color='blue')
        plt.savefig(os.getcwd() + "/Salida/" + nameAudio + "-spectrogram.png")
        plt.show()
        return




