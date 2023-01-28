from functools import reduce
from re import split
from operator import itemgetter
from sys import argv


def leer(ruta):
    with open(ruta) as archivo:
        for linea in archivo:
            yield linea


def dividir(linea):
    palabras = split('([0-9]*=)|\n', linea)[2]
    return palabras.split(',')


def getNGramas(n):
    def getGramas(palabras):
        for i in range(0, len(palabras) - n + 1):
            yield ','.join(palabras[i:i + n])

    return getGramas


def incrementar(resultado, nGrama):
    resultado[nGrama] = resultado.get(nGrama, 0) + 1
    return resultado


def contarNGramas(n):
    def contarGramas(linea):
        return reduce(incrementar, getNGramas(n)(dividir(linea)), {})
    return contarGramas


def acumularTotal(resultado, objGramas):
    for clave, valor in objGramas.items():
        resultado[clave] = resultado.get(clave, 0) + valor
    return resultado


def contarFrecuenciaGramas(lineas, tamañoGramas):
    return reduce(acumularTotal, map(contarNGramas(tamañoGramas), lineas), {})


def guardarResultado(resultado, umbralFrecuencia, archivo):
    with open(archivo, 'w') as salida:
        descendente = sorted(resultado.items(), key=itemgetter(1), reverse=True)
        impresion = (f'[{valor}]\t{clave}\n' for clave, valor in descendente if valor >= umbralFrecuencia)
        salida.writelines(impresion)


def busquedaGramas(archivoEntrada, tamañoGramas, umbralFrecuencia, archivoSalida):
    archivo = leer(archivoEntrada)
    resultado = contarFrecuenciaGramas(archivo, tamañoGramas)
    guardarResultado(resultado, umbralFrecuencia, archivoSalida)


def main(argumentos):
    entrada = argumentos[0]
    tamañoGrama = int(argumentos[1])
    umbralFrecuencia = int(argumentos[2])
    salida = argumentos[3]
    busquedaGramas(entrada, tamañoGrama, umbralFrecuencia, salida)


if __name__ == '__main__':
    main(argv[1:])

