from Cliente import Cliente
from Producto import Producto
from estructuras.Lista import Lista
#from Inventario import inventario

class Carrito:
    def __init__(self, id):
        self.id = id
        self.productos = Lista()
        
    def agregar_producto(self, producto):
        id_producto = producto.getIdProducto()
        busqueda = self.productos.buscar(producto)
        if busqueda == -1:
            self.productos.agregar(producto)
            return True
        return False
          
    def eliminar_producto(self, producto):
        id_producto = producto.getIdProducto()
        busqueda = self.productos.buscar(producto)
        if busqueda != -1:
            self.productos.eliminar(producto)
            return True
        return False
    
    def mostrar_carrito(self):
        if not self.productos.esta_vacia():
            return self.productos
        return None

    def vaciar_carrito(self):
        """
        Vacía el carrito eliminando todos los productos.
        """
        self.productos.limpiar()
        return True

        