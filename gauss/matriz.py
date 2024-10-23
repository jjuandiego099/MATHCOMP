def ingresar_matriz(filas, columnas, nombre):
    matriz = []
    print(f"Ingrese los elementos de la matriz {nombre} ({filas}x{columnas}):")
    for i in range(filas):
        fila = []
        for j in range(columnas):
            elemento = float(input(f"Elemento [{i+1}][{j+1}]: "))
            fila.append(elemento)
        matriz.append(fila)
    return matriz

def mostrar_matriz(matriz):
    for fila in matriz:
        print(" ".join(map(str, fila)))

def escalar_matriz(matriz, escalar):
    return [[elemento * escalar for elemento in fila] for fila in matriz]

def suma_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def multiplicar_matrices(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Las matrices no se pueden multiplicar: columnas de A deben ser iguales a filas de B.")
    
    resultado = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                resultado[i][j] += A[i][k] * B[k][j]
    return resultado

def main():
    
    filas_A = int(input("Ingrese el número de filas de la matriz A: "))
    columnas_A = int(input("Ingrese el número de columnas de la matriz A: "))
    A = ingresar_matriz(filas_A, columnas_A, 'A')

    filas_B = int(input("Ingrese el número de filas de la matriz B: "))
    columnas_B = int(input("Ingrese el número de columnas de la matriz B: "))
    B = ingresar_matriz(filas_B, columnas_B, 'B')

    
    A_escalada = escalar_matriz(A, 3)
    print("\n3A:")
    mostrar_matriz(A_escalada)

 
    B_escalada = escalar_matriz(B, 4)
    print("\n4B:")
    mostrar_matriz(B_escalada)


    if filas_A == filas_B and columnas_A == columnas_B:
        C = suma_matrices(A, B)
        print("\nA + B:")
        mostrar_matriz(C)
    else:
        print("\nNo se pueden sumar las matrices A y B: dimensiones no coinciden.")


    try:
        D = multiplicar_matrices(B, A)
        print("\nB x A:")
        mostrar_matriz(D)
    except ValueError as e:
        print(f"\nError: {e}")

main()
