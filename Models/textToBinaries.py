from cmd import Cmd


class TextoBinarioApp(Cmd):
    def __init__(mi):
        super().__init__()
        mi.codigo = 'utf8'

    def do_codigo(mi, argumento):
        """Fija el código (ascii, utf8, etc.) que se usa para codificar/decodificar."""
        codigo = argumento.strip()
        try:
            bytearray('', codigo)
        except LookupError:
            print('**Código desconocido.')
        else:
            mi.codigo = codigo

    def do_codificar(mi, argumento):
        """Codifica un texto en binario."""
        try:
            octetos = bytearray(argumento, mi.codigo)
        except:
            print(f'**No se puede codificar en {mi.codigo}.')
        else:
            print(' '.join(f'{x:b}'.rjust(8, '0') for x in octetos))

    def do_decodificar(mi, argumento):
        """Decodifica un texto en binario."""
        try:
            octetos = bytearray(int(x, 2) for x in argumento.split())
        except:
            print('**No es una cadena binaria.')
            return None
        try:
            print(octetos.decode(encoding=mi.codigo))
        except:
            print(f'**No es una cadena codificada en {mi.codigo}')

    def do_salir(mi, arg):
        """Salir del programa."""
        return True


app = TextoBinarioApp()
app.cmdloop()