import numpy as np
import matplotlib.pyplot as plt

# Cargar los archivos
profile = np.load('profile_pearson.npy')
indices = np.load('index_pearson.npy')
cc_suma = np.load('cc_suma.npy')

# Graficar el perfil de correlación
plt.figure(figsize=(10, 6))
plt.plot(profile)
plt.title('Perfil de Correlación de Pearson')
plt.xlabel('Índice de subsecuencia')
plt.ylabel('Coeficiente de Correlación')
plt.grid()
plt.show()