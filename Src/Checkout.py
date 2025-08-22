class Checkout:
    def __init__(self, carrito, cliente):
        self.carrito = carrito
        self.cliente = cliente
        self.total = 0
    def procesar_checkout(self, metodo_pago, direccion_envio):
        if not self.carrito.mostrar_carrito():
            raise ValueError("El carrito está vacío")
        self.calcular_total()
        self.verificar_stock()
        #self.procesar_pago(metodo_pago)
        #self.generar_orden(direccion_envio)
        self.actualizar_inventario()
        #self.crear_recibo()
        self.carrito.vaciar_carrito()

    def calcular_total(self):
        for producto in self.carrito.mostrar_carrito().obtener_elementos():
            self.total += producto.precio * producto.stock

    def verificar_stock(self):
        for producto in self.carrito.mostrar_carrito().obtener_elementos():
            if producto.stock <= 0:
                raise ValueError(f"El producto {producto.nombre} no tiene stock disponible")
    
    def procesar_pago(self, metodo_pago):
        #Implementar lógica de pago
        pass

    def generar_orden(self, direccion_envio):
        #Implementar lógica de generación de orden
        pass

    def actualizar_inventario(self):
        for producto in self.carrito.mostrar_carrito().obtener_elementos():
            producto.reducir_stock(producto.stock)
    
    def crear_recibo(self):
        #Implementar lógica de creación de recibo
        pass

    def vaciar_carrito(self):
        self.carrito.vaciar_carrito()
    
