from scipy.interpolate import interp1d
from Models.graphic import Graphic
from Models.audio import Audio
from Models.archive import Archive
from Models.textToBinaries import TextoBinario
import numpy as np
from numpy import linspace, cos, interp, random, arange, pi
import time
import scipy.integrate as integrate
import scipy.signal as signal
import matplotlib.pyplot as plt
from numpy import arange
import os
import math
from scipy import signal
from cmd import Cmd
import matplotlib.pyplot as plt

class Modulation:

    ## - ATTRIBUTES - ##

    freq1 = 0
    freq2 = 0
    time = []
    function1 = []
    function2 = []
    function3 = []
    function4 = []
    freqSampling = 0
    audio = Audio(0,0,0,0,0,0,0,0,0,0)
    freqX = 250000
    ask_function1 = []
    ask_function2 = []
    ask_function3 = []
    ask_function4 = []
    ask_time1 = []
    ask_time2 = []
    ask_tb = 0
    ask_fs = 0
    ook_function1 = []
    ook_function2 = []
    ook_function3 = []
    ook_function4 = []
    ook_time1 = []
    ook_time2 = []
    ook_tb = 0
    ook_fs = 0
    fsk_function1 = []
    fsk_function2 = []
    fsk_function3 = []
    fsk_function4 = []
    fsk_time1 = []
    fsk_time2 = []
    fsk_tb = 0
    fsk_fs = 0
    fsk_array = []
    psk_function1 = []
    psk_function2 = []
    psk_function3 = []
    psk_function4 = []
    psk_time1 = []
    psk_time2 = []
    noise = []

    ## - FUNCTIONS - ##

    # CONSTRUCTOR////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, freq1, freq2):
        self.freq1 = freq1
        self.freq2 = freq2

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: amModulation
    # - DESCRIPTION: Funcion que realiza una modulación AM de ejemplo
    # - PARAMS: Frecuencia de la funcion a modular y frecuencia del carrier
    # - OUT: Objeto de tipo modulation, que contiene todas las funciones creadas en esta función

    def amModulationCos (self, f, fc):

        graphic = Graphic()
        modulation = Modulation(f,fc)
        modulation.freqSampling = 18*fc

        modulation.time = np.arange(0,2,1/modulation.freqSampling)

        modulation.function1 = np.cos(2*np.pi*f*modulation.time)  #Funcion coseno de ejemplo para modular
        modulation.function2 = np.cos(2*np.pi*fc*modulation.time) #Funcion que modula por amplitud
        modulation.function3 = modulation.function1 * modulation.function2 #Función modulada

        graphic.generateGraphics4(modulation.function1, modulation.function2, modulation.function3, modulation.time,"Grafico de tiempo de señal modulada de Cosenos")
        graphic.generateGraphics5(modulation.function1, modulation.function2, modulation.function3, modulation.freqSampling, "Grafico de Transformada de señal modulada de Cosenos")

        return modulation

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: demodulatorAMCos
    # - DESCRIPTION: Funcion que realiza el proceso de demodulación para la fución coseno de ejemplo
    # - PARAMS: Objeto de tipo modulation, que contiene la función a demodular
    # - OUT: Objeto de tipo modulation, que contiene la función demodulada

    def demodulatorAMCos(self, modulation):

        graphic = Graphic()
        dataCarrier = modulation.function3 * modulation.function2
        print(dataCarrier)

        modulation.function4 = dataCarrier
        audio = Audio(modulation.freqSampling, 0,0, dataCarrier, dataCarrier, modulation.time, modulation.audio.audio_name, (modulation.freq2 + (modulation.freq2 / 2)), 0, 8)

        graphic.generateGraphics4(modulation.function1, modulation.function3, dataCarrier, modulation.time,"Grafico de tiempo de Cosenos de señal demodulada")
        graphic.generateGraphics6(modulation, audio, "Grafico de Transformada de Cosenos de señal demodulada")

        return modulation

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: amModulation
    # - DESCRIPTION: Funcion que realiza el proceso de modulación AM de un audio
    # - PARAMS: La señal a modular
    # - OUT: Objeto de tipo modulation que contiene la señal, el carrier y la función modulada

    def amModulation (self, modulatingSignal):

        graphic = Graphic()
        modulation = Modulation(0, 1000)
        modulation.freqSampling = 18 * modulation.freq2
        modulation.audio = modulatingSignal

        #print("El largo del audio es: " + str(len(modulatingSignal.data_array)))

        carrier_signal_time = linspace(0, modulatingSignal.duration, modulation.freqX*modulatingSignal.duration)
        #print(carrier_signal_time)
        #print ( "El largo es: " + str(len(carrier_signal_time) ))
        modulation.time = carrier_signal_time

        new_data = interp(carrier_signal_time, modulatingSignal.time, modulatingSignal.data_array)
        #print(new_data)
        #print("El largo de la new_data es: "+ str(len(new_data)))
        modulation.function1 = new_data

        carrier_signal = cos(2 * np.pi * modulation.freqSampling * carrier_signal_time)
        modulation.function2 = carrier_signal

        modulated_signal = carrier_signal * new_data
        #print(modulated_signal)
        #print("El largo de la new_data es: "+ str(len(modulated_signal)))
        modulation.function3 = modulated_signal

        graphic.generateGraphics4(modulation.function1,modulation.function2,modulation.function3, modulation.time, modulation.audio.audio_name)
        #  (Descomentar despues se demora)
        graphic.generateGraphics5(modulation.function1, modulation.function2, modulation.function3, modulation.freqSampling, "Grafico de tranformada de fourier de señal modulada de audio " + modulation.audio.audio_name)

        return modulation

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: demodulatorAM
    # - DESCRIPTION: Funcion que realiza el proceso de demodulación para cualquier función modulada por amplitud
    # - PARAMS: Objeto de tipo modulation, que contiene la función a demodular
    # - OUT: Objeto de tipo modulation, que contiene la función demodulada

    def demodulatorAM(self, modulation):

        graphic = Graphic()
        demoduleAM = modulation.function3 * modulation.function2
        #print(demoduleAM)
        modulation.function4 = demoduleAM
        audio = Audio(modulation.freqSampling, 0,0, demoduleAM, demoduleAM, modulation.time, modulation.audio.audio_name, 5 * modulation.freq2 , 0, 8)
        #graphic.generateGraphics4(modulation.function1, modulation.function3, demoduleAM, modulation.time, "Grafico de tiempo de señal demodulada de audio" + modulation.audio.audio_name)
        graphic.generateGraphics6(modulation, audio, "Grafico de transformada de fourier de señal demodulada de audio" + modulation.audio.audio_name)
        newDemo = interp(modulation.audio.time, modulation.time, demoduleAM)
        #print(newDemo)
        archive = Archive(0)
        archive.saveWav(os.getcwd() + "/Audios/AudiosDemodulado/_"+ modulation.audio.audio_name +".wav", modulation.audio.sampling_rate, newDemo)

        return modulation

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: fmModulation
    # - DESCRIPTION: Funcion que realiza el proceso de modulación por frecuencia para una función coseno de ejemplo
    # - PARAMS: Objeto de tipo modulation, frecuencia de la función de ejemplo, la frecuencia de la nueva función modulada y un parametro k
    # - OUT: Objeto de tipo modulation, que contiene la función modulada

    def fmModulation (self, modulation, f, fc, k):

        graphic = Graphic()
        modulation.freq1 = f
        modulation.freqSampling = 18 * fc
        modulation.time = np.arange(0, 0.5, 1 / modulation.freqSampling)
        modulating_signal = np.cos(2 * np.pi * f * modulation.time)
        modulation.function1 = modulating_signal
        phase = k * (integrate.cumtrapz(modulation.function1, modulation.time, initial=0))
        print(phase)
        modulated_signal = np.cos((2 * np.pi * fc * modulation.time) + phase)
        modulation.function3 = modulated_signal
        graphic.generateGraphics7(modulation, "Grafico de tiempo de modulacion FM de cosenos")
        graphic.generateGraphics8(modulation, "Grafico de frecuencia de modulacion FM de cosenos")
        return modulation

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: fmModulationSound
    # - DESCRIPTION: Funcion que realiza el proceso de modulación por frecuencia para un audio
    # - PARAMS: Objeto de tipo modulation, frecuencia de la función de ejemplo, la frecuencia de la nueva función modulada y un parametro k
    # - OUT: Objeto de tipo modulation, que contiene la función modulada

    def fmModulationSound(self, originalAudio, k, modulation):
        graphic = Graphic()

        interp = interp1d(originalAudio.time, originalAudio.data_array)
        newTime = np.linspace(0, len(originalAudio.data_array) / originalAudio.sampling_rate,len(originalAudio.data_array) * 10)
        newData = interp(newTime)
        newLen = len(newData)
        timesCarrier = linspace(0, len(originalAudio.data_array) / originalAudio.sampling_rate, newLen)
        #print(newLen)
        fc = 0.7*originalAudio.sampling_rate
        w = fc*timesCarrier
        integral = integrate.cumtrapz(newData, timesCarrier, initial=0)
        result = np.cos(2*np.pi * w + k * integral)
        # print(result)
        modulation.function1 = newData
        modulation.function4 = result
        modulation.time = newTime
        modulation.freq1 = fc
        modulation.audio = originalAudio

        graphic.generateGraphics9(newData,timesCarrier,result, "Grafico de tiempo de modulacion FM de audio " + modulation.audio.audio_name)
        graphic.generateGraphics10(originalAudio,fc,result, "Grafico de frecuencia de modulacion FM de audio " + modulation.audio.audio_name)

        return modulation

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: generateCarrierSignalAM
    # - DESCRIPTION: Funcion que genera una función carrier
    # - PARAMS: frecuencia del carrier, frecuencia de muestreo, tiempo de bit
    # - OUT: arreglo de datos para el tiempo de bit y la señal carrier

    def generateCarrierSignalAm(self, fr, rate, bit_time):
        tb = arange(0, bit_time, 1 / rate)
        #tb = linspace(0,(bit_time*100),rate/(bit_time*100))
        carrier = cos(2 * pi * fr * tb)
        return tb, carrier

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: askModulation
    # - DESCRIPTION: Funcion que realiza el proceso de modulación ask para un arreglo de bits (0 y 1)
    # - PARAMS: Objeto de tipo modulation
    # - OUT: Objeto de tipo modulation, que contiene la función modulada

    def askModulation(self, modulation):

        x = [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1]

        f = 7000 # hertz -> Frecuencia con la que la vamos a probar
        bit_time = 0.5 # tasa de bits por segundo
        rate = 44100 # Frecuencia de muestreo ( Audio)

        len_signal = len(modulation.ask_function4)

        t , carrier_signal = self.generateCarrierSignalAm(f, rate, bit_time)

        #t1 = linspace(0, bit_time * 100, rate / (bit_time * 100 ))  # vector de tiempo de 1 bit

        amplitud1 = input("Ingrese la amplitud numero 1: ")
        amplitud2 = input("Ingrese la amplitud numero 2: ")

        c1 = (int(amplitud1) * carrier_signal) #funcion que representa los 1
        c2 = (int(amplitud2) * carrier_signal) #funcion que representa los 0

        #Arreglo que guardara los datos de las funciones
        y = []
        for bit in x:
            if bit == 1:
                y.extend(c1)
            else:
                y.extend(c2)

        y = np.array(y)
        t = np.array(t)
        x = linspace(0, bit_time, int(len(t)) * len(x))

        archive = Archive(0)
        # Realizando el audio de salida
        name = "audio"
        archive.saveWav(os.getcwd() + "/Audios/AudiosModulados/" + name + "_ask.wav",rate,y)

        #Realizando el grafico
        graphic = Graphic()
        graphic.generateGraphics11("Modulacion ask", c1, c2, y, t, x)

        #Datos necesarios a guardar
        modulation.ask_function1 = np.array(c1)
        modulation.ask_function2 = np.array(c2)
        modulation.ask_function3 = y
        modulation.ask_time1 = t
        modulation.ask_time2 = x
        modulation.ask_fs = rate
        modulation.ask_tb = bit_time
        return modulation

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: demodulationASK
    # - DESCRIPTION: Funcion que realiza el proceso de demodulación ask
    # - PARAMS: Objeto de tipo modulation
    # - OUT: Arreglo de bit rescatados de la función modulada

    def demoulationASK(self,modulation):
        graphic = Graphic()

        c2 = modulation.ask_function1
        c1 = modulation.ask_function2
        ask_signal = modulation.ask_function4
        corr0 = signal.fftconvolve(ask_signal, c1, 'same')
        corr1 = signal.fftconvolve(ask_signal, c2, 'same')

        corr0 = modulation.windows_rms(corr0, 101)
        corr1 = modulation.windows_rms(corr1, 101)

        """
        plt.figure(1)
        plt.subplot(211)
        # plt.title("Sonido Original")
        plt.plot(corr0)
        plt.subplot(212)
        # plt.title("Sonido aplicadando transformada")
        plt.plot(corr1)
        plt.show()
        """

        maxCorre = max(corr1)
        minCorre = min(corr1)
        prom = (maxCorre - minCorre) / 2
        print(minCorre)
        print(maxCorre)

        bit_position = arange(modulation.ask_fs * modulation.ask_tb / 2, len(ask_signal), modulation.ask_fs * modulation.ask_tb).astype(int)

        bit_array = []
        for position in bit_position:
            print( prom )
            if corr1[position] > prom :
                bit_array.append(1)
            else:
                bit_array.append(0)

        title1 = 'Correlator 0'
        title2 = 'Correlator 1'
        graphic.graphicCorr(title1, 44100, corr0)
        graphic.graphicCorr(title2, 44100, corr1)

        print(bit_array)
        return bit_array

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: 00kModulation
    # - DESCRIPTION: Funcion que realiza el proceso de modulación ook para un arreglo de bits (0 y 1)
    # - PARAMS: Objeto de tipo modulation
    # - OUT: Objeto de tipo modulation, que contiene la función modulada

    def ookModulation(self, modulation):

        x = [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1]

        f = 7000 # hertz -> Frecuencia con la que la vamos a probar
        bit_time = 0.5 # Cantidad de bit por segundo
        rate = 44100 # Frecuencia de muestreo ( Audio)

        len_signal = len(modulation.ook_function4)

        t , carrier_signal = self.generateCarrierSignalAm(f, rate, bit_time)

        #t1 = linspace(0, bit_time * 100, rate / (bit_time * 100 ))  # vector de tiempo de 1 bit

        amplitud1 = input("Ingrese la amplitud numero 1: ")

        c1 = (int(amplitud1) * carrier_signal) #Funcion que representa los bits 1, con una amplitud dada
        c2 = (0*carrier_signal) #Función que representa los bits 0, con una amplitud 0

        y = []
        for bit in x:
            if bit == 1:
                y.extend(c1)
            else:
                y.extend(c2)


        y = np.array(y)
        t = np.array(t)
        x = linspace(0, bit_time, int(len(t)) * len(x))

        archive = Archive(0)
        # Realizando el audio de salida
        name = "audio"
        archive.saveWav(os.getcwd() + "/Audios/AudiosModulados/" + name + "_ook.wav",rate,y)

        #Realizando el grafico
        graphic = Graphic()
        graphic.generateGraphics11("Modulacion ook", c1, c2, y, t, x)

        modulation.ook_function1 = np.array(c1)
        modulation.ook_function2 = np.array(c2)
        modulation.ook_function3 = y
        modulation.ook_time1 = t
        modulation.ook_time2 = x
        modulation.ook_fs = rate
        modulation.ook_tb = bit_time

        return modulation

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: demodulationOOK
    # - DESCRIPTION: Funcion que realiza el proceso de demodulación ook
    # - PARAMS: Objeto de tipo modulation
    # - OUT: Arreglo de bit rescatados de la función modulada

    def demoulationOOK(self,modulation):

        graphic = Graphic()

        c2 = modulation.ook_function1
        c1 = modulation.ook_function2
        ook_signal = modulation.ook_function4
        corr0 = signal.fftconvolve(ook_signal, c1, 'same')
        corr1 = signal.fftconvolve(ook_signal, c2, 'same')

        corr0 = modulation.windows_rms(corr0, 101)
        corr1 = modulation.windows_rms(corr1, 101)

        maxCorre = max(corr1)
        minCorre = min(corr1)
        prom = (maxCorre - minCorre) / 2
        print(minCorre)
        print(maxCorre)

        bit_position = arange(modulation.ook_fs * modulation.ook_tb / 2, len(ook_signal), modulation.ook_fs * modulation.ook_tb).astype(int)

        bit_array = []
        for position in bit_position:
            print( prom )
            if corr1[position] > prom :
                bit_array.append(1)
            else:
                bit_array.append(0)

        title1 = 'Correlator 0'
        title2 = 'Correlator 1'
        graphic.graphicCorr(title1, 44100, corr0)
        graphic.graphicCorr(title2, 44100, corr1)

        print(bit_array)
        return bit_array

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: fskModulationm
    # - DESCRIPTION: Funcion que realiza el proceso de modulación fsk para un arreglo de bits (0 y 1) que representa un textp
    # - PARAMS: Objeto de tipo modulation
    # - OUT: Objeto de tipo modulation, que contiene la función modulada

    def fskModulation(self,modulation):

        #x = [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1]

        text = TextoBinario()
        text1 = input("Ingrese el texto a binarizar")
        a = text.do_codificar(text,text1) #Función que transforma texto en binario
        print(a)
        x = a

        #frecuencia = input("Ingrese la frecuencia a utilizar: ")
        #fc = frecuencia

        fc = 18000 # hertz
        tb = 760 # bit por segundo
        #fs = 4.5 * fc # FRECUENCIA DE MUESTREO
        fs = 44100
        t = linspace(0, 1 / tb, fs/tb ) # vector de tiempo de 1 bit

        amplitud = input("Ingrese la amplitud a utilizar: ")

        c1 = float(amplitud) * np.cos(2 * np.pi * fc/4 * t) #Función que representa los bist 0, con una frecuencia1 dada
        c2 = float(amplitud) * np.cos(2 * np.pi * fc * t)   #Función que representa los bist 1, con una frecuencia2 dada
        y = []

        for b in x:
            if b:
                y.extend(c1)
            else:
                y.extend(c2)

        y = np.array(y)
        t = np.array(t)
        x = linspace(0, 1/tb, int(len(t)) * len(x))

        archive = Archive(0)
        # Realizando el audio de salida
        name = "audio"
        archive.saveWav(os.getcwd() + "/Audios/AudiosModulados/" + name + "_fsk.wav",int(fs),y)

        #Realizando el grafico
        graphic = Graphic()
        graphic.generateGraphics11("Modulacion fsk",c1,c2,y,t,x)

        modulation.fsk_function1 = c1
        modulation.fsk_function2 = c2
        modulation.fsk_function3 = y
        modulation.fsk_time1 = t
        modulation.fsk_time2 = x
        modulation.fsk_array = a
        modulation.fsk_tb = 1/tb
        modulation.fsk_fs = fs

        print(y)

        return modulation

    # - NAME: pskModulationm
    # - DESCRIPTION: Funcion que realiza el proceso de modulación psk para un arreglo de bits (0 y 1) que representa un texto
    # - PARAMS: Objeto de tipo modulation
    # - OUT: Objeto de tipo modulation, que contiene la función modulada

    def pskModulation(self,modulation):

        #x = [0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1]

        text = TextoBinario()
        text1 = input("Ingrese el texto a binarizar")
        a = text.do_codificar(text, text1)
        print(a)

        #print(len(modulation.audio.data_array))

        # for i in modulation.audio.data_array:
        #    print(i)
        archive = Archive(0)
        #x1 = archive.openWav("ook")

        x = a

        #frecuencia = input("Ingrese la frecuencia a utilizar: ")
        #fc = frecuencia

        fc = 500000 # her
        tb = 10000 # bit por segundo
        fs = 12.5 * fc # FRECUENCIA DE MUESTREO
        t = linspace(0, 1 / tb, fs/tb ) # vector de tiempo de 1 bit

        amplitud = input("Ingrese amplitud a utilizar: ")
        grados = input("Ingrese fase a desfasar (en grados [0 - 90]) : ")

        phase = float(math.radians(int(grados)))

        c1 = float(amplitud) * np.cos(2 * np.pi * fc * t)
        c2 = float(amplitud) * np.cos( (2 * np.pi * fc * t) + phase)
        y = []

        for b in x:
            if b:
                y.extend(c1)
            else:
                y.extend(c2)

        y = np.array(y)
        t = np.array(t)
        x = linspace(0, 1/tb, int(len(t)) * len(x))

        archive = Archive(0)
        # Realizando el audio de salida
        name = "audio"
        archive.saveWav(os.getcwd() + "/Audios/AudiosModulados/" + name + "_psk.wav",int(fs),y)

        #Realizando el grafico
        graphic = Graphic()
        graphic.generateGraphics11("Modulacion psk",c1,c2,y,t,x)

        modulation.psk_function1 = c1
        modulation.psk_function2 = c2
        modulation.psk_function3 = y
        modulation.psk_time1 = t
        modulation.psk_time2 = x
        modulation.psk_array = a
        modulation.psk_tb = 1/tb
        modulation.psk_fs = fs

        return modulation

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: DemodulatorFsk
    # - DESCRIPTION: Funcion que realiza el proceso de demodulación fsk que utiliza dos correlacionadores
    # - PARAMS: Objeto de tipo modulation
    # - OUT: Arreglo de bit rescatados de la función modulada

    def DemulatorFsk(self, modulation):
        graphic = Graphic()

        c2 = modulation.fsk_function1
        c1 = modulation.fsk_function2
        fsk_signal = modulation.fsk_function4

        #Se crean los correlacionadores
        corr0 = signal.fftconvolve(fsk_signal, c1, 'same')
        corr1 = signal.fftconvolve(fsk_signal, c2, 'same')

        t1 = time.time()

        #Filtro para los correlacionadores
        corr0 = modulation.windows_rms(corr0, 101)
        corr1 = modulation.windows_rms(corr1, 101)

        #corr0 = np.abs(corr0)
        #corr1 = np.abs(corr1)

        t2 = time.time()

        #print("TIME: ", t2 - t1)

        #Posiciones donde termina le tiempo de bits para determinar el tipo de bits
        bit_position = arange(modulation.fsk_fs * modulation.fsk_tb / 2, len(fsk_signal), modulation.fsk_fs * modulation.fsk_tb).astype(int)

        print(str(len(bit_position)))

        bit_array = []
        for position in bit_position:
            if corr0[position] < corr1[position]:
                bit_array.append(1)
            else:
                bit_array.append(0)

        title1 = 'Correlator 0'
        title2 = 'Correlator 1'
        graphic.graphicCorr(title1, 44100, corr0)
        graphic.graphicCorr(title2, 44100, corr1)

        print(bit_array)
        print("EL largo es: " + str(len(bit_array)))
        print("EL largo es: " + str(len(modulation.fsk_array)))
        con = 0
        for i in range(0,len(bit_array)):
            if (bit_array[i] != modulation.fsk_array[i]):
                #print("malo ")
                con = con + 1
                #print (" antes: " + str(modulation.fsk_array[i]) + " - ahora: " + str(bit_array[i]) + " \n")
        print(con)

        d = []
        i = 0
        j = 0
        while i < len(bit_array):
            binaries = ""
            while j < 8:
                print("x1 = " + str(len(bit_array))+ " - x2 : " + str(i))
                binaries = binaries + str(bit_array[i])
                j = j + 1
                i = i + 1
            d.append(binaries)
            binaries = ""
            j = 0

        text = TextoBinario()
        textFinaly = ""
        print(d)
        for i in d:
            print(i)
            aux = text.do_decodificar(text,i)
            print(aux)
            textFinaly = textFinaly + str(aux)
            print("\n")

        print(textFinaly)

        return bit_array

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: DemodulatorPsk
    # - DESCRIPTION: Funcion que realiza el proceso de demodulación psk que utiliza dos correlacionadores
    # - PARAMS: Objeto de tipo modulation
    # - OUT: Arreglo de bit rescatados de la función modulada

    def DemulatorPsk(self, modulation):
        graphic = Graphic()

        c2 = modulation.psk_function1
        c1 = modulation.psk_function2
        psk_signal = modulation.psk_function4
        corr0 = signal.fftconvolve(psk_signal, c1, 'same')
        corr1 = signal.fftconvolve(psk_signal, c2, 'same')

        t1 = time.time()

        corr0 = modulation.windows_rms(corr0, 101)
        corr1 = modulation.windows_rms(corr1, 101)

        t2 = time.time()

        #print("TIME: ", t2 - t1)

        bit_position = arange(modulation.psk_fs * modulation.psk_tb / 2, len(psk_signal), modulation.psk_fs * modulation.psk_tb).astype(int)

        #print(bit_position)

        bit_array = []
        for position in bit_position:
            if corr0[position] < corr1[position]:
                bit_array.append(1)
            else:
                bit_array.append(0)

        title1 = 'Correlator 0'
        title2 = 'Correlator 1'
        graphic.graphicCorr(title1, 44100, corr0)
        graphic.graphicCorr(title2, 44100, corr1)

        print(bit_array)
        print("EL largo es: " + str(len(bit_array)))
        print("EL largo es: " + str(len(modulation.psk_array)))
        con = 0
        for i in bit_array:
            if (bit_array[i] != modulation.psk_array[i]):
                #print("malo ")
                con = con + 1
                #print (" antes: " + str(modulation.psk_array[i]) + " - ahora: " + str(bit_array[i]) + " \n")
        print(con)

        d = []
        i = 0
        j = 0
        while i < len(bit_array):
            binaries = ""
            while j < 8:
                binaries = binaries + str(bit_array[i])
                j = j + 1
                i = i + 1
            d.append(binaries)
            binaries = ""
            j = 0

        text = TextoBinario()
        textFinaly = ""
        for i in d:
            print(i)
            aux = text.do_decodificar(text, str(i))
            textFinaly = textFinaly + str(aux)
            print("\n")

        print(textFinaly)

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: windows_rms
    # - DESCRIPTION: Funcion que aplica el filtro a los correlaciondores determinando la media cuadratica
    # - PARAMS: correlacionador, valor constante
    # - OUT: correlacionador filtrado

    def windows_rms(self, corr, windowssize):
        corr2 = np.power(corr, 2)
        window = np.ones(windowssize)/float(windowssize)
        raiz = np.sqrt(np.convolve(corr2, window, mode='same'))
        return raiz

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: addNoise
    # - DESCRIPTION: Funcion que aplica ruido blanco gaussiano a una función modulada, para simular un medio real
    # - PARAMS: señal modulada
    # - OUT: señal con ruidio, el ruido

    def addNoise(self,signal):

        noise = random.normal(0.0, 0.1, len(signal))
        signal = signal + noise
        return np.array(signal), np.array(noise)


