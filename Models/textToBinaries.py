
class TextoBinario :

    codigo = ''

    def __init__(self):
        self.codigo = 'utf8'

    def do_codigo(self,mi, argumento):
        """Fija el código (ascii, utf8, etc.) que se usa para codificar/decodificar."""
        codigo = argumento.strip()
        try:
            bytearray('', codigo)
        except LookupError:
            print('**Código desconocido.')
        else:
            mi.codigo = codigo

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

    def do_decodificar(self,mi, argumento):
        """Decodifica un texto en binario."""
        try:
            octetos = bytearray(int(x, 2) for x in argumento.split())
        except:
            print('**No es una cadena binaria.')
            return None
        try:
            #print("estamos aca")
            #print(octetos.decode(encoding=mi.codigo))
            return octetos.decode(encoding=mi.codigo)
        except:
            print(f'**No es una cadena codificada en {mi.codigo}')

    def do_salir(self,mi, arg):
        """Salir del programa."""
        return True