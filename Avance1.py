from scipy.io.wavfile import read
from Models.audio import Audio
from Models.graphic import Graphic
from Models.menu import Menu
import os
import warnings
warnings.filterwarnings('ignore')

def main():

    aux = 1
    choice = '0'

    while choice != '-1':
        print("\n")
        print("******** Les mostramos las distintas opciones que contiene nuestro programa*******")
        print("1. Leer el archivo de audio")
        print("2. Realizamos analisis completo del audio")
        print("3. Creditos")
        print("4. Salir")
        print("\n")

        choice = input("Ingrese opcion a realizar: ")

        if choice == "1":
            print("\n")
            while (aux == 1):
                audio_name = input("Introduzca el nombre del archivo: ")
                try:
                    nameText = os.getcwd() + '/Audios/' + audio_name + '.wav'
                    sampling_rate, data_array = read(nameText)
                    dimension = data_array[0].size
                    aux = 0

                except FileNotFoundError:
                    print("No se pudo abrir el audio intentelo nuevamente\n")
            print("\n")

        elif choice == "2":
            print("\n")
            low_cutoff = float(input("Introduzca la frecuencia de filtro bajo (Hz): "))
            high_cutoff = float(input("Introduzca la frecuencia de filtro alto (Hz): "))
            order = float(input("Introduzca el orden deseado para el filtro (N): "))
            # print(dimension)

            # data: datos del audio(arreglo de numpy)
            if dimension == 1:
                data = data_array
            else:
                data = data_array[:, dimension - 1]

            time = len(data) / sampling_rate
            originalAudio = Audio(sampling_rate, dimension, data, time, audio_name, low_cutoff, high_cutoff, order)
            grafic = Graphic()
            grafic.createGraphics(originalAudio, low_cutoff, high_cutoff, order)
            print("\n")

        elif choice == "3":
            print("\n")
            print("\n")
            print("********************************")
            print("Universidad de Santiago de Chile")
            print("Nombres: * Luis Abello")
            print("         * Cristian Espinoza")
            print("         * Carlos Perez")
            print("********************************")
            print("\n")
            print("\n")

        else:
            choice = "-1"
            print("\n")
            input(" Hasta una nueva oportunidad ")
            print("\n")


if __name__ == '__main__':
    main()







