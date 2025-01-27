import numpy as np
import matplotlib.pyplot as plt
from obspy import read

# Cargar datos
data = read('../../Datos/C1.MT12.HH*.2017.207-209.mseed')
signal = data[0].data
stats = data[0].stats
sampling_rate = stats.sampling_rate

# Cargar los arrays generados previamente
profile = np.load('profile_pearson.npy')
index = np.load('index_pearson.npy')

# Obtener los índices de los 5 valores más altos de profile
top_5_indices = np.argsort(profile)[-10:][::-1]  # Ordenar de mayor a menor y obtener los últimos 5

# Parámetros para graficar
time_window = 11  # Ventana de tiempo en segundos
sublen_samples = int(time_window * sampling_rate)

# Crear figura
fig, axes = plt.subplots(len(top_5_indices), 2, figsize=(12, 3 * len(top_5_indices)))

# Graficar cada par de señales
for i, top_index in enumerate(top_5_indices):
    # Índice correlacionado
    related_index = int(index[top_index])
    
    if related_index < 0 or related_index >= len(signal):
        continue  # Si el índice correlacionado es inválido, pasar al siguiente

    # Extraer la señal principal
    start_main = max(0, top_index - sublen_samples // 2)
    end_main = min(len(signal), top_index + sublen_samples // 2)
    main_signal = signal[start_main:end_main]
    main_time = np.linspace(-time_window / 2, time_window / 2, len(main_signal))

    # Extraer la señal correlacionada
    start_related = max(0, related_index - sublen_samples // 2)
    end_related = min(len(signal), related_index + sublen_samples // 2)
    related_signal = signal[start_related:end_related]
    related_time = np.linspace(-time_window / 2, time_window / 2, len(related_signal))

    # Graficar señal principal
    axes[i, 0].plot(main_time, main_signal, color='black', linewidth=0.8)
    axes[i, 0].set_title(f'Señal principal (Índice: {top_index}, Profile: {profile[top_index]:.3f})')
    axes[i, 0].set_ylabel("Amplitud")
    axes[i, 0].set_xlabel("Tiempo relativo (s)")
    axes[i, 0].grid(False)

    # Graficar señal relacionada
    axes[i, 1].plot(related_time, related_signal, color='blue', linewidth=0.8)
    axes[i, 1].set_title(f'Señal relacionada (Índice: {related_index})')
    axes[i, 1].set_ylabel("Amplitud")
    axes[i, 1].set_xlabel("Tiempo relativo (s)")
    axes[i, 1].grid(False)

# Ajustar el diseño de la figura
plt.tight_layout()

# Guardar la figura
fig.savefig('top_detecciones.png')
