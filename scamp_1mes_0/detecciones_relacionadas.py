from obspy import read, UTCDateTime
import numpy as np
import matplotlib.pyplot as plt

# Cargar los datos originales
data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.182-212.0merge.mseed')
signal = data[0].data
stats = data[0].stats
sampling_rate = stats.sampling_rate
index = np.load('index_pearson.npy')
profile = np.load('profile_pearson.npy')

# Señales principales definidas en el código original
signals = [
    UTCDateTime(2017, 7, 23, 12, 47, 57),
    UTCDateTime(2017, 7, 24, 0, 46, 32),
    UTCDateTime(2017, 7, 24, 0, 52, 22),
    UTCDateTime(2017, 7, 26, 5, 40, 5),
    UTCDateTime(2017, 7, 26, 6, 52, 26),
    UTCDateTime(2017, 7, 26, 6, 57, 58),
    UTCDateTime(2017, 7, 26, 7, 24, 12),
    UTCDateTime(2017, 7, 28, 6, 7, 17),
    UTCDateTime(2017, 7, 28, 6, 46, 36),
]

# Desplazamientos en segundos
time_offsets = [
    [8.01, 6.29],
    [6.61, 6.06, 8.06, 7.13],
    [6.88, 8],
    [5.88, 6.54, 7.95, 8.03],
    [8.03, -0.49],
    [-3.77, 6.33, 8.02],
    [8],
    [8.06],
    [8.05]
]

# Rango de revisión para encontrar señales relacionadas
sublen_samples = int(8 * sampling_rate)  # 8 segundos en muestras
min_time_diff = 20  # Diferencia mínima en segundos para aceptar señales relacionadas

# Graficar cada señal principal y sus relacionadas
for i, signal_time in enumerate(signals):
    # Obtener el índice de la señal principal
    selected_index = int((signal_time - stats.starttime) * sampling_rate)

    # Rango de índices para buscar señales relacionadas
    start_range = max(0, selected_index - sublen_samples)
    end_range = min(len(index), selected_index + sublen_samples + 1)
    related_indices = np.arange(start_range, end_range)

    # Buscar las señales relacionadas
    related_times = []
    related_profiles = []  # Para almacenar los valores de profile correspondientes
    for idx in related_indices:
        most_correlated_idx = index[idx]  # Índice más correlacionado
        if most_correlated_idx > 0:  # Índice válido
            # Calcular el tiempo asociado al índice correlacionado como UTCDateTime
            correlated_time = stats.starttime + most_correlated_idx / sampling_rate

            # Verificar la diferencia temporal mínima
            if all(abs((correlated_time - t)) >= min_time_diff for t in related_times):
                related_times.append(correlated_time)
                related_profiles.append(profile[most_correlated_idx])  # Guardar valor de profile

    # Ordenar los tiempos relacionados y sus perfiles
    sorted_related = sorted(zip(related_times, related_profiles), key=lambda x: x[0])
    related_times, related_profiles = zip(*sorted_related) if sorted_related else ([], [])

    # Crear figura para la señal principal y sus relacionadas
    num_plots = len(related_times) + 1  # Uno para la muestra original + cada secuencia relacionada
    fig, axes = plt.subplots(num_plots, 1, figsize=(10, 2 * num_plots), sharex=False)
    
    # Graficar la señal principal (en negro)
    start_index = int((signal_time - 5 - stats.starttime) * sampling_rate)
    end_index = int((signal_time + 15 - stats.starttime) * sampling_rate)
    signal_segment = signal[start_index:end_index]
    time_axis = np.linspace(0, 20, len(signal_segment))  # Tiempo relativo (5 s antes, 15 s después)
    axes[0].plot(time_axis, signal_segment, color='black', linewidth=0.8)
    axes[0].set_title(f"Señal principal: {signal_time.strftime('%Y-%m-%d %H:%M:%S')}")
    axes[0].set_ylabel("Amplitud")
    axes[0].grid(False)  # Sin cuadrícula

    # Graficar las señales relacionadas (en azul)
    for j, (related_time, related_profile) in enumerate(zip(related_times, related_profiles)):
        offset = time_offsets[i][j]
        start_idx_related = int((related_time + offset - 5 - stats.starttime) * sampling_rate)
        end_idx_related = int((related_time + offset + 15 - stats.starttime) * sampling_rate)
        related_segment = signal[start_idx_related:end_idx_related]
        axes[j + 1].plot(time_axis, related_segment, color='blue', linewidth=0.8)
        axes[j + 1].set_title(
            f"Señal relacionada: {related_time.strftime('%Y-%m-%d %H:%M:%S')} (Correlación: {related_profile:.2f})"
        )
        axes[j + 1].set_ylabel("Amplitud")
        axes[j + 1].grid(False)  # Sin cuadrícula

    # Ajustar el diseño
    axes[-1].set_xlabel("Tiempo relativo (s)")
    plt.tight_layout()

    # Guardar la figura como imagen PNG
    plt.savefig(f"señal_principal_{i + 1}_y_relacionadas.png", dpi=300, bbox_inches='tight')

    plt.show()

    plt.close(fig)

print("Figuras generadas y guardadas correctamente.")
