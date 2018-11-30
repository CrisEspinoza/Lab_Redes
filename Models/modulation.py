from scipy.interpolate import interp1d
from Models.graphic import Graphic
from Models.audio import Audio
import numpy as np
from numpy import linspace, cos, interp
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import os

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

        graphic.generateGraphics4(modulation.function1, modulation.function2, modulation.function3, modulation.time)
        graphic.generateGraphics5(modulation.function1, modulation.freqSampling, modulation.function2, modulation.freqSampling, modulation.function3, modulation.time)

        return modulation

    def demodulatorAMCos(self, modulation):

        graphic = Graphic()
        dataCarrier = modulation.function3 * modulation.function2
        print(dataCarrier)

        modulation.function4 = dataCarrier
        audio = Audio(modulation.freqSampling, 0, dataCarrier, modulation.time, "demodulada", (modulation.freq2 + (modulation.freq2 / 2) ), 0, 8,modulation.time)

        graphic.generateGraphics4(modulation.function1, modulation.function3, dataCarrier, modulation.time)
        graphic.generateGraphics6(modulation,audio)

        return modulation

    def amModulation (self, modulatingSignal):

        graphic = Graphic()
        modulation = Modulation(1, 62500)
        modulation.freqSampling = 10000

        carrier_signal_time = linspace(0, modulatingSignal.duration, 250000 * modulatingSignal.duration)
        print(carrier_signal_time)
        modulation.time = carrier_signal_time

        new_data = interp(carrier_signal_time, modulatingSignal.time, modulatingSignal.data_array)
        print(new_data)
        modulation.function1 = new_data

        carrier_signal = cos(2 * np.pi * modulation.freqSampling * carrier_signal_time)
        modulation.function2 = carrier_signal

        modulated_signal = carrier_signal * new_data
        print(modulated_signal)
        modulation.function3 = modulated_signal

        graphic.generateGraphics4(carrier_signal, new_data, modulated_signal, carrier_signal_time)

        demodulated_signal = self.demodulatorAM(modulation)

        #print(demodulated_signal)

        #graphic.inverseGraphic(carrier_signal_time,demodulated_signal,"a",0,0)

        #graphic.generateGraphics4(carrier_signal, new_data, demodulated_signal, carrier_signal_time)

        #graphic.generateGraphics4(modulatingSignal, modulated_signal, demodulated_signal, carrier_signal_time)

        return modulation


    def demodulatorAM(self, modulation):
        graphic = Graphic()
        demoduleAM = modulation.function3 * modulation.function2
        print(demoduleAM)
        modulation.function4 = demoduleAM

        modulation.function4 = demoduleAM
        audio = Audio(modulation.freqSampling, 0, demoduleAM, modulation.time, "demodulada", 5000, 0, 8, modulation.time)

        graphic.generateGraphics4(modulation.function1, modulation.function3, demoduleAM, modulation.time)
        graphic.generateGraphics6(modulation, audio)

        return modulation


    def fmModulation (self, modulation, f, fc, k):

        graphic = Graphic()
        modulation.freqSampling = 18 * fc

        modulation.time = np.arange(0, 0.5, 1 / modulation.freqSampling)

        modulating_signal = np.cos(2 * np.pi * f * modulation.time)
        modulation.function1 = modulating_signal

        phase = k * (integrate.cumtrapz(modulation.function1, modulation.time, initial=0))
        print(phase)

        modulated_signal = np.cos( (2 * np.pi * fc * modulation.time) + phase)
        modulation.function3 = modulated_signal

        graphic.generateGraphics7(modulation)
        graphic.generateGraphics8(modulation)

        return modulation

    def fmModulationSound(self, originalAudio, k):
        graphic = Graphic()

        interp = interp1d(originalAudio.time, originalAudio.data_array)
        newTime = np.linspace(0, len(originalAudio.data_array) / originalAudio.sampling_rate,
                              len(originalAudio.data_array) * 10)
        newData = interp(newTime)

        newLen = len(newData)

        timesCarrier = linspace(0, len(originalAudio.data_array) / originalAudio.sampling_rate, newLen)
        #print(newLen)

        fc = 80000

        w = fc*timesCarrier

        integral = integrate.cumtrapz(newData, timesCarrier, initial=0)

        result = np.cos(2*np.pi * w + k * integral)
        # print(result)

        graphic.generateGraphics9(originalAudio,timesCarrier,result)
        graphic.generateGraphics10(originalAudio,fc,result)

        #plt.subplot(311)
        #plt.plot(originalAudio.time, originalAudio.data_array, linewidth=0.5)
        #plt.title("senal del mensaje")
        #plt.subplot(312)
        #plt.plot(timesCarrier, result, linewidth=0.5)
        #plt.title("modulacion fm")
        #plt.savefig(os.getcwd() + "/Salida/fmModulation.png")
        #plt.show()



