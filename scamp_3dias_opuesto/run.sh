#!/bin/bash

# Nombre del trabajo
#SBATCH --job-name=opuesto_pyscamp
# Archivo de salida
#SBATCH --output=salida.txt
# Partición CPUS
#SBATCH --partition=512x1024
# Partición GPUS
##SBATCH --partition=gpus
# Solicitud de cpus
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
# Solicitud de GPUS
##SBATCH --gres=gpu:1
#SBATCH --mail-user=lfardella@uc.cl
#SBATCH --mail-type=ALL

eval "$(conda shell.bash hook)"
conda activate scamp_env

python scamp_3dias_opuesto.py
