class Nodo:
    def __init__(self, clave):
        self.izquierda = None
        self.derecha = None
        self.clave = clave

class Arbol:
    def __init__(self):
        self.raiz = None

    def insertar(self, clave):
        if self.raiz is None:
            self.raiz = Nodo(clave)
        else:
            self.insertar_recursivo(self.raiz, clave)

    def insertar_recursivo(self, nodo, clave):
        if clave < nodo.clave:      # comparar el nodo a insertar con el nodo actual
            if nodo.izquierda is None: # si el nodo izquiero no existe se inserta ahi 
                nodo.izquierda = Nodo(clave)
            else:
                self.insertar_recursivo(nodo.izquierda, clave) # si no la se vulve a llamar a la funcion
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(clave)
            else:
                self.insertar_recursivo(nodo.derecha, clave)

    def inorder(self, nodo):
        if nodo:
            self.inorder(nodo.izquierda)
            print(nodo.clave, end=' ')
            self.inorder(nodo.derecha)
            
    def preorder(self, nodo):
        if nodo:
            print(nodo.clave, end=' ')
            self.preorder(nodo.izquierda)
            self.preorder(nodo.derecha)

    def postorder(self, nodo):
        if nodo:
            self.postorder(nodo.izquierda)
            self.postorder(nodo.derecha)
            print(nodo.clave, end=' ')


arbol = Arbol()
numeros = [6,4,1,8,5,9]

for num in numeros:
    arbol.insertar(num)

print("Recorrido Inorder:")
arbol.inorder(arbol.raiz)

print("\nRecorrido Preorder:")
arbol.preorder(arbol.raiz)

print("\nRecorrido Postorder:")
arbol.postorder(arbol.raiz)

