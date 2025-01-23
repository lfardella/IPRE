import numpy as np
import matplotlib.pyplot as plt
from obspy import read
from datetime import datetime, timedelta

# Leer los datos originales y los resultados generados
data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.207.mseed')  # Archivo específico de un día
signal = data[0].data
stats = data[0].stats
sampling_rate = stats.sampling_rate

# Cargar los archivos generados
profile = np.load('profile_pearson.npy')
index = np.load('index_pearson.npy')

# Crear un eje de tiempo en horas para un solo día
time_signal = np.arange(0, len(signal)) / sampling_rate / 3600  # Señal completa en horas
time_profile = np.arange(0, len(profile)) / sampling_rate / 3600  # Perfiles e índices en horas

# Convertir los índices filtrados a tiempo en horas con un umbral de 0.9
filter_mask = profile > 0.9
filtered_indices = index[filter_mask]
filtered_time_profile = time_profile[filter_mask]
filtered_time_indices = filtered_indices / sampling_rate / 3600  # Convertir índices a tiempo en horas

# Imprimir detecciones
print(f"Detecciones con perfil > 0.9: {len(filtered_time_profile)}")

# Fecha fija del archivo
start_date = datetime(2017, 7, 26)  # Fecha inicial específica
end_date = start_date + timedelta(days=1)  # Solo un día
date_range_str = f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"

# Crear el gráfico con tres paneles
fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

# Gráfico 1: Señal sísmica
axes[0].plot(time_signal, signal, color='black', linewidth=0.8)
axes[0].set_title("Señal Sísmica", fontsize=12)
axes[0].set_ylabel("Amplitud")
axes[0].set_xlim(0, 24)  # Limitar el eje X a 24 horas

# Gráfico 2: Perfil de correlación
axes[1].plot(time_profile, profile, color='blue', linewidth=0.8)
axes[1].axhline(y=0.9, color='red', linestyle='--', linewidth=1, label="Umbral 0.9")
axes[1].set_title("Matrix Profile", fontsize=12)
axes[1].set_ylabel("Correlación")
axes[1].legend()
axes[1].set_xlim(0, 24)  # Limitar el eje X a 24 horas

# Gráfico 3: Índices filtrados (convertidos a horas)
axes[2].scatter(filtered_time_profile, filtered_time_indices, color='teal', s=10, alpha=0.7)
axes[2].set_title("Índice de Matrix Profile", fontsize=12)
axes[2].set_ylabel("Tiempo (horas)")
axes[2].set_ylim(0, 24)  # Ajustar límites del eje Y a 24 horas
axes[2].set_xlabel("Tiempo (horas)")

# Ajustes de diseño
plt.tight_layout()
plt.subplots_adjust(top=0.92)
fig.suptitle(f"Análisis Sísmico - Fecha: {date_range_str}", fontsize=14, y=0.98)

# Guardar o mostrar la figura
plt.savefig("results_plot_26jul2017.png", dpi=300, bbox_inches='tight')
plt.show()
