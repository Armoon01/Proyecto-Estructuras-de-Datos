"""
Clase Producto simplificada para el sistema de e-commerce universitario.
Solo incluye funcionalidades esenciales.
"""

class Producto:
    """Clase simplificada para representar productos en el sistema."""
    
    def __init__(self, id_producto, nombre, precio, categoria="General", stock=0):
        """
        Inicializa un producto con información básica.
        
        Args:
            id_producto (str): ID único del producto
            nombre (str): Nombre del producto  
            precio (float): Precio del producto
            categoria (str): Categoría del producto
            stock (int): Cantidad disponible
        """
        # Validaciones básicas
        if not id_producto:
            raise ValueError("ID del producto no puede estar vacío")
        if not nombre:
            raise ValueError("Nombre del producto no puede estar vacío")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        # Atributos principales
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock
        self.disponible = stock > 0
    
    def actualizar_stock(self, cantidad):
        """
        Actualiza el stock del producto.
        
        Args:
            cantidad (int): Nueva cantidad de stock
            
        Returns:
            bool: True si se actualizó correctamente
        """
        if cantidad < 0:
            return False
        
        self.stock = cantidad
        self.disponible = cantidad > 0
        return True
    
    def reducir_stock(self, cantidad):
        """
        Reduce el stock en la cantidad especificada.
        
        Args:
            cantidad (int): Cantidad a reducir
            
        Returns:
            bool: True si hay suficiente stock y se redujo
        """
        if cantidad <= 0 or cantidad > self.stock:
            return False
        
        self.stock -= cantidad
        self.disponible = self.stock > 0
        return True
    
    def agregar_stock(self, cantidad):
        """
        Agrega stock al producto.
        
        Args:
            cantidad (int): Cantidad a agregar
            
        Returns:
            bool: True si se agregó correctamente
        """
        if cantidad <= 0:
            return False
        
        self.stock += cantidad
        self.disponible = True
        return True
    
    def actualizar_precio(self, nuevo_precio):
        """
        Actualiza el precio del producto.
        
        Args:
            nuevo_precio (float): Nuevo precio
            
        Returns:
            bool: True si se actualizó correctamente
        """
        if nuevo_precio < 0:
            return False
        
        self.precio = nuevo_precio
        return True
    
    def esta_disponible(self):
        """
        Verifica si el producto está disponible.
        
        Returns:
            bool: True si está disponible
        """
        return self.disponible and self.stock > 0
    
    def obtener_info_basica(self):
        """
        Obtiene información básica del producto.
        
        Returns:
            dict: Información básica del producto
        """
        return {
            'id': self.id_producto,
            'nombre': self.nombre,
            'precio': self.precio,
            'categoria': self.categoria,
            'stock': self.stock,
            'disponible': self.disponible
        }
    
    def __str__(self):
        """Representación en cadena del producto."""
        estado = "✅" if self.disponible else "❌"
        return f"{estado} {self.nombre} - ${self.precio:.2f} | Stock: {self.stock}"
    
    def __repr__(self):
        """Representación técnica del producto."""
        return f"Producto(id='{self.id_producto}', nombre='{self.nombre}', precio={self.precio}, stock={self.stock})"
    
    def __eq__(self, otro):
        """Compara productos por ID."""
        if not isinstance(otro, Producto):
            return False
        return self.id_producto == otro.id_producto
    
    def __hash__(self):
        """Hash basado en el ID del producto."""
        return hash(self.id_producto)
