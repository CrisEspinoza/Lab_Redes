from numpy import linspace
from scipy import fft, ifft
import matplotlib.pyplot as plt
import os
import numpy as np

    #Clase que se encarga de tener los distintos graficos necesarios

class Graphic:

## - FUNCTIONS - ##

    #CONSTRUCTOR///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self):

        super(Graphic, self).__init__()

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: makeGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def makeGraphic(self, title, xlabel, xdata, ylabel, ydata):
        plt.title(title, fontsize = 16, color = 'blue')
        plt.xlabel(xlabel, color = 'red')
        plt.ylabel(ylabel, color = 'orange')
        plt.plot(xdata, ydata)
        plt.savefig( os.getcwd()+ "/Salida/" + title + ".png")
        return

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: timeGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def timeGraphic(self, data, duration, audioName):
        t = linspace(0, duration, len(data))
        self.makeGraphic("Sonido: " + audioName + " original", "Tiempo [s]", t, "Amplitud [dB]", data)
        plt.show()
        return

    #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: frequencyGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def frequencyGraphic(self, data, samplingRate, audioName):
        sample_length = len(data)
        #Calcula la tranformada de fourier unidimensional (matriz de data) y luego divide por el largo de la muestra
        new_data = fft(data) / sample_length
        # Funcion que retorna los resultados aplicando fourier y crea una matriz con el resultado
        fftFrequency = np.fft.fftfreq(sample_length, 1 / samplingRate)
        self.makeGraphic("Sonido: " + audioName + " aplicando T.Fourier", "Frecuencia [Hz]", fftFrequency, "Amplitud [dB]", abs(new_data))
        plt.show()
        return new_data, fft(data)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: bandpassFilteredGraphic
    # - DESCRIPTION:
    # - OUT:
    # - PARAMS:🤡

    def bandpassFilteredGraphic(self, audio, low_cutoff, high_cutoff, order):
        y = audio.butterBandpassFilter(audio.data_array, low_cutoff, high_cutoff, audio.sampling_rate, order)
        sample_length = len(y)
        new_data = fft(y) / sample_length
        fftFrequency = np.fft.fftfreq(sample_length, 1 / audio.sampling_rate)
        self.makeGraphic("Sonido: " + audio.audio_name + " aplicando T.Fourier (Paso Banda)", "Frecuencia [Hz]", abs(fftFrequency), "Amplitud [dB]", abs(new_data))
        plt.show()
        return new_data, fft(y)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: lowpassFilteredGraphic
    # - DESCRIPTION:
    # - OUT:
    # - PARAMS:🤡

    def lowpassFilteredGraphic(self, audio, low_cutoff, order):
        y = audio.butterLowpassFilter(audio.data_array, low_cutoff, audio.sampling_rate, order)
        sample_length = len(y)
        new_data = fft(y) / sample_length
        fftFrequency = np.fft.fftfreq(sample_length, 1 / audio.sampling_rate)
        self.makeGraphic("Sonido: " + audio.audio_name + " aplicando T.Fourier (Paso Bajo)", "Frecuencia [Hz]", abs(fftFrequency), "Amplitud [dB]", abs(new_data))
        plt.show()
        return new_data, fft(y)

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: spectrogramGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def spectrogramGraphic(self, audio):
        plt.specgram(audio.data_array, NFFT=1024, Fs=audio.sampling_rate)
        plt.xlabel('Tiempo[s]')
        plt.ylabel('Frecuencia[Hz]')
        plt.title(audio.audio_name, fontsize=16, color='blue')
        plt.savefig(os.getcwd() + "/Salida/" + audio.audio_name + "-spectrogram.png")
        plt.show()
        return

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: spectrogramGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def filteredSpectrogramGraphic(self, audio, cutoff, order):
        y = audio.butterLowpassFilter(audio.data_array, cutoff, audio.sampling_rate, order)
        plt.specgram(y, NFFT=1024, Fs=audio.sampling_rate)
        plt.xlabel('Tiempo[s]')
        plt.ylabel('Frecuencia[Hz]')
        plt.title(audio.audio_name, fontsize=16, color='blue')
        plt.savefig(os.getcwd() + "/Salida/" + audio.audio_name + "-spectrogram.png")
        plt.show()
        return

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: inverseGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def inverseGraphic(self, data, fourierT, audioName):
        timp = len(fourierT)/data
        iFourier = ifft(fourierT)
        newtime = linspace(0,timp,len(iFourier))
        self.makeGraphic("Sonido: "+audioName+" aplicando TF. Inversa","Tiempo [s]",newtime,"Amplitud [dB]", iFourier)
        plt.show()
        return

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: createGraphics
    # - DESCRIPTION: Genera todos los graficos de manera conjunta
    # - PARAMS:
    # - OUT:

    def createGraphics(self, originalAudio, low_cutoff, high_cutoff, order):
        self.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name)
        originalAudio.informationNumpyFourier, fourierT = self.frequencyGraphic(originalAudio.data_array, originalAudio.sampling_rate, originalAudio.audio_name)
        self.lowpassFilteredGraphic(originalAudio, low_cutoff, order)
        #self.bandpassFilteredGraphic(originalAudio, low_cutoff, high_cutoff, order)
        self.spectrogramGraphic(originalAudio)
        self.filteredSpectrogramGraphic(originalAudio, low_cutoff, order)
        self.inverseGraphic(originalAudio.sampling_rate, fourierT, originalAudio.audio_name)
        return

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////