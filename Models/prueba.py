
###################################################
# Laboratorio n°3 Redes de Computadores			  #
# INTEGRANTES:									  #
#   - Javier Arredondo							  #
#	- Shalini Ramchandani						  #
###################################################

###################################################
################## Importaciones ##################
###################################################
import numpy as np
from numpy import linspace, cos, interp
from scipy.io.wavfile import read, write
from scipy.fftpack import fft, ifft
from scipy.signal import firwin, lfilter
import scipy.integrate as integrate
import matplotlib.pyplot as plt
from math import pi

###################################################
############# Definición de funciones #############
###################################################
"""
Función que se encarga de abrir archivos .wav y obtiene la frecuencia e información de la señal.
Entrada:
        name-> nombre del archivo con extensión .wav
Salida:
        rate  -> frecuencia de muestreo.
        info  -> datos de la señal.
        times -> tiempo para cada dato en info.
"""


def openWav(name):
    rate, info = read(name)  # rate = frecuencia_muestreo
    dimension = info[0].size
    if (dimension == 1):
        data = info
    else:
        data = info[:, dimension - 1]
    n = len(data)
    Ts = n / rate  # Ts = Tiempo total
    times = np.linspace(0, Ts, n)
    return (rate, data, times)


"""
Función general utilizada para graficar.
Entrada: 
        title -> titulo del gráfico
        xlabel -> nombre del eje x
        xdata -> datos del eje x
        ylabel -> nombre del eje y 
        ydata -> datos del eje y
"""


def makeGraphic(title, xlabel, xdata, ylabel, ydata):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(xdata, ydata)
    plt.savefig("images/" + title + ".png")
    plt.show()
    plt.close('all')


"""
Función que gráfica el audio en dominio del tiempo. Para esto se adquiere la duración del audio (1)
y el tiempo en segundos para cada dato en el rate (2). Posteriormente se gráfica el contenido del audio.
Entrada:
    data -> Son los datos obtenidos al leer el audio
    rate -> Frecuencia de muestreo del archivo wav
    title -> Titulo del gráfico
Salida:
    None
"""


def timeGraphic(data, rate, title):
    duration = len(data) / rate  # Tiempo que dura todo el audio
    t = linspace(0, duration, len(
        data))  # Intervalos de tiempo de 0 a t, generando la misma cantidad de datos que hay en data o vector tiempo
    makeGraphic(title, "Tiempo [s]", t, "Amplitud [dB]", data)


"""
Función que guarda en un archivo .wav datos de una señal
Entrada:
        title -> nombre de salida del archivo.
        rate  -> frecuencia de muestreo de una señal.
        data  -> señal en dominio del tiempo.
"""


def saveWav(title, rate, data):
    write("audios/" + title + ".wav", rate, data.astype('int16'))


"""
Función que realiza el proceso de modulación AM dependiendo del porcentaje de modulación entregado.
El porcentaje de modulacion varía la amplitud de la onda portadora. Al finalizar la modulación, 
realiza el llamado a la función que realiza la demodulación.
Entrada:
        percentage -> Porcentaje de modulación
        dataAudio  -> Son los datos del audio (eje y)
        timesAudio -> Son los tiempos del mensaje 
        rate       -> frecuencia de muestreo del audio
        totalTime  -> tiempo total del audio.
Salida:
        AM           -> datos de la señal modulada
        timesCarrier -> tiempos de la señal portadora, que es la misma que la modulada
        newDemo      -> Datos de la señal demodulada
"""


