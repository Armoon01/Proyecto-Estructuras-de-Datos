class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamaño = 0
    
    def agregar_inicio(self, elemento):
        """Agregar elemento al inicio de la lista"""
        nuevo_nodo = NodoDoble(elemento)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        self.tamaño += 1
    
    def agregar_final(self, elemento):
        """Agregar elemento al final de la lista"""
        nuevo_nodo = NodoDoble(elemento)
        if self.cola is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo
        self.tamaño += 1
    
    def eliminar(self, elemento):
        """Eliminar primera ocurrencia del elemento"""
        actual = self.cabeza
        while actual:
            if actual.dato == elemento:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior
                
                self.tamaño -= 1
                return True
            actual = actual.siguiente
        return False
    
    def buscar(self, elemento):
        """Buscar elemento en la lista"""
        actual = self.cabeza
        posicion = 0
        while actual:
            if actual.dato == elemento:
                return posicion
            actual = actual.siguiente
            posicion += 1
        return -1
    
    def esta_vacia(self):
        """Verificar si la lista está vacía"""
        return self.cabeza is None
    
    def obtener_tamaño(self):
        """Obtener tamaño de la lista"""
        return self.tamaño
    
    def obtener_elementos(self):
        """Obtener lista de elementos para visualización"""
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos
    
    def __str__(self):
        return f"ListaDoble: {self.obtener_elementos()}"
