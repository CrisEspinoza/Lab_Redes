from scipy.io.wavfile import read
from Models.audio import Audio
from Models.graphic import Graphic
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print(" Avanze numero 1")

    nameAudio = input("Introduzca el nombre del archivo: ")
    low_cutoff = float (input ("Introduzca la frecuencia de filtro paso bajo (Hz): ") )
    order = float ( input ("Introduzca el orden deseado para el filtro (N): ") )

    nameText = os.getcwd() + '/Audios/' + nameAudio + '.wav'
    sampling_rate, data_array = read(nameText)
    dimension = data_array[0].size
    #print(dimension)

    #data: datos del audio(arreglo de numpy)
    if dimension == 1:
        data = data_array
    else:
        data = data_array[:,dimension-1]

    time = len(data)/sampling_rate

    grafic = Graphic()
    originalAudio = Audio(sampling_rate, dimension, data, time,nameAudio)

    grafic.timeGraphic(originalAudio.data_array, originalAudio.duration, originalAudio.audio_name)
    originalAudio.informationNumpyFourier, fourierT = grafic.frequencyGraphic(originalAudio.data_array, originalAudio.sampling_rate, originalAudio.audio_name)
    grafic.lowpassFilteredGraphic(originalAudio, low_cutoff, order)
    grafic.spectrogramGraphic(originalAudio.data_array, originalAudio.sampling_rate, originalAudio.audio_name)
    grafic.inverseGraphic(originalAudio.sampling_rate, fourierT, originalAudio.audio_name)

    #Se muestra la nueva matriz de datos que se tiene al aplicar la tranformada de fourier al audio
    #print(newData)

if __name__ == '__main__':
    main()







