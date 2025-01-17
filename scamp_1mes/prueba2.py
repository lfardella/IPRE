import numpy as np
import matplotlib.pyplot as plt
from obspy import read, UTCDateTime

# Cargar los datos originales y procesados
Data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.182-212.mseed')
cc_suma = np.load('cc_suma.npy')      # Correlaciones acumuladas
index = np.load('index_pearson.npy')  # Índices del matrix profile
profile = np.load('profile_pearson.npy')  # Matrix profile
SR = Data[0].stats.sampling_rate      # Frecuencia de muestreo
sublen = int(11 * SR)                 # Tamaño de subsecuencia en muestras

# Tiempos de inicio de las secuencias encontradas
sequence_times = [
    UTCDateTime("2017-07-07T03:05:24.8883937"),
    UTCDateTime("2017-07-07T03:05:40.128393Z"),
    UTCDateTime("2017-07-07T03:05:45.728393Z"),
    UTCDateTime("2017-07-07T03:05:30.488393Z"),
    UTCDateTime("2017-07-07T07:26:51.5683"),
    UTCDateTime("2017-07-07T07:26:45.808393Z"),
    UTCDateTime("2017-07-07T07:45:11.048393Z"),
    UTCDateTime("2017-07-22T07:45:02.768393Z")
]

# Graficar detecciones para cada secuencia
for seq_time in sequence_times:
    # Identificar todas las detecciones asociadas a la secuencia
    seq_index = int((seq_time - Data[0].stats.starttime) * SR)  # Índice inicial en muestras
    associated_indices = [i for i, val in enumerate(index) if val == seq_index]

    # Extraer y apilar las señales detectadas
    detected_signals = [
        Data[1].data[idx:idx + sublen] for idx in associated_indices if idx + sublen < len(Data[1].data)
    ]
    
    # Normalizar las señales detectadas
    normalized_signals = [sig / np.max(np.abs(sig)) if np.max(np.abs(sig)) > 0 else sig for sig in detected_signals]

    # Graficar las señales detectadas
    plt.figure(figsize=(10, 6))
    for i, sig in enumerate(normalized_signals):
        plt.plot(
            np.arange(len(sig)) / SR,  # Tiempo en segundos
            sig + i * 2,               # Desplazamiento vertical para stackear
            color='k', lw=0.7
        )
    
    plt.title(f'Secuencias asociadas a {seq_time}')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud normalizada')
    plt.tight_layout()
    plt.show()
