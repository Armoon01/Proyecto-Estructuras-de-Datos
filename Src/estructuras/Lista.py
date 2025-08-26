class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Lista:
    """
    Implementación de Lista Enlazada Simple
    
    Análisis de Complejidad Temporal:
    - agregar(elemento): O(n) - debe recorrer hasta el final
    - eliminar(elemento): O(n) - búsqueda lineal
    - buscar(elemento): O(n) - búsqueda lineal  
    - obtener_tamaño(): O(1) - se mantiene contador
    - esta_vacia(): O(1)
    
    Análisis de Complejidad Espacial: O(n) donde n es el número de elementos
    
    Notación Asintótica:
    - Mejor caso: O(1) para eliminar/buscar primer elemento
    - Caso promedio: O(n/2) ≈ O(n) para operaciones de búsqueda
    - Peor caso: O(n) para buscar/eliminar último elemento
    
    Ventajas: Inserción/eliminación eficiente si se tiene referencia al nodo
    Desventajas: No hay acceso aleatorio O(1) como en arrays
    """
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
    
    def ordenar_recursivo(self, lista_elementos=None, comparar_func=None):
        """
        Algoritmo de ordenamiento recursivo (Merge Sort)
        Complejidad temporal: O(n log n) en todos los casos
        Complejidad espacial: O(n) por la recursión y arrays temporales
        """
        if lista_elementos is None:
            lista_elementos = self.obtener_elementos()
        
        if comparar_func is None:
            comparar_func = lambda x, y: str(x) < str(y)
        
        # Caso base: lista de 0 o 1 elemento ya está ordenada
        if len(lista_elementos) <= 1:
            return lista_elementos
        
        # Dividir la lista por la mitad
        medio = len(lista_elementos) // 2
        izquierda = lista_elementos[:medio]
        derecha = lista_elementos[medio:]
        
        # Llamadas recursivas para ordenar cada mitad
        izquierda_ordenada = self.ordenar_recursivo(izquierda, comparar_func)
        derecha_ordenada = self.ordenar_recursivo(derecha, comparar_func)
        
        # Combinar las mitades ordenadas
        return self._merge_recursivo(izquierda_ordenada, derecha_ordenada, comparar_func)
    
    def _merge_recursivo(self, izq, der, comparar_func, resultado=None):
        """
        Función auxiliar recursiva para combinar dos listas ordenadas
        Complejidad temporal: O(n + m) donde n y m son tamaños de las listas
        """
        if resultado is None:
            resultado = []
        
        # Casos base
        if not izq:
            return resultado + der
        if not der:
            return resultado + izq
        
        # Caso recursivo: tomar el menor elemento
        if comparar_func(izq[0], der[0]):
            resultado.append(izq[0])
            return self._merge_recursivo(izq[1:], der, comparar_func, resultado)
        else:
            resultado.append(der[0])
            return self._merge_recursivo(izq, der[1:], comparar_func, resultado)
        
    def __str__(self):
        return f"Lista: {self.obtener_elementos()}"