def modAM(percentage, dataAudio, timesAudio, rate, totalTime):
    # Señal Portadora
    timesCarrier = linspace(0, totalTime, 250000 * totalTime)
    dataCarrier = (percentage / 100) * cos(2 * pi * 62500 * timesCarrier)

    print(dataCarrier)
    print(timesCarrier)

    # Se interpola para tener la misma cantidad de datos
    newData = interp(timesCarrier, timesAudio, dataAudio)

    # Señal modulada
    AM = dataCarrier * newData

    # Gráficos
    fig = plt.figure(1)
    plt.subplot(411)
    plt.title("Señal Entrante")
    graph1 = plt.plot(timesCarrier[0:1000], newData[0:1000])
    plt.subplot(412)
    plt.title("Señal Portadora")
    graph2 = plt.plot(timesCarrier[0:1000], dataCarrier[0:1000], linewidth=0.3, color="red")
    plt.subplot(413)
    plt.title("Señal Modulada AM al " + str(percentage) + "%")
    graph3 = plt.plot(timesCarrier[0:1000], AM[0:1000], linewidth=0.3, color="green", marker="o", markersize=0.5)

    demo = demoduladorAM(percentage, timesCarrier, AM)

    plt.subplot(414)
    plt.title("Señal Demodulada AM al " + str(percentage) + "%")
    graph3 = plt.plot(timesCarrier[0:1000], demo[0:1000], linewidth=0.3, color="yellow")

    newDemo = interp(timesAudio, timesCarrier, demo)
    plt.tight_layout()
    saveWav("salida" + str(percentage), rate, newDemo)
    plt.savefig("images/modYDemodAM" + str(percentage) + ".png")
    plt.show()

    return AM, timesCarrier, newDemo


"""
Función que se encarga del proceso de modulación FM, que también al igual que en la función anterior,
se requiere del porcentaje de modulación pero en este caso, no afecta a la amplitud de la onda portadora,
si no que a la frecuencia. No se realiza la demodulación de esta función.
Entrada:
        percentage -> Porcentaje de modulación
        dataAudio  -> Son los datos del audio (eje y)
        timesAudio -> Son los tiempos del mensaje 
        rate       -> frecuencia de muestreo del audio
        totalTime  -> tiempo total del audio.
Salida:
        newData -> los datos ya modulados FM
"""


def modFM(percentage, dataAudio, timesAudio, rate, totalTime):
    freqP = 5 / 2 * rate  # Se necesita de una frecuencia portadora que sea la mitad de la freq obtenida y minimo 4 veces mayor a la freq de muestreo.
    # ^ Eso da 20480

    # Señal portadora
    A = 1  # Amplitud definida para la señal portadora
    timesCarrier = linspace(0, totalTime, 250000 * totalTime)
    dataCarrier = A * cos(pi * timesCarrier * 6500)  # Podriamos cambiar el 6500 por freqP
    # Reestructuración de datos originales
    dataAudio = interp(timesCarrier, timesAudio, dataAudio)
    timesAudio = timesCarrier
    # Señal modulada en su frecuencia
    signalIntegrate = integrate.cumtrapz(dataAudio, timesAudio, initial=0)  # Integral acumulada
    dataModulated = A * cos(pi * timesCarrier * 6500 + pi * (percentage / 100) * signalIntegrate)

    plt.figure(1)
    plt.subplot(311)
    plt.title("Señal Entrante")
    plt.plot(timesAudio[:2000], dataAudio[:2000])

    plt.subplot(312)
    plt.title("Señal Portadora")
    plt.plot(timesCarrier[:2000], dataCarrier[:2000], linewidth=0.3, color="red")

    plt.subplot(313)
    plt.title("Modulación FM " + str(percentage) + " %")
    plt.plot(timesAudio[:2000], dataModulated[:2000], linewidth=0.3, color="green", marker="o", markersize=0.5)
    plt.tight_layout()
    plt.savefig("images/modFM" + str(percentage) + ".png")

    plt.show()
    newData = interp(timesAudio, timesCarrier, dataModulated)

    return newData


"""
Función que realiza la demodulación AM.
Entrada:
        timesModulated -> los tiempos de la señal modulada
        dataModulated  -> los datos de la señal modulada
Salida: 
        demoduleAM -> los datos de la señal demodulada.
"""


def demoduladorAM(percentage, timesModulated, dataModulated):
    timesCarrier = linspace(0, totalTime, 250000 * totalTime)
    dataCarrier = cos(2 * pi * 62500 * timesCarrier)
    demoduleAM = dataModulated * dataCarrier
    return demoduleAM


"""
Función que realiza la transformada de fourier en base a los datos obtenidos del audio.
Entrada:
        data     -> señal en dominio del tiempo.
        rate     -> frecuencia de muestreo de la señal.
Salida:
        fftData  -> transformada de fourier normalizada para los valores de la señal original.
        fftFreqs -> frecuencias de muestreo que dependen del largo del arreglo data y de rate.
"""


