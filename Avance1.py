from scipy.io.wavfile import read
from Models.audio import Audio
from Models.graphic import Graphic
from Models.modulation import Modulation
from Models.menu import Menu
import os
from numpy import linspace
import warnings
warnings.filterwarnings('ignore')

# Definimos variables globales a utilizar dentro del programa y las inicializamos en 0 (Con el fin de declararlas)

def main():

    menuPrincipal()

def menuPrincipal():

    choice = '0'
    originalAudio = []

    while choice != '-1':
        print("\n")
        print("******** Les mostramos las distintas etapas del programa desarrollado*******")
        print("1. Analisis de señales")
        print("2. Codificacion y modulacion digital")
        print("3. Recepción y demodulación")
        print("4. Protocolos de enlace y acceso al medio")
        print("5. Protocolo de red y prototipo final")
        print("6. Creditos")
        print("7. Salir")
        print("\n")

        choice = input("Ingrese opcion a realizar: ")

        if choice == "1":
            originalAudio = signalAnaysisMenu()
            input("Presiona Enter para continuar")

        elif choice == "2":
            digitalCodingAndModulation(originalAudio)
            input("Presiona Enter para continuar")

        elif choice == "3":
            print("Parte 3")
            input("Presiona Enter para continuar")

        elif choice == "4":
            print("Parte 4")
            input("Presiona Enter para continuar")

        elif choice == "5":
            print("Parte 5")
            input("Presiona Enter para continuar")

        elif choice == "6":
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

def signalAnaysisMenu ():

    aux = 1
    choice = '0'
    originalAudio = 0

    while choice != '-1':
        print("\n")
        print("******** Les mostramos las distintas opciones que contiene la primera iteración *******")
        print("1. Leer el archivo de audio")
        print("2. Realizamos analisis completo del audio")
        print("3. Volver")
        print("\n")

        choice = input("Ingrese opcion a realizar: ")

        if choice == "1":
            print("\n")
            while (aux == 1):
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

        elif choice == "2":
            print("\n")
            low_cutoff = float(input("Introduzca la frecuencia de filtro bajo (Hz): "))
            order = float(input("Introduzca el orden deseado para el filtro (N): "))
            # print(dimension)

            # data: datos del audio(arreglo de numpy)
            if dimension == 1:
                data = data_array
            else:
                data = data_array[:, dimension - 1]

            duration = len(data) / sampling_rate
            high_cutoff = 0
            time = linspace(0, duration, len(data))
            originalAudio = Audio(sampling_rate, dimension, data, duration, audio_name, low_cutoff, high_cutoff, order, time)
            grafic = Graphic()
            grafic.createGraphics(originalAudio)
            print("\n")

        else:
            choice = "-1"
            print("\n")
            print(" Volviendo al menu inicial")
            print("\n")
            return originalAudio

def digitalCodingAndModulation(originalAudio):

    choice = '0'
    modulationAM = Modulation(0, 0)
    modulationFM = Modulation(0, 0)

    while choice != '-1':
        print("\n")
        print("******** Les mostramos las distintas opciones que contiene la primera iteración *******")
        print("1. Realizar modulacion AM")
        print("2. Realizar modulacion FM")
        print("3. Realizar demodulacion AM")
        print("4. Volver")
        print("\n")

        choice = input("Ingrese opcion a realizar: ")

        if choice == "1":
            print("Realizando modulacion AM\n")
            #modulationAM = modulationAM.amModulationCos(7, 100)
            modulationAM = modulationAM.amModulation(originalAudio)
            input("Presiona Enter para continuar")

        elif choice == "2":
            print("Realizando modulacion FM")
            modulationFM = modulationFM.fmModulation(modulationFM, 7, 100, 50)
            input("Presiona Enter para continuar")

        elif choice == "3":
            print("Realizando demodulacion AM")
            modulationAM = modulationAM.demodulatorAMCos(modulationAM)
            input("Presiona Enter para continuar")

        else:
            choice = "-1"
            print("\n")
            print(" Volviendo al menu inicial")
            print("\n")
            return modulationFM, modulationAM

if __name__ == '__main__':
    main()