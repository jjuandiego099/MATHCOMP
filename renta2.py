import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# Cargar el conjunto de datos desde un archivo Excel
try:
    data = pd.read_excel(r'C:\Users\juanw\Downloads\SaratogaHouses.csv', engine='openpyxl')
except Exception as e:
    print(f"Error al cargar el archivo: {e}")

# Explorar los datos
print(data.head())  # Muestra las primeras filas del dataset
print(data.info())  # Información general sobre el dataset
print(data.describe())  # Estadísticas descriptivas

# Convertir variables categóricas en variables dummy
data = pd.get_dummies(data, drop_first=True)

# Verificar valores faltantes
print(data.isnull().sum())  # Conteo de valores faltantes por columna
data = data.dropna()  # Opcional: eliminar filas con valores faltantes

# Separar características (X) y variable objetivo (y)
X = data.drop('price', axis=1)  # Características features
y = data['price']                # Variable objetivo precio de vivienda

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Agregar un intercepto (bias) a la matriz X
X_train_b = np.c_[np.ones(X_train.shape[0]), X_train]  # Agregar columna de unos ya que necesito el intercepto
X_test_b = np.c_[np.ones(X_test.shape[0]), X_test]     # Agregar columna de unos

# Calcular los coeficientes usando la fórmula de mínimos cuadrados
beta = np.linalg.inv(X_train_b.T @ X_train_b) @ X_train_b.T @ y_train

# Hacer predicciones sobre el conjunto de prueba
y_pred = X_test_b @ beta

# Calcular métricas de evaluación
mse = np.mean((y_test - y_pred) ** 2)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Mostrar resultados
print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'R^2 Score: {r2}')

# Mostrar coeficientes del modelo
coefficients = pd.DataFrame(beta, index=['Intercept'] + list(X.columns), columns=['Coefficient'])
print(coefficients)

# Tamaño del conjunto de entrenamiento y prueba
print(f'Tamaño del conjunto de entrenamiento: {len(X_train)}')
print(f'Tamaño del conjunto de prueba: {len(X_test)}')
