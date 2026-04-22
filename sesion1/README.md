# Sesión 1 — Multiplicación de matrices y acceso a memoria

> **Nota para el profesor:** El código ejecuta exactamente según la guía — se compila con `make` y se puede ejecutar con el Con el script de la guía sesion 1. Se creó un script.sh para facilitar ejecución `bash script.sh <filas> <cols> <block_size>` en el que difieren los nombre de los archivos de salida y además los envía al a carpeta `outputs/` que se crea automáticamente al primer lanzamiento. Los demás archivos adicionales se dejan como evidencia del trabajo realizado pero no son necesarios ni afectan la ejecución recomendada.

---

## Organización de archivos

```
sesion1/
├── 1-multiply_matrices.c   # Programa principal: recibe argumentos y ejecuta la multiplicación
├── functions.c / .h        # Implementación de los distintos métodos de multiplicación
├── Makefile                # Compila el proyecto con gcc
├── script.sh               # Lanza un job en SLURM con los parámetros dados
├── exp_run.py              # Orquesta los experimentos: genera combinaciones y llama a script.sh
├── exp_analysis.py         # Analiza y grafica los resultados desde los archivos de salida
└── outputs/                # Resultados generados: logs de experimentos realizados.
```

---

## Flujo de uso

### 1. Compilar

```bash
make
```

Genera el ejecutable `1-multiply_matrices`.

### 2. Ejecutar manualmente

```bash
bash script.sh <n_filas> <n_cols> <block_size>
```

Ejemplo:
```bash
bash script.sh 1024 1024 64
```
También funcióna el script de la guía de sesion 1.

Envía un job a SLURM que ejecuta `./1-multiply_matrices n_filas n_cols block_size` y guarda la salida en `outputs/`.

### 3. Orquestar experimentos

```bash
python exp_run.py
```

Genera automáticamente todas las combinaciones de dimensiones y tamaños de bloque definidas en los experimentos, y llama a `script.sh` por cada una. Soporta múltiples repeticiones para estimar variabilidad.

### 4. Analizar resultados

```bash
python exp_analysis.py
```

Lee los archivos de salida en `outputs/`, calcula estadísticas de error de medición y genera gráficas comparativas guardadas como PDF en `outputs/graphs/`.

> **Nota:** `exp_analysis.py` usa rutas relativas — debe ejecutarse desde la carpeta `sesion1/`, no desde un directorio superior.


---

## Experimentos definidos


| 0 | Aleatoriedad de tiempos (variabilidad) | matriz 1536×1536, bloque 512, 30 repeticiones |
| 1 | Barrido de tamaño de bloque 1 repetición| matrices 1024–3072, bloques 8–1024 |
| 2 | Barrido de tamaño de matriz con bloque fijo 5 repeticiones | matrices 1024–5120, bloque 512 |
