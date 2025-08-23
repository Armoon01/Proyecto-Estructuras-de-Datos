class Cola:
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
    
    def __str__(self):
        return f"Cola: {self.elementos}"





#cree esta clase para que funcione con la clase Pago porque no sabia si hiba a funcionar correctamente, pero mayormente es un copia y pega de la clase original
class ColaPagos:
    
    
    def __init__(self):
        self.pagos = []  # Cola para almacenar los pagos
    
    def enqueue(self, pago):
        
        self.pagos.append(pago)
    
    def dequeue(self):
        
        if not self.esta_vacia():
            return self.pagos.pop(0)
        return None
    
    def peek(self):
        
        if not self.esta_vacia():
            return self.pagos[0]
        return None
    
    def esta_vacia(self):
        
        return len(self.pagos) == 0
    
    def tamanio(self):
        
        return len(self.pagos)
    
    def obtener_todos(self):
        
        return self.pagos.copy()
    
    def procesar_siguiente_pago(self):
        
        if not self.esta_vacia():
            pago = self.dequeue()
            pago.procesar_pago()
            return pago
        return None
    
    def __str__(self):
        if self.esta_vacia():
            return 
        
        pagos_str = "\n".join([f"  {pago}" for pago in self.pagos])
        return f"Cola de Pagos (primero en salir arriba):\n{pagos_str}"
    
    def __len__(self):
        return len(self.pagos)
