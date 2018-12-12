from scipy.io.wavfile import read, write
from Models.audio import Audio
import os
from numpy import linspace
import warnings
warnings.filterwarnings('ignore')


class Archive:

    aux = 0

    def __init__(self, aux):
        self.aux = aux

    def readAudio(self,aux):

        dimension = 0

        while aux == 1:
            audio_name = input("Introduzca el nombre del archivo: ")
            try:
                nameText = os.getcwd() + '/Audios/' + audio_name + '.wav'
                sampling_rate, data_array = read(nameText)
                print(sampling_rate)
                dimension = data_array[0].size
                aux = 0

            except FileNotFoundError:
                print("No se pudo abrir el audio intentelo nuevamente\n")
        print("\n")
        if dimension == 1:
            data = data_array
        else:
            data = data_array[:, dimension - 1]

        duration = len(data) / sampling_rate
        time = linspace(0, duration, len(data))
        originalAudio = Audio(sampling_rate, time, dimension, data, data_array, duration, audio_name, 0,
                              22000, 10)
        return aux, originalAudio


    def saveWav(self,title, rate, data):
        #x = data.astype('int16')
        write(title, rate, data)


