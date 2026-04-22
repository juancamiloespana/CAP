#!/bin/bash
mkdir -p outputs
JOB_ID=$(sbatch --parsable --wrap="./1-multiply_matrices $1 $2 $3" \
  --job-name=1-multiply_matrices \
  --output=outputs/results_${1}x${2}_b${3}_%j.txt \
  --error=outputs/logs_${1}x${2}_b${3}_%j.txt \
  --time=10:50:00 \
  --nodes=1 \
  --ntasks=1)
echo "Submitted job $JOB_ID: ${1}x${2} block=${3}"