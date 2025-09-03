from datetime import datetime
from TarjetaCredito import TarjetaCredito
class Pago:


    def __init__(self, id_pago, monto, metodo, cliente, fecha):
        self.id_pago = id_pago
        self.estado = "Pendiente"
        self.monto = monto
        self.cliente = cliente
        self.fecha = fecha
        self.metodo = metodo

    def procesar_pago(self, metodo_pago):
        if isinstance(metodo_pago, TarjetaCredito):
            if not metodo_pago:
                raise ValueError("No se proporcionó una tarjeta de crédito")
            if not metodo_pago.autorizar_pago(self.monto):
                raise ValueError("El pago fue rechazado por la entidad bancaria")
        self.estado = "Completado"
        self.metodo = metodo_pago

    def consultar_estado(self):
        return self.estado
    
    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def obtener_detalles(self):
        return {
            "id_pago": self.id_pago,
            "monto": self.monto,
            "cliente": self.cliente,
            "fecha": self.fecha,
            "estado": self.estado,
            "metodo": self.metodo
        }

    def __str__(self):
        return f"Pago de ${self.monto:.2f} - {self.cliente} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')} - {self.metodo}"
    
    def __repr__(self):
        return f"Pago(monto={self.monto}, cliente='{self.cliente}', fecha={self.fecha})"