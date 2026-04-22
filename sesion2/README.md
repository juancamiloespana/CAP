# Sesion 2 — Multiplicación de matrices: Python puro y ctypes

Tres implementaciones del mismo algoritmo para comparar rendimiento:

| Carpeta | Estrategia |
|---|---|
| `F1/` | Python puro |
| `F2/` | Python llama a C via ctypes (Python convierte las matrices) |
| `F3/` | Python llama a C via ctypes (C gestiona toda la memoria) |

Todas implementan los mismos tres algoritmos: **row-major**, **column-major**, **z-order (blocked)**.

---

## Estructura

```
sesion2/
├── exp_run.py          Orquestador de experimentos SLURM
├── outputs/            Resultados de todos los jobs
├── F1/
│   ├── 2-multiply_matrices.py
│   └── script.sh
├── F2/
│   ├── 2-multiply_matrices_hybrid.py
│   ├── liboperations.c
│   ├── Makefile
│   └── script.sh
└── F3/
    ├── 2-multiply_matrices_hybrid_pro.py
    ├── liboperations.c
    ├── Makefile
    └── script.sh
```

---

## Setup (solo F2 y F3, una vez por sesión)

```bash
cd ~/sesion2/F2 && make
cd ~/sesion2/F3 && make
```

---

## Ejecución manual (un job)

```bash
cd ~/sesion2/F1
bash script.sh <rows> <cols> <block_size> [carpeta]

# Ejemplo:
bash script.sh 512 512 64
bash script.sh 512 512 64 prueba1
```

Salida en `sesion2/outputs/<F1|F2|F3>_[prefijo_]<timestamp>/`. El prefijo de subcarpeta lo agrega el script automáticamente.

---

## Ejecución orquestada (múltiples jobs)

```bash
cd ~/sesion2
python3 exp_run.py <F1|F2|F3> [prefijo]

# Ejemplos:
python3 exp_run.py F1
python3 exp_run.py F2 barrido1
```

Todos los jobs del mismo experimento van a `outputs/<F1|F2|F3>_[prefijo_]<timestamp>/`.  
Editar los experimentos activos directamente en `exp_run.py`.

---

## Argumentos

| Arg | Descripción |
|---|---|
| `rows` | Número de filas (= columnas) |
| `cols` | Número de columnas |
| `block_size` | Tamaño de bloque para z-order |

## Salidas por job

| Archivo | Contenido |
|---|---|
| `results_*.txt` | stdout: parámetros y tiempos por algoritmo |
| `logs_*.txt` | stderr: línea CSV `rows,cols,block_size,t_zorder,t_col,t_row,t_total` |
