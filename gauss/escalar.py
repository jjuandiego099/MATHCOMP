def producto_escalar(v1,v2 ,n):
    nVector=[]
    for a in range(0,n):
        nVector.append(v1[a]*v2[a])
    return nVector

def main():
    n = int(input("Ingrese la longitud de los vectores: "))
    v1 = []
    v2 = []
    print("Ingrese los elementos del primer vector:")
    for i in range(n):
        v1.append(float(input(f"Elemento {i + 1}: ")))

    print("Ingrese los elementos del segundo vector:")
    for i in range(n):
        v2.append(float(input(f"Elemento {i + 1}: ")))

    resultado = producto_escalar(v1, v2,n)
    print(f"El producto escalar de los vectores es: {resultado}")
main()
