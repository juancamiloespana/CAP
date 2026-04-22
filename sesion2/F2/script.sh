#!/bin/bash
SOURCE=$(basename "$(dirname "$(realpath "$0")")")
TIMESTAMP=${4:-$(date +%Y-%m-%d_%H-%M-%S)}
FOLDER="${SOURCE}_${TIMESTAMP}"
mkdir -p ../outputs/$FOLDER
JOB_ID=$(sbatch --parsable --wrap="python3 2-multiply_matrices_hybrid.py $1 $2 $3" \
  --job-name=2-multiply_matrices_hybrid \
  --output=../outputs/$FOLDER/results_${1}x${2}_b${3}_%j.txt \
  --error=../outputs/$FOLDER/logs_${1}x${2}_b${3}_%j.txt \
  --time=00:10:00 \
  --nodes=1 \
  --ntasks=1)
echo "Submitted job $JOB_ID: ${1}x${2} block=${3} -> outputs/$FOLDER"