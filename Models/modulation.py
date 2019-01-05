from scipy.interpolate import interp1d
from Models.graphic import Graphic
from Models.audio import Audio
from Models.archive import Archive
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
    fsk_function1 = []
    fsk_function2 = []
    fsk_function3 = []
    fsk_function4 = []
    fsk_time1 = []
    fsk_time2 = []
    fsk_tb = 0
    fsk_fs = 0
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

    def amModulationCos (self, f, fc):

        graphic = Graphic()
        modulation = Modulation(f,fc)
        modulation.freqSampling = 18*fc

        modulation.time = np.arange(0,2,1/modulation.freqSampling)

        modulation.function1 = np.cos(2*np.pi*f*modulation.time)
        modulation.function2 = np.cos(2*np.pi*fc*modulation.time)
        modulation.function3 = modulation.function1 * modulation.function2

        graphic.generateGraphics4(modulation.function1, modulation.function2, modulation.function3, modulation.time,"Grafico de tiempo de señal modulada de Cosenos")
        graphic.generateGraphics5(modulation.function1, modulation.function2, modulation.function3, modulation.freqSampling, "Grafico de Transformada de señal modulada de Cosenos")

        return modulation

    def demodulatorAMCos(self, modulation):

        graphic = Graphic()
        dataCarrier = modulation.function3 * modulation.function2
        print(dataCarrier)

        modulation.function4 = dataCarrier
        audio = Audio(modulation.freqSampling, 0,0, dataCarrier, dataCarrier, modulation.time, modulation.audio.audio_name, (modulation.freq2 + (modulation.freq2 / 2)), 0, 8)

        graphic.generateGraphics4(modulation.function1, modulation.function3, dataCarrier, modulation.time,"Grafico de tiempo de Cosenos de señal demodulada")
        graphic.generateGraphics6(modulation, audio, "Grafico de Transformada de Cosenos de señal demodulada")

        return modulation

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

    def generateCarrierSignalAm(self, fr, rate, bit_time):
        tb = arange(0, bit_time, 1 / rate)
        #tb = linspace(0,(bit_time*100),rate/(bit_time*100))
        carrier = cos(2 * pi * fr * tb)
        return tb, carrier

    def askModulation(self, modulation):

        x = [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1]

        f = 7000 # herz -> Frecuencia con la que la vamos a probar
        bit_time = 0.5 # Cantidad de bit por segundo
        rate = 44100 # Frecuencia de muestreo ( Audio)

        len_signal = len(modulation.ask_function4)

        t , carrier_signal = self.generateCarrierSignalAm(f, rate, bit_time)

        #t1 = linspace(0, bit_time * 100, rate / (bit_time * 100 ))  # vector de tiempo de 1 bit

        amplitud1 = input("Ingrese la amplitud numero 1: ")
        amplitud2 = input("Ingrese la amplitud numero 2: ")

        c1 = ( int (amplitud1) * carrier_signal) / rate
        c2 = ( int (amplitud2) * carrier_signal) / rate

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

        modulation.ask_function1 = np.array(c1)
        modulation.ask_function2 = np.array(c2)
        modulation.ask_function3 = y
        modulation.ask_time1 = t
        modulation.ask_time2 = x
        modulation.ask_fs = rate
        modulation.ask_tb = bit_time


        return modulation

    def demoulationASK(self,modulation):

        graphic = Graphic()

        c2 = modulation.ask_function1
        c1 = modulation.ask_function2
        ask_signal = modulation.ask_function4
        corr0 = signal.fftconvolve(ask_signal, c1, 'same')
        corr1 = signal.fftconvolve(ask_signal, c2, 'same')

        corr0 = modulation.windows_rms(corr0, 101)
        corr1 = modulation.windows_rms(corr1, 101)

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

    def fskModulation(self,modulation):

        x = [0, 1, 0, 0, 1, 0, 1, 0, 0, 1,0, 1, 0, 0, 1, 0, 1, 0, 0, 1,0, 1, 0, 0, 1, 0, 1, 0, 0, 1]

        #frecuencia = input("Ingrese la frecuencia a utilizar: ")
        #fc = frecuencia

        fc = 1000 # hertz
        tb = 10 # bit por segundo
        fs = 4.5 * fc # FRECUENCIA DE MUESTREO
        t = linspace(0, 1 / tb, fs/tb ) # vector de tiempo de 1 bit

        amplitud = input("Ingrese la amplitud a utilizar: ")

        c1 = float(amplitud) * np.cos(2 * np.pi * fc/2 * t)
        c2 = float(amplitud) * np.cos(2 * np.pi * fc * t)
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
        archive.saveWav(os.getcwd() + "/Audios/AudiosModulados/"+ name + "_fsk.wav",int(fs),y)

        #Realizando el grafico
        graphic = Graphic()
        graphic.generateGraphics11("Modulacion fsk",c1,c2,y,t,x)

        modulation.fsk_function1 = c1
        modulation.fsk_function2 = c2
        modulation.fsk_function3 = y
        modulation.fsk_time1 = t
        modulation.fsk_time2 = x
        modulation.fsk_tb = 1/tb
        modulation.fsk_fs = fs

        return modulation


    def pskModulation(self,modulation):

        x = [0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1]

        #frecuencia = input("Ingrese la frecuencia a utilizar: ")
        #fc = frecuencia

        fc = 1000 # her
        tb = 10 # bit por segundo
        fs = 4.5 * fc # FRECUENCIA DE MUESTREO
        t = linspace(0, 1 / tb, fs/tb ) # vector de tiempo de 1 bit

        amplitud = input("Ingrese amplitud a utilizar: ")
        grados = input("Ingrese fase a desfasar (en grados) : ")

        phase = float(math.radians(int(grados)))

        c1 = float(amplitud) * np.cos(2 * np.pi * fc/2 * t)
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

        return modulation

    def DemulatorFsk(self, modulation):
        graphic = Graphic()

        c2 = modulation.fsk_function1
        c1 = modulation.fsk_function2
        fsk_signal = modulation.fsk_function4
        corr0 = signal.fftconvolve(fsk_signal, c1, 'same')
        corr1 = signal.fftconvolve(fsk_signal, c2, 'same')

        t1 = time.time()

        corr0 = modulation.windows_rms(corr0, 101)
        corr1 = modulation.windows_rms(corr1, 101)

        t2 = time.time()

        #print("TIME: ", t2 - t1)

        bit_position = arange(modulation.fsk_fs * modulation.fsk_tb / 2, len(fsk_signal), modulation.fsk_fs * modulation.fsk_tb).astype(int)

        #print(bit_position)

        bit_array = []
        for position in bit_position:
            if corr0[position] < corr1[position]:
                bit_array.append(1)
            else:
                bit_array.append(0)

        title1 = 'Correlator 0'
        title2 = 'Correlator 1'
        #graphic.graphicCorr(title1, 44100, corr0)
        #graphic.graphicCorr(title2, 44100, corr1)

        print(bit_array)
        return bit_array

    def windows_rms(self, corr, windowssize):
        corr2 = np.power(corr, 2)
        window = np.ones(windowssize)/float(windowssize)
        raiz = np.sqrt(np.convolve(corr2, window, mode='valid'))
        return raiz


    def addNoise(self,signal):

        noise = random.normal(0.0, 0.00001, len(signal))
        signal = signal + noise
        return np.array(noise + signal), np.array(noise)


