import numpy as np
import matplotlib.pyplot as plt
from obspy import read, UTCDateTime

# Cargar los datos originales y procesados
Data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.182-212.mseed')  # Datos originales
cc_suma = np.load('cc_suma.npy')                # Correlaciones acumuladas
index = np.load('index_pearson.npy')            # Índices del matrix profile
profile = np.load('profile_pearson.npy')        # Matrix profile
SR = Data[0].stats.sampling_rate                # Frecuencia de muestreo
sublen = int(11 * SR)                           # Tamaño de subsecuencia en muestras

# Parámetros de filtrado
min_distance = sublen // 2                      # Mínima distancia entre subsecuencias
var_threshold = 1e-8                            # Umbral mínimo de varianza (ajustar según los datos)

# Identificar las 50 subsecuencias con más detecciones
sorted_indices = np.argsort(cc_suma)[::-1]      # Orden descendente por detecciones
selected_indices = []

for idx in sorted_indices:
    # Filtrar por mínima distancia y varianza
    subseq = Data[1].data[idx:idx + sublen]
    if (
        not selected_indices or all(abs(idx - sel) > min_distance for sel in selected_indices)
    ) and np.var(subseq) > var_threshold:  # Filtrar por varianza
        selected_indices.append(idx)
    if len(selected_indices) >= 50:             # Limitar a las 50 más significativas
        break

# Extraer las subsecuencias seleccionadas y sus tiempos de inicio
selected_subsequences = [Data[1].data[start:start + sublen] for start in selected_indices]
start_times = [Data[1].stats.starttime + (idx / SR) for idx in selected_indices]

# Visualizar las subsecuencias
plt.figure(figsize=(12, 10))
for i, subseq in enumerate(selected_subsequences):
    plt.subplot(10, 5, i + 1)                   # Crear subplots para las 50 secuencias
    plt.plot(np.arange(len(subseq)) / SR, subseq, color='blue')
    plt.title(f'Secuencia {i+1}\n{start_times[i]}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.tight_layout()

plt.show()
