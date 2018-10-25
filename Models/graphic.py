from numpy import linspace
import matplotlib.pyplot as plt

    #Clase que se encarga de tener los distintos graficos necesarios
class Graphic:

    def __init__(self):
        super(Graphic, self).__init__()

    def makeGraphic(self,title, xlabel, xdata, ylabel, ydata):
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.plot(xdata, ydata)
        plt.savefig(title + ".png")
        return

    def timeGraphic(self,data, duration):

        t = linspace(0, duration, len( data ))
        self.makeGraphic("Audio original", "Tiempo [s]", t, "Amplitud [dB]", data)
        plt.show()
        return

