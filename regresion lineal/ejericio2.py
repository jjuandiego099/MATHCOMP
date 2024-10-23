import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

x = np.array([1, 2, 3, 4, 5])
y = np.array([5, 6.6, 8.8, 10.8, 14.2])

ln_x = np.log(x)
ln_y = np.log(y)

slope, intercept, r_value, p_value, std_err = stats.linregress(ln_x, ln_y)

b = slope
a = np.exp(intercept)

x_fit = np.linspace(1, 5, 100)
y_fit = a * x_fit**b

plt.scatter(x, y, label='Datos originales')
plt.plot(x_fit, y_fit, color='red', label='Ajuste de potencia')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Ajuste de Potencia')
plt.show()

print(f'Parámetro a: {a}')
print(f'Parámetro b: {b}')
