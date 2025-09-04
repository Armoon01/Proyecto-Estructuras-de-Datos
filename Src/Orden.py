class Orden:

    def __init__(self, id_orden, fecha_compra, productos, recibo, fecha_entrega, fecha_envio, total):
        self.id = id_orden
        self.fecha = fecha_compra
        self.estado = "Pendiente"
        self.productos = productos
        self.recibo = recibo
        self.fecha_entrega = fecha_entrega
        self.fecha_envio = fecha_envio
        self.total = total

    def generar_recibo(self):
        from .Recibo import Recibo  # Importación local para evitar dependencias circulares
        self.recibo = Recibo(self)
        return self.recibo

    def consultar_estado(self):
        return self.estado
    
    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def calcular_total(self):
        self.total = sum(producto['precio'] * producto['cantidad'] for producto in self.productos)
        return self.total

    def __str__(self):
        return f"Orden #{self.id} - ${self.total:.2f} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"

    def __repr__(self):
        return f"Orden(id={self.id}, total={self.total})"
