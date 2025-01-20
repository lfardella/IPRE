import numpy as np
import matplotlib.pyplot as plt
from obspy import read
from datetime import datetime, timedelta

# Cargar los datos originales
data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.182-212.0merge.mseed')
signal = data[0].data
stats = data[0].stats
sampling_rate = stats.sampling_rate
start_time = stats.starttime            # Tiempo de inicio del archivo
start_datetime = start_time.datetime

# Cargar los resultados generados previamente
profile = np.load('profile_pearson.npy')
index = np.load('index_pearson.npy')
cc_suma = np.load('cc_suma.npy')

# Longitud de las subsecuencias
sublen = int(11 * sampling_rate)

# Agrupar índices por día y seleccionar el índice con más detecciones de cada día
indices_by_day = {}
for idx in range(len(cc_suma)):
    sample_time = start_datetime + timedelta(seconds=idx / sampling_rate)
    day_str = sample_time.strftime('%Y-%m-%d')
    if day_str not in indices_by_day or cc_suma[idx] > cc_suma[indices_by_day[day_str]]:
        indices_by_day[day_str] = idx

# Seleccionar el índice del día 27/07/2017
target_day = '2017-07-27'
if target_day in indices_by_day:
    original_index = indices_by_day[target_day]
    print(f"Índice con más detecciones el {target_day}: {original_index}")
else:
    raise ValueError(f"No se encontraron datos para el día {target_day}.")

# Función para encontrar subsecuencias relacionadas (con intersección)
def find_related_subsequences(original_index, threshold=0.9):
    """
    Encuentra todas las subsecuencias directamente relacionadas a un índice original.
    """
    similar_indices = np.where(profile >= threshold)[0]
    related_indices = np.where(index == original_index)[0]
    all_related = np.intersect1d(similar_indices, related_indices)
    return all_related

# Encontrar las subsecuencias relacionadas
related_indices = find_related_subsequences(original_index)

# Graficar las señales
def plot_related_subsequences(original_index, related_indices):
    """
    Grafica la subsecuencia original y todas las relacionadas.

    Args:
        original_index (int): Índice de la subsecuencia original.
        related_indices (list): Índices de las subsecuencias relacionadas.
    """
    original_start = original_index
    original_signal = signal[original_start:original_start + sublen]

    # Configuración de la figura
    fig, axs = plt.subplots(len(related_indices) + 1, 1, figsize=(10, 3 * (len(related_indices) + 1)))
    if len(related_indices) == 0:
        axs = [axs]  # Asegurarse de que axs sea iterable si hay solo un gráfico

    # Gráfico de la subsecuencia original
    axs[0].plot(original_signal, label=f'Subsecuencia original (índice {original_index})')
    axs[0].set_title(f'Subsecuencia original (índice {original_index})')
    axs[0].set_xlabel('Muestra')
    axs[0].set_ylabel('Amplitud')
    axs[0].legend()

    # Gráficos de subsecuencias relacionadas
    for i, idx in enumerate(related_indices):
        start = idx
        related_signal = signal[start:start + sublen]
        axs[i + 1].plot(related_signal, label=f'Relacionada (índice {idx})')
        axs[i + 1].set_title(f'Subsecuencia relacionada (índice {idx})')
        axs[i + 1].set_xlabel('Muestra')
        axs[i + 1].set_ylabel('Amplitud')
        axs[i + 1].legend()

    plt.tight_layout()
    plt.show()

# Graficar las subsecuencias
plot_related_subsequences(original_index, related_indices)
