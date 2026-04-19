# CAP — Computación de Altas Prestaciones

A learning project exploring **high-performance computing (HPC)** through progressive matrix multiplication implementations. The goal is to understand how memory access patterns, language choice, and hardware (CPU vs GPU) affect performance.

---

## What this project is about

We implement the same algorithm — matrix multiplication — in increasingly powerful ways, and measure execution time to understand *why* one approach beats another. The key concepts under study are:

- **Memory access patterns** (cache locality, row-major vs column-major, blocking)
- **Language-level overhead** (pure Python vs C via ctypes vs native C)
- **GPU parallelism** (CUDA kernels on an A100 GPU)

This is a hands-on way to build intuition for the performance triangle: **algorithm × language × hardware**.

---

## Project structure

```
CAP/
├── sesion0/       CUDA environment check — verify the A100 GPU is available
├── sesion1/       Pure C — three multiplication strategies + timing (CPU)
├── sesion2/
│   ├── F1/        Pure Python — same three strategies, very slow baseline
│   ├── F2/        Python orchestrates C via ctypes (Python converts matrices)
│   └── F3/        Python orchestrates C via ctypes (C owns all memory)
└── Sesion3/       CUDA — GPU kernel (incomplete, work in progress)
```

---

## Sessions explained

### Session 0 — Verify CUDA
Quick check: does `torch.cuda.is_available()` return True on the HPC node?  
Submitted via SLURM requesting partition `gpu-20` (hosts A100 GPUs).

### Session 1 — C with three memory strategies
**File:** `sesion1/1-multiply_matrices.c`  
Compares three loop orderings for `C = A × B`:

| Strategy | Loop order | Why it matters |
|---|---|---|
| Row-major | i → j → k | A is accessed row-by-row (cache friendly) |
| Column-major | j → i → k | C is accessed column-by-column |
| Z-order (blocked) | blocks of i/k/j | Reuses cache lines for all three matrices |

The C code outputs CSV to stderr: `rows,cols,block_size,time_zorder,time_col,time_row`  
Build: `make` inside `sesion1/`  
Run via SLURM: `./script.sh <rows> <cols> <block_size>`

### Session 2 — Python/C hybrids via ctypes

**F1 — Pure Python baseline** (`sesion2/F1/2-multiply_matrices.py`)  
Same three algorithms in pure Python. Very slow: ~73 s for 1000×1000.  
This establishes the "worst case" baseline.

**F2 — ctypes with Python-side conversion** (`sesion2/F2/`)  
Python generates matrices as lists, converts them to C pointers, calls a shared library.  
The conversion overhead is included in measured time.  
The `.so` is built from `liboperations.c`.

**F3 — ctypes with C-side memory** (`sesion2/F3/`)  
Python only orchestrates: C allocates, fills, multiplies, and frees all memory.  
This removes Python-side overhead and shows the true cost of each algorithm.

Performance trend: F1 >> F2 > F3 (F3 fastest, F1 slowest by far).

### Session 3 — CUDA (in progress)
**File:** `Sesion3/3-multiply_matrices_cuda.cu`  
A GPU kernel where each thread computes one output cell `C[row][col]`.  
Still incomplete: missing argument parsing, thread grid setup, memory copies, and timing.

---

## How experiments run

All jobs go through **SLURM** (job scheduler on the HPC cluster at Universidad de Oviedo).  
Each `script.sh` wraps the executable in `sbatch` with a 10-minute time limit.

```bash
# Example: session 1
sbatch --wrap="./1-multiply_matrices 1000 1000 64" \
  --job-name=1-multiply_matrices --time=00:10:00 --nodes=1 --ntasks=1
```

Output lands in timestamped `.txt` files. Error output goes to `-error_*.txt` files.

---

## Build instructions

```bash
# Session 1 (C executable)
cd sesion1 && make

# Session 2 shared libraries
cd sesion2/F2 && gcc -shared -fPIC -o liboperations.so liboperations.c
cd sesion2/F3 && gcc -shared -fPIC -o liboperations.so liboperations.c

# Session 3 (CUDA — requires nvcc on HPC node)
nvcc -o 3-multiply_matrices_cuda Sesion3/3-multiply_matrices_cuda.cu
```

---

## Teaching goals & concepts to explain along the way

Because this is a **learning project**, Claude should explain concepts when relevant — not just write code. Key concepts to cover as they come up:

- **Cache lines and spatial locality** — why loop order matters
- **Z-order / Morton curves** — what blocking does for cache reuse
- **ctypes** — how Python talks to compiled C code, pointer semantics
- **CUDA grid/block/thread hierarchy** — how work is split across GPU threads
- **SLURM** — what job schedulers do and why HPC uses them
- **Timing accuracy** — `clock()` (CPU time) vs `time.time()` (wall time) vs CUDA events
- **Shared libraries (.so)** — compilation flags (`-shared -fPIC`), `dlopen` under the hood

---

## Current work in progress

- `sesion1/run_experiments.py` — script to sweep matrix sizes and block sizes, submit SLURM jobs, and collect CSV results. **Currently incomplete.**
- `Sesion3/3-multiply_matrices_cuda.cu` — CUDA kernel exists but main() is missing argument parsing, grid dimensions, cudaMemcpy calls, and event-based timing.

---

## Environment notes

- HPC cluster: `hpc.dptoinformatica.uniovi.es` (Universidad de Oviedo)
- GPU partition: `gpu-20` with NVIDIA A100 GPUs
- Conda environment: `cuda13` at `/soft/miniconda3/`
- C standard: C11 (`-std=c11 -Wall -Wextra -pedantic`)
- Python: Python 3 with standard library only (no numpy) in F1-F3

---

## Key files at a glance

| File | Purpose |
|---|---|
| `sesion1/1-multiply_matrices.c` | Three C multiplication kernels + timing |
| `sesion1/functions.c` | Matrix alloc/free/fill/print helpers |
| `sesion2/F1/2-multiply_matrices.py` | Pure Python baseline |
| `sesion2/F2/2-multiply_matrices_hybrid.py` | ctypes with Python matrix conversion |
| `sesion2/F2/liboperations.c` | Shared C library for F2 |
| `sesion2/F3/2-multiply_matrices_hybrid_pro.py` | ctypes with full C memory ownership |
| `sesion2/F3/liboperations.c` | Shared C library for F3 (adds alloc/free/generate) |
| `Sesion3/3-multiply_matrices_cuda.cu` | CUDA kernel (incomplete) |
| `sesion0/haycuda.py` | CUDA availability check |
