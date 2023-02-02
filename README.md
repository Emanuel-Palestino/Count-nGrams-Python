# n-Grams Counter in Python
A n-grams searcher and counter in python without use of libraries

## Usage

### Input File
Each line on input file have the next sintax:
```
<number line>=<word>,<word>,...,<word>
```
Example:
```
12=hola,como,estas
```

### Output File
Output File have the next content:
```
Se encontraron <m> gramas de tamaño <n>
[x_1]   n-gram
[x_2]   n-gram
...
```
Where m is the number of n-grams found which x_i >= frequency_threshold; n is the size of the n-grams; and x_i is the frecuency of the n-gram in the input file.

### Execute
```bash
python3 busqueda.py <input file> <n-grams size> <frequency threshold> <output file>
```
