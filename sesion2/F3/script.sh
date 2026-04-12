#!/bin/bash
sbatch --wrap="python3 2-multiply_matrices_hybrid_pro.py $1 $2 $3" \
  --job-name=2-multiply_matrices_hybrid_pro \
  --output=2-multiply_matrices_hybrid_pro_$(date +%Y-%m-%d_%H-%M-%S).txt \
  --error=2-multiply_matrices_hybrid_pro-error_$(date +%Y-%m-%d_%H-%M-%S).txt \
  --time=00:10:00 \
  --nodes=1 \
  --ntasks=1