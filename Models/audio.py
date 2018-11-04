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