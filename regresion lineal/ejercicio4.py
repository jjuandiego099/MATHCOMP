import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit

x = np.array([1, 3, 5, 7, 9, 11, 13, 15])
y = np.array([2.1, 3.2, 3.8, 4, 4.2, 4.4, 4.5, 4.7])

def modelo_lineal(x, m, b):
    return m * x + b

def modelo_exponencial(x, a, b):
    return a * np.exp(b * x)

def modelo_potencias(x, a, b):
    return a * x ** b

params_lineal, _ = curve_fit(modelo_lineal, x, y)
params_exponencial, _ = curve_fit(modelo_exponencial, x, y, p0=(1, 0.1))
params_potencias, _ = curve_fit(modelo_potencias, x, y)

x_fit = np.linspace(1, 15, 100)
y_fit_lineal = modelo_lineal(x_fit, *params_lineal)
y_fit_exponencial = modelo_exponencial(x_fit, *params_exponencial)
y_fit_potencias = modelo_potencias(x_fit, *params_potencias)

plt.scatter(x, y, label='Datos originales', color='black')

plt.plot(x_fit, y_fit_lineal, label='Ajuste lineal', color='red')
plt.plot(x_fit, y_fit_exponencial, label='Ajuste exponencial', color='blue')
plt.plot(x_fit, y_fit_potencias, label='Ajuste de potencias', color='green')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Ajuste de Modelos')
plt.legend()
plt.grid()
plt.show()

print(f'Parámetros modelo lineal (m, b): {params_lineal}')
print(f'Parámetros modelo exponencial (a, b): {params_exponencial}')
print(f'Parámetros modelo de potencias (a, b): {params_potencias}')
