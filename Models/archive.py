from scipy.io.wavfile import read, write
from Models.audio import Audio
import os
import numpy as np
import sounddevice as sd
from numpy import linspace
import scipy.io.wavfile as wavfile
import wave
import warnings
warnings.filterwarnings('ignore')


class Archive:

    aux = 0

    """
    Entrada: Entra un numero auxiliar para saber que lo que vamos a realizar
    Procedimiento: Asigna el valor a la variable local
    Salida: -
    """

    def __init__(self, aux):
        self.aux = aux

    """
        Entrada: Entra un numero auxiliar para saber si el archvo fue leido coorectamente.
        Procedimiento: Se encarga de leer el audio, verificando si se abrio correctamente con la variable que utilizamos como bandera.
        Salida: tiene como salida el estado que se produce y el archivo leido.
    """

    def readAudio(self, aux):

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

    """
        Entrada: Entra el titulo, la frecuencia de muestro y los datos.
        Procedimiento: Se encarga de guarda los datos en un archivo.wav
        Salida: -
    """

    def saveWav(self,title, rate, data):
        #x = data.astype('int16')
        write(title, rate, data)

    """
        Entrada: Entra la duracion del audio que vamos a grabar
        Procedimiento: Se encarga de grabar un audio desde el exterior
        Salida: Entrega el audio que se grabo desde el exterior, para poder trabajarlo
    """

    def audioRecord(self,duration):
        fs = 44100  # Samples por segundo
        char = input("Listo para grabar: ")
        myrecording = sd.rec(int((duration + 0.6) * fs), samplerate=fs, channels=1)
        sd.wait()  # Usar wait, debe ser solo despues de haber hecho lo necesario como calculos de fft y otras cosas,
        # todas estas funciones trabajan en background.
        # Es probable que no se deba hacer sd.wait() a menos que se
        # comparta el tiempo que debe ser el archivo con un calculo simple
        return np.ndarray.flatten(myrecording, 1)
        # return myrecording

    """
        Entrada: Entra los datos que vamos a reproducir
        Procedimiento: Se encarga de reproducir los datos que fueron ingresados.
        Salida: -
    """

    def audioPlay(self,data):
        fs = 44100
        sd.play(data, fs)
        sd.wait()




