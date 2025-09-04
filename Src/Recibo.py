from datetime import datetime

class Recibo:
    @property
    def id(self):
        return self.id_recibo
    """Clase que representa un recibo de compra en el sistema de e-commerce."""

    def __init__(self, id_recibo, cliente, productos, monto_total, metodo_pago):
        """
        Inicializa un recibo.

        Args:
            id_recibo (str): ID único del recibo
            cliente (Cliente): Cliente que genera el recibo
            productos (list): Lista de productos comprados
            monto_total (float): Total pagado en la compra
            metodo_pago (TarjetaCredito): Método de pago usado
        """
        self.id_recibo = id_recibo
        self.cliente = cliente
        self.productos = productos  # Lista de productos (objetos Producto)
        self.monto_total = monto_total
        self.metodo_pago = metodo_pago
        self.fecha_emision = datetime.now()
        self.estado = "Pagado"


    @classmethod
    def generar_desde_carrito(cls, id_recibo, cliente, carrito):
        """
        Genera un recibo a partir de un cliente y su carrito de compras.

        Args:
            id_recibo (str): ID único del recibo
            cliente (Cliente): Cliente que realiza la compra
            carrito (Carrito): Carrito con los productos seleccionados

        Returns:
            Recibo: Objeto Recibo generado
        """
        # Usar obtener_items_agrupados() para compatibilidad con la clase Carrito actual
        productos = carrito.obtener_items_agrupados() if carrito and hasattr(carrito, 'obtener_items_agrupados') else []
        monto_total = sum(getattr(p, "precio", 0) for p in productos)
        return cls(id_recibo, cliente, productos, monto_total, cliente.get_metodo_pago())

    def imprimir(self):
        """Imprime el recibo en pantalla (ejemplo de interfaz simple)."""
        print("\n" + "=" * 40)
        print(f"RECIBO #{self.id_recibo}")
        print(f"Cliente: {self.cliente.get_nombre()} ({self.cliente.get_id_cliente()})")
        print(f"Email: {self.cliente.get_email()}")
        print(f"Fecha: {self.fecha_emision.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 40)
        print("Productos:")
        for p in self.productos:
            nombre = getattr(p, "nombre", "Desconocido")
            precio = getattr(p, "precio", 0.0)
            print(f" - {nombre}: ${precio:.2f}")
        print("-" * 40)
        print(f"Método de pago: {self.metodo_pago.get_numero() if self.metodo_pago else 'N/A'}")
        print(f"TOTAL: ${self.monto_total:.2f}")
        print(f"Estado: {self.estado}")
        print("=" * 40 + "\n")

    def __repr__(self):
        return f"Recibo(id='{self.id_recibo}', cliente='{self.cliente.get_nombre()}', total={self.monto_total})"