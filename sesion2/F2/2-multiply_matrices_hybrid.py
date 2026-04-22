import sys
import random
import time
import ctypes
import os



script_dir = os.path.dirname(os.path.abspath(__file__))
lib = ctypes.CDLL(os.path.join(script_dir, "liboperations.so"))

pp_int = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

lib.row_major_mul.argtypes = [ctypes.c_int, ctypes.c_int,  pp_int, pp_int, pp_int]
lib.row_major_mul.restype = None

lib.column_major_mul.argtypes = [ctypes.c_int, ctypes.c_int,  pp_int, pp_int, pp_int]
lib.column_major_mul.restype = None

lib.zorder_mul.argtypes = [ctypes.c_int, ctypes.c_int, pp_int, pp_int, pp_int, ctypes.c_int]
lib.zorder_mul.restype = None


def convert_matrix(matrix):
      
	cols=len(matrix[0])
	rows=len(matrix)

	matrix_rows = [(ctypes.c_int*cols)(*row) for row in matrix]

	p_int=ctypes.POINTER(ctypes.c_int)
	c_matrix_pre = (p_int * rows)(*[ctypes.cast(r, ctypes.POINTER(ctypes.c_int)) for r in matrix_rows])
	
	c_matrix = ctypes.cast(c_matrix_pre, pp_int)

	return matrix_rows, c_matrix





def generate_matrix(rows, cols):
    """Create an array in Python as a list of lists."""
    return [[random.randint(0, 9) for _ in range(cols)] for _ in range(rows)]


   
if __name__ == "__main__":

	time_total_start = time.time()

	rows=int(sys.argv[1]) 
	cols=int(sys.argv[2])
	block_size=int(sys.argv[3])


	# rows=400
	# cols =400   
	# block_size=40
	
	# Generate random matrices

	A=generate_matrix(rows=rows, cols=cols)
	B=generate_matrix(rows=rows, cols=cols)

	C_RM = [[0] * cols for _ in range(rows)]  # Initialize C with zeros
	C_CM = [[0] * cols for _ in range(rows)]  # Initialize C with zeros
	C_Z = [[0] * cols for _ in range(rows)]  # Initialize C with zeros


	#### Transform to C matrix pointers ####

	A_C_rows, A_Cmatrix=convert_matrix(A)
	B_C_rows, B_Cmatrix=convert_matrix(B)
	C_C_RMrows, C_C_RM=convert_matrix(C_RM)
	C_C_CMrows, C_C_CM=convert_matrix(C_CM)
	C_C_Zrows, C_C_Z=convert_matrix(C_Z)
    



    # Multiply matrices and measure times
    
	start_time = time.time()
	lib.row_major_mul(rows, cols,A_Cmatrix, B_Cmatrix, C_C_RM)  ## call c function
	row_major_time = time.time() - start_time	

	start_time = time.time()
	lib.column_major_mul(rows, cols,A_Cmatrix, B_Cmatrix, C_C_CM) ## call c function
	column_major_time = time.time() - start_time

	start_time = time.time()
	lib.zorder_mul(rows, cols,A_Cmatrix, B_Cmatrix, C_C_Z, block_size)
	zorder_time = time.time() - start_time
    

	print(f"\n\n################ Parámetros ################\n")
	print(f"rows: {rows}\ncols: {cols}\nblock size: {block_size}")

	print(f"\n\n################ Tiempos ################\n")
	print(f"Row-major: {row_major_time:.6f} seconds")
	print(f"Column-major: {column_major_time:.6f} seconds")
	print(f"Z-order: {zorder_time:.6f} seconds")

	time_total = time.time() - time_total_start
	print(f"Total:    {time_total:.6f} seconds")

	print(f"{rows},{cols},{block_size},{zorder_time:.4f},{column_major_time:.4f},{row_major_time:.4f},{time_total:.4f}", file=sys.stderr)
