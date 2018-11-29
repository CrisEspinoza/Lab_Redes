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
    function1 = 0
    function2 = 0
    function3 = 0
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

        self.demodulatorAMCos(modulation)

        graphic.generateGraphics4(modulation.function1, modulation.function2, modulation.function3, modulation.time)
        graphic.generateGraphics5(modulation.function1, modulation.freqSampling, modulation.function2, modulation.freqSampling, modulation.function3, modulation.time)

    def amModulation (self, modulatingSignal, carrierSignalFequency, lowCutoff):

        graphic = Graphic()
        carrier_signal_time = linspace(0, modulatingSignal.duration, 250000 * modulatingSignal.duration)
        print(carrier_signal_time)
        new_data = interp(carrier_signal_time, modulatingSignal.time, modulatingSignal.data_array)
        print(new_data)
        carrier_signal = cos(2 * np.pi * 62500 * carrier_signal_time)
        modulated_signal = carrier_signal * new_data
        print(modulated_signal)

        graphic.generateGraphics4(carrier_signal, new_data, modulated_signal, carrier_signal_time)

        demodulated_signal = self.amDemodulation(modulated_signal, modulatingSignal.duration)

        print(demodulated_signal)

        graphic.inverseGraphic(carrier_signal_time,demodulated_signal,"a",0,0)

        graphic.generateGraphics4(carrier_signal, new_data, demodulated_signal, carrier_signal_time)

        graphic.generateGraphics4(modulatingSignal, modulated_signal, demodulated_signal, carrier_signal_time)


    def amDemodulation (self, modulatedSignal, lowCutoff, order, ):

        return

    def demodulatorAM(self, AM, totalTime):
        timesCarrier = linspace(0, totalTime, 250000 * totalTime)
        dataCarrier = cos(2 * np.pi * 62500 * timesCarrier)
        demoduleAM = AM * dataCarrier
        print(demoduleAM)
        return demoduleAM

    def demodulatorAMCos(self, modulation):

        graphic = Graphic()
        dataCarrier = modulation.function3 * modulation.function2
        print(dataCarrier)
        graphic.generateGraphics4(modulation.function1, modulation.function3, dataCarrier,modulation.time)
        graphic.frequencyGraphic(dataCarrier,modulation.freqSampling,"demodulada",10000,8)
        audio = Audio(modulation.freqSampling,0,dataCarrier,modulation.time,"demodulada",150,10000,10,modulation.time)
        newdata, fft = graphic.lowpassFilteredGraphic(audio,150,5)
        graphic.inverseGraphic(modulation.freqSampling,2*fft,"demodulacion",150,10)
        #graphic.generateGraphics5(modulation.function1, modulation.freqSampling, modulation.function3,modulation.freqSampling, dataCarrier, modulation.time)


    def fmModulation (self, f, fc, k):

        graphic = Graphic()
        modulation = Modulation(f, fc)
        modulation.freqSampling = 18 * fc

        modulation.time = np.arange(0, 0.5, 1 / modulation.freqSampling)

        modulating_signal = np.cos(2 * np.pi * f * modulation.time)

        phase = k * (integrate.cumtrapz(modulating_signal, modulation.time, initial=0))
        print(phase)
        modulated_signal = np.cos( (2 * np.pi * fc * modulation.time) + phase)

        graphic.generateGraphics4(modulating_signal, modulating_signal, modulated_signal, modulation.time)
        graphic.generateGraphics5(modulating_signal, modulation.freqSampling, modulating_signal,
                                  modulation.freqSampling, modulated_signal, modulation.time)

        plt.subplot(311)
        plt.plot(modulation.time, modulating_signal, linewidth=1)
        plt.title("senal")
        plt.subplot(312)
        plt.plot(modulation.time, modulated_signal, linewidth = 1)
        plt.title("Resultado")
        plt.show()

    def fmModulationSound(self, originalAudio, k):
        graphic = Graphic()

        interp = interp1d(originalAudio.time, originalAudio.data_array)
        newTime = np.linspace(0, len(originalAudio.data_array) / originalAudio.sampling_rate,
                              len(originalAudio.data_array) * 10)
        newData = interp(newTime)

        newLen = len(newData)

        timesCarrier = linspace(0, len(originalAudio.data_array) / originalAudio.sampling_rate, newLen)
        # print(timesCarrier)
        # print(newData)
        fc = 50000

        carrier = np.sin(2 * np.pi * timesCarrier)
        w = fc*timesCarrier

        integral = integrate.cumtrapz(newData, timesCarrier, initial=0)

        result = np.cos(2*np.pi * w + k * integral)
        # print(result)

        plt.subplot(311)
        plt.plot(originalAudio.time, originalAudio.data_array, linewidth=0.5)
        plt.title("senal del mensaje")
        plt.subplot(312)
        plt.plot(timesCarrier[200:800], result[200:800], linewidth=0.5)
        plt.title("modulacion fm")
        plt.savefig(os.getcwd() + "/Salida/fmModulation.png")
        plt.show()



