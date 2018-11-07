import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


    # Clase que se encarga de guardar los datos de un audio
class Audio:

## - ATTRIBUTES - ##
    sampling_rate = 0
    data_array = 0
    bandpass_data = 0
    duration = 0
    dimension = 0
    audio_name = ""
    information_numpy_fourier = []

## - FUNCTIONS - ##

    #CONSTRUCTOR////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, samplingRate, dimension, data, time, audioName, low_cutoff, high_cutoff,  order):
        self.sampling_rate = samplingRate
        self.data_array = data
        self.duration = time
        self.dimension = dimension
        self.audio_name = audioName

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: butterBandpass
    # - DESCRIPTION: Genera los coeficientes para el filtrado de frecuencias dadas las frecuencias de corte
    # - PARAMS: - low_cutoff: Frecuencia de corte de frecuencias bajas, atenua frecuencias bajo este valor
    #           - high_cutoff: Frecuencia de corte de frecuencias altas, atenua frecuencias sobre este valor
    #           - samplingRate: Frecuencia de la muestra, en este caso del audio que se analiza
    #           - order: Valor que indica el orden del polinomio de
    # - OUT: Coeficientes a y b

    def butterBandpass(self, low_cutoff, high_cutoff, samplingRate, order):
        nyq_rate = samplingRate * 0.5    #La tasa Nyquist de la señal
        normalized_low_cut = low_cutoff / nyq_rate
        normalized_high_cut = high_cutoff / nyq_rate
        b, a = butter(order, [normalized_low_cut, normalized_high_cut], btype='band', analog=False)
        return b, a

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: butterBandpassFilter
    # - DESCRIPTION: Realiza el filtro de paso de banda de las frecuencias del audio de entrada de acuerdo a dos frecuencias de corte y el orden
    # - PARAMS: - data:
    #           - low_cutoff:
    #           - high_cutoff:
    #           - samplingRate:
    #           - order:
    # - OUT:

    def butterBandpassFilter(self, data, low_cutoff, high_cutoff, samplingRate, order):
        b, a = self.butterBandpass(low_cutoff, high_cutoff, samplingRate, order)
        y = lfilter(b, a, data)
        return y

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: butterBandpass
    # - DESCRIPTION: Genera los coeficientes para el filtrado de frecuencias dadas las frecuencias de corte
    # - PARAMS: - low_cutoff: Frecuencia de corte de frecuencias bajas, atenua frecuencias bajo este valor
    #           - high_cutoff: Frecuencia de corte de frecuencias altas, atenua frecuencias sobre este valor
    #           - samplingRate: Frecuencia de la muestra, en este caso del audio que se analiza
    #           - order: Valor que indica el orden del polinomio de
    # - OUT: Coeficientes a y b

    def butterLowpass(self, cutoff, samplingRate, order):
        nyq_rate = samplingRate * 0.5  # La tasa Nyquist de la señal
        normalized_cutoff = cutoff / nyq_rate
        b, a = butter(order, normalized_cutoff, btype='low', analog=False)
        return b, a

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # - NAME: butterBandpassFilter
    # - DESCRIPTION: Realiza el filtro de paso de banda de las frecuencias del audio de entrada de acuerdo a dos frecuencias de corte y el orden
    # - PARAMS: - data:
    #           - low_cutoff:
    #           - high_cutoff:
    #           - samplingRate:
    #           - order:
    # - OUT:

    def butterLowpassFilter(self, data, cutoff, samplingRate, order):
        b, a = self.butterLowpass(cutoff, samplingRate, order)
        y = lfilter(b, a, data)
        return y

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
