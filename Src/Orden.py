import time

class Orden:
    
    def __init__(self, id, fecha, estado, recibo, fechaEntrega, fecha_envio):
        self.id = id
        self.fecha = fecha
        self.estado = estado
        self.recibo = recibo
        self.Productos = set()
        self.fechaEntrega = fechaEntrega
        self.fecha_envio = fecha_envio

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getFecha(self):
        return self.fecha

    def setFecha(self, fecha):
        self.fecha = fecha

    def getEstado(self):
        return self.estado

    def setEstado(self, estado):
        self.estado = estado

    def getRecibo(self):
        return self.recibo

    def setRecibo(self, recibo):
        self.recibo = recibo

    def getFechaEntrega(self):
        return self.fechaEntrega

    def setFechaEntrega(self, fechaEntrega):
        self.fechaEntrega = fechaEntrega

    def getFechaEnvio(self):
        return self.fecha_envio

    def setFechaEnvio(self, fecha_envio):
        self.fecha_envio = fecha_envio
        
    