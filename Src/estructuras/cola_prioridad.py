class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ColaPrioridad:
    def __init__(self):
        self.elementos = []
    
    def enqueue(self, elemento, prioridad=0):
        """Agregar elemento con prioridad"""
        self.elementos.append((prioridad, elemento))
        self.elementos.sort(key=lambda x: x[0], reverse=True)
    
    def dequeue(self):
        """Quitar elemento con mayor prioridad"""
        if self.esta_vacia():
            return None
        return self.elementos.pop(0)[1]
    
    def peek(self):
        """Ver elemento con mayor prioridad sin quitarlo"""
        if self.esta_vacia():
            return None
        return self.elementos[0][1]
    
    def esta_vacia(self):
        """Verificar si la cola está vacía"""
        return len(self.elementos) == 0
    
    def obtener_tamaño(self):
        """Obtener tamaño de la cola"""
        return len(self.elementos)
    
    def obtener_elementos(self):
        """Obtener elementos para visualización"""
        return [elemento for prioridad, elemento in self.elementos]
    
    def __str__(self):
        return f"ColaPrioridad: {self.obtener_elementos()}"
