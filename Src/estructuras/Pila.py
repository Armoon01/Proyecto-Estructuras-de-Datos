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
    
    def __str__(self):
        return f"Pila: {self.elementos}"


class PilaOrdenes:
    """Clase para manejar una pila de órdenes"""
    
    def __init__(self):
        self.ordenes = []  # Pila para almacenar las órdenes
    
    def push(self, orden):
        """Agregar una orden a la pila"""
        self.ordenes.append(orden)
    
    def pop(self):
        """Sacar la última orden de la pila"""
        if not self.esta_vacia():
            return self.ordenes.pop()
        return None
    
    def peek(self):
        """Ver la última orden sin sacarla"""
        if not self.esta_vacia():
            return self.ordenes[-1]
        return None
    
    def esta_vacia(self):
        """Verificar si la pila está vacía"""
        return len(self.ordenes) == 0
    
    def tamanio(self):
        """Obtener el tamaño de la pila"""
        return len(self.ordenes)
    
    def obtener_todas(self):
        """Obtener todas las órdenes de la pila"""
        return self.ordenes.copy()
    
    def __str__(self):
        if self.esta_vacia():
            return "Pila de órdenes vacía"
        
        ordenes_str = "\n".join([f"  {orden}" for orden in reversed(self.ordenes)])
        return f"Pila de Órdenes (última arriba):\n{ordenes_str}"
    
    def __len__(self):
        return len(self.ordenes)