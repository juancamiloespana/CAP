import subprocess
import sys
import os
from datetime import datetime

sesion2_dir = os.path.dirname(os.path.abspath(__file__))

VALID_TARGETS = ["F1", "F2", "F3"]

if len(sys.argv) < 2 or sys.argv[1] not in VALID_TARGETS:
    print(f"Uso: python3 exp_run.py <{'|'.join(VALID_TARGETS)}> [prefijo]")
    sys.exit(1)

target = sys.argv[1]
_prefix = sys.argv[2] if len(sys.argv) > 2 else ""
script_dir = os.path.join(sesion2_dir, target)


def build_block_jobs(matrix_sizes, block_sizes):
    jobs = []
    for n in matrix_sizes:
        for b in block_sizes:
            jobs.append((n, n, b))
    return jobs


def submit_job(rows, cols, block_size, folder):
    result = subprocess.run(
        ["bash", "script.sh", str(rows), str(cols), str(block_size), folder],
        cwd=script_dir,
        capture_output=True,
        text=True
    )
    print(result.stdout.strip())


def run_experiment(name, matrix_sizes, block_sizes, repetitions=1):
    jobs = build_block_jobs(matrix_sizes, block_sizes)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = f"{_prefix}_{timestamp}" if _prefix else timestamp
    print(f"\n--- [{target}] {name} ({len(jobs)} jobs x {repetitions} repeticiones) ---")
    print(f"    carpeta: outputs/{folder}")
    for rep in range(repetitions):
        print(f"  [rep {rep + 1}/{repetitions}]")
        for rows, cols, block_size in jobs:
            submit_job(rows, cols, block_size, folder)
    print("All jobs submitted.")


#########################################################################################
#####----------------------- Experimento F1/F2/F3: Verificar tamaño usando dos tam de bloques ----------------#####
#########################################################################################

run_experiment(
    name="Aleatoriedad de tiempos de una misma configuración",
    matrix_sizes=[256, 512, 1024, 2048],
    block_sizes=[ 256, 512],
    repetitions=1,
)



# #########################################################################################
# #####----------------------- Experimento F2: Verificar tamaño usando dos tam de bloques ----------------#####
# #########################################################################################

# run_experiment(
#     name="Aleatoriedad de tiempos de una misma configuración",
#     matrix_sizes=[256, 512, 1024, 2048],
#     block_sizes=[ 256, 512],
#     repetitions=1,
# )

