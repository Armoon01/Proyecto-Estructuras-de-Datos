class Pila:
    def __init__(self):
        self.elementos = []
    
    def push(self, elemento):
        """Agregar elemento al tope de la pila"""
        self.elementos.append(elemento)
    
    def pop(self):
        """Quitar y retornar elemento del tope"""
        if self.esta_vacia():
            return None
        return self.elementos.pop()
    
    def peek(self):
        """Ver elemento del tope sin quitarlo"""
        if self.esta_vacia():
            return None
        return self.elementos[-1]
    
    def esta_vacia(self):
        """Verificar si la pila está vacía"""
        return len(self.elementos) == 0
    
    def obtener_tamaño(self):
        """Obtener tamaño de la pila"""
        return len(self.elementos)
    
    def obtener_elementos(self):
        """Obtener lista de elementos para visualización"""
        return self.elementos.copy()
    
    def obtener_todas(self):
        """Obtener todos los elementos (alias para compatibilidad)"""
        return self.elementos.copy()
    
    def tamanio(self):
        """Obtener tamaño de la pila (alias para compatibilidad)"""
        return len(self.elementos)
    
    def __str__(self):
        return f"Pila: {self.elementos}"