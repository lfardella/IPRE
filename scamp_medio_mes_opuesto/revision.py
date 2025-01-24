from obspy import read
import numpy as np
import matplotlib.pyplot as plt

# Cargar los datos originales
data = read('../../Datos/C1.MT12.HH*.2017.197-212.mseed')
signal = data[0].data
profile = np.load('profile_pearson.npy')
index = np.load('index_pearson.npy')
sampling_rate = data[0].stats.sampling_rate

# Crear un eje de tiempo en días (para referencia)
time_signal = np.arange(0, len(signal)) / sampling_rate / 3600 / 24

# Filtrar los perfiles con valores > 80%
filter_mask = profile > 80
filtered_indices = np.where(filter_mask)[0]  # Índices de los perfiles que cumplen la condición
related_indices = index[filter_mask]         # Índices de las señales relacionadas

# Crear gráficos para cada par de señales
for i, (main_idx, related_idx) in enumerate(zip(filtered_indices, related_indices)):
    # Calcular el rango de tiempo para la señal principal
    start_time_main = main_idx - int(5 * sampling_rate)  # 5 segundos antes
    end_time_main = main_idx + int(15 * sampling_rate)   # 15 segundos después
    start_time_main = max(0, start_time_main)           # Asegurar que no sea negativo
    end_time_main = min(len(signal), end_time_main)     # Asegurar que no exceda la longitud

    # Extraer la señal principal
    main_signal = signal[start_time_main:end_time_main]
    time_axis_main = np.linspace(-5, 15, len(main_signal))  # Tiempo relativo en segundos

    # Calcular el rango de tiempo para la señal relacionada
    related_idx = int(related_idx)  # Convertir a entero
    start_time_related = related_idx - int(5 * sampling_rate)
    end_time_related = related_idx + int(15 * sampling_rate)
    start_time_related = max(0, start_time_related)
    end_time_related = min(len(signal), end_time_related)

    # Extraer la señal relacionada
    related_signal = signal[start_time_related:end_time_related]
    time_axis_related = np.linspace(-5, 15, len(related_signal))  # Tiempo relativo en segundos

    # Crear la figura y los subgráficos
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # Graficar la señal principal
    axes[0].plot(time_axis_main, main_signal, color='black', linewidth=0.8)
    axes[0].set_title(f"Señal principal {i + 1} (Profile > 80%)")
    axes[0].set_ylabel("Amplitud")
    axes[0].grid(False)

    # Graficar la señal relacionada
    axes[1].plot(time_axis_related, related_signal, color='blue', linewidth=0.8)
    axes[1].set_title(f"Señal relacionada {i + 1}")
    axes[1].set_ylabel("Amplitud")
    axes[1].set_xlabel("Tiempo relativo (s)")
    axes[1].grid(False)

    # Ajustar el diseño y guardar la figura
    plt.tight_layout()
    plt.savefig(f"senial_principal_{i + 1}_y_relacionada.png", dpi=300)
    plt.close(fig)

print("Figuras generadas y guardadas correctamente.")
