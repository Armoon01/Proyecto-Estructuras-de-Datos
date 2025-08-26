import sys
import os

# Agregar el directorio Src al path para poder importar las clases
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Src'))

from Carrito import Carrito
from Producto import Producto

def test_carrito():
    print("=== TESTS PARA CARRITO ===")
    
    # Configuración inicial
    carrito = Carrito("CART001")
    producto1 = Producto("PROD001", "Laptop", "Computadora portátil", 1500.0, 10)
    producto2 = Producto("PROD002", "Mouse", "Mouse inalámbrico", 25.0, 50)
    
    # Test 1: Crear carrito
    print("\n1. Test crear carrito:")
    print(f"ID del carrito: {carrito.id}")
    print(f"Productos inicializados: {carrito.productos is not None}")
    
    # Test 2: Agregar producto
    print("\n2. Test agregar producto:")
    carrito.agregar_producto(producto1)
    carrito.agregar_producto(producto2)
    productos = carrito.mostrar_carrito()
    print(f"Producto agregado exitosamente: {productos is not None}")
    if productos:
        print(f"Carrito vacío: {productos.esta_vacia()}")
    
    print(f"Productos en el carrito: {[prod.nombre for prod in productos.obtener_elementos()]}")
    # Test 3: Eliminar producto
    print("\n3. Test eliminar producto:")
    resultado = carrito.eliminar_producto(producto1)
    print(f"Producto eliminado exitosamente: {resultado}")
    
    # Test 4: Carrito vacío
    print("\n4. Test carrito vacío:")
    carrito_vacio = Carrito("CART002")
    productos_vacio = carrito_vacio.mostrar_carrito()
    print(f"Carrito vacío retorna: {productos_vacio}")
    if productos_vacio:
        print(f"¿Está vacío?: {productos_vacio.esta_vacia()}")

if __name__ == '__main__':
    test_carrito()