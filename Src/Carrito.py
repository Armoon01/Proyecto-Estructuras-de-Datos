from datetime import datetime
from TarjetaCredito import TarjetaCredito

class ItemCarrito:
    """Representa un item en el carrito con cantidad"""
    def __init__(self, producto, cantidad=1):
        self.producto = producto
        self.cantidad = cantidad
        self.fecha_agregado = datetime.now()
    
    def __str__(self):
        return f"{self.producto.nombre} (x{self.cantidad})"

from estructuras.Lista import Lista

class Carrito:
    """
    Carrito de compras mejorado
    Análisis de complejidad:
    - Agregar producto: O(1) amortizado (diccionario)
    - Buscar producto: O(1) promedio (hash table)
    - Calcular total: O(n) donde n es número de items únicos
    - Buscar recursivo: O(n) en peor caso, O(log n) promedio
    """
    
    def __init__(self, cliente_id="invitado"):
        self.cliente_id = cliente_id
        self.productos = Lista()  # Lista de productos individuales
        self.items = {}  # Diccionario de items agrupados {producto_id: ItemCarrito}
        self.fecha_creacion = datetime.now()
        print(f"🛒 Carrito creado para cliente: {cliente_id}")
    
    def buscar_producto_recursivo(self, lista_productos, nombre_buscado, indice=0):
        """
        Función recursiva para buscar un producto por nombre
        Complejidad temporal: O(n) donde n es el número de productos
        Complejidad espacial: O(n) por la pila de recursión
        """
        # Caso base: llegamos al final de la lista
        if indice >= len(lista_productos):
            return None
        
        # Caso base: encontramos el producto
        producto_actual = lista_productos[indice]
        if hasattr(producto_actual, 'nombre') and nombre_buscado.lower() in producto_actual.nombre.lower():
            return producto_actual
        
        # Caso recursivo: buscar en el siguiente elemento
        return self.buscar_producto_recursivo(lista_productos, nombre_buscado, indice + 1)
    
    def calcular_descuento_recursivo(self, items_lista, indice=0, descuento_acumulado=0):
        """
        Función recursiva para calcular descuentos escalonados
        Complejidad temporal: O(n) donde n es número de items
        Complejidad espacial: O(n) por recursión
        """
        # Caso base: procesamos todos los items
        if indice >= len(items_lista):
            return descuento_acumulado
        
        item = items_lista[indice]
        producto = item.producto
        cantidad = item.cantidad
        
        # Lógica de descuento escalonado
        descuento_item = 0
        if cantidad >= 10:
            descuento_item = producto.precio * cantidad * 0.15  # 15% descuento
        elif cantidad >= 5:
            descuento_item = producto.precio * cantidad * 0.10  # 10% descuento
        elif cantidad >= 3:
            descuento_item = producto.precio * cantidad * 0.05  # 5% descuento
        
        # Caso recursivo: procesar siguiente item
        return self.calcular_descuento_recursivo(items_lista, indice + 1, descuento_acumulado + descuento_item)
    
    def _obtener_id_producto(self, producto):
        """Obtener ID del producto de manera robusta"""
        try:
            # Intentar obtener ID con diferentes métodos
            if hasattr(producto, 'id') and producto.id:
                return producto.id
            elif hasattr(producto, 'id_producto') and producto.id_producto:
                return producto.id_producto
            elif hasattr(producto, 'getIdProducto'):
                return producto.getIdProducto()
            else:
                # Como último recurso, usar el hash del objeto
                return str(hash(producto))
        except Exception as e:
            print(f"❌ Error obteniendo ID del producto: {e}")
            return str(hash(producto))
    
    def agregar_producto(self, producto, cantidad=1):
        """Agregar producto al carrito"""
        try:
            if not producto:
                print("❌ Error: Producto no válido")
                return False
            
            if cantidad <= 0:
                print("❌ Error: Cantidad debe ser mayor a 0")
                return False
            
            if producto.stock < cantidad:
                print(f"❌ Error: Stock insuficiente. Disponible: {producto.stock}")
                return False
            
            # ✅ ARREGLO: Usar método robusto para obtener ID
            producto_id = self._obtener_id_producto(producto)
            
            # Agregar a lista de productos individuales (para compatibilidad)
            for _ in range(cantidad):
                self.productos.agregar(producto)
            
            # Agregar o actualizar en items agrupados
            if producto_id in self.items:
                self.items[producto_id].cantidad += cantidad
            else:
                self.items[producto_id] = ItemCarrito(producto, cantidad)
            
            print(f"✅ Agregado {cantidad}x {producto.nombre} al carrito")
            print(f"📊 Total items en carrito: {self.obtener_cantidad_items()}")
            return True
            
        except Exception as e:
            print(f"❌ Error agregando producto al carrito: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def remover_producto(self, producto_id, cantidad=1):
        """Remover cantidad específica de un producto"""
        try:
            if producto_id not in self.items:
                print(f"❌ Producto {producto_id} no está en el carrito")
                return False
            
            item = self.items[producto_id]
            
            if cantidad >= item.cantidad:
                # Remover completamente
                return self.eliminar_producto_completo(producto_id)
            else:
                # Reducir cantidad
                item.cantidad -= cantidad
                
                # Remover de lista de productos individuales
                contador = 0
                nuevos_productos = []
                for p in self.productos:
                    p_id = self._obtener_id_producto(p)
                    if p_id == producto_id and contador < cantidad:
                        contador += 1
                        # No agregar a la nueva lista
                    else:
                        nuevos_productos.agregar(p)
                
                self.productos = nuevos_productos
                
                print(f"✅ Removido {cantidad}x {item.producto.nombre}")
                return True
                
        except Exception as e:
            print(f"❌ Error removiendo producto: {e}")
            return False
    
    def eliminar_producto_completo(self, producto_id):
        """Eliminar completamente un producto del carrito"""
        try:
            if producto_id not in self.items:
                print(f"❌ Producto {producto_id} no está en el carrito")
                return False
            
            item = self.items[producto_id]
            producto_nombre = item.producto.nombre
            
            # Remover de items agrupados
            del self.items[producto_id]
            
            # Remover de lista de productos individuales
            productos_iterable = self.productos
            try:
                productos_iterable = list(self.productos)
            except Exception:
                pass
            self.productos = [p for p in productos_iterable 
                              if self._obtener_id_producto(p) != producto_id]
            
            print(f"🗑️ Eliminado completamente: {producto_nombre}")
            return True
            
        except Exception as e:
            print(f"❌ Error eliminando producto completo: {e}")
            return False
    
    def obtener_items_agrupados(self):
        """Obtener lista de items agrupados por producto"""
        try:
            items_lista = list(self.items.values())
            print(f"📋 Obteniendo {len(items_lista)} items agrupados del carrito")
            return items_lista
        except Exception as e:
            print(f"❌ Error obteniendo items agrupados: {e}")
            return []
    
    def obtener_productos(self):
        """Obtener lista de productos individuales (compatibilidad)"""
        return self.productos.copy()
    
    def obtener_cantidad_items(self):
        """Obtener cantidad total de items en el carrito"""
        try:
            total = sum(item.cantidad for item in self.items.values())
            return total
        except Exception as e:
            print(f"❌ Error calculando cantidad de items: {e}")
            return 0
    
    def calcular_total(self):
        """Calcular total del carrito"""
        try:
            total = sum(item.producto.precio * item.cantidad for item in self.items.values())
            return total
        except Exception as e:
            print(f"❌ Error calculando total: {e}")
            return 0.0
    
    def obtener_resumen(self):
        """Obtener resumen detallado del carrito"""
        try:
            return {
                'cantidad_items': self.obtener_cantidad_items(),
                'cantidad_productos_unicos': len(self.items),
                'total': self.calcular_total(),
                'items': self.obtener_items_agrupados()
            }
        except Exception as e:
            print(f"❌ Error obteniendo resumen: {e}")
            return {
                'cantidad_items': 0,
                'cantidad_productos_unicos': 0, 
                'total': 0.0,
                'items': []
            }
    
    def limpiar(self):
        """Limpiar completamente el carrito"""
        try:
            self.productos.clear()
            self.items.clear()
            print("🧹 Carrito limpiado completamente")
        except Exception as e:
            print(f"❌ Error limpiando carrito: {e}")
    
    def esta_vacio(self):
        """Verificar si el carrito está vacío"""
        return len(self.items) == 0
    
    def __str__(self):
        return f"Carrito({self.cliente_id}): {self.obtener_cantidad_items()} items, ${self.calcular_total():.2f}"
    
    def __len__(self):
        return self.obtener_cantidad_items()
    
    def pago_Carrito(self, metodo_pago):
        if not isinstance(metodo_pago, TarjetaCredito):
            print("Método de pago no soportado")
            return False
        
        if self.esta_vacio():
            print("El carrito está vacío")
            return False

        total = self.calcular_total()
        print(f"💳 Procesando pago de ${total:.2f} para el carrito")
        if metodo_pago.autorizar_pago(total):
            self.limpiar()
            return True
        return False