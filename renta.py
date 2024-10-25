import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Cargar el conjunto de datos desde un archivo Excel
data = pd.read_excel('C:\Users\juanw\Downloads\SaratogaHouses.csv', engine='openpyxl')

# Explorar los datos
print(data.head())  # Muestra las primeras filas del dataset
print(data.info())  # Información general sobre el dataset

# Convertir variables categóricas en variables dummy, si es necesario varieable categorica a numerica
data = pd.get_dummies(data, drop_first=True)

# Verificar valores faltantes
print(data.isnull().sum())  # Muestra el conteo de valores faltantes por columna

# Separar características (X) y variable objetivo (y)
X = data.drop('price', axis=1)  # Características features
y = data['price']                # Variable objetivo precio de vivienda

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Crear el modelo de regresión lineal
model = LinearRegression()

# Entrenar el modelo
model.fit(X_train, y_train)

# Hacer predicciones sobre el conjunto de prueba
y_pred = model.predict(X_test)

# Calcular el error cuadrático medio manualmente
mse = np.mean((y_test - y_pred) ** 2)

# Evaluar el modelo entre mas cercano al 1 predice mejor los valores 
r2 = r2_score(y_test, y_pred)

# Mostrar resultados
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Tamaño del conjunto de entrenamiento: 1382 80%
# Tamaño del conjunto de prueba: 346 20%
