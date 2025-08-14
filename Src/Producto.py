import exception

class Producto:
    
    def __init__(self, descripcion, precio, nombre, id_producto, stock):
        self.descripcion = descripcion
        self.precio = precio
        self.nombre = nombre
        self.id_producto = id_producto
        self.stock = stock

    def getDescripcion(self):
        return self.descripcion

    def setDescripcion(self, descripcion):
        self.descripcion = descripcion

    def getPrecio(self):
        return self.precio

    def setPrecio(self, precio):
        self.precio = precio

    def getNombre(self):
        return self.nombre

    def setNombre(self, nombre):
        self.nombre = nombre

    def getIdProducto(self):
        return self.id_producto

    def setIdProducto(self, id_producto):
        self.id_producto = id_producto


    def actualizar_stock(self, cant, actualizacion):
      
        if (cant <= 0 or cant > self.stock and actualizacion == False):
            print("Cantidad no válida para actualizar el stock.") #cambiar a excepciones
            return 
        
        else:
            if (actualizacion):
                self.stock += cant
                
            else:
                self.stock -= cant