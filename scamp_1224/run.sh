#!/bin/bash

# Nombre del trabajo
#SBATCH --job-name=test_pyscamp.py
# Archivo de salida
#SBATCH --output=salida.txt
# Partición CPUS
#SBATCH --partition=full
# Partición GPUS
##SBATCH --partition=gpus
# Solicitud de cpus
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
# Solicitud de GPUS
##SBATCH --gres=gpu:1
#SBATCH --mail-user=lfardella@uc.cl
#SBATCH --mail-type=ALL

eval "$(conda shell.bash hook)"
conda activate scamp_env

python scamp_1dia.py
