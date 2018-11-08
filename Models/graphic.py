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
        plt.title(title, fontsize = 12, color = 'blue')
        plt.xlabel(xlabel, color = 'red')
        plt.ylabel(ylabel, color = 'orange')
        plt.plot(xdata, ydata)
        plt.savefig( os.getcwd()+ "/Salida/" + title + ".png")

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: timeGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def timeGraphic(self, data, duration, audioName):
        print("\n")
        print("Realizando el grafico del audio completo")
        print("\n")
        t = linspace(0, duration, len(data))
        self.makeGraphic("Sonido: " + audioName + " original", "Tiempo [s]", t, "Amplitud [dB]", data)

    #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: frequencyGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def frequencyGraphic(self, data, samplingRate, audioName):
        print("\n")
        print("Realizando el grafico de frecuencia de audio")
        print("\n")
        sample_length = len(data)
        #Calcula la tranformada de fourier unidimensional (matriz de data) y luego divide por el largo de la muestra
        new_data = fft(data) / sample_length
        # Funcion que retorna los resultados aplicando fourier y crea una matriz con el resultado
        fftFrequency = np.fft.fftfreq(sample_length, 1 / samplingRate)
        self.makeGraphic("Sonido: " + audioName + " aplicando T.Fourier", "Frecuencia [Hz]", fftFrequency, "Amplitud [dB]", abs(new_data))
        return new_data, fft(data)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: bandpassFilteredGraphic
    # - DESCRIPTION:
    # - OUT:
    # - PARAMS:🤡

    def bandpassFilteredGraphic(self, audio, low_cutoff, high_cutoff, order):
        print("\n")
        print("Realizando el filtro de paso de banda")
        print("\n")
        y = audio.butterBandpassFilter(audio.data_array, low_cutoff, high_cutoff, audio.sampling_rate, order)
        sample_length = len(y)
        new_data = fft(y) / sample_length
        fftFrequency = np.fft.fftfreq(sample_length, 1 / audio.sampling_rate)
        self.makeGraphic("Sonido: " + audio.audio_name + " aplicando T.Fourier (Paso Banda)", "Frecuencia [Hz]", abs(fftFrequency), "Amplitud [dB]", abs(new_data))
        return new_data, fft(y)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: lowpassFilteredGraphic
    # - DESCRIPTION:
    # - OUT:
    # - PARAMS:🤡

    def lowpassFilteredGraphic(self, audio, low_cutoff, order):
        print("\n")
        print("Realizando el filtro de paso de bajo")
        print("\n")
        y = audio.butterLowpassFilter(audio.data_array, low_cutoff, audio.sampling_rate, order)
        sample_length = len(y)
        new_data = fft(y) / sample_length
        fftFrequency = np.fft.fftfreq(sample_length, 1 / audio.sampling_rate)
        self.makeGraphic("Sonido: " + audio.audio_name + " aplicando T.Fourier (Paso Bajo)", "Frecuencia [Hz]", abs(fftFrequency), "Amplitud [dB]", abs(new_data))
        return new_data, fft(y)

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: spectrogramGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def spectrogramGraphic(self, audio):
        print("\n")
        print("Realizando el grafico de espectograma")
        print("\n")
        plt.specgram(audio.data_array, NFFT=1024, Fs=audio.sampling_rate)
        plt.xlabel('Tiempo[s]',color = 'red')
        plt.ylabel('Frecuencia[Hz]',color = 'orange')
        plt.title("Espectograma de audio "+audio.audio_name, fontsize=12, color='blue')
        plt.savefig(os.getcwd() + "/Salida/" + audio.audio_name + "-spectrogram.png")

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: spectrogramGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def filteredSpectrogramGraphic(self, audio, cutoff, order):
        print("\n")
        print("Realizando el grafico de espectograma aplicado el filtro")
        print("\n")
        y = audio.butterLowpassFilter(audio.data_array, cutoff, audio.sampling_rate, order)
        plt.specgram(y, NFFT=1024, Fs=audio.sampling_rate)
        plt.xlabel('Tiempo[s]',color = 'red')
        plt.ylabel('Frecuencia[Hz]',color = 'orange')
        plt.title("Espectograma aplicando tranformada de audio: "+ audio.audio_name, fontsize=12, color='blue')
        plt.savefig(os.getcwd() + "/Salida/" + audio.audio_name + "-spectrogramFiltrado.png")

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: inverseGraphic
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def inverseGraphic(self, data, fourierT, audioName):
        print("\n")
        print("Realizando el grafico de regenracion de audio al aplicar el filtro")
        print("\n")
        timp = len(fourierT)/data
        iFourier = ifft(fourierT)
        newtime = linspace(0,timp,len(iFourier))
        self.makeGraphic("Sonido: "+audioName+" aplicando TF. Inversa","Tiempo [s]",newtime,"Amplitud [dB]", iFourier)
        plt.savefig(os.getcwd() + "/Salida/" + audioName + "-AudioRetornado.png")

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: createGraphics
    # - DESCRIPTION: Genera todos los graficos de manera conjunta
    # - PARAMS:
    # - OUT:

    def generateGraphics1 (self, originalAudio, low_cutoff, order,title):
        print("\n")
        print("Realizando el grafico de conjunto numero 1")
        print("El cual contiene los grafico del audio completo, de frecuencia y filtro aplicado")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        self.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name)
        plt.subplot(312)
        originalAudio.informationNumpyFourier, fourierT = self.frequencyGraphic(originalAudio.data_array,originalAudio.sampling_rate,originalAudio.audio_name)
        plt.subplot(313)
        self.lowpassFilteredGraphic(originalAudio, low_cutoff, order)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title + ".png")
        plt.show()

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: createGraphics
    # - DESCRIPTION: Genera todos los graficos de manera conjunta
    # - PARAMS:
    # - OUT:

    def generateGraphics2 (self, originalAudio,title):
        print("\n")
        print("Realizando el grafico de conjunto numero 2")
        print("El cual contiene los grafico del audio completo, de frecuencia y espectograma")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        #plt.title("Sonido Original")
        self.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name)
        plt.subplot(312)
        #plt.title("Sonido aplicadando transformada")
        originalAudio.informationNumpyFourier, fourierT = self.frequencyGraphic(originalAudio.data_array,originalAudio.sampling_rate,originalAudio.audio_name)
        plt.subplot(313)
        #plt.title("Espectograma")
        self.spectrogramGraphic(originalAudio)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title + ".png")
        plt.show()
        return fourierT

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: createGraphics
    # - DESCRIPTION: Genera todos los graficos de manera conjunta
    # - PARAMS:
    # - OUT:

    def generateGraphics3 (self, originalAudio, low_cutoff, order,fourierT,title):
        print("\n")
        print("Realizando el grafico de conjunto numero 3")
        print("El cual contiene los grafico del audio completo, espectrograma (aplicado el filtro) y audio regenerado")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        p1 = plt.plot(linewidth = 2)
        self.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name)
        plt.subplot(312)
        p2 = plt.plot(linewidth = 2)
        self.filteredSpectrogramGraphic(originalAudio, low_cutoff, order)
        plt.subplot(313)
        p3 = plt.plot(linewidth = 2)
        self.inverseGraphic(originalAudio.sampling_rate, fourierT, originalAudio.audio_name)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title + ".png")
        plt.show()

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: createGraphics
    # - DESCRIPTION: Genera todos los graficos de manera conjunta
    # - PARAMS:
    # - OUT:

    def SingleGraphics(self, originalAudio, low_cutoff, high_cutoff, order):
        print("\n")
        print("Empezando la generaciones de los graficos singles........ ")
        print("\n")
        self.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name)
        plt.show()
        originalAudio.informationNumpyFourier, fourierT = self.frequencyGraphic(originalAudio.data_array, originalAudio.sampling_rate, originalAudio.audio_name)
        plt.show()
        self.lowpassFilteredGraphic(originalAudio, low_cutoff, order)
        plt.show()
        #self.bandpassFilteredGraphic(originalAudio, low_cutoff, high_cutoff, order)
        #plt.show()
        self.spectrogramGraphic(originalAudio)
        plt.show()
        self.filteredSpectrogramGraphic(originalAudio, low_cutoff, order)
        plt.show()
        self.inverseGraphic(originalAudio.sampling_rate, fourierT, originalAudio.audio_name)
        plt.show()

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: createGraphics
    # - DESCRIPTION: Genera todos los graficos de manera conjunta
    # - PARAMS:
    # - OUT:

    def createGraphics(self, originalAudio, low_cutoff, high_cutoff, order):

        self.SingleGraphics(originalAudio, low_cutoff, high_cutoff, order)


        print("\n")
        print("Empezando la generaciones de los graficos en conjunto........ ")
        print("\n")

        self.generateGraphics1(originalAudio,low_cutoff,order,"Conjunto_1")

        fourierT = self.generateGraphics2(originalAudio,"Conjunto_2")

        self.generateGraphics3(originalAudio,low_cutoff,order,fourierT,"Conjunto_3")



    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////