from datetime import datetime

class Recibo:
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