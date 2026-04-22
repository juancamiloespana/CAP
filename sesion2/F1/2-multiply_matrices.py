import sys
import random
import time


def generate_matrix(rows, cols):
    return [[random.randint(0, 9) for _ in range(cols)] for _ in range(rows)]


def row_major_mul(A, B, C, rows, cols):
    for i in range(rows):
        for k in range(cols):
            for j in range(cols):
                C[i][j] += A[i][k] * B[k][j]


def column_major_mul(A, B, C, rows, cols):
    for j in range(cols):
        for k in range(cols):
            for i in range(rows):
                C[i][j] += A[i][k] * B[k][j]


def zorder_mul(A, B, C, rows, cols, block_size):
    for ib in range(0, rows, block_size):
        for kb in range(0, rows, block_size):
            for jb in range(0, cols, block_size):
                for i in range(ib, min(ib + block_size, rows)):
                    for k in range(kb, min(kb + block_size, rows)):
                        for j in range(jb, min(jb + block_size, cols)):
                            C[i][j] += A[i][k] * B[k][j]


if __name__ == "__main__":

    time_total_start = time.time()

    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
    block_size = int(sys.argv[3])

    random.seed(35)

    A = generate_matrix(rows, cols)
    B = generate_matrix(rows, cols)

    print(f"\n\n################ Parámetros ################\n")
    print(f"rows: {rows}\ncols: {cols}\nblock size: {block_size}")

    print(f"\n\n################ Tiempos ################\n")

    C_row = [[0] * cols for _ in range(rows)]
    start_time = time.time()
    row_major_mul(A, B, C_row, rows, cols)
    time_row = time.time() - start_time
    print(f"Row-major: {time_row:.6f} seconds")

    C_col = [[0] * cols for _ in range(rows)]
    start_time = time.time()
    column_major_mul(A, B, C_col, rows, cols)
    time_col = time.time() - start_time
    print(f"Column-major: {time_col:.6f} seconds")

    # time_col = 0.0  ### para pruebas de Z-order, ignorar tiempos de row y col
    # time_row = 0.0

    C_zorder = [[0] * cols for _ in range(rows)]
    start_time = time.time()
    zorder_mul(A, B, C_zorder, rows, cols, block_size)
    time_zorder = time.time() - start_time
    print(f"Z-order: {time_zorder:.6f} seconds")

    time_total = time.time() - time_total_start
    print(f"Total:    {time_total:.6f} seconds")

    print(f"{rows},{cols},{block_size},{time_zorder:.4f},{time_col:.4f},{time_row:.4f},{time_total:.4f}", file=sys.stderr)
