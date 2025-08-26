from Carrito import Carrito
from Cliente import Cliente
from TarjetaCredito import TarjetaCredito
from Orden import Orden
from datetime import datetime
class Checkout:
    def __init__(self, carrito, cliente, tarjetaDeCredito=None):
        self.carrito = carrito
        self.cliente = cliente
        self.total = 0
        self.tarjetaDeCredito = tarjetaDeCredito

    def procesar_checkout(self, direccion_envio, metodo_pago):
        if not self.carrito.mostrar_carrito():
            raise ValueError("El carrito está vacío")
        self.calcular_total()
        self.verificar_stock()
        self.procesar_pago(metodo_pago)
        self.generar_orden(direccion_envio)
        self.actualizar_inventario()
        self.crear_recibo()
        self.carrito.vaciar_carrito()

    def calcular_total(self):
        for item in self.carrito.mostrar_carrito().obtener_elementos():
            if hasattr(item, 'producto'):  # Es un ItemCarrito
                self.total += item.producto.precio * item.cantidad
            else:  # Es un Producto directamente
                self.total += item.precio * item.stock

    def verificar_stock(self):
        for item in self.carrito.mostrar_carrito().obtener_elementos():
            if hasattr(item, 'producto'):  # Es un ItemCarrito
                if item.producto.stock < item.cantidad:
                    raise ValueError(f"El producto {item.producto.nombre} no tiene stock suficiente. Stock disponible: {item.producto.stock}, solicitado: {item.cantidad}")
            else:  # Es un Producto directamente
                if item.stock <= 0:
                    raise ValueError(f"El producto {item.nombre} no tiene stock disponible")
    
    def procesar_pago(self, metodo_pago):
        if metodo_pago == "Tarjeta de Crédito":
            if not self.tarjetaDeCredito:
                raise ValueError("No se proporcionó una tarjeta de crédito")
            if not self.tarjetaDeCredito.validar_tarjeta():
                raise ValueError("La tarjeta de crédito no es válida")
            if not self.tarjetaDeCredito.autorizar_pago(self.total):
                raise ValueError("El pago fue rechazado por la entidad bancaria")

    def generar_orden(self, direccion_envio):
        fecha_compra = datetime.now()
        fecha_entrega = fecha_compra.replace(day=fecha_compra.day + 5)
        fecha_envio = fecha_compra.replace(day=fecha_compra.day + 2)
        items = self.carrito.mostrar_carrito().obtener_elementos()
        self.orden = Orden(id_orden=1, fecha_compra=fecha_compra, productos=items, recibo=None, fecha_entrega=fecha_entrega, fecha_envio=fecha_envio, total=self.total)
        # Actualizar el estado después de la creación
        self.orden.actualizar_estado("Procesando")

    def actualizar_inventario(self):
        for item in self.carrito.mostrar_carrito().obtener_elementos():
            if hasattr(item, 'producto'):  # Es un ItemCarrito
                item.producto.reducir_stock(item.cantidad)
            else:  # Es un Producto directamente
                item.reducir_stock(item.stock)
    
    def crear_recibo(self):
        self.orden.generar_recibo()
        pass

    def vaciar_carrito(self):
        self.carrito.vaciar_carrito()
    
