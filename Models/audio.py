from Models.filter import Filter

    # Clase que se encarga de guardar los datos de un audio
class Audio:

## - ATTRIBUTES - ##
    sampling_rate = []
    data_array = []
    info = 0
    bandpass_data = 0
    duration = []
    time = []
    dimension = []
    audio_name = ""
    information_numpy_fourier = []
    filter = Filter(0, 0, 0)

## - FUNCTIONS - ##

    #CONSTRUCTOR////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, samplingRate,time,dimension,data,data_array, duration, audioName, low_cutoff, high_cutoff,order):
        self.sampling_rate = samplingRate
        self.info = data_array
        self.data_array = data
        self.duration = duration
        self.dimension = dimension
        self.audio_name = audioName
        self.time = time
        self.filter = Filter(low_cutoff, high_cutoff, order)

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
