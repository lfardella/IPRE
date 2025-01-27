import numpy as np
import matplotlib.pyplot as plt
from obspy import read, UTCDateTime

# Carga de datos sísmicos
data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.182-212.0merge.mseed')
signal = data[0]
start_time = signal.stats.starttime

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

# Graficar todas las señales alineadas al mínimo
plt.figure(figsize=(10, 8))

for i, time in enumerate(times):
    # Primera extracción ampliada (20 segundos)
    start = time - start_time - 5  # 5 segundos antes del inicio detectado
    end = start + 20  # Ventana total de 20 segundos
    extended_signal = signal.slice(starttime=start_time + start, endtime=start_time + end)
    
    # Normalizar la señal
    extended_normalized = extended_signal.data / np.max(np.abs(extended_signal.data))
    
    # Buscar el mínimo
    min_index = np.argmin(extended_normalized)
    min_time = extended_signal.times()[min_index]
    
    # Segunda extracción ajustada alrededor del mínimo (6s antes, 5s después)
    adjusted_start = min_time - 6
    adjusted_end = min_time + 5
    aligned_signal = extended_signal.slice(
        starttime=start_time + start + adjusted_start,
        endtime=start_time + start + adjusted_end
    )
    
    # Normalizar la señal alineada
    aligned_normalized = aligned_signal.data / np.max(np.abs(aligned_signal.data))
    time_axis = aligned_signal.times() - aligned_signal.times()[0]  # Eje de tiempo relativo

    # Formatear tiempo
    time_str = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Graficar
    plt.plot(
        time_axis, aligned_normalized + i * 2, c='k', lw=1, label=f'Señal {i + 1} ({time_str})'
    )

plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud Normalizada')
plt.title('Señales Detectadas')
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('stacking.png')
