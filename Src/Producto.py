class Producto:
    def __init__(self,id_producto,nombre,descripcion,precio,stock = 0):
        """
        Inicializa un producto con información básica.
        
        Args:
            id_producto (str): ID único del producto
            nombre (str): Nombre del producto  
            precio (float): Precio del producto
            descripcion (str): Descripcion del producto
            stock (int): Cantidad disponible
        """
        if not id_producto:
             raise ValueError("ID del producto no puede estar vacío")

        if not nombre:
            raise ValueError("Nombre del cliente no puede estar vacío")
        
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    def actualizar_stock(self,stock):
        self.stock = stock

    def actualizar_precio(self,precio):
        self.precio = precio

    def reducir_stock(self,cantidad):
        self.stock = self.stock - cantidad

    def getIdProducto(self):
        return self.id_producto
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f}"
    
    def __repr__(self):
        return f"Producto(id_producto={self.id_producto}, nombre='{self.nombre}', precio={self.precio})"
    
    def __eq__(self, other):
        
        if isinstance(other, Producto):
            return self.id_producto == other.id_producto
        return False