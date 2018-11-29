from numpy import linspace
from scipy import fft, ifft
import matplotlib.pyplot as plt
import os
import numpy as np
from Models.filter import Filter

    #Clase que se encarga de tener los distintos graficos necesarios

class Graphic:

## - FUNCTIONS - ##

    #CONSTRUCTOR///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self):

        super(Graphic, self).__init__()

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: makeGraphic
    # - DESCRIPTION: Funcion que crea un gráficoz, según parametros de entrada y utilizando la biblioteca matplotlib
    # - PARAMS: Titulo del gráfico, nombre del eje x, datos del eje x, nombre del eje y, datos del eje y
    # - OUT: Void

    def makeGraphic(self, title, xlabel, xdata, ylabel, ydata, low_cutoff, order):
        plt.title(title, fontsize = 12, color = 'blue')
        plt.xlabel(xlabel, color = 'red')
        plt.ylabel(ylabel, color = 'orange')
        plt.plot(xdata, ydata)#, "*-")
        plt.savefig( os.getcwd() + "/Salida/" + title + "_" + str(low_cutoff) + "_" + str(order) + ".png")
        print("Aca")
        #plt.show()


    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: timeGraphic
    # - DESCRIPTION: procesa el audio para generar un gráfico, que muestra la amplitud v/s el tiempo
    # - PARAMS: Datos del audio, la duración del audio y el nombre del audio
    # - OUT: Void

    def timeGraphic(self, data, duration, audioName, low_cutoff, order):
        print("\n")
        print("Realizando el grafico del audio completo")
        print("\n")
        t = linspace(0, duration, len(data))
        self.makeGraphic("Sonido: " + audioName + " original", "Tiempo [s]", t, "Amplitud [dB]", data, low_cutoff, order)

    #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: frequencyGraphic
    # - DESCRIPTION: Procesa el audio, se le aplica la tranformada de fourier y se crea el gráfico de amplitud v/s frecuencia
    # - PARAMS: Datos del audio, frecuencia de la muestra y nombre del audio
    # - OUT: Transformada de Fourier arreglada y la transformada de fourier

    def frequencyGraphic(self, data, samplingRate, audioName, low_cutoff, order):
        print("\n")
        print("Realizando el grafico de frecuencia de audio")
        print("\n")
        sample_length = len(data)
        #Calcula la tranformada de fourier unidimensional (matriz de data) y luego divide por el largo de la muestra
        new_data = fft(data) / sample_length
        # Funcion que retorna los resultados aplicando fourier y crea una matriz con el resultado
        fftFrequency = np.fft.fftfreq(sample_length, 1 / samplingRate)
        self.makeGraphic("Sonido: " + audioName + " aplicando T.Fourier", "Frecuencia [Hz]", fftFrequency, "Amplitud [dB]", abs(new_data),low_cutoff,order)
        #plt.show()
        return new_data, fft(data)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: bandpassFilteredGraphic
    # - DESCRIPTION: Crea el gráfico amplitud v/s frecuencia utilizando el filtro paso banda
    # - PARAMS: La clase audio, Frecuencia de corte de frecuencias bajas, Frecuencia de corte de frecuencias altas, orden del polinomio
    # - OUT:transformada de Fourier arreglada y la transformada de fourier, con el filtro aplicado

    def bandpassFilteredGraphic(self, audio, low_cutoff, high_cutoff, order):
        print("\n")
        print("Realizando el filtro de paso de banda")
        print("\n")
        filter = Filter(audio.filter.low_cutoff,audio.filter.high_cutoff,audio.filter.order)
        y = filter.butterBandpassFilter(audio.data_array, low_cutoff, high_cutoff, audio.sampling_rate, order)
        sample_length = len(y)
        new_data = fft(y) / sample_length
        fftFrequency = np.fft.fftfreq(sample_length, 1 / audio.sampling_rate)
        self.makeGraphic("Sonido: " + audio.audio_name + " aplicando T.Fourier (Paso Banda)", "Frecuencia [Hz]", abs(fftFrequency), "Amplitud [dB]", abs(new_data),low_cutoff,order)
        return new_data, fft(y)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: lowpassFilteredGraphic
    # - DESCRIPTION: Crea el gráfico amplitud v/s frecuencia utilizando el filtro paso bajo
    # - PARAMS: La clase audio, Frecuencia de corte de frecuencias bajas, orden del polinomio
    # - OUT:transformada de Fourier arreglada y la transformada de fourier, con el filtro aplicado

    def lowpassFilteredGraphic(self, audio, low_cutoff, order):
        print("\n")
        print("Realizando el filtro de paso de bajo")
        print("\n")
        filter = Filter(audio.filter.low_cutoff,audio.filter.high_cutoff,audio.filter.order)
        y = filter.butterLowpassFilter(audio.data_array, low_cutoff, audio.sampling_rate, order)
        sample_length = len(y)
        new_data = fft(y) / sample_length
        fftFrequency = np.fft.fftfreq(sample_length, 1 / audio.sampling_rate)
        self.makeGraphic("Sonido: " + audio.audio_name + " aplicando T.Fourier (Paso Bajo)", "Frecuencia [Hz]", abs(fftFrequency), "Amplitud [dB]", abs(new_data),low_cutoff,order)
        return new_data, fft(y)

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: spectrogramGraphic
    # - DESCRIPTION: Crea un espectrograma, el cual muestra la frecuencia v/s tiempo v/s eamplitud
    # - PARAMS: La clase audio
    # - OUT: Void

    def spectrogramGraphic(self, audio, low_cutoff, order):
        print("\n")
        print("Realizando el grafico de espectograma")
        print("\n")
        plt.specgram(audio.data_array, NFFT=1024, Fs=audio.sampling_rate)
        plt.xlabel('Tiempo[s]',color = 'red')
        plt.ylabel('Frecuencia[Hz]',color = 'orange')
        plt.title("Espectograma de audio "+audio.audio_name, fontsize=12, color='blue')
        plt.savefig(os.getcwd() + "/Salida/" + audio.audio_name + "-spectrogram" + str(low_cutoff) + "_" + str(order) + ".png")

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: filteredSpectrogramGraphic
    # - DESCRIPTION: Crea un espectrograma, el cual muestra la frecuencia v/s tiempo v/s eamplitud utilizando el filtro paso bajo
    # - PARAMS: La clase audio
    # - OUT: Void

    def filteredSpectrogramGraphic(self, audio, cutoff, order):
        print("\n")
        print("Realizando el grafico de espectograma aplicado el filtro")
        print("\n")
        filter = Filter(audio.filter.low_cutoff,audio.filter.high_cutoff,audio.filter.order)
        y = filter.butterLowpassFilter(audio.data_array, cutoff, audio.sampling_rate, order)
        plt.specgram(y, NFFT=1024, Fs=audio.sampling_rate)
        plt.xlabel('Tiempo[s]',color = 'red')
        plt.ylabel('Frecuencia[Hz]',color = 'orange')
        plt.title("Espectograma aplicando tranformada de audio: "+ audio.audio_name, fontsize=12, color='blue')
        plt.savefig(os.getcwd() + "/Salida/" + audio.audio_name + "-spectrogramFiltrado_" + str(cutoff) + "_" + str(order) + ".png")

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: inverseGraphic
    # - DESCRIPTION: Crea un gráfico utilizanod la transformada inversa
    # - PARAMS: Datos del audio, la transformada de fourier, nombre del audio
    # - OUT: void

    def inverseGraphic(self, data, fourierT, audioName, low_cutoff, order):
        print("\n")
        print("Realizando el grafico de regenracion de audio al aplicar el filtro")
        print("\n")
        timp = len(fourierT)/data
        iFourier = ifft(fourierT)
        newtime = linspace(0,timp,len(iFourier))
        self.makeGraphic("Sonido: "+audioName+" aplicando TF. Inversa","Tiempo [s]",newtime,"Amplitud [dB]", iFourier,low_cutoff,order)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: generateGraphics1
    # - DESCRIPTION: Genera todos los graficos de manera conjunta (audio completo, de frecuencia y filtro aplicado)
    # - PARAMS: La clase audio, Frecuencia de corte de frecuencias bajas, orden del polinomio, titulo del gráfico
    # - OUT: void

    def generateGraphics1 (self, originalAudio, low_cutoff, order,title):
        print("\n")
        print("Realizando el grafico de conjunto numero 1")
        print("El cual contiene los grafico del audio completo, de frecuencia y filtro aplicado")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        self.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name,low_cutoff,order)
        plt.subplot(312)
        originalAudio.informationNumpyFourier, fourierT = self.frequencyGraphic(originalAudio.data_array,originalAudio.sampling_rate,originalAudio.audio_name,low_cutoff,order)
        plt.subplot(313)
        filter = Filter(low_cutoff,8,order)
        #filter.butterBandpass(low_cutoff,10000,originalAudio.sampling_rate,order)
        self.lowpassFilteredGraphic(originalAudio, low_cutoff, order)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(low_cutoff) + "_" + str(order) + ".png")
        plt.show()

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: createGraphics
    # - DESCRIPTION: Genera todos los graficos de manera conjunta (audio completo, de frecuencia y espectograma)
    # - PARAMS: Clase audio, titulo del gráfico
    # - OUT: Trasformada de Fourier

    def generateGraphics2 (self, originalAudio,title, low_cutoff,order):
        print("\n")
        print("Realizando el grafico de conjunto numero 2")
        print("El cual contiene los grafico del audio completo, de frecuencia y espectograma")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        #plt.title("Sonido Original")
        self.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name,low_cutoff,order)
        plt.subplot(312)
        #plt.title("Sonido aplicadando transformada")
        originalAudio.informationNumpyFourier, fourierT = self.frequencyGraphic(originalAudio.data_array,originalAudio.sampling_rate,originalAudio.audio_name,low_cutoff,order)
        plt.subplot(313)
        #plt.title("Espectograma")
        self.spectrogramGraphic(originalAudio,low_cutoff,order)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(low_cutoff) + "_" + str(order) + ".png")
        plt.show()
        return fourierT

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: createGraphics3
    # - DESCRIPTION: Genera todos los graficos de manera conjunta (audio completo, espectrograma (aplicado el filtro) y audio regenerado)
    # - PARAMS: La clase audio, Frecuencia de corte de frecuencias bajas, orden del polinomio, transformada de Fourier, titulo del gráfico
    # - OUT:Void

    def generateGraphics3 (self, originalAudio, low_cutoff, order,fourierT,title):
        print("\n")
        print("Realizando el grafico de conjunto numero 3")
        print("El cual contiene los grafico del audio completo, espectrograma (aplicado el filtro) y audio regenerado")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        p1 = plt.plot(linewidth = 2)
        self.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name,low_cutoff,order)
        plt.subplot(312)
        p2 = plt.plot(linewidth = 2)
        self.filteredSpectrogramGraphic(originalAudio, low_cutoff, order)
        plt.subplot(313)
        p3 = plt.plot(linewidth = 2)
        self.inverseGraphic(originalAudio.sampling_rate, fourierT, originalAudio.audio_name,low_cutoff,order)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(low_cutoff) + "_" + str(order) +".png")
        plt.show()

    def generateGraphics4 (self, cos,cos2,result,time):
        print("\n")
        print("Realizando el grafico de conjunto numero 4")
        print("El cual contiene los grafico del audio completo, espectrograma (aplicado el filtro) y audio regenerado")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        p1 = plt.plot(linewidth = 2)
        self.makeGraphic("Coseno 1","Tiempo",time,"Coseno",cos,5,5)
        plt.subplot(312)
        p2 = plt.plot(linewidth = 2)
        self.makeGraphic("Coseno 2","Tiempo",time,"Coseno",cos2,3,3)
        plt.subplot(313)
        p3 = plt.plot(linewidth = 2)
        self.makeGraphic("Resultado","Tiempo",time,"Resultado",result,7,7)
        plt.tight_layout()
        #plt.savefig(os.getcwd() + "/Salida_" + str(low_cutoff) + "_" + str(order) +".png")
        plt.show()

    def generateGraphics5 (self, cos, f, cos2, fc, result, time):
        print("\n")
        print("Realizando el grafico de conjunto numero 5")
        print("El cual contiene los grafico del audio completo, espectrograma (aplicado el filtro) y audio regenerado")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        p1 = plt.plot(linewidth = 2)
        trans1 = self.frequencyGraphic(cos, (18*f), "Coseno 1", 4, 3)
        plt.subplot(312)
        p2 = plt.plot(linewidth = 2)
        trans2 = self.frequencyGraphic(cos2, (18*fc), "Coseno 2", 4, 3)
        plt.subplot(313)
        p3 = plt.plot(linewidth = 2)
        self.frequencyGraphic(result, (18*fc), "Result", 4, 3)
        plt.tight_layout()
        #plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(low_cutoff) + "_" + str(order) +".png")
        plt.show()

    def generateGraphics6 (self, modulation, audio):
        print("\n")
        print("Realizando el grafico de conjunto numero 6")
        print("El cual contiene los grafico del audio completo, espectrograma (aplicado el filtro) y audio regenerado")
        print("\n")
        graphic = Graphic()
        plt.figure(1)
        plt.subplot(311)
        p1 = plt.plot(linewidth = 2)
        graphic.frequencyGraphic(modulation.function4, modulation.freqSampling, "demodulada", audio.filter.low_cutoff, audio.filter.order)
        plt.subplot(312)
        p2 = plt.plot(linewidth = 2)
        newdata, fft = graphic.lowpassFilteredGraphic(audio, audio.filter.low_cutoff, audio.filter.order)
        plt.subplot(313)
        p3 = plt.plot(linewidth = 2)
        graphic.inverseGraphic(modulation.freqSampling, 2 * fft, "demodulacion", audio.filter.low_cutoff, audio.filter.order)
        plt.tight_layout()
        #plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(low_cutoff) + "_" + str(order) +".png")
        plt.show()

    def generateGraphics7 (self, modulation):
        print("\n")
        print("Realizando el grafico de conjunto numero 7")
        print("El cual contiene los grafico del audio completo, espectrograma (aplicado el filtro) y audio regenerado")
        print("\n")
        graphic = Graphic()
        plt.figure(1)
        plt.subplot(211)
        p1 = plt.plot(linewidth = 2)
        self.makeGraphic("Moduladora", "Tiempo", modulation.time, "Coseno", modulation.function1, 5, 5)
        plt.subplot(212)
        p2 = plt.plot(linewidth = 2)
        self.makeGraphic("Modulacion FM", "Tiempo", modulation.time, "Coseno", modulation.function3, 5, 5)
        plt.tight_layout()
        #plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(low_cutoff) + "_" + str(order) +".png")
        plt.show()

    def generateGraphics8 (self, modulation):
        print("\n")
        print("Realizando el grafico de conjunto numero 8")
        print("El cual contiene los grafico del audio completo, espectrograma (aplicado el filtro) y audio regenerado")
        print("\n")
        plt.figure(1)
        plt.subplot(211)
        p1 = plt.plot(linewidth = 2)
        trans1 = self.frequencyGraphic(modulation.function1, modulation.freqSampling, "Moduladora", 4, 3)
        plt.subplot(212)
        p2 = plt.plot(linewidth = 2)
        trans2 = self.frequencyGraphic(modulation.function3, modulation.freqSampling, "Modulacion FM", 4, 3)
        plt.tight_layout()
        #plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(low_cutoff) + "_" + str(order) +".png")
        plt.show()

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: SingleGraphics
    # - DESCRIPTION: Genera todos los graficos de manera separada
    # - PARAMS: Clase audio, Frecuencia de corte de frecuencias bajas, Frecuencia de corte de frecuencias altas, Orden del polinomio
    # - OUT: Void

    def SingleGraphics(self, originalAudio, low_cutoff, high_cutoff, order):
        print("\n")
        print("Empezando la generaciones de los graficos singles........ ")
        print("\n")
        self.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name,low_cutoff,order)
        plt.show()
        originalAudio.informationNumpyFourier, fourierT = self.frequencyGraphic(originalAudio.data_array, originalAudio.sampling_rate, originalAudio.audio_name,low_cutoff,order)
        plt.show()
        self.lowpassFilteredGraphic(originalAudio, low_cutoff, order)
        plt.show()
        #self.bandpassFilteredGraphic(originalAudio, low_cutoff, high_cutoff, order)
        #plt.show()
        self.spectrogramGraphic(originalAudio,low_cutoff,order)
        plt.show()
        self.filteredSpectrogramGraphic(originalAudio, low_cutoff, order)
        plt.show()
        self.inverseGraphic(originalAudio.sampling_rate, fourierT, originalAudio.audio_name,low_cutoff,order)
        plt.show()

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: createGraphics
    # - DESCRIPTION: Genera todos los graficos de manera conjunta
    # - PARAMS: Clase audio, Frecuencia de corte de frecuencias bajas, Frecuencia de corte de frecuencias altas, orden del polinomio
    # - OUT: Void

    def createGraphics(self, originalAudio):


        print("\n")
        print("Empezando la generaciones de los graficos en conjunto........ ")
        print("\n")

        self.generateGraphics1(originalAudio, originalAudio.filter.low_cutoff, originalAudio.filter.order, "Conjunto_1")

        fourierT = self.generateGraphics2(originalAudio, "Conjunto_2", originalAudio.filter.low_cutoff, originalAudio.filter.order)

        self.generateGraphics3(originalAudio, originalAudio.filter.low_cutoff, originalAudio.filter.order,fourierT, "Conjunto_3")

        self.SingleGraphics(originalAudio, originalAudio.filter.low_cutoff, originalAudio.filter.high_cutoff, originalAudio.filter.order)



    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////