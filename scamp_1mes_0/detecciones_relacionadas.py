from obspy import read, UTCDateTime
import numpy as np
import matplotlib.pyplot as plt

# Cargar los datos originales
data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.182-212.0merge.mseed')
signal = data[0].data
stats = data[0].stats
sampling_rate = stats.sampling_rate
index = np.load('index_pearson.npy')
cc_suma = np.load('cc_suma.npy')

# Señales a revisar
signals = [
    UTCDateTime(2017, 7, 23, 12, 47, 57),
    UTCDateTime(2017, 7, 26, 5, 40, 5),
    UTCDateTime(2017, 7, 26, 6, 52, 26),
    UTCDateTime(2017, 7, 26, 6, 57, 58),
    UTCDateTime(2017, 7, 28, 6, 7, 18),
]

# Graficar 5 segundos antes y 15 segundos después de cada señal en una misma figura
num_subplots = len(signals)
fig, axes = plt.subplots(num_subplots, 1, figsize=(10, 5 * num_subplots))

# Iterar sobre las señales y graficar
for i, signal_time in enumerate(signals):
    # Obtener el índice correspondiente al tiempo inicial y final
    start_index = int((signal_time - 5 - stats.starttime) * sampling_rate)
    end_index = int((signal_time + 15 - stats.starttime) * sampling_rate)
    
    # Extraer los datos en ese intervalo
    signal_segment = signal[start_index:end_index]
    time_axis = np.linspace(-5, 15, len(signal_segment))
    
    # Graficar la señal
    ax = axes[i] if num_subplots > 1 else axes  # Soporte para un solo subplot
    ax.plot(time_axis, signal_segment, label=f"Señal {i+1}: {signal_time}", color='blue')
    ax.axvline(0, color='red', linestyle='--', label="Evento")
    ax.set_title(f"Señal {i+1}: {signal_time}")
    ax.set_xlabel("Tiempo relativo (s)")
    ax.set_ylabel("Amplitud")
    ax.legend()
    ax.grid()

# Ajustar el layout y mostrar el gráfico
plt.tight_layout()
plt.show()

# Guardar la figura
fig.savefig('detecciones_relacionadas.png', dpi=300)