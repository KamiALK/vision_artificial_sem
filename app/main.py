import mediapipe as mp
import cv2
import numpy as np


print("kamilo eso el mejor")
print("mediapipe:", mp.__version__)
print("opencv:", cv2.__version__)
print("numpy:", np.__version__)

datra = np.array([1, 2, 3])
print("data:", datra)


# Crear un array de 2x3 con números aleatorios entre 0 y 1
matriz = np.random.rand(2, 3)
ma = np.reshape(matriz, (2, 3))
print("Matriz aleatoria 2x3:")
print(matriz)

# Calcular la transpuesta de la matriz
transpuesta = matriz.T
print("\nTranspuesta:")
print(transpuesta)

# Calcular la suma de todos los elementos
suma = np.sum(matriz)
print("\nSuma total de los elementos:", suma)
