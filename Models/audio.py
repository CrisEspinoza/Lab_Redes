    # Clase que se encarga de guardar los datos de un audio
class Audio:
    frequency = 0
    information = 0
    informationNumpy = 0
    duration = 0
    dimension = 0
    nameAudio = ""
    informationNumpyFourier = []

    def __init__(self,info1,info2,dimension,data,time,nameAudio):
        self.frequency = info1
        self.information = info2
        self.informationNumpy = data
        self.duration = time
        self.dimension = dimension
        self.nameAudio = nameAudio