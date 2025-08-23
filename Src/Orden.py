from datetime import datetime

class Orden:
    
    
    def __init__(self, id, items, total, fecha, cliente):
        self.id = id
        self.items = items
        self.total = total
        self.fecha = fecha
        self.cliente = cliente
        self.estado = "Pendiente"
    
    def procesar_orden(self):
        
        self.estado = "Procesada"
        return True
    
    def __str__(self):
        return f"Orden #{self.id} - {self.cliente} - ${self.total:.2f} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def __repr__(self):
        return f"Orden(id={self.id}, cliente='{self.cliente}', total={self.total})"
