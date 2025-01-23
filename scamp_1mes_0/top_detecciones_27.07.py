import numpy as np
import matplotlib.pyplot as plt
from obspy import read
from datetime import datetime, timedelta
from obspy import UTCDateTime

# Cargar los datos originales
data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.182-212.0merge.mseed')
signal = data[0].data
stats = data[0].stats
sampling_rate = stats.sampling_rate

# Información temporal
start_time = stats.starttime  # Tiempo de inicio del archivo
start_datetime = start_time.datetime

# Cargar los índices de correlación
index = np.load('index_pearson.npy')
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

# Día objetivo
target_date = "2017-07-27"
selected_index = indices_by_day[target_date]

# Rango de revisión
sublen_samples = int(8 * sampling_rate)

# Rango completo para evaluar todos los índices desde x-8*SR hasta x+8*SR
start_range = max(0, selected_index - sublen_samples)               # Limitar para no salir del rango
end_range = min(len(index), selected_index + sublen_samples + 1)    # Limitar al final del array
related_indices = np.arange(start_range, end_range)                 # Incluir todos los índices

# Buscar las secuencias más correlacionadas para cada índice
related_times = []  # Cambiamos a lista para verificar la diferencia temporal
min_time_diff = 20  # Diferencia mínima en segundos

for idx in related_indices:
    most_correlated_idx = index[idx]    # Índice más correlacionado
    if most_correlated_idx > 0:         # Índice válido
        # Calcular tiempo asociado al índice
        correlated_time = start_datetime + timedelta(seconds=most_correlated_idx / sampling_rate)
        
        # Verificar si cumple con la diferencia mínima respecto a los tiempos ya guardados
        if all(abs((correlated_time - t).total_seconds()) >= min_time_diff for t in related_times):
            related_times.append(correlated_time)  # Agregar tiempo si cumple la condición

# Ordenar los tiempos para graficarlos en secuencia
related_times = sorted(related_times)

# Configuración del rango de tiempo para los gráficos (5 segundos antes y 15 segundos después)
pre_duration = 5                                    # segundos antes
post_duration = 15                                  # segundos después
segment_duration = pre_duration + post_duration     # Duración total en segundos
segment_samples = int(segment_duration * sampling_rate)
pre_samples = int(pre_duration * sampling_rate)

# Desplazamientos en segundos para las detecciones relacionadas
time_offsets = [7.1, 7.55, 7.65, 7.7, -7.5]  # Ejemplo: tiempo de desplazamiento para las primeras detecciones

# Crear la figura y los subgráficos
num_subplots = len(related_times) + 1  # Uno para la muestra original + cada secuencia relacionada
fig, axes = plt.subplots(num_subplots, 1, figsize=(10, 2 * num_subplots), sharex=False)

# Graficar la muestra original
main_start_sample = selected_index - pre_samples
main_end_sample = main_start_sample + segment_samples
if main_start_sample < 0:
    main_start_sample = 0
    main_end_sample = main_start_sample + segment_samples
if main_end_sample > len(signal):
    main_end_sample = len(signal)
    main_start_sample = main_end_sample - segment_samples

main_signal = signal[main_start_sample:main_end_sample]
relative_time = np.linspace(0, segment_duration, len(main_signal))  # Tiempo relativo para el eje x

axes[0].plot(relative_time, main_signal, color='black', linewidth=0.8)
axes[0].set_title(f"Muestra original: {start_datetime + timedelta(seconds=main_start_sample / sampling_rate)}")
axes[0].set_ylabel("Amplitud")

# Graficar las secuencias relacionadas con desplazamiento de tiempo
for i, correlated_time in enumerate(related_times):
    # Convertir tiempo relacionado a UTCDateTime
    correlated_time_utc = UTCDateTime(correlated_time)
    
    # Aplicar desplazamiento si está dentro del rango definido
    if i < len(time_offsets):
        correlated_time_utc += time_offsets[i]  # Agregar desplazamiento de tiempo
    
    # Convertir tiempo a índice
    correlated_index = int((correlated_time_utc - start_time) * sampling_rate)
    
    # Calcular inicio y fin del segmento
    start_sample = correlated_index - pre_samples
    end_sample = start_sample + segment_samples
    if start_sample < 0:
        start_sample = 0
        end_sample = start_sample + segment_samples
    if end_sample > len(signal):
        end_sample = len(signal)
        start_sample = end_sample - segment_samples

    # Extraer la señal
    segment_signal = signal[start_sample:end_sample]
    relative_time = np.linspace(0, segment_duration, len(segment_signal))  # Tiempo relativo para el eje x
    
    # Graficar
    axes[i + 1].plot(relative_time, segment_signal, color='blue', linewidth=0.8)
    axes[i + 1].set_title(f"Relacionado (desplazado): {correlated_time_utc.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    axes[i + 1].set_ylabel("Amplitud")

# Ajustar ejes y etiquetas
axes[-1].set_xlabel("Tiempo relativo (s)")
plt.tight_layout()

# Guardar la figura como imagen PNG
plt.savefig("top_detecciones_27.07_desplazadas.png", format='png', dpi=300)

# Mostrar la figura
plt.show()
