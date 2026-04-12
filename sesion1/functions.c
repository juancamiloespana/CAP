#include <stdio.h>
#include "functions.h" 


void print_matrix(int rows, int columns, int **matrix)
{

if(rows <= 5 && columns <= 5) // Only print if the matrix is small enough
{
	for (int i=0;i<rows;i++)
	{
		printf("|");
		for (int j=0;j<columns;j++)
		{
			if (j>0) printf(" ");
			//printf("%d  (%p)", matrix[i][j], (void *)&matrix[i][j]);
			printf("%d  (%04lx)", matrix[i][j], (unsigned long)&matrix[i][j] & 0xFFFF);
		}
		printf("|\n");
	}

}

}