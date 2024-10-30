import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Datos
x1 = np.array([1, 1, 2, 3, 1, 2, 3, 3])
x2 = np.array([-1, 0, 0, 1, 1, 2, 2, 0])
y = np.array([1.6, 3, 1.1, 1.2, 3.2, 3.3, 1.7, 0.1])

# Ajuste lineal
X = np.vstack([x1, x2]).T  # Matriz de características
slope, intercept, r_value, p_value, std_err = linregress(X.flatten(), y)

# Resultados
print(f"Ecuación de la recta: y = {slope:.4f} * (x1, x2) + {intercept:.4f}")
print(f"Coeficiente de correlación (r): {r_value:.4f}")

# Graficar los datos y la línea de ajuste
plt.scatter(X[:, 0], y, color='blue', label='Datos (x1)')
plt.scatter(X[:, 1], y, color='red', label='Datos (x2)')
plt.plot(X[:, 0], slope * X[:, 0] + intercept, color='green', label='Ajuste lineal')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ajuste lineal de datos')
plt.legend()
plt.show()
