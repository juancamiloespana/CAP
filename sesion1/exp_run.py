import subprocess
import os
import time

# Directorio donde se encuentra este script (para localizar script.sh)
script_dir = os.path.dirname(os.path.abspath(__file__))


def build_block_jobs(matrix_sizes, block_sizes):
    # Genera todas las combinaciones (filas, cols, bloque) como lista de tuplas
    jobs = []
    for n in matrix_sizes:
        for b in block_sizes:
            jobs.append((n, n, b))
    return jobs


def submit_job(rows, cols, block_size, script_dir):
    # Ejecuta script.sh con los parámetros dados y muestra la salida por consola
    result = subprocess.run(
        ["bash", "script.sh", str(rows), str(cols), str(block_size)],
        cwd=script_dir,
        capture_output=True,
        text=True
    )



def run_experiment(name, matrix_sizes, block_sizes, repetitions=1):
    # Corre todas las combinaciones de dimensión y bloque, repetidas `repetitions` veces
    jobs = build_block_jobs(matrix_sizes, block_sizes)
    print(f"\n--- {name} ({len(jobs)} jobs x {repetitions} repeticiones) ---")
    for rep in range(repetitions):
        print(f"  [rep {rep + 1}/{repetitions}]")
        for rows, cols, block_size in jobs:
            # time.sleep(1)  # Pequeña pausa entre jobs para evitar saturar el sistema
            submit_job(rows, cols, block_size, script_dir)
    print("All jobs submitted.")



#########################################################################################
#####----------------------- Experimento 0: verificar aleatoriedad de tiempos-------#####
#########################################################################################

# run_experiment(
#     name="Aleatoriedad de tiempos de una misma configuración",
#     matrix_sizes=[1536],
#     block_sizes=[ 512],
#     repetitions=30,
# )


# #########################################################################################
# #####----------------------- Experimento 1: Barrido de block size ------------------#####
# #########################################################################################

run_experiment(
    name="Barrido de block size",
    matrix_sizes=[1024, 2048, 3072],
    block_sizes=[8, 16, 32, 64, 128, 256, 512, 1024],
    repetitions=5,
)


# #########################################################################################
# #####          Experimento 2: Tamaño de matrices con bloque fijo (b=512)         ########
# #########################################################################################

# run_experiment(
#     name="Tamaño de matrices con bloque fijo (b=512)",
#     matrix_sizes=[1024, 2048, 3072, 4096, 5120],
#     block_sizes=[512],
#     repetitions=5,
# )
