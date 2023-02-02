from functools import reduce
from re import split
from operator import itemgetter
from sys import argv


# Leer archivo línea por línea
# Retorna un generador
def leer(ruta):
    with open(ruta) as archivo:
        for linea in archivo:
            yield linea


# Limpiar una línea: Elimina '<num>=' y separa las palabras
def dividir(linea):
    palabras = split('([0-9]*=)|\n', linea)[2]
    return palabras.split(',')


# Closure para obtener los n-gramas de una lista de palabras
def getNGramas(n):
    # Retorna un generador
    # Cada n-grama es un string con todas las palabras
    # del n-grama separado por ','
    def getGramas(palabras):
        for i in range(0, len(palabras) - n + 1):
            yield ','.join(palabras[i:i + n])

    return getGramas


# Incrementa 1 al n-grama específico
# Recibe un diccionario y el n-grama,
# si el n-grama no existe en el diccionario
# lo inicializa en 1
def incrementar(resultado, nGrama):
    resultado[nGrama] = resultado.get(nGrama, 0) + 1
    return resultado


# Closure para contar los n-gramas en una línea
def contarNGramas(n):
    # Retorna un diccionario con n-grama como clave
    # y la cantidad de aparición como valor
    def contarGramas(linea):
        return reduce(incrementar, getNGramas(n)(dividir(linea)), {})
    return contarGramas


# Acumula los n-gramas de 'objGramas' en el diccionario 'resultado'
def acumularTotal(resultado, objGramas):
    # Recorre los elementos de 'objGramas' y los acumula
    for clave, valor in objGramas.items():
        resultado[clave] = resultado.get(clave, 0) + valor
    return resultado


# Función principal
# Cuenta la frecuencia de aparición de los n-gramas en todas las líneas
def contarFrecuenciaGramas(lineas, tamañoGramas):
    # Reduce que recibe un map con todos los diccionarios de cada línea
    return reduce(acumularTotal, map(contarNGramas(tamañoGramas), lineas), {})


# Guarda y formatea el resultado en un archivo específico
def guardarResultado(resultado, tamañoGramas, umbralFrecuencia, archivo):
    with open(archivo, 'w') as salida:
        descendente = sorted(resultado.items(), key=itemgetter(1), reverse=True)

        resultado = filter(lambda x: x[1] >= umbralFrecuencia, descendente)
        total = reduce(lambda x, y: y[0], enumerate(resultado))
        salida.write(f'Se encontraron {total + 1} gramas de tamaño {tamañoGramas}\n')

        impresion = (f'[{valor}]\t{clave}\n' for clave, valor in descendente if valor >= umbralFrecuencia)
        salida.writelines(impresion)


# Busca y cuenta los n-gramas específicos de un archivo y guarda el resultado
def busquedaGramas(archivoEntrada, tamañoGramas, umbralFrecuencia, archivoSalida):
    archivo = leer(archivoEntrada)
    resultado = contarFrecuenciaGramas(archivo, tamañoGramas)
    guardarResultado(resultado, tamañoGramas, umbralFrecuencia, archivoSalida)


def main(argumentos):
    # Lectura de argumentos
    if len(argumentos) < 4:
        print('Faltan Argumentos')
        exit(0)

    ## Archivo de entrada
    entrada = argumentos[0]
    ## Tamaño de los n-gramas
    tamañoGrama = int(argumentos[1])
    ## Umbral de Frecuencia para el resultado
    umbralFrecuencia = int(argumentos[2])
    ## Archivo de salida del resultado
    salida = argumentos[3]

    # Ejecución
    busquedaGramas(entrada, tamañoGrama, umbralFrecuencia, salida)


if __name__ == '__main__':
    main(argv[1:])

