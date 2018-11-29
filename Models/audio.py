from Models.filter import Filter
    # Clase que se encarga de guardar los datos de un audio
class Audio:

## - ATTRIBUTES - ##
    sampling_rate = []
    data_array = []
    bandpass_data = 0
    duration = []
    time = []
    dimension = []
    audio_name = ""
    information_numpy_fourier = []
    filter = Filter(0, 0, 0)

## - FUNCTIONS - ##

    #CONSTRUCTOR////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, samplingRate, dimension, data, duration, audioName, low_cutoff, high_cutoff, order, time):
        self.sampling_rate = samplingRate
        self.data_array = data
        self.duration = duration
        self.dimension = dimension
        self.audio_name = audioName
        self.time = time
        self.filter = Filter(low_cutoff,high_cutoff,order)



    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
