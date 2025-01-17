import numpy as np
import matplotlib.pyplot as plt
from obspy import read, UTCDateTime

# --- Cargar datos guardados ---
print("Cargando resultados guardados...")
cc_suma = np.load('cc_suma.npy')
profile = np.load('profile_pearson.npy')
index = np.load('index_pearson.npy')

# --- Configuración inicial ---
Data = read('../../Datos/2017/Julio/C1.MT12.HH*.2017.182-212.mseed')  # Ajusta la ruta si es necesario
SR = Data[0].stats.sampling_rate
start_time = Data[0].stats.starttime  # Tiempo de inicio de la traza
sublen = 11  # Duración de subsecuencia en segundos

# Identificar las subsecuencias con más detecciones
percentile_threshold = 95  # Percentil para detecciones destacadas
top_detections = np.where(cc_suma > np.percentile(cc_suma, percentile_threshold))[0]

# Ordenar detecciones por la cantidad de correlaciones altas (valor en cc_suma)
top_detections_sorted = top_detections[np.argsort(cc_suma[top_detections])[::-1]]

# --- Mostrar formas de onda de las subsecuencias con más detecciones ---
print("Visualizando subsecuencias destacadas...")
detections_to_show = 0  # Contador para subsecuencias mostradas
max_detections_to_show = 20  # Límite en el número de subsecuencias a mostrar

for idx in top_detections_sorted:  # Iterar sobre todas las detecciones
    detection_time = start_time + (idx / SR)  # Tiempo de inicio de la subsecuencia
    detection_end_time = detection_time + sublen  # Tiempo de fin de la subsecuencia
    
    # Verificar si la detección es del día 16 de julio
    if detection_time.date() == UTCDateTime("2017-07-16").date():
        continue  # Omitir detecciones del día 16 de julio
    
    # Usar slice para extraer la subsecuencia
    print(f"Subsecuencia destacada en {detection_time} - {detection_end_time}")
    subsequence = Data.slice(starttime=detection_time, endtime=detection_end_time)
    
    # Filtrar para graficar solo la componente Este
    east_component = subsequence.select(channel="*E")  # Filtrar componente Este (HH2 o similar)
    
    if len(east_component) == 0:  # Verificar que existe la componente Este
        print(f"No se encontró la componente Este para {detection_time} - {detection_end_time}")
        continue

    # Graficar la componente Este
    plt.figure(figsize=(10, 3))
    for trace in east_component:  # Graficar cada traza de la componente Este
        time_axis = np.arange(len(trace.data)) / SR  # Eje X en segundos
        plt.plot(time_axis, trace.data, label=f"Canal {trace.stats.channel}")
    
    plt.title(f"Subsecuencia Este desde {detection_time.strftime('%Y-%m-%d %H:%M:%S')} "
              f"hasta {detection_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Amplitud")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
    
    detections_to_show += 1  # Incrementar el contador de detecciones mostradas
    
    if detections_to_show >= max_detections_to_show:  # Limitar el número de gráficos
        break  # Salir del bucle si se ha alcanzado el límite

print("Visualización completada.")
