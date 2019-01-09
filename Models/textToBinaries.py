
class TextoBinario:

    codigo = ''

    """
    Entrada: -
    Procedimiento: Crea el objeto
    Salida: -
    """

    def __init__(self):
        self.codigo = 'utf8'

    """
    Entrada: Entra el objeto a utilizar y la letra a convertir a binario
    Procedimiento: Realiza la conversion de la letra a binario, que contiene 8 bits
    Salida: Entrega el arreglo de bit donde contiene la letra ingresada en binarios
    """

    def do_codificar(self,mi, argumento):
        """Codifica un texto en binario."""
        try:
            octetos = bytearray(argumento, mi.codigo)
        except:
            print(f'**No se puede codificar en {mi.codigo}.')
        else:
            #print(' '.join(f'{x:b}'.rjust(8, '0') for x in octetos))
            #print(octetos)
            c = []
            d = []
            for x in octetos:
                print(x)
                a = ''.join(f'{x:b}'.rjust(8,'0') )
                print(a)
                for x1 in a:
                    c.append(x1)
            print(c)

            for elemento in c:
                if elemento == '0':
                    d.append(0)
                else:
                    d.append(1)
            #print(d)
            return d

    """
    Entrada: Entra el objeto a utilizar y una cadena de bit.
    Procedimiento: Convierte esa cadena de bits en la letra que corresponde.
    Salida: Entrega la letra corresondiente a la cadena de bits ingresada.
    """

    def do_decodificar(self, mi, argumento):
        """Decodifica un texto en binario."""
        try:
            print(argumento)
            octetos = bytearray(int(x, 2) for x in argumento.split())
            print(octetos)
        except:
            print('**No es una cadena binaria.')
            return None
        try:
            print("estamos aca")
            print(octetos.decode(encoding=mi.codigo))
            return octetos.decode(encoding=mi.codigo)
        except:
            print(f'**No es una cadena codificada en {mi.codigo}')
