#include <stdlib.h>



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
        for (int j=0;j<columns;j++)
        {
         
           for (int k=0;k<rows;k++)
           {
            C[i][j]+=A[i][k]*B[k][j];
           }
            
        }


    }
   
}


// Function to multiply matrices in column-major order
void column_major_mul(int rows, int columns, int **A, int **B, int **C)
{
    for (int j=0;j<columns;j++)
    {
        for (int i=0;i<rows;i++)
        {
            for (int k=0;k<columns;k++)
           {
            C[i][j]+=A[i][k]*B[k][j];
           }
            
        }


    }
   
}

// Function to multiply matrices in Z order row-major order
void zorder_mul(int rows, int columns, int **A, int **B, int **C, int block_size)
{
    for (int iB=0;iB<rows;iB+=block_size) //indice para fila de bloque salida
    {
        for (int jB=0;jB<columns;jB+=block_size) //indice para columna de bloque salida
        {
            for (int kB=0;kB<rows;kB+=block_size) //indice compartido bloque entrada
            {
                for (int i=iB;i<iB+block_size && i<rows;i++)  //indice para fila de salida
                {       
                    for(int j=jB;j<jB+ block_size && j<columns;j++)  //indice para fila de salida
                    {       
                        for (int k=kB;k<kB+block_size && k<rows;k++)
                            {
                                C[i][j]+=A[i][k]*B[k][j];
                            }
                        
                    }
            
                }
            }
        }
    }
                  
}