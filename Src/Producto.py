class Producto:
    def __init__(self, id_producto, nombre, descripcion, precio, stock=0, imagen_ruta=None):
        """
        Inicializa un producto con información básica.
        
        Args:
            id_producto (str): ID único del producto
            nombre (str): Nombre del producto  
            precio (float): Precio del producto
            descripcion (str): Descripcion del producto
            stock (int): Cantidad disponible
            imagen_ruta (str): Ruta a la imagen del producto
        """
        if not id_producto:
             raise ValueError("ID del producto no puede estar vacío")

        if not nombre:
            raise ValueError("Nombre del producto no puede estar vacío")
        
        # ✅ ARREGLO: Mantener ambos atributos para compatibilidad
        self.id_producto = id_producto
        self.id = id_producto  # ← Agregar esta línea para compatibilidad
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen_ruta = imagen_ruta or 'Images\\productos\\producto_default.png'
        
        # ✅ ARREGLO: Agregar atributo imagen para compatibilidad con InterfazCarrito
        self.imagen = self.imagen_ruta

    def actualizar_stock(self, stock):
        """Actualizar stock del producto"""
        if stock < 0:
            raise ValueError("Stock no puede ser negativo")
        self.stock = stock

    def actualizar_precio(self, precio):
        """Actualizar precio del producto"""
        if precio < 0:
            raise ValueError("Precio no puede ser negativo")
        self.precio = precio

    def actualizar_imagen(self, imagen_ruta):
        """Actualizar la ruta de la imagen del producto"""
        self.imagen_ruta = imagen_ruta
        self.imagen = imagen_ruta  # ✅ Mantener sincronizado

    def reducir_stock(self, cantidad):
        """Reducir stock del producto"""
        if cantidad < 0:
            raise ValueError("Cantidad a reducir no puede ser negativa")
        if cantidad > self.stock:
            raise ValueError(f"No hay suficiente stock. Disponible: {self.stock}")
        self.stock = self.stock - cantidad

    def aumentar_stock(self, cantidad):
        """Aumentar stock del producto"""
        if cantidad < 0:
            raise ValueError("Cantidad a aumentar no puede ser negativa")
        self.stock = self.stock + cantidad

    def tiene_stock_suficiente(self, cantidad):
        """Verificar si hay stock suficiente"""
        return self.stock >= cantidad

    def getIdProducto(self):
        """Obtener ID del producto (método legacy)"""
        return self.id_producto
    
    def get_id(self):
        """Obtener ID del producto (método moderno)"""
        return self.id
    
    def get_nombre(self):
        """Obtener nombre del producto"""
        return self.nombre
    
    def get_precio(self):
        """Obtener precio del producto"""
        return self.precio
    
    def get_stock(self):
        """Obtener stock del producto"""
        return self.stock
    
    def get_imagen_ruta(self):
        """Obtener ruta de imagen del producto"""
        return self.imagen_ruta
    
    def to_dict(self):
        """Convertir producto a diccionario"""
        return {
            'id': self.id,
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'imagen_ruta': self.imagen_ruta,
            'imagen': self.imagen
        }
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f} (Stock: {self.stock})"
    
    def __repr__(self):
        return f"Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio}, stock={self.stock})"
    
    def __eq__(self, other):
        """Verificar igualdad entre productos"""
        if isinstance(other, Producto):
            return self.id == other.id
        return False
    
    def __hash__(self):
        """Hash para uso en sets y diccionarios"""
        return hash(self.id)