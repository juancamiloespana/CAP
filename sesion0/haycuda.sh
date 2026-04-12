#!/bin/bash
#SBATCH --job-name=haycuda
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=gpu-20
#SBATCH --gres=gpu:A100
#SBATCH --output=haycuda.out
#SBATCH --error=haycuda.err
host=`hostname`
echo "Nodo de cálculo asignado: $host"

source /soft/miniconda3/etc/profile.d/conda.sh
conda activate cuda13

python3 haycuda.py