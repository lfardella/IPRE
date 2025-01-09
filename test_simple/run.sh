#!/bin/bash

# Nombre del trabajo
#SBATCH --job-name=test.py
# Archivo de salida
#SBATCH --output=salida.txt
# Cola de trabajo
#SBATCH --partition=gpus
# Solicitud de gpus
#SBATCH --gres=gpu:quadro_rtx_8000:1
# Reporte por correo
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lfardella@ing.puc.cl

module load cuda/11.2

eval "$(conda shell.bash hook)"
conda activate scamp_env 

python test.py