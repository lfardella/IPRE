import matplotlib.pyplot as plt
from obspy import read, UTCDateTime
import numpy as np

# Cargar los datos y resultados previos
data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.182-212.0merge.mseed')
signal = data[0]
SR = signal.stats.sampling_rate
profile = np.load('profile_pearson.npy')
index = np.load('index_pearson.npy')

# Tiempos de inicio de las señales detectadas
times = [
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

# Ventana de ±5 y +15 segundos
pre_window = int(5 * SR)
post_window = int(15 * SR)

# Umbral de diferencia mínima entre señales similares (en segundos)
time_tolerance = 15  # 15 segundos

# Crear la figura
fig, axes = plt.subplots(len(times), 2, figsize=(10, len(times) * 3), sharex=False)

if len(times) == 1:
    axes = [axes]  # Para manejar casos con una sola señal

# Buscar correlaciones altas alrededor de cada tiempo
for i, t in enumerate(times):
    # Convertir tiempo a índice en el array de la señal
    start_index = int((t - signal.stats.starttime) * SR)

    # Señal principal (ventana de 5 segundos antes a 15 segundos después)
    signal_start = max(0, start_index - pre_window)
    signal_end = min(len(signal.data), start_index + post_window)
    original_signal = signal.data[signal_start:signal_end]

    # Filtrar correlaciones altas (≥ 0.95)
    search_range = int(8 * SR)  # Rango de búsqueda
    window_start = max(0, start_index - search_range)
    window_end = min(len(profile), start_index + search_range)
    high_corr_indices = np.where(profile[window_start:window_end] >= 0.95)[0]
    high_corr_indices += window_start  # Ajustar los índices al rango original

    # Agrupar señales correlacionadas, pero evitar señales cercanas a la principal
    grouped_signals = []
    current_group = []

    for idx in high_corr_indices:
        corr_time = signal.stats.starttime + idx / SR
        corr_value = profile[idx]

        # Verificar si la señal está demasiado cerca de la señal principal
        if abs(idx - start_index) > 15 * SR:  # No considerar señales dentro de ±15 segundos de la principal
            if not current_group or (corr_time - current_group[-1][0]) <= time_tolerance:
                current_group.append((corr_time, corr_value, idx))  # (tiempo, correlación, índice)
            else:
                best_signal = max(current_group, key=lambda x: x[1])
                grouped_signals.append(best_signal)
                current_group = [(corr_time, corr_value, idx)]
    
    if current_group:
        best_signal = max(current_group, key=lambda x: x[1])
        grouped_signals.append(best_signal)

    # Graficar la señal original
    time_axis = np.linspace(0, 20, len(original_signal))  # Eje temporal en segundos relativo al inicio
    axes[i][0].plot(time_axis, original_signal, color="black")
    axes[i][0].set_title(f"Señal principal: {t.strftime('%Y-%m-%d %H:%M:%S')}")
    axes[i][0].set_xlabel("Tiempo relativo (s)")

    # Graficar señales correlacionadas si existen
    if grouped_signals:
        for corr_time, corr_value, corr_idx in grouped_signals:
            corr_start = max(0, corr_idx - pre_window)
            corr_end = min(len(signal.data), corr_idx + post_window)
            detected_signal = signal.data[corr_start:corr_end]

            detected_time_axis = np.linspace(0, 20, len(detected_signal))  # Tiempo relativo
            axes[i][1].plot(
                detected_time_axis, detected_signal, color="blue"
            )
            axes[i][1].set_title(
                f"Señal relacionada: {corr_time.strftime('%Y-%m-%d %H:%M:%S')} (Correlación: {corr_value:.2f})"
            )
    else:
        axes[i][1].text(
            0.5, 0.5, "Sin correlaciones detectadas",
            horizontalalignment="center", verticalalignment="center",
            transform=axes[i][1].transAxes
        )
        axes[i][1].set_title("Sin señales relacionadas")

    axes[i][1].set_xlabel("Tiempo relativo (s)")

# Ajustar diseño
plt.tight_layout()

# Guardar como archivo PNG
plt.savefig("repeating.png", dpi=300)
plt.close(fig)
