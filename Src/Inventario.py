import csv
import os
from Producto import Producto
from estructuras.Lista import Lista

class Inventario:
    """Clase para gestionar el inventario de productos"""
    
    def __init__(self):
        self.productos = Lista()
        self.cargar_productos()
    
    def cargar_productos(self):
        """Cargar productos desde archivo CSV"""
        try:
            # Ruta al archivo CSV
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'productos.csv')
            
            if os.path.exists(data_path):
                with open(data_path, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        imagen_ruta = row.get('imagen_ruta', 'Images\\productos\\producto_default.png')
                        
                        producto = Producto(
                            id_producto=row['id_producto'],
                            nombre=row['nombre'],
                            descripcion=row['descripcion'],
                            precio=float(row['precio']),
                            stock=int(row['stock']),
                            imagen_ruta=imagen_ruta
                        )
                        
                        self.productos.agregar(producto)
            else:
                # Crear productos de ejemplo
                self.crear_productos_ejemplo()
                
        except Exception as e:
            print(f"Error cargando inventario: {e}")
            self.crear_productos_ejemplo()
    
    def crear_productos_ejemplo(self):
        """Crear productos de ejemplo"""
        productos_ejemplo = [
            {
                'id_producto': '1', 
                'nombre': 'Aceite Roland Especial Sésamo', 
                'precio': 4000, 
                'descripcion': 'Aceite especial de sésamo Roland - 185ml',
                'stock': 10,
                'imagen_ruta': 'Images\\productos\\aceite_sesamo.png'
            },
            {
                'id_producto': '2', 
                'nombre': 'Frijoles La Costeña Charros', 
                'precio': 1820, 
                'descripcion': 'Frijoles charros en lata - 560g',
                'stock': 25,
                'imagen_ruta': 'Images\\productos\\frijoles_charros.png'
            },
            {
                'id_producto': '3', 
                'nombre': 'Chop Suey Yigui', 
                'precio': 1900, 
                'descripcion': 'Chop suey presentación mediano bolsa - 425g',
                'stock': 15,
                'imagen_ruta': 'Images\\productos\\chop_suey.png'
            },
            {
                'id_producto': '4', 
                'nombre': 'Chiles Jalapeños Malher', 
                'precio': 610, 
                'descripcion': 'Chiles jalapeños Malher Trocitos Lata - 156g',
                'stock': 30,
                'imagen_ruta': 'Images\\productos\\chiles_jalapenos.png'
            }
        ]
        
        for prod_data in productos_ejemplo:
            producto = Producto(
                id_producto=prod_data['id_producto'],
                nombre=prod_data['nombre'],
                descripcion=prod_data['descripcion'],
                precio=prod_data['precio'],
                stock=prod_data['stock'],
                imagen_ruta=prod_data['imagen_ruta']
            )
            self.productos.agregar(producto)
    
    def obtener_productos(self):
        """Obtener lista de productos"""
        return self.productos.obtener_elementos()
    
    def buscar_producto(self, id_producto):
        """Buscar producto por ID"""
        elementos = self.productos.obtener_elementos()
        for producto in elementos:
            if producto.getIdProducto() == id_producto:
                return producto
        return None
    
    def agregar_producto(self, producto):
        """Agregar nuevo producto al inventario"""
        if self.buscar_producto(producto.getIdProducto()) is None:
            self.productos.agregar(producto)
            return True
        return False
    
    def actualizar_stock(self, id_producto, nuevo_stock):
        """Actualizar stock de un producto"""
        producto = self.buscar_producto(id_producto)
        if producto:
            producto.actualizar_stock(nuevo_stock)
            return True
        return False
    
    def reducir_stock(self, id_producto, cantidad):
        """Reducir stock de un producto Y GUARDAR CAMBIOS"""
        producto = self.buscar_producto(id_producto)
        if producto and producto.stock >= cantidad:
            producto.reducir_stock(cantidad)
            # ✅ GUARDAR CAMBIOS EN CSV
            self.guardar_productos()
            return True
        return False
    
    def guardar_productos(self):
        """Guardar productos actualizados en CSV"""
        try:
            # Ruta al archivo CSV  
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'productos.csv')
            
            # Crear backup del archivo original
            if os.path.exists(data_path):
                backup_path = data_path + '.bak'
                import shutil
                shutil.copy2(data_path, backup_path)
            
            # Escribir productos actualizados
            with open(data_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Escribir header
                writer.writerow(['id_producto', 'nombre', 'precio', 'descripcion', 'stock', 'imagen_ruta'])
                
                # Escribir todos los productos con su stock actualizado
                elementos = self.productos.obtener_elementos()
                for producto in elementos:
                    writer.writerow([
                        producto.id_producto,
                        producto.nombre,  
                        producto.precio,
                        producto.descripcion,
                        producto.stock,  # ✅ Stock actualizado
                        producto.imagen_ruta
                    ])
            
            print(f"💾 Productos guardados en {data_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando productos: {e}")
            return False
    
    def obtener_productos_disponibles(self):
        """Obtener solo productos con stock disponible"""
        productos_disponibles = []
        elementos = self.productos.obtener_elementos()
        for producto in elementos:
            if producto.stock > 0:
                productos_disponibles.append(producto)
        return productos_disponibles
    
    def __str__(self):
        """Representación en string del inventario"""
        elementos = self.productos.obtener_elementos()
        return f"Inventario con {len(elementos)} productos"