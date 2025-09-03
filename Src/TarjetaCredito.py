from datetime import datetime

class TarjetaCredito:
    def __init__(self, numero, titular, fecha_expiracion, cvv):
        self.numero = numero
        self.titular = titular
        self.fecha_expiracion = fecha_expiracion
        self.cvv = cvv
        self.fondo = 500000

    def validar(self):
        if len(self.numero) != 16 or not self.numero.isdigit():
            return False
        if len(self.cvv) != 3 or not self.cvv.isdigit():
            return False
        if self.fecha_expiracion < datetime.now().date():
            return False
        return True

    def validar_tarjeta(self):
        """Método de compatibilidad para validar_tarjeta()"""
        return self.validar()

    def autorizar_pago(self, monto):
        if not self.validar():
            raise ValueError("Tarjeta de crédito inválida")
        if monto < 0:
            raise ValueError("El monto a procesar debe ser positivo")
        if monto > self.fondo:
            raise ValueError("Fondos insuficientes en la tarjeta")

        self.fondo -= monto
        return True
