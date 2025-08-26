class Pila:
    """
    Implementación de Pila (Stack) usando lista de Python
    
    Análisis de Complejidad Temporal:
    - push(elemento): O(1) amortizado
    - pop(): O(1) 
    - peek(): O(1)
    - esta_vacia(): O(1)
    - obtener_tamaño(): O(1)
    
    Análisis de Complejidad Espacial: O(n) donde n es el número de elementos
    
    Notación Asintótica:
    - Mejor caso: O(1) para todas las operaciones básicas
    - Caso promedio: O(1) para todas las operaciones básicas  
    - Peor caso: O(1) para todas las operaciones básicas
    """
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