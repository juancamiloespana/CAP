# CAP
Codigos curso computación de altas prestaciones

## Contenido

### Sesion 0 — Verificación de entorno CUDA
Scripts para comprobar disponibilidad de GPU/CUDA usando PyTorch.

- `haycuda.py` / `haycuda2.py` — verifican si `torch.cuda.is_available()` y reportan el resultado.
- `haycuda.sh` — script de shell para lanzar la verificación.

### Sesion 1 — Multiplicación de matrices en C (memoria y acceso)
Implementación en C puro que compara tres estrategias de multiplicación de matrices cuadradas, midiendo el impacto del patrón de acceso a memoria en el rendimiento.

- `1-multiply_matrices.c` + `functions.c/h` — implementación de las tres estrategias:
  - **Row-major**: recorre la matriz resultado fila por fila.
  - **Column-major**: recorre la matriz resultado columna por columna.
  - **Z-order (Morton order)**: multiplica por bloques para mejorar localidad de caché.
- `Makefile` — compila el ejecutable con las dependencias.
- `script.sh` — lanza pruebas con distintos tamaños de matriz y tamaños de bloque.
- Archivos `*.txt` — resultados de ejecución con tiempos medidos.

### Sesion 2 — Multiplicación de matrices híbrida Python/C
Tres formulaciones progresivas que combinan Python con código C compilado como biblioteca compartida.

#### F1 — Python puro
- `2-multiply_matrices.py` — implementa row-major, column-major y Z-order directamente en Python.
- `script.sh` + archivos `*.txt` de resultados.

#### F2 — Python + ctypes (matrices Python convertidas a punteros C)
- `liboperations.c` — funciones de multiplicación compiladas como `.so`.
- `2-multiply_matrices_hybrid.py` — genera matrices en Python, las convierte a punteros C con `ctypes` y delega el cálculo a la librería.
- `script.sh` + archivos `*.txt` de resultados.

#### F3 — Python + ctypes (allocación completa en C)
- `liboperations.c` — extiende la librería con `allocate_matrix`, `generate_matrix` y `free_matrix`.
- `2-multiply_matrices_hybrid_pro.py` — toda la memoria se maneja en C; Python sólo orquesta las llamadas y mide tiempos.
- `script.sh` + archivos `*.txt` de resultados.

### Sesion 3 *(pendiente)*
Directorio reservado para contenido futuro del curso.
