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

## sesion2 analysis pipeline (completed)

### exp_analysis.py (`sesion2/exp_analysis.py`)
Single script that loads, analyzes and plots all three phases. Run from `sesion2/` directory.

**Functions:**
- `load_logs(folder)` — reads all `logs_*.txt` from `outputs/<folder>/`, returns DataFrame
- `compare_block_sizes(df)` — prints Z-order pivot table for b=256 vs b=512
- `table_times(df, label)` — prints mean times per method and matrix size
- `table_diff_vs_row(df, label)` — prints differences vs row-major as base (`*` marks baseline)
- `plot_methods(df, title, path)` — line chart: three methods vs matrix size
- `plot_total_vs_sum(df, title, path)` — line chart: time_total vs Sum_times

**Per-phase pattern** (F1, F2, F3):
1. `load_logs(FOLDER)` with b=256 filter
2. `df["Sum_times"] = time_zorder + time_row + time_col`
3. `compare_block_sizes` → `table_times` → `table_diff_vs_row` → `plot_methods` → `plot_total_vs_sum`

**Comparative section** generates two layout figures:
- `comp_total_sum.pdf` — subplot left: time_total, subplot right: Sum_times, all three phases
- `comp_metodos.pdf` — three subplots, one per method (row/col/zorder), all three phases

**Output graphs saved to:** `sesion2/outputs/graphs/`

### Experiment folders used
| Phase | Folder |
|---|---|
| F1 | `F1_met_size_2026-04-22_10-59-59` |
| F2 | `F2_met_size_2026-04-22_11-00-04` |
| F3 | `F3_met_size_2026-04-22_11-00-09` |

### Key experimental findings
- Block size (b=256 vs b=512) has no significant effect in any phase (<2%)
- **F1**: column-major slowest, z-order fastest; total ≈ sum (overhead negligible)
- **F2**: row-major becomes slowest for large N (inverted vs expected); total - sum = 1-6s (Python conversion overhead)
- **F3**: same method order as F2; total - sum ≈ 0.07-0.6s (only interpreter startup overhead)
- F1 is ~14-17× slower than F2/F3 for 2048×2048; F2 and F3 multiplication times are indistinguishable
- In F2, row-major being slower than column-major for large N is hypothesized to relate to pointer array access patterns and prefetcher behavior with dispersed row memory layout

### LaTeX report
`sesion2/F2/informe.tex` — sections for F1, F2, F3, and comparative analysis with figure references.
Figures referenced from `images/` folder (same names as `outputs/graphs/` PDFs/PNGs).

---

## Environment notes

- HPC cluster: `hpc.dptoinformatica.uniovi.es` (Universidad de Oviedo)
- SSH alias: `hpc-uo` (configured with SSH keys, no password needed)
- Remote structure: sessions live directly in `~/sesion1/`, `~/sesion2/`, etc. — no `CAP/` parent folder
- Sync command: `rsync -av sesion1/ hpc-uo:~/sesion1/`
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