def tFourier(data, rate):
    n = len(data)
    Ts = n / rate
    fftData = fft(data) / n
    fftFreqs = np.fft.fftfreq(n, 1 / rate)
    return (fftData, fftFreqs)


"""
Función que realiza el filtro paso bajo sobre una señal dada, eliminando todas las frecuencias altas y manteniendo las bajas.
Entrada: 
        data -> señal en dominio del tiempo.
        rate -> frecuencia de muestreo de la señal. 
Salida:
        Señal filtrada
"""


def lowFilter(data, rate):
    nyq = rate / 2
    cutoff = 4000
    numtaps = cutoff + 1
    coeff = firwin(numtaps, (cutoff / nyq))  # ,window= 'blackmanharris'
    filtered = lfilter(coeff, 1.0, data)
    return filtered


###################################################
################ Bloque Principal #################
###################################################
# Se lee el archivo
rate, data, times = openWav(
    "audios/handel.wav")  # rate = frecuencia_muestreo, data = datos(eje y), times = tiempos(eje x)
totalTime = len(data) / rate
fftData, fftFreqs = tFourier(data, rate)

# Modulación AM.
print("Modulacion AM 15%")
AM15, timesCarrier15, demo15 = modAM(15, data, times, rate, totalTime)
fftDataAM15, fftFreqsAM15 = tFourier(demo15, rate)

print("Modulacion AM 100%")
AM100, timesCarrier100, demo100 = modAM(100, data, times, rate, totalTime)
fftDataAM100, fftFreqsAM100 = tFourier(demo100, rate)

print("Modulacion AM 125%")
AM125, timesCarrier125, demo125 = modAM(125, data, times, rate, totalTime)
fftDataAM125, fftFreqsAM125 = tFourier(demo125, rate)

# Modulación FM.
print("Modulacion FM 15%")
FM15 = modFM(15, data, times, rate, totalTime)
fftDataFM15, fftFreqsFM15 = tFourier(FM15, rate)
print("Modulacion FM 100%")
FM100 = modFM(100, data, times, rate, totalTime)
fftDataFM100, fftFreqsFM100 = tFourier(FM100, rate)
print("Modulacion FM 125%")
FM125 = modFM(125, data, times, rate, totalTime)
fftDataFM125, fftFreqsFM125 = tFourier(FM125, rate)

# Graficos Espectros de frecuencia
print("Espectros de Frecuencia 15%")
plt.figure(1)
plt.subplot(311)
plt.title("Señal Entrante")
plt.plot(fftFreqs, abs(fftData))
plt.subplot(312)
plt.title("Señal Modulada AM 15%")
plt.plot(fftFreqsAM15, abs(fftDataAM15))
plt.subplot(313)
plt.title("Señal Modulada FM 15%")
plt.plot(fftFreqsFM15, abs(fftDataFM15))
plt.tight_layout()
plt.savefig("images/espectroFrecuencias15.png")
plt.show()

plt.figure(1)
print("Espectros de Frecuencia 100%")
plt.subplot(311)
plt.title("Señal Entrante")
plt.plot(fftFreqs, abs(fftData))
plt.subplot(312)
plt.title("Señal Modulada AM 100%")
plt.plot(fftFreqsAM100, abs(fftDataAM100))
plt.subplot(313)
plt.title("Señal Modulada FM 100%")
plt.plot(fftFreqsFM100, abs(fftDataFM100))
plt.tight_layout()
plt.savefig("images/espectroFrecuencias100.png")
plt.show()

plt.figure(1)
print("Espectros de Frecuencia 125%")
plt.subplot(311)
plt.title("Señal Entrante")
plt.plot(fftFreqs, abs(fftData))
plt.subplot(312)
plt.title("Señal Modulada AM 125%")
plt.plot(fftFreqsAM125, abs(fftDataAM125))
plt.subplot(313)
plt.title("Señal Modulada FM 125%")
plt.plot(fftFreqsFM125, abs(fftDataFM125))
plt.tight_layout()
plt.savefig("images/espectroFrecuencias125.png")
plt.show()

print("Ejecución Finalizada")
