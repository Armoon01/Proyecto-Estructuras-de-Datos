import Cliente
import Producto
#import inventario

class Carrito:
    def __init__(self, id):
        self.id = id
        self.productos = set()
        
    def agregar_producto(self, producto):
        if producto:
            self.productos.add(producto)
            print(f"Producto {producto.getNombre()} agregado al carrito.")

    def eliminar_producto(self, producto):
        id_producto = producto.getIdProducto()
        for prod in list(self.productos):
            if prod.getIdProducto() == id_producto:
                self.productos.remove(prod)
                print(f"Producto {prod.getNombre()} eliminado del carrito.")
                return True
        print("Producto no encontrado en el carrito.")
        return False
    
    def mostrar_carrito(self):
        if not self.productos:
            print("El carrito está vacío.")
            return
        
        else:
            print("Productos en el carrito:")
            for producto in self.productos:
                i=1
                print(f"{i}. Nombre: {producto.getNombre()}, Precio: {producto.getPrecio()}, Descripción: {producto.getDescripcion()}, ID: {producto.getIdProducto()}")
                i += 1

        