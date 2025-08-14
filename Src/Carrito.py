import Cliente
import producto
import inventario

class Carrito:
    def __init__(self, Id):
        self.id = id
        self.productos = set()
        
    def agregar_producto(self, producto):
        if (producto):
            self.productos.push(producto)
            print(f"Producto {producto.get_nombre()} agregado al carrito.")
            
    def eliminar_producto(self, producto):
        id_producto = producto.get_id()
        
        for prod in self.productos:
            if prod.get_id() == id_producto:
                self.productos.remove(prod)
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
                print(f"{i}. Nombre: {producto.get_nombre()}, Precio: {producto.get_precio()}, Descripción: {producto.get_descripcion()}, ID: {producto.get_id()}")
                i += 1
    
producto1 = producto.Producto("Laptop", 1500, "Dell XPS 13", 1, 10)
producto2 = producto.Producto("Smartphone", 800, "iPhone 13", 2, 5) 
carrito = Carrito(1)
carrito.agregar_producto(producto1)
carrito.agregar_producto(producto2)
carrito.eliminar_producto(producto1)
        
    
        