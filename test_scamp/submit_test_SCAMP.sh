#!/bin/bash

# Nombre del trabajo
#SBATCH --job-name=test_pyscamp.py
# Archivo de salida
#SBATCH --output=salida.txt
# Partición CPUS
#SBATCH --partition=512x1024
# Partición GPUS
##SBATCH --partition=gpus
# Solicitud de cpus
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
# Solicitud de GPUS
##SBATCH --gres=gpu:1
#SBATCH --mail-user=leoncio.cabrera@uc.cl
#SBATCH --mail-type=ALL

eval "$(conda shell.bash hook)"
conda activate SCAMP

python SCAMP_1day.py
