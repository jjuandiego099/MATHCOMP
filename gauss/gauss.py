import numpy as np

def gauss_jordan(A, b):
    Ab = np.hstack([A, b.reshape(-1, 1)])
    
    n = Ab.shape[0]
    
    for i in range(n):
        Ab[i] = Ab[i] / Ab[i, i]
        
        for j in range(n):
            if i != j:
                Ab[j] = Ab[j] - Ab[j, i] * Ab[i]
    
    return Ab[:, -1]

def main():
    A = np.array([[1, 0, 1],  
                  [5, 4, 3], 
                  [4, 1, 0]]) 

    b = np.array([2, 11, 15])  

    soluciones = gauss_jordan(A, b)

    print("Las soluciones son:")
    for i, sol in enumerate(soluciones):
        print(f"x_{i+1} = {sol}")


main()
