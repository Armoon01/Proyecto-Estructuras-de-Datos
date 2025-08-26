class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Lista:
    def __init__(self):
        self.cabeza = None
        self.tamaño = 0
    
    def agregar(self, elemento):
        """Agregar elemento al final de la lista"""
        nuevo_nodo = Nodo(elemento)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamaño += 1
    
    def eliminar(self, elemento):
        """Eliminar primera ocurrencia del elemento"""
        if self.cabeza is None:
            return False
        
        if self.cabeza.dato == elemento:
            self.cabeza = self.cabeza.siguiente
            self.tamaño -= 1
            return True
        
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.dato == elemento:
                actual.siguiente = actual.siguiente.siguiente
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
    
    def limpiar(self):
        """Limpiar la lista"""
        self.cabeza = None
        self.tamaño = 0
        
    def __str__(self):
        return f"Lista: {self.obtener_elementos()}"
