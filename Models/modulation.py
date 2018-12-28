from scipy.interpolate import interp1d
from Models.graphic import Graphic
from Models.audio import Audio
from Models.archive import Archive
import numpy as np
from numpy import linspace, cos, interp, random
import scipy.integrate as integrate
import os
import math
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
    fsk_function1 = []
    fsk_function2 = []
    fsk_function3 = []
    fsk_function4 = []
    fsk_time1 = []
    fsk_time2 = []
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
        graphic.generateGraphics5(modulation.function1, modulation.function2, modulation.function3, modulation.freqSampling, modulation.audio.audio_name)

        return modulation


    def demodulatorAM(self, modulation):

        graphic = Graphic()
        demoduleAM = modulation.function3 * modulation.function2
        #print(demoduleAM)

        modulation.function4 = demoduleAM
        audio = Audio(modulation.freqSampling,0, 0, demoduleAM, demoduleAM, modulation.time, modulation.audio.audio_name, (modulation.freq2 + (modulation.freq2/2) ), 0, 8)

        graphic.generateGraphics4(modulation.function1, modulation.function3, demoduleAM, modulation.time, "Grafico de tiempo de señal demodulada de audio" + modulation.audio.audio_name)
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

    def askModulation(self,modulation):

        x = [0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1]

        #frecuencia = input("Ingrese la frecuencia a utilizar")
        #fc = frecuencia

        fc = 1000 # herz
        tb = 10 # bit por segundo
        fs = 4.5 * fc # FRECUENCIA DE MUESTREO
        t = linspace(0, 1 / tb, fs/tb ) # vector de tiempo de 1 bit

        amplitud1 = input("Ingrese la amplitud numero 1: ")
        amplitud2 = input("Ingrese la amplitud numero 2: ")

        c1 = float(amplitud1) * np.cos(2 * np.pi * fc * t)
        c2 = float(amplitud2) * np.cos(2 * np.pi * fc * t)

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
        archive.saveWav(os.getcwd() + "/Audios/AudiosModulados/" + name + "_ask.wav",int(fs),y)

        #Realizando el grafico
        graphic = Graphic()
        graphic.generateGraphics11("Modulacion ask",c1,c2,y,t,x)

        modulation.ask_function1 = c1
        modulation.ask_function2 = c2
        modulation.ask_function3 = y
        modulation.ask_time1 = t
        modulation.ask_time2 = x

        return modulation

    def fskModulation(self,modulation):

        x = [0, 1, 0, 0, 1, 0, 1, 0, 0, 1,0, 1, 0, 0, 1, 0, 1, 0, 0, 1,0, 1, 0, 0, 1, 0, 1, 0, 0, 1]

        #frecuencia = input("Ingrese la frecuencia a utilizar: ")
        #fc = frecuencia

        fc = 1000 # her
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

    def addNoise(self,signal):

        noise = random.normal(0.0, 1.6, len(signal))
        signal = signal + noise
        return signal, noise











