from functools import reduce
import re


def leer(ruta):
    with open(ruta) as archivo:
        for linea in archivo:
            yield linea


def dividir(linea):
    palabras = re.split('([0-9]*=)|\n', linea)[2]
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
    for clave in objGramas.keys():
        resultado[clave] = resultado.get(clave, 0) + objGramas[clave]
    return resultado


def contarFrecuenciaGramas(lineas, tamañoGramas):
    return reduce(acumularTotal, map(contarNGramas(tamañoGramas), lineas), {})


def guardarResultado(resultado, umbralFrecuencia, archivo):
    with open(archivo, 'w') as salida:
        descendente = sorted(resultado.keys(), key=lambda x: resultado[x], reverse=True)
        impresion = (f'[{resultado[x]}]\t{x}\n' for x in descendente if resultado[x] >= umbralFrecuencia)
        salida.writelines(impresion)


def busquedaGramas(archivoEntrada, tamañoGramas, umbralFrecuencia, archivoSalida):
    archivo = leer(archivoEntrada)
    resultado = contarFrecuenciaGramas(archivo, tamañoGramas)
    guardarResultado(resultado, umbralFrecuencia, archivoSalida)


def main():
    busquedaGramas('Ejemplo.txt', 2, 5, 'Resultado.txt')


if __name__ == '__main__':
    main()

