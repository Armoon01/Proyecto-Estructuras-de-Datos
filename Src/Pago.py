from datetime import datetime

class Pago:

    
    def __init__(self, monto, fecha, cliente, email):
        self.monto = monto
        self.fecha = fecha
        self.cliente = cliente
        self.email = email
        self.estado = "Pendiente"
    
    def procesar_pago(self):
        
        self.estado = "Procesado"
        return True
    
    def __str__(self):
        return f"Pago de ${self.monto:.2f} - {self.cliente} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def __repr__(self):
        return f"Pago(monto={self.monto}, cliente='{self.cliente}', fecha={self.fecha})"
