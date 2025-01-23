import numpy as np
import matplotlib.pyplot as plt
from obspy import read, UTCDateTime
from datetime import timedelta, datetime

# Cargar los datos originales
data = read('../../Datos/C1.MT12.HH*.2017.207.mseed')
signal = data[0].data
stats = data[0].stats
sampling_rate = stats.sampling_rate

# Información temporal
start_time = stats.starttime  # Tiempo de inicio del archivo

# Cargar los índices de correlación
index = np.load('index_pearson.npy')
profile = np.load('profile_pearson.npy')

# Buscar el índice con el valor de la señal del cluster
start = datetime(2017, 7, 26, 0, 0, 0)
target_time = datetime(2017, 7, 26, 6, 57, 58)
time_difference_seconds = (target_time - start).total_seconds()
selected_index = int(time_difference_seconds * sampling_rate)
print(f"Índice de muestra: {selected_index}")

# Obtener el índice asociado desde index
detection_index = int(index[selected_index])  # Asegurar que sea un entero válido
print(f"Índice de detección asociado: {detection_index}")

# Verificar si el índice asociado es válido
if detection_index <= 0 or detection_index >= len(signal):
    print("El índice asociado no es válido o está fuera del rango de la señal.")
else:
    # Configuración del rango para graficar
    window_seconds = 10  # Duración de la ventana de la señal a mostrar, en segundos
    window_samples = int(window_seconds * sampling_rate)

    # Rango de la señal principal
    start_sample_main = max(0, selected_index - window_samples // 2)
    end_sample_main = min(len(signal), start_sample_main + window_samples)
    main_signal = signal[start_sample_main:end_sample_main]

    # Rango de la señal asociada
    start_sample_related = max(0, detection_index - window_samples // 2)
    end_sample_related = min(len(signal), start_sample_related + window_samples)
    related_signal = signal[start_sample_related:end_sample_related]

    # Tiempo relativo para los gráficos
    time_main = np.linspace(0, (end_sample_main - start_sample_main) / sampling_rate, len(main_signal))
    time_related = np.linspace(0, (end_sample_related - start_sample_related) / sampling_rate, len(related_signal))

    # Crear gráficos
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    # Gráfico de la señal principal
    axes[0].plot(time_main, main_signal, color='black', linewidth=0.8)
    axes[0].set_title(f"Señal con más detecciones ({start_time + timedelta(seconds=selected_index / sampling_rate)})")
    axes[0].set_ylabel("Amplitud")

    # Gráfico de la señal asociada
    axes[1].plot(time_related, related_signal, color='blue', linewidth=0.8)
    axes[1].set_title(f"Señal asociada ({start_time + timedelta(seconds=detection_index / sampling_rate)})")
    axes[1].set_ylabel("Amplitud")
    axes[1].set_xlabel("Tiempo relativo (s)")

    # Gráfico superpuesto
    axes[2].plot(time_main, main_signal, color='black', linewidth=0.8, label="Señal Principal")
    axes[2].plot(time_related, related_signal, color='blue', linewidth=0.8, label="Señal Asociada")
    axes[2].set_title("Señales superpuestas")
    axes[2].set_ylabel("Amplitud")
    axes[2].set_xlabel("Tiempo relativo (s)")
    axes[2].legend()

    # Ajustes finales
    plt.tight_layout()
    plt.savefig("signal_detections_overlay.png", dpi=300)
    plt.show()
