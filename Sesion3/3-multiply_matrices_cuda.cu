#include <stdio.h>
#include <cuda.h>
#include <stdlib.h>
#include <time.h>

// Function to allocate a matrix of size rows x cols
int *allocate_matrix(int rows, int cols)
{
    // We use calloc to allocate and initialize the memory to zero.
    int *matrix = (int *)calloc(rows * cols, sizeof(int));
    if (matrix == NULL)
    {
        fprintf(stderr, "Error: Could not allocate memory for the matrix.\n");
        return NULL;
    }

    return matrix;
}

// Function to generate a random matrix of size rows x cols
void generate_matrix(int rows, int cols, int *matrix)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            matrix[i *cols+ j] = rand() % 10; // Generate numbers between 0 and 9
        }
    }
}

__global__ void mul(int *A, int *B, int *C, int rows, int cols)
{

	int row= blockIdx.y*blockDim.y + threadIdx.y;
	int col= blockIdx.x*blockDim.x + threadIdx.x;






	if (row < rows && col < cols) 
	{
		int sum = 0;
    	int k;

		for (k=0; k<cols; k++)
		{   
			
			sum+=A[row*cols +k]*B[k*cols +col];
		}

		C[row*cols +col]=sum;

	}



}

int main(int argc, char *argv[])
{
    int rows, columns; // Matrix size (rows x columns), and block size for z-order
    size_t size;                   // Matrix size in bytes
    int *h_A, *h_B, *h_C;                // CPU matrices
    int *d_A, *d_B, *d_C;          // GPU matrices
    cudaEvent_t start, end;        // To measure time
    float ms;                      // Time in ms

    CudaEventCreate(&start);
    CudaEventCreate(&end);
    

    // Check if the required arguments are provided

    // Allocate memory for matrices in CPU

    // Generate random matrices
    srand(time(NULL)); // Initialize the random number generator once

    // Allocate memory for matrices in GPU
    size = rows * columns * sizeof(int);

    // Copy matrices from the CPU to the GPU

	cudaMemcpy(d_A, h_A, rows*cols*sizeof(int), cudaMemcpyHostToDevice);
	cudaMemcpy(d_B, h_B, rows*cols*sizeof(int), cudaMemcpyHostToDevice);
	cudaMemcpy(d_C, h_C, rows*cols*sizeof(int), cudaMemcpyHostToDevice);

    // Launch kernels multiplication and measure times
    mul<<<numBlocks, threadsPerBlock>>>(d_A, d_B, d_C, rows, columns, block_size);

    // Copy C from GPU to CPU

    printf("Time (seconds): %.5f\n", ms / 1000);

    // Free the memory of the matrices in CPU and GPU

    // Destroy time events

    return 0;
}