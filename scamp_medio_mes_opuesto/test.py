import numpy as np

# Cargar profile si ya está guardado en un archivo
profile = np.load('profile_pearson.npy')

# Calcular estadísticas
mean_profile = np.mean(profile)
std_profile = np.std(profile)
min_profile = np.min(profile)
max_profile = np.max(profile)

print(f"Media: {mean_profile}")
print(f"Desviación estándar: {std_profile}")
print(f"Valor mínimo: {min_profile}")
print(f"Valor máximo: {max_profile}")

import matplotlib.pyplot as plt

# Histograma
plt.hist(profile, bins=50, color='blue', edgecolor='black', alpha=0.7)
plt.title("Distribución de valores en profile")
plt.xlabel("Correlación (Profile)")
plt.ylabel("Frecuencia")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
