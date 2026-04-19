#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "functions.h"


// Function to allocate a matrix of size rows x columns
int **allocate_matrix(int rows, int columns)
{
    int **matrix = malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++)
    {
        matrix[i] = malloc(columns * sizeof(int));
    }


    return matrix;
}


// Function to free the memory of the matrix
void free_matrix(int rows, int **matrix)
{
    for (int i=0;i<rows;i++)
    {
        free(matrix[i]);
    }

    free(matrix);
}

// Function to generate a random matrix of size rows x columns
void generate_matrix(int rows, int columns, int **matrix)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < columns; j++)
        {
            matrix[i][j] = rand() % 10; // Generate numbers between 0 and 9
        }
    }
}

// Function to multiply matrices in row-major order
void row_major_mul(int rows, int columns, int **A, int **B, int **C)
{
    for (int i=0;i<rows;i++)
    {
        for (int k=0;k<columns;k++)
    	{
	
			for (int j=0;j<columns;j++)
			{
				C[i][j]+=A[i][k]*B[k][j];
			}
				
		}


    }
   
}

// Function to multiply matrices in column-major order
void column_major_mul(int rows, int columns, int **A, int **B, int **C)
{
    for (int j=0;j<rows;j++)
    {
        for (int k=0;k<rows;k++)
        {     
           for (int i=0;i<columns;i++)
           {
            C[i][j]+=A[i][k]*B[k][j];
           }
            
        }


    }
   
}

// Function to multiply matrices in Z order 
void zorder_mul(int rows, int columns, int **A, int **B, int **C, int block_size)
{
    for (int iB=0;iB<rows;iB+=block_size) //indice para fila de bloque salida
    {
        for (int kB=0;kB<rows;kB+=block_size) //indice para columna de bloque salida
        {
            for (int jB=0;jB<columns;jB+=block_size) //indice compartido bloque entrada
            {
                for (int i=iB;i<iB+block_size && i<rows;i++)  //indice para fila de salida
                {       
                    for(int k=kB;k<kB+block_size && k<rows;k++)  //indice para fila de salida
                    {       
                        for (int j=jB;j<jB+ block_size && j<columns;j++)
                            {
                                C[i][j]+=A[i][k]*B[k][j];
                            }
                        
                    }
            
                }
            }
        }
    }
                  
}

int main(int argc, char *argv[])
{
 
    int rows, columns, block_size;                               // Matrix size (rows x columns)
    int **A, **B, **C_rows, **C_columns, **C_zorder; // Matrices
    clock_t start, end;                              // To measure time

    //Get matrices size

    rows= atoi(argv[1]);
    columns= atoi(argv[2]);
    block_size= atoi(argv[3]);
 

    // Allocate memory for matrices

    A=allocate_matrix(rows,columns);
    B=allocate_matrix(rows,columns);
    C_rows=allocate_matrix(rows,columns);
    C_columns=allocate_matrix(rows,columns);
    C_zorder=allocate_matrix(rows,columns);

    

    // Generate random matrices

    srand(35); // Initialize the random number generator once
    
    generate_matrix(rows,columns, A);
    generate_matrix(rows,columns, B);
   

	
	printf("\n\n################ Parámetros ################\n\n");
	printf("rows: %d\ncolumns: %d\nblock size: %d", rows, columns, block_size);
    
	// multiply matrices and measure times
	printf("\n\n################Tiempos ################\n\n");
   
	
    start = clock();
    zorder_mul(rows, columns, A, B, C_zorder, block_size);
    end = clock();
	double time_zorder = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Z-order: %f seconds\n", time_zorder);

    start = clock();
    column_major_mul(rows, columns, A, B, C_columns);
    end = clock();
	double time_column = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Column-major: %f seconds\n", time_column);

	start = clock();
    row_major_mul(rows, columns, A, B, C_rows);
    end = clock();
	double time_row = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Row-major: %f seconds\n", time_row);

	

	
	printf("\n\n################ Valores y direcciones ################\n\n");
	if(rows <= 5 && columns <= 5) // Only print if the matrix is small enough
	{
		
		printf("\nA (%d x %d):\n\n", rows, columns);
		print_matrix(rows, columns, A);
		printf("\nB (%d x %d):\n\n", rows, columns);
		print_matrix(rows, columns, B);
		printf("\nC_rows (%d x %d):\n\n", rows, columns);
		print_matrix(rows, columns, C_rows);
		printf("\nC_columns (%d x %d):\n\n", rows, columns);
		print_matrix(rows, columns, C_columns);
		printf("\nC_zorder (%d x %d):\n\n", rows, columns);
		print_matrix(rows, columns, C_zorder);
	}
	else
	{
		printf("Matrixes are too large to print.\n");
	}


	fprintf(stderr, "%d,%d,%d,%.4f,%.4f,%.4f\n", rows,columns,block_size,time_zorder,time_column,time_row);



    // Free matrices

    free_matrix(rows, A);
    free_matrix(rows, B);
    free_matrix(rows, C_rows  );
    free_matrix(rows, C_columns);
    free_matrix(rows, C_zorder);

    

    return 0;
}