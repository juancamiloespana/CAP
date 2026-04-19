import sys
import random
import time



def generate_matrix(rows, cols):
    """Create an array in Python as a list of lists."""
    return [[random.randint(0, 9) for _ in range(cols)] for _ in range(rows)]


def row_major_mul(A, B, C):
    """Multiplication of matrices in row-major order."""

    rows=len(A[0])
    cols=len(B[0])

    for i in range(rows):
        for j in range(cols):
            for k in range(cols):
                C[i][j] += A[i][k] * B[k][j]

    return C

    
def column_major_mul(A, B, C):
    """Multiplication of matrices in column-major order."""

    rows=len(A[0])
    cols=len(B[0])
    
    for j in range(cols):
        for i in range(rows):
            for k in range(cols):
                C[i][j] += A[i][k] * B[k][j]

    return C

    
def zorder_mul(A, B, C, block_size):
    """Matrix multiplication in Z order (Morton Order)."""
    
    rows=len(A[0])
    cols=len(B[0])

    for ib in range(0, rows, block_size):
        for jb in range(0, cols, block_size):
            for kb in range(0, cols, block_size):
                for i in range(ib, min(ib + block_size, rows)):
                   for j in range(jb, min(jb + block_size, cols)):
                        for k in range(kb, min(kb + block_size, cols)):
                             C[i][j] += A[i][k] * B[k][j]

    return C

    
if __name__ == "__main__":
    
    # Get matrices size
    
	rows=int(sys.argv[1]) 
	cols=int(sys.argv[2])
	block_size=int(sys.argv[3])

	# rows=400
	# cols =400   
	# block_size=40
	
	# Generate random matrices

	A=generate_matrix(rows=rows, cols=cols)
	B=generate_matrix(rows=rows, cols=cols)

	C = [[0] * cols for _ in range(rows)]  # Initialize C with zeros
    
    # Multiply matrices and measure times
    
	start_time = time.time()
	row_major_mul(A, B, C)
	row_major_time = time.time() - start_time	

	start_time = time.time()
	column_major_mul(A, B, C)
	column_major_time = time.time() - start_time

	start_time = time.time()
	zorder_mul(A, B, C, block_size=2)
	zorder_time = time.time() - start_time
    

	print(f'{rows}, Cols={cols}, block_size={block_size}')
	print(f'Row-major time: {row_major_time:.6f} seconds')
	print(f'Column-major time: {column_major_time:.6f} seconds')
	print(f'Z-order time: {zorder_time:.6f} seconds')
		
	
    