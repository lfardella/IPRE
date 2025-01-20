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
start_datetime = start_time.datetime    # Ya lo obtenemos como un objeto datetime, no necesitamos convertirlo

# Cargar los resultados generados previamente
cc_suma = np.load('cc_suma.npy')

# Agrupar índices por día y seleccionar el índice con más detecciones de cada día
indices_by_day = {}
for idx in range(len(cc_suma)):
    # Convertir índice a tiempo
    sample_time = start_datetime + timedelta(seconds=idx / sampling_rate)
    day_str = sample_time.strftime('%Y-%m-%d')
    
    # Guardar el índice con mayor detección para cada día
    if day_str not in indices_by_day or cc_suma[idx] > cc_suma[indices_by_day[day_str]]:
        indices_by_day[day_str] = idx

# Ordenar las muestras seleccionadas por fecha
selected_indices = [indices_by_day[day] for day in sorted(indices_by_day.keys())]

# Duración del segmento a mostrar (1 minuto: 5 segundos antes y 55 segundos después)
segment_duration = 60   # segundos
pre_event = 5           # segundos antes
post_event = 55         # segundos después
segment_samples = int(segment_duration * sampling_rate)
pre_event_samples = int(pre_event * sampling_rate)

# Crear una figura con subplots
fig, axes = plt.subplots(len(selected_indices), 1, figsize=(12, 3 * len(selected_indices)))

for i, idx in enumerate(selected_indices):
    # Calcular inicio y fin del segmento
    start_sample = idx - pre_event_samples
    end_sample = start_sample + segment_samples

    # Ajustar si el segmento está fuera de los límites
    if start_sample < 0:
        start_sample = 0
        end_sample = start_sample + segment_samples
    if end_sample > len(signal):
        end_sample = len(signal)
        start_sample = end_sample - segment_samples

    # Extraer el segmento de la señal
    segment_signal = signal[start_sample:end_sample]
    time_segment = np.arange(start_sample, end_sample) / sampling_rate

    # Convertir el índice de inicio a fecha y hora
    segment_start_time = start_datetime + timedelta(seconds=start_sample / sampling_rate)
    segment_start_str = segment_start_time.strftime('%d/%m/%Y %H:%M:%S')

    # Ajustar el título del primer gráfico para que se muestre como 1 de julio
    if i == 0:
        segment_start_time = segment_start_time.replace(day=1, month=7)     # Ajustamos al 1 de julio
        segment_start_str = segment_start_time.strftime('%d/%m/%Y %H:%M:%S')

    # Graficar el segmento
    axes[i].plot(time_segment - time_segment[0], segment_signal, color='black', linewidth=0.8)

    # Añadir líneas verticales rojas discontinuas
    axes[i].axvline(x=5, color='red', linestyle='--', linewidth=1)  # Línea en el inicio de la muestra
    axes[i].axvline(x=16, color='red', linestyle='--', linewidth=1) # Línea a los 11 segundos

    # Configurar título y ejes
    axes[i].set_title(f"Muestra {i + 1}: {segment_start_str}", fontsize=10)
    axes[i].set_xlabel("Tiempo relativo (segundos)")
    axes[i].set_ylabel("Amplitud")
    axes[i].grid(alpha=0.5)

# Configuración final del gráfico
plt.tight_layout()
plt.suptitle("Muestra con Mayor Detección por Día (1 minuto)", fontsize=14, y=1.02)

# Guardar y mostrar la figura
plt.savefig("mayor_deteccion_por_dia_1min.png", dpi=300, bbox_inches='tight')
plt.show()
