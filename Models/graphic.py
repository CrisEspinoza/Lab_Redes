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
        self.makeGraphic("Sonido: " + str(audio.audio_name) + " aplicando T.Fourier (Paso Bajo)", "Frecuencia [Hz]", fftFrequency, "Amplitud [dB]", new_data,low_cutoff, order)
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
        #plt.savefig(os.getcwd() + "/Salida/" + audio.audio_name + "-spectrogram" + str(low_cutoff) + "_" + str(order) + ".png")

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
        #plt.savefig(os.getcwd() + "/Salida/" + audio.audio_name + "-spectrogramFiltrado_" + str(cutoff) + "_" + str(order) + ".png")

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

    def generateGraphics1 (self, originalAudio, low_cutoff, order, title):
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

    def generateGraphics2 (self, originalAudio, title, low_cutoff, order):
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

    def generateGraphics3 (self, originalAudio, low_cutoff, order, fourierT, title):
        print("\n")
        print("Realizando el grafico de conjunto numero 3")
        print("El cual contiene los grafico del audio completo, espectrograma (aplicado el filtro) y audio regenerado")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        self.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name,low_cutoff,order)
        plt.subplot(312)
        self.filteredSpectrogramGraphic(originalAudio, low_cutoff, order)
        plt.subplot(313)
        self.inverseGraphic(originalAudio.sampling_rate, fourierT, originalAudio.audio_name,low_cutoff,order)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(low_cutoff) + "_" + str(order) +".png")
        plt.show()

    """
        Entrada: Entra los dos cosenos y el resultado obtenido al realizar la modulacion, el tiempo de cada 
        uno de ellos y el titulo que le colcocaremos al grafico.
        Procedimiento: Se encarga de graficar cada uno de los cosenos y ademas del recultado obtenido, por ultimo
        guarda cada uno de los graficos en la carpeta que tenemos de salida.
        Salida: -
    """

    def generateGraphics4(self, cos, cos2, result, time, title):
        print("\n")
        print("Realizando el grafico de conjunto numero 4")
        print("El cual contiene los grafico de tiempo de cada una de las señales ha analizar")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        self.makeGraphic("Señal Moduladora", "Tiempo", time, "Amplitud", cos, 5, 5)
        plt.subplot(312)
        self.makeGraphic("Señal Portadora", "Tiempo", time, "Amplitud", cos2, 3, 3)
        plt.subplot(313)
        self.makeGraphic("Señal Modulada", "Tiempo", time, "Amplitud", result, 7, 7)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/_" + "Graficos_Tiempo_Modulacion_AM_" + title + ".png")
        plt.show()
        # Realizando graficos individuales
        self.makeGraphic("Señal Moduladora", "Tiempo", time, "Amplitud", cos, 5, 5)
        plt.savefig(os.getcwd() + "/Salida/_" + "Grafico_Tiempo_Moduladora_" + title + ".png")
        plt.show()
        self.makeGraphic("Señal Portadora", "Tiempo", time, "Amplitud", cos2, 3, 3)
        plt.savefig(os.getcwd() + "/Salida/_" + "Grafico_Tiempo_Portadora_" + title + ".png")
        plt.show()
        self.makeGraphic("Señal Modulada", "Tiempo", time, "Amplitud", result, 7, 7)
        plt.savefig(os.getcwd() + "/Salida/_" + "Grafico_Tiempo_Modulada_" + title + ".png")
        plt.show()


    """
        Entrada: Entra los dos cosenos y el resultado obtenido al realizar la modulacion, la frecuencia de
        muestreo que contiene y el titulo que contendra dicho grafico.
        Procedimiento: Se encarga de graficar cada una de las tranformadas de foruier de los cosenos y el 
        resultado que se obtuvo para poder comparar cada uno de estos resultados. Luego, por ultimo se
        encarga de guarda cada uno de estos graficos en la caprtea de salida que tenemos.
        Salida: -
    """

    def generateGraphics5 (self, cos, cos2, result, freqSampling,title):
        print("\n")
        print("Realizando el grafico de conjunto numero 5")
        print("El cual contiene los grafico de frecuencia de cada una de las señales analizadas")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        trans1 = self.frequencyGraphic(cos, freqSampling, "Señal moduladora", 4, 3)
        plt.subplot(312)
        trans2 = self.frequencyGraphic(cos2, freqSampling, "Señal portadora", 4, 3)
        plt.subplot(313)
        self.frequencyGraphic(result, freqSampling, "Señal modulada", 4, 3)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title +".png")
        plt.show()
        # Realizando graficos indivuales
        self.frequencyGraphic(cos, freqSampling, "Señal moduladora", 4, 3)
        plt.savefig(os.getcwd() + "/Salida/" + title + ".png")
        plt.show()
        trans2 = self.frequencyGraphic(cos2, freqSampling, "Señal portadora", 4, 3)
        plt.savefig(os.getcwd() + "/Salida/" + title + ".png")
        plt.show()
        self.frequencyGraphic(result, freqSampling, "Señal modulada", 4, 3)
        plt.savefig(os.getcwd() + "/Salida/" + title + ".png")
        plt.show()


    """
        Entrada: ENtra la modulacion que contiene cada una de las variables que estamos utilizando, ademas
        del audio que estamos utilkizando y el tituklo que se le colocara al grafico.
        Procedimiento: Se encarga de hacer 4 graficos dentro de 1, donde tenemos que realiza la grafico que
        contiene al audio en su normalidad, la transformada de foruier que se obtiene del resultado y luego
        le aplicamos el filtro para poder graficarlo de igual manera, para poder apreciar como se vio reflejada
        la modulacion dentro de esos graficos y por tulimo realizamos la antitranformada para poder apreciar
        si tenemos que nos devuelve el mismo audio que el original que se encuentra en una primera instacncia
        dentro del grafico. Para por utlimo gurdar cada uno de estos graficos en la carpeta que tenemos de salida
        de lso graficos.
        Salida: -
    """

    def generateGraphics6 (self, modulation, audio, title):
        print("\n")
        print("Realizando el grafico de conjunto numero 6")
        print("El cual contiene los grafico de la transformada de fourier, el filtro paso bajo y el audio demodulado")
        print("\n")
        graphic = Graphic()
        plt.figure(1)
        plt.subplot(411)
        self.makeGraphic("Señal Moduladora", "Tiempo", modulation.time, "Amplitud", modulation.function1, 5, 5)
        plt.subplot(412)
        graphic.frequencyGraphic(modulation.function4, modulation.freqSampling, "demodulada", audio.filter.low_cutoff, audio.filter.order)
        plt.subplot(413)
        newdata, fft = graphic.lowpassFilteredGraphic(audio, audio.filter.low_cutoff, audio.filter.order)
        plt.subplot(414)
        graphic.inverseGraphic(modulation.freqX, 2*fft, "demodulacion", audio.filter.low_cutoff, audio.filter.order)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title +".png")
        plt.show()
        # Realizando graficos indivuales
        graphic.frequencyGraphic(modulation.function4, modulation.freqSampling, "demodulada", audio.filter.low_cutoff,audio.filter.order)
        plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(audio.filter.low_cutoff) + "_" + str(audio.filter.order) + ".png")
        plt.show()
        newdata, fft = graphic.lowpassFilteredGraphic(audio, audio.filter.low_cutoff, audio.filter.order)
        plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(audio.filter.low_cutoff) + "_" + str(audio.filter.order) + ".png")
        plt.show()
        graphic.inverseGraphic(modulation.freqX, 2 * fft, "demodulacion", audio.filter.low_cutoff, audio.filter.order)
        plt.savefig(os.getcwd() + "/Salida/" + title + "_" + str(audio.filter.low_cutoff) + "_" + str(audio.filter.order) + ".png")
        plt.show()


    """
        Entrada: ENtra la modulacion que contiene cada una de las variables que estamos utilizando, ademas
        del audio que estamos utilkizando y el tituklo que se le colocara al grafico.
        Procedimiento: Se encarga de realizar dos graficos en 1. Se encarga de graficar cada la señal 
        portadora y la modualdora, para luego guardar cada uno de estos grafivos en la caprtea que 
        tenemos de salida de los gafricos.
        Salida: -
    """


    def generateGraphics7 (self, modulation,title):
        print("\n")
        print("Realizando el grafico de conjunto numero 7")
        print("El cual contiene los grafico de tiempo de la señal moduladora y la señal modulada con FM")
        print("\n")
        graphic = Graphic()
        plt.figure(1)
        plt.subplot(211)
        p1 = plt.plot(linewidth = 2)
        self.makeGraphic("Moduladora", "Tiempo", modulation.time, "Señal moduladora coseno de Freq. " + str(modulation.freq1), modulation.function1, 5, 5)
        plt.subplot(212)
        p1 = plt.plot(linewidth = 2)
        self.makeGraphic("Modulacion FM", "Tiempo", modulation.time, "Señal portadora", modulation.function3, 5, 5)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title +".png")
        plt.show()
        # Realizando graficos indivuales
        self.makeGraphic("Moduladora", "Tiempo", modulation.time, "Señal moduladora coseno de Freq. " + str(modulation.freq1),modulation.function1, 5, 5)
        plt.show()
        self.makeGraphic("Modulacion FM", "Tiempo", modulation.time, "Señal portadora", modulation.function3, 5, 5)
        plt.show()

    """
        Entrada: ENtra la modulacion que contiene cada una de las variables que estamos utilizando, ademas
        del audio que estamos utilkizando y el tituklo que se le colocara al grafico.
        Procedimiento: Se encarga de realizar dos graficos en 1.Ademas, se encarga de graficar cada la señal portadora y la modualdora pero dentro del dominio
        de su tranformada de fourier para poder comprar cada uno de los reuasltados obtenidos, para 
        luego guardar cada uno de estos grafivos en la caprtea que tenemos de salida de los gafricos.
        Salida: -
    """

    def generateGraphics8 (self, modulation, title):
        print("\n")
        print("Realizando el grafico de conjunto numero 8")
        print("El cual contiene los grafico de frecuencia de la señal moduladora y la señal modulada por FM")
        print("\n")
        plt.figure(1)
        plt.subplot(211)
        p1 = plt.plot(linewidth = 2)
        trans1 = self.frequencyGraphic(modulation.function1, modulation.freqSampling, "Señal moduladora de coseno de Freq. " + str(modulation.freq1), 4, 3)
        plt.subplot(212)
        p1 = plt.plot(linewidth = 2)
        trans2 = self.frequencyGraphic(modulation.function3, modulation.freqSampling, "Modulacion FM", 4, 3)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title +".png")
        plt.show()
        # Realizando graficos indivuales
        trans1 = self.frequencyGraphic(modulation.function1, modulation.freqSampling,"Señal moduladora de coseno de Freq. " + str(modulation.freq1), 4, 3)
        plt.show()
        trans2 = self.frequencyGraphic(modulation.function3, modulation.freqSampling, "Modulacion FM", 4, 3)
        plt.show()

    """
        Entrada: Entra el nuevo data que obtenidmos y el carrier, ademas del resultado obtenido y por ultimo
        tenemos que ingtresamos le titulo que le colcaremos al grafico.
        Procedimiento: Se encarga de realizar dos graficos en 1. donde tenemos que graficamos cada uno de los
        graficos para poder apreciar los resultados que obtuvimos, para luego guardar cada uno de estos
        pero cortando sus datos, con el fin de apreciar aun de mejor forma los resultados y poder interpretar
        los resultados obtenidos de una mejor forma, debido a que vamos a tener una mejor apreciacion de los
        datos que contempla los graficos.
        Salida: -
    """

    def generateGraphics9 (self, newData,timeCarrier,result,title):
        print("\n")
        print("Realizando el grafico de conjunto numero 9")
        print("El cual contiene los grafico de tiempo del audio representadno a la señal moduladora y la señal modulada por FM")
        print("\n")
        graphic = Graphic()
        plt.figure(1)
        plt.subplot(211)
        p2 = plt.plot(linewidth = 1)
        self.makeGraphic("Moduladora", "Tiempo[s]", timeCarrier, "Amplitud[Bd]", newData, 5, 5)
        plt.subplot(212)
        p2 = plt.plot(linewidth = 1)
        self.makeGraphic("Modulacion FM", "Tiempo[s]", timeCarrier, "Amplitud[Bd]", result, 5, 5)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title +".png")
        plt.show()

        plt.figure(2)
        plt.subplot(211)
        p2 = plt.plot(linewidth=1)
        self.makeGraphic("Moduladora extracto", "Tiempo[s]", timeCarrier[100000:101000], "Amplitud[Bd]",
                         newData[100000:101000], 5, 5)
        plt.subplot(212)
        p2 = plt.plot(linewidth=1)
        self.makeGraphic("Modulacion FM extracto", "Tiempo[s]", timeCarrier[100000:101000], "Amplitud[Bd]"
                         ,result[100000:101000], 5, 5)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title + " extracto.png")
        plt.show()
        # Realizando graficos indivuales
        self.makeGraphic("Moduladora", "Tiempo[s]", timeCarrier, "Amplitud[Bd]", newData, 5, 5)
        plt.show()
        self.makeGraphic("Modulacion FM", "Tiempo[s]", timeCarrier, "Amplitud[Bd]", result, 5, 5)
        plt.show()

    """
        Entrada: Entra el audio original, la frecuencia que contiene, el resultado obtenido luego de realizar 
        el analisis correspondiente y por utlimo tnemos que ingresamos le titulo que le colcoaremos al graficos
        que vamos a realizar.
        Procedimiento: Se encarga de realizar dos graficos en 1, Ademas, tenemos que grafica cada uno de los datos
        en el ambito de sus tranformadas de foruier para poder apreciar de mejor forma los resutlados que obtuvimos.
        Para luego pasar a guardar cada uno de los graficos que se realizaron en el archivo donde tenemos la salida
        de cada unon de los graficos que se generan.
        Salida: -
    """

    def generateGraphics10 (self, originalAudio,frecuencia,result,title):
        print("\n")
        print("Realizando el grafico de conjunto numero 10")
        print("El cual contiene los grafico de frecuencia de la señal moduladora (audio) y la señal portadora")
        print("\n")
        plt.figure(1)
        plt.subplot(211)
        p2 = plt.plot(linewidth = 1)
        trans1 = self.frequencyGraphic(originalAudio.data_array, originalAudio.sampling_rate, "Moduladora", 4, 3)
        plt.subplot(212)
        p2 = plt.plot(linewidth = 1)
        trans2 = self.frequencyGraphic(result, originalAudio.sampling_rate, "Modulacion FM", 4, 3)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/" + title  +".png")
        plt.show()
        # Realizando graficos indivuales
        trans1 = self.frequencyGraphic(originalAudio.data_array, originalAudio.sampling_rate, "Moduladora", 4, 3)
        plt.show()
        trans2 = self.frequencyGraphic(result, originalAudio.sampling_rate, "Modulacion FM", 4, 3)
        plt.show()


    """
        Entrada: Entra el titulo que le colocaremos al grafico a realizar,ademas de cada uno de los cosenos 
        que vamos a utilizat, la modulacion ask y el tiempo de esta y por ultimo tambien tebemos el tiempo
        que se encarga de poder graficar junto al coseno.
        Procedimiento: Se encarga de realizar tres graficos en 1. Donde ademas, tenemos que grafica cada una 
        de las señales que aprticipan en la modulacion digital ask, con el fin de apreciar cada uno de sus
        resultados. Para luego para a guardar cada uno de estos valores en la carptea donde tenemos las salida
        de cada uno de los graficos que son generados por le programa.
        Salida: -
    """

    def generateGraphics11 (self, title, cos1, cos2, askModulation,timeCos, timeModulation):
        print("\n")
        print("Realizando el grafico de conjunto numero 4")
        print("El cual contiene los grafico de tiempo de cada una de las señales ha analizar")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        self.makeGraphic("Señal Portadora 1","Tiempo",timeCos,"Amplitud",cos1,5,5)
        plt.subplot(312)
        self.makeGraphic("Señal Portadora 0","Tiempo",timeCos,"Amplitud",cos2,3,3)
        plt.subplot(313)
        self.makeGraphic("Señal Modulada","Tiempo",timeModulation,"Amplitud",askModulation,7,7)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/_" + title +".png")
        plt.show()
        # Realizando graficos individuales
        self.makeGraphic("Señal Moduladora", "Tiempo", timeCos, "Amplitud", cos1, 5, 5)
        plt.show()
        self.makeGraphic("Señal Portadora", "Tiempo", timeCos, "Amplitud", cos2, 3, 3)
        plt.show()
        self.makeGraphic("Señal Modulada", "Tiempo", timeModulation, "Amplitud", askModulation, 7, 7)
        plt.show()

    """
        Entrada: Entra el titulo que le colocaremos al grafico a realizar, ademas del tiempo de las señales 
        y cada uno de los datas de las funciones y ambien el ruido que colocamos a cada una de las funciones, 
        con el fin de poder simulador el ruido del medio donde vamos a transmitir en un futuro.
        Procedimiento: Se encarga de realizar tres graficos en 1. Donde tenemos que grafica la señal normal, es decir
        sin ruido, luego grafica el ruido que tnenemos que genetramos que es el ruido blanco gaussiano, ademas
        despyues de graficar la señal con el ruido includio. Donde por utlimo , tenemos que guarda cada uno de los
        graficos de forma indicual en la carpeta que tenemos donde guardamos las salidas de cada una de las funciones
        que tenemos implementadas que generan los disintos graifocs que itulizamos para analizare cada una de
        las modulaciones que realizamos.
        Salida: -
    """

    def generateGraphics12 (self,title,  time , function_1, function_2, noise):
        print("\n")
        print("Realizando el grafico de conjunto numero 4")
        print("El cual contiene los grafico de tiempo de cada una de las señales ha analizar")
        print("\n")
        plt.figure(1)
        plt.subplot(311)
        self.makeGraphic("Señal sin ruido","Tiempo",time ,"Amplitud",function_1,5,5)
        plt.subplot(312)
        self.makeGraphic("Ruido","Tiempo",time ,"Amplitud",noise,3,3)
        plt.subplot(313)
        self.makeGraphic("Señal con rudio","Tiempo",time ,"Amplitud",function_2,7,7)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/_" + title +".png")
        plt.show()
        # # Realizando graficos individuales
        self.makeGraphic("Señal sin ruido","Tiempo",time ,"Amplitud",function_1,5,5)
        plt.show()
        self.makeGraphic("Ruido","Tiempo",time ,"Amplitud",noise,3,3)
        plt.show()
        self.makeGraphic("Señal con rudio","Tiempo",time ,"Amplitud",function_2,7,7)
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
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: graphicCorr
    # - DESCRIPTION: Genera el grafico de un correlacionador
    # - PARAMS: Titulo del gráfico, frecuencia del correlacionador y el array de datos del correlacionador
    # - OUT: Void

    def graphicCorr(self, title, data):
        plt.title(title, fontsize=12, color='blue')
        plt.xlabel('Sample', color='red')
        plt.ylabel('Amplitude (dB)', color='orange')
        plt.grid()
        plt.plot(data)
        #plt.show()

    def graphicCorrAll(self, title, title1, title2, title3, corr0, corr1, corr2):
        plt.figure(1)
        plt.subplot(311)
        self.graphicCorr(title1, corr0)
        plt.subplot(312)
        self.graphicCorr(title2, corr1)
        plt.subplot(313)
        self.graphicCorr(title3, corr2)
        plt.tight_layout()
        plt.savefig(os.getcwd() + "/Salida/_" + title + ".png")
        plt.show()

        # # Realizando graficos individuales
        self.graphicCorr(title1, corr0)
        plt.show()
        self.graphicCorr(title2, corr1)
        plt.show()
        self.graphicCorr(title3, corr2)
        plt.show()




