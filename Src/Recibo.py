from datetime import datetime

class Recibo:
    @classmethod
    def generar_desde_carrito(cls, id_recibo, cliente, carrito):
        """
        Genera un recibo a partir de un cliente y su carrito de compras.
        Args:
            id_recibo (str): ID único del recibo
            cliente: objeto cliente
            carrito: objeto carrito
        Returns:
            Recibo: instancia de Recibo
        """
        productos = carrito.obtener_items_agrupados() if hasattr(carrito, 'obtener_items_agrupados') else []
        subtotal = sum(item.producto.precio * item.cantidad for item in productos if hasattr(item, 'producto'))
        from .Orden import Orden
        orden = Orden(
            id_orden=id_recibo.replace('REC', 'ORD'),
            fecha_compra=datetime.now(),
            productos=productos,
            recibo=None,
            fecha_entrega=None,
            fecha_envio=None,
            total=subtotal
        )
        recibo = cls(orden)
        recibo.id_recibo = id_recibo
        recibo.cliente = cliente
        recibo.productos = productos
        recibo.monto_total = subtotal
        recibo.fecha_emision = orden.fecha
        recibo.estado = "Pagado"
        return recibo
    
    def __init__(self, orden):
        self.orden = orden  # Guardamos referencia a la orden

    def imprimir(self):
        print("=" * 40)
        print(f"      RECIBO DE COMPRA")
        print("=" * 40)
        print(f"Orden:   #{self.orden.id}")
        print(f"Fecha:   {self.orden.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Estado:  {self.orden.estado}")
        print("-" * 40)

        # Detalle de productos
        for item in self.orden.productos:
            if hasattr(item, 'producto'):  # Es un ItemCarrito
                nombre = item.producto.nombre
                cantidad = item.cantidad
                precio = item.producto.precio
            else:  # Es un Producto directamente
                nombre = item.nombre
                cantidad = item.stock
                precio = item.precio

            subtotal = precio * cantidad
            print(f"{nombre:20} x{cantidad:<3} ${subtotal:>7.2f}")

        print("-" * 40)
        print(f"TOTAL: ${self.orden.total:.2f}")
        print("=" * 40)

    def __str__(self):
        return f"Recibo de la Orden #{self.orden.id} - Total: ${self.orden.total:.2f}"