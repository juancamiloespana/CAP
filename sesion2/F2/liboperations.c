#include <stdlib.h>


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
    for (int j=0;j<columns;j++)
    {
        for (int k=0;k<columns;k++)
        {
            for (int i=0;i<rows;i++)
           {
            C[i][j]+=A[i][k]*B[k][j];
           }
        }
    }
}

// Function to multiply matrices in Z order
void zorder_mul(int rows, int columns, int **A, int **B, int **C, int block_size)
{
    for (int iB=0;iB<rows;iB+=block_size)
    {
        for (int kB=0;kB<rows;kB+=block_size)
        {
            for (int jB=0;jB<columns;jB+=block_size)
            {
                for (int i=iB;i<iB+block_size && i<rows;i++)
                {
                    for (int k=kB;k<kB+block_size && k<rows;k++)
                    {
                        for (int j=jB;j<jB+block_size && j<columns;j++)
                            {
                                C[i][j]+=A[i][k]*B[k][j];
                            }
                    }
                }
            }
        }
    }
}