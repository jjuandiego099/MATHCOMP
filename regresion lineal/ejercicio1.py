import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x = np.array([1, 2, 3, 4, 5, 6])
y = np.array([4.5, 6, 9, 12, 17, 24])

def modelo_exponencial(x, a, b):
    return a * np.exp(b * x)

params, covariance = curve_fit(modelo_exponencial, x, y)

a, b = params

x_fit = np.linspace(1, 6, 100)
y_fit = modelo_exponencial(x_fit, a, b)

plt.scatter(x, y, label='Datos originales')
plt.plot(x_fit, y_fit, color='red', label='Ajuste exponencial')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Ajuste Exponencial')
plt.show()

print(f'Parámetro a: {a}')
print(f'Parámetro b: {b}')
