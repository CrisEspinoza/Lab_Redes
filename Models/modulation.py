

from Models.graphic import Graphic
from Models.audio import Audio
import numpy as np
from numpy import linspace, cos, interp
import matplotlib.pyplot as plt

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

    def amModulation (self, originalAudio):

        graphic = Graphic()
        timesCarrier = linspace(0, originalAudio.duration, 250000 * originalAudio.duration)
        print(timesCarrier)
        newData = interp(timesCarrier, originalAudio.time, originalAudio.data_array)
        print(newData)
        f1 = cos(2 * np.pi * 62500 * timesCarrier)
        result = f1 * newData
        print(result)

        graphic.generateGraphics4(f1, newData, result, timesCarrier)

        demoduleAM = self.demodulatorAM(result, originalAudio.duration)

        print(demoduleAM)

        #graphic.inverseGraphic(timesCarrier,demoduleAM,"a",0,0)

        graphic.generateGraphics4(f1, newData, demoduleAM, timesCarrier)

        #graphic.generateGraphics4(originalAudio, result, demoduleAM, timesCarrier)


    def demodulatorAM(self, AM, totalTime):
        timesCarrier = linspace(0, totalTime, 250000 * totalTime)
        dataCarrier = cos(2 * np.pi * 62500 * timesCarrier)
        demoduleAM = AM * dataCarrier * dataCarrier
        print(demoduleAM)
        return demoduleAM

    def demodulatorAMCos(self, modulation):

        graphic = Graphic()
        dataCarrier = modulation.function3 * modulation.function2
        print(dataCarrier)
        graphic.generateGraphics4(modulation.function1, modulation.function3, dataCarrier,modulation.time)
        graphic.frequencyGraphic(dataCarrier,modulation.freqSampling,"demodulada",10000,8)
        audio = Audio(modulation.freqSampling,0,dataCarrier,modulation.time,"demodulada",150,10000,10,modulation.time)
        newdata, fft = graphic.lowpassFilteredGraphic(audio,150,10)
        graphic.inverseGraphic(modulation.freqSampling,2*fft,"demodulacion",150,10)
        #graphic.generateGraphics5(modulation.function1, modulation.freqSampling, modulation.function3,modulation.freqSampling, dataCarrier, modulation.time)





