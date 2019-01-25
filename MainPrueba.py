from Models.graphic import Graphic
from Models.modulation import Modulation
from Models.audio import Audio
import warnings
warnings.filterwarnings('ignore')

# Definimos variables globales a utilizar dentro del programa y las inicializamos en 0 (Con el fin de declararlas)

def main():

    menuPrincipal()

def menuPrincipal():

    choice = '0'
    aux = 1

    while choice != '-1':

        print("\n")
        print("******** Les mostramos las distintas etapas del programa desarrollado*******")
        print("1. Comenzar Conversación")
        print("2. Finalizar Conversación")
        print("\n")

        choice = input("Ingrese opcion a realizar: ")

        if choice == "1":
            if aux == 1:
                digital()

        else:
            choice = "-1"
            print("\n")
            input(" Hasta una nueva oportunidad ")
            print("\n")

def digital():

    modulation = Modulation(0, 0)
    modulation.audio = Audio(0,0,0,0,0,0,0,0,0,0)
    choice = '0'
    graphic = Graphic()

    while choice != '-1':

        print("\n")
        print("******** Les mostramos las distintas opciones que contiene la primera iteración *******")
        print("1. Enviar Mensaje (Modulación)")
        print("2. Recbibir Mensaje (Demodulacion)")
        print("3. Volver")
        print("\n")

        choice = input("Ingrese opcion a realizar: ")

        if choice == "1":
            print("Opcion 1")
            modulation = modulation.fskModulation(modulation)

        elif choice == "2":
            print("Opcion 2")
            print("Aplicando ruido")
            modulation.fsk_function4, modulation.noise = modulation.addNoise(modulation.fsk_function3)
            graphic.generateGraphics12("Agregando ruido a señal modulada_fsk", modulation.fsk_time2, modulation.fsk_function3, modulation.fsk_function4, modulation.noise)
            modulation.DemulatorFsk(modulation)

        else:
            choice = "-1"
            print("\n")
            print(" Volviendo al menu inicial")
            print("\n")

if __name__ == '__main__':
    main()