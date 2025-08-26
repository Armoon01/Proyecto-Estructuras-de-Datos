class Cola:
    """
    Implementación de Cola (Queue) usando lista de Python
    
    Análisis de Complejidad Temporal:
    - enqueue(elemento): O(1) amortizado
    - dequeue(): O(n) debido a pop(0) - NOTA: Ineficiente para listas grandes
    - front(): O(1)
    - esta_vacia(): O(1)
    - obtener_tamaño(): O(1)
    
    Análisis de Complejidad Espacial: O(n) donde n es el número de elementos
    
    Notación Asintótica:
    - Mejor caso: O(1) para enqueue, front, esta_vacia, obtener_tamaño
    - Caso promedio: O(n) para dequeue debido a reestructuración de lista
    - Peor caso: O(n) para dequeue
    
    OPTIMIZACIÓN POSIBLE: Usar collections.deque para O(1) en ambos extremos
    """
    def __init__(self):
        self.elementos = []
    
    def enqueue(self, elemento):
        """Agregar elemento al final de la cola"""
        self.elementos.append(elemento)
    
    def dequeue(self):
        """Quitar y retornar elemento del frente"""
        if self.esta_vacia():
            return None
        return self.elementos.pop(0)
    
    def front(self):
        """Ver elemento del frente sin quitarlo"""
        if self.esta_vacia():
            return None
        return self.elementos[0]
    
    def esta_vacia(self):
        """Verificar si la cola está vacía"""
        return len(self.elementos) == 0
    
    def obtener_tamaño(self):
        """Obtener tamaño de la cola"""
        return len(self.elementos)
    
    def obtener_elementos(self):
        """Obtener lista de elementos para visualización"""
        return self.elementos.copy()
    
    def obtener_todos(self):
        """Obtener todos los elementos (alias para compatibilidad)"""
        return self.elementos.copy()
    
    def tamanio(self):
        """Obtener tamaño de la cola (alias para compatibilidad)"""
        return len(self.elementos)
    
    def __str__(self):
        return f"Cola: {self.elementos}"
