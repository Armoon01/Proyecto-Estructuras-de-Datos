from datetime import datetime

class TarjetaCredito:
    def __init__(self, numero, titular, fecha_expiracion, cvv):
        self.numero = numero
        self.titular = titular
        self.fecha_expiracion = fecha_expiracion
        self.cvv = cvv
        self.fondo = 0

    def validar(self):
        if len(self.numero) != 16 or not self.numero.isdigit():
            return False
        if len(self.cvv) != 3 or not self.cvv.isdigit():
            return False
        if self.fecha_expiracion < datetime.now().date():
            return False
        return True
    
    def agregar_fondo(self, monto):
        """Agrega un monto al total de la tarjeta"""
        if not self.validar():
            raise ValueError("Tarjeta de crédito inválida")
        if monto < 0:
            raise ValueError("El monto a agregar debe ser positivo")
        self.fondo += monto

    def validar_tarjeta(self):
        """Método de compatibilidad para validar_tarjeta()"""
        return self.validar()

    def autorizar_pago(self, monto):
        """Autoriza un pago por el monto especificado"""
        if not self.validar():
            return False
        # Simulamos autorización exitosa
        return True

    def procesar_pago(self, monto):
        if not self.validar():
            raise ValueError("Tarjeta de crédito inválida")
        if monto < 0:
            raise ValueError("El monto a procesar debe ser positivo")
        if monto > self.fondo:
            raise ValueError("Fondos insuficientes en la tarjeta")

        self.fondo -= monto
        return True
