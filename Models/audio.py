import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


    # Clase que se encarga de guardar los datos de un audio
class Audio:

## - ATTRIBUTES - ##
    sampling_rate = 0
    data_array = 0
    duration = 0
    dimension = 0
    audio_name = ""
    information_numpy_fourier = []

## - FUNCTIONS - ##

    #CONSTRUCTOR////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, samplingRate, dimension, data, time, audioName):
        self.sampling_rate = samplingRate
        self.data_array = data
        self.duration = time
        self.dimension = dimension
        self.audio_name = audioName

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: butterLowpass
    # - DESCRIPTION: Genera los coeficientes para el filtrado de frecuencias a partir de determiados parametros de entrada
    # - PARAMS: - cutoff: Frecuencia de corte, que atenua las frecuencias superiores a esta
    # - OUT: Coeficientes

    def butterLowpass(self, cutoff, samplingRate, order):
        nyq_rate = samplingRate * 0.5    #La tasa Nyquist de la señal
        normalized_cutoff = cutoff / nyq_rate
        b, a = butter(order, normalized_cutoff, btype='low', analog=False)
        return b, a

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: butterLowpassFilter
    # - DESCRIPTION:
    # - PARAMS:
    # - OUT:

    def butterLowpassFilter(self, data, cutoff, samplingRate, order):
        b, a = self.butterLowpass(cutoff, samplingRate, order)
        y = lfilter(b, a, data)
        return y
