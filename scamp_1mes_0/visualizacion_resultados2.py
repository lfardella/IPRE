import numpy as np
import matplotlib.pyplot as plt
from obspy import read
from datetime import datetime, timedelta

# Leer los datos originales y los resultados generados
data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.182-212.0merge.mseed')
signal = data[0].data
stats = data[0].stats
sampling_rate = stats.sampling_rate

# Cargar los archivos generados
profile = np.load('profile_pearson.npy')
index = np.load('index_pearson.npy')
cc_suma = np.load('cc_suma.npy')

# Crear un eje de tiempo en días (para considerar 31 días)
time_signal = np.arange(0, len(signal)) / sampling_rate / 3600 / 24  # Señal completa en días
time_profile = np.arange(0, len(profile)) / sampling_rate / 3600 / 24  # Perfiles e índices en días

# Convertir los índices filtrados a tiempo en días con un umbral de 0.9
filter_mask = profile > 0.9
filtered_indices = index[filter_mask]
filtered_time_profile = time_profile[filter_mask]
filtered_time_indices = filtered_indices / sampling_rate / 3600 / 24  # Convertir índices a tiempo en días

# Imprimir detecciones
print(f"Detecciones con perfil > 0.9: {len(filtered_time_profile)}")

# Extraer la fecha inicial y final del archivo
start_year, start_day_of_year = 2017, 182
start_date = datetime(start_year, 1, 1) + timedelta(days=start_day_of_year - 1)
end_date = start_date + timedelta(days=31 - 1)  # 31 días en total
date_range_str = f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"

# Crear el gráfico con cuatro paneles
fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

# Gráfico 1: Señal sísmica
axes[0].plot(time_signal, signal, color='black', linewidth=0.8)
axes[0].set_title("Señal Sísmica", fontsize=12)
axes[0].set_ylabel("Amplitud")

# Gráfico 2: Perfil de correlación
axes[1].plot(time_profile, profile, color='blue', linewidth=0.8)
axes[1].axhline(y=0.9, color='red', linestyle='--', linewidth=1, label="Umbral 0.9")
axes[1].set_title("Matrix Profile", fontsize=12)
axes[1].set_ylabel("Correlación")
axes[1].legend()

# Gráfico 3: Índices filtrados (convertidos a días)
axes[2].scatter(filtered_time_profile, filtered_time_indices, color='teal', s=10, alpha=0.7)
axes[2].set_title("Índice de Matrix Profile", fontsize=12)
axes[2].set_ylabel("Tiempo (días)")
axes[2].set_ylim(0, 31)  # Ajustar límites del eje Y para 31 días

# Gráfico 4: cc_suma
axes[3].plot(time_profile, cc_suma, color='hotpink', linewidth=0.8)
axes[3].set_title("Conteo de Correlaciones Altas", fontsize=12)
axes[3].set_xlabel("Tiempo (días)")
axes[3].set_ylabel("Conteo")
axes[3].set_ylim(0, 80)  # Límite máximo en el eje Y

# Ajustes de diseño
plt.tight_layout()
plt.subplots_adjust(top=0.92)
fig.suptitle(f"Análisis Sísmico - Fecha: {date_range_str}", fontsize=14, y=0.98)

# Guardar o mostrar la figura
plt.savefig("results_plot_31days_09_2.png", dpi=300, bbox_inches='tight')
plt.show()
