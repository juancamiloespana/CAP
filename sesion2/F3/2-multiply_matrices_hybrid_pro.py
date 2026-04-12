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

lib.allocate_matrix.argtypes = [ctypes.c_int, ctypes.c_int]
lib.allocate_matrix.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

lib.free_matrix.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_int))]
lib.free_matrix.restype = None

lib.generate_matrix.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_int))]
lib.generate_matrix.restype = None



def convert_matrix(matrix):
      
	cols=len(matrix[0])
	rows=len(matrix)

	matrix_rows = [(ctypes.c_int*cols)(*row) for row in matrix]

	p_int=ctypes.POINTER(ctypes.c_int)
	c_matrix_pre = (p_int * rows)(*[ctypes.cast(r, ctypes.POINTER(ctypes.c_int)) for r in matrix_rows])
	
	c_matrix = ctypes.cast(c_matrix_pre, pp_int)

	return matrix_rows, c_matrix



   
if __name__ == "__main__":
    
    # Get matrices size
    
	rows=int(sys.argv[1]) 
	cols=int(sys.argv[2])
	block_size=int(sys.argv[3])


     #allocate matrixes
	A_address=lib.allocate_matrix(rows, cols)
	B_address=lib.allocate_matrix(rows, cols)
	C_RM_address=lib.allocate_matrix(rows, cols)
	C_CM_address=lib.allocate_matrix(rows, cols)
	C_ZO_address=lib.allocate_matrix(rows, cols)

	


	#### generate matrixes ####

	lib.generate_matrix(rows, cols, A_address)
	lib.generate_matrix(rows, cols, B_address)
	



    # Multiply matrices and measure times
    
	start_time = time.time()
	lib.row_major_mul(rows, cols, A_address, B_address, C_RM_address)  ## call c function
	row_major_time = time.time() - start_time	

	start_time = time.time()
	lib.column_major_mul(rows, cols,A_address, B_address, C_CM_address) ## call c function
	column_major_time = time.time() - start_time

	start_time = time.time()
	lib.zorder_mul(rows, cols,A_address, B_address, C_ZO_address, block_size)
	zorder_time = time.time() - start_time
    

	print(f'{rows}, Cols={cols}, block_size={block_size}')
	print(f'Row-major time: {row_major_time:.6f} seconds')
	print(f'Column-major time: {column_major_time:.6f} seconds')
	print(f'Z-order time: {zorder_time:.6f} seconds')
		
	
    
	lib.free_matrix(rows, A_address)
	lib.free_matrix(rows, B_address)
	lib.free_matrix(rows, C_RM_address)
	lib.free_matrix(rows, C_CM_address)
	lib.free_matrix(rows, C_ZO_address)