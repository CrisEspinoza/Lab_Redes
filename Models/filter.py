from scipy.signal import butter, lfilter

class Filter:

    ## - ATTRIBUTES - ##
    name = ""
    low_cutoff = 0
    high_cutoff = 0
    order = 0

    ## - FUNCTIONS - ##

    # CONSTRUCTOR////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, low_cutoff, high_cutoff, order):
        self.high_cutoff = high_cutoff
        self.order = order
        self.low_cutoff = low_cutoff

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


