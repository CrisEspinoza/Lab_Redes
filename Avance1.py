from Models.graphic import Graphic
from Models.modulation import Modulation
from Models.archive import Archive
from Models.audio import Audio
from Models.filter import Filter
import warnings
warnings.filterwarnings('ignore')

# Definimos variables globales a utilizar dentro del programa y las inicializamos en 0 (Con el fin de declararlas)

def main():

    menuPrincipal()

def menuPrincipal():

    choice = '0'
    aux = 0
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
            aux  = 1
            input("Presiona Enter para continuar")

        elif choice == "2":
            if aux == 1:
                digitalCodingAndModulation(originalAudio)
                input("Presiona Enter para continuar")
            else:
                print("Primero debe cargaro un audio para continuar (Opción numero 1)")
                input("Presione Enter para continuar")

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
    originalAudio = Audio(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

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
            archive = Archive(0)
            aux, originalAudio = archive.readAudio(aux)
            print("\n")

        elif choice == "2":
            grafic = Graphic()
            print("\n")
            low_cutoff = float(input("Introduzca la frecuencia de filtro bajo (Hz): "))
            order = float(input("Introduzca el orden deseado para el filtro (N): "))
            originalAudio.filter = Filter(low_cutoff, 0, order)
            #grafic.createGraphics(originalAudio)
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
            #Modulacion FM para audios
            modulationFM = modulationFM.fmModulationSound(originalAudio, 2, modulationFM)

            # Modulacion FM para cosenos
            modulationFM = modulationFM.fmModulation(modulationFM, 7, 100, 100)
            input("Presiona Enter para continuar")

        elif choice == "3":
            print("Realizando demodulacion AM")
            #modulationAM = modulationAM.demodulatorAMCos(modulationAM)
            modulationAM = modulationAM.demodulatorAM(modulationAM)
            input("Presiona Enter para continuar")

        else:
            choice = "-1"
            print("\n")
            print(" Volviendo al menu inicial")
            print("\n")
            return modulationFM, modulationAM

if __name__ == '__main__':
    main()