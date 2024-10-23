import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Datos
x = np.array([1, 2, 3, 4, 5])
y = np.array([3.5, 5.5, 6.8, 7.8, 8.3])

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

x_fit = np.linspace(1, 5, 100)
y_fit = slope * x_fit + intercept

plt.scatter(x, y, label='Datos originales')
plt.plot(x_fit, y_fit, color='red', label='Ajuste lineal')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Ajuste Lineal')
plt.show()

print(f'Pendiente (m): {slope}')
print(f'Intersección (b): {intercept}')
