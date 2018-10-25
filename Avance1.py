from scipy.io.wavfile import read
from Models.audio import Audio
from Models.graphic import Graphic
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print(" Avanze numero 1")

    nameAudio = input("Introduzca el nombre del archivo: ")
    nameText = os.getcwd() + '/Audios/' + nameAudio + '.wav'

    info1, info2 = read(nameText)

    dimension = info2[0].size
    #print(dimension)

    #data: datos del audio(arreglo de numpy)
    if dimension == 1:
        data = info2
    else:
        data = info2[:,dimension-1]

    time = len(data)/info1

    grafic = Graphic()
    audio = Audio(info1, info2, dimension, data, time,nameAudio)

    grafic.timeGraphic(audio.informationNumpy,audio.duration,audio.nameAudio)
    grafic.frequencyGraphic(audio.informationNumpy,audio.frequency,audio.nameAudio)


if __name__ == '__main__':
    main()







