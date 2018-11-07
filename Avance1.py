from scipy.io.wavfile import read
from Models.audio import Audio
from Models.graphic import Graphic
from Models.menu import Menu
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print(" Avance numero 1")
    app = Menu()
    audio_name = input("Introduzca el nombre del archivo: ")
    low_cutoff = float (input ("Introduzca la frecuencia de filtro bajo (Hz): ") )
    high_cutoff = float (input ("Introduzca la frecuencia de filtro alto (Hz): ") )
    order = float ( input ("Introduzca el orden deseado para el filtro (N): ") )

    nameText = os.getcwd() + '/Audios/' + audio_name + '.wav'
    sampling_rate, data_array = read(nameText)
    dimension = data_array[0].size
    #print(dimension)

    #data: datos del audio(arreglo de numpy)
    if dimension == 1:
        data = data_array
    else:
        data = data_array[:,dimension-1]

    time = len(data)/sampling_rate
    originalAudio = Audio(sampling_rate, dimension, data, time, audio_name, low_cutoff, high_cutoff, order)
    grafic = Graphic()
    grafic.createGraphics(originalAudio, low_cutoff, high_cutoff, order)

    #Se muestra la nueva matriz de datos que se tiene al aplicar la tranformada de fourier al audio
    #print(newData)

if __name__ == '__main__':
    main()







