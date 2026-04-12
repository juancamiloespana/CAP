#!/bin/bash
sbatch --wrap="./1-multiply_matrices $1 $2 $3" \
  --job-name=1-multiply_matrices \
  --output=1-matrices_access_$(date +%Y-%m-%d_%H-%M-%S).txt \
  --error=1-multiply_matrices-error_$(date +%Y-%m-%d_%H-%M-%S).txt \
  --time=00:10:00 \
  --nodes=1 \
  --ntasks=1