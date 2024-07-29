import os
import numpy as np
import matplotlib.pyplot as plt  

import soundfile as sf

audio, sample_rate = sf.read('AudiosTest/Homer/Homer-Anda-Porra.mp3')

datos_np = np.array(audio)

max_value = np.max(datos_np)

print(max_value)

# x = np.arange(len(datos_np))


# # Crear la figura y los ejes
# plt.figure(figsize=(10, 6))

# # Ploteo del canal 1
# plt.plot(x, datos_np, label=['Canal 1','Canal 2'])


# # Agregar título y etiquetas a los ejes
# plt.title('Valores de los dos canales de audio')
# plt.xlabel('Muestra')
# plt.ylabel('Amplitud')

# # Agregar una leyenda
# plt.legend()

# # Mostrar el gráfico
# plt.show()