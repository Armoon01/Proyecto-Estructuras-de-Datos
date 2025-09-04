from datetime import datetime

class TarjetaCredito:
    def __init__(self, numero, titular, fecha_expiracion, cvv):
        self.numero = numero
        self.titular = titular
        self.fecha_expiracion = fecha_expiracion
        self.cvv = cvv
        self.fondo = 500000

    def validar(self):
        if not self.numero or len(self.numero) != 16 or not self.numero.isdigit():
            raise ValueError("El número de tarjeta debe tener 16 dígitos numéricos")
        if not self.cvv or len(self.cvv) != 3 or not self.cvv.isdigit():
            raise ValueError("El CVV debe tener 3 dígitos numéricos")
        if not self.titular or len(self.titular.strip()) < 3:
            raise ValueError("El nombre del titular es obligatorio y debe tener al menos 3 caracteres")
        if not self.fecha_expiracion:
            raise ValueError("La fecha de expiración es obligatoria")
        if self.fecha_expiracion < datetime.now().date():
            raise ValueError("La tarjeta está vencida")
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
    
    def get_numero(self):
        return self.numero
    def get_titular(self):
        return self.titular