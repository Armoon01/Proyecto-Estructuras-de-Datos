from Carrito import Carrito
from Producto import Producto
from estructuras.Lista import Lista
from TarjetaCredito import TarjetaCredito

class Cliente:
    """Clase para representar clientes del sistema."""

    def __init__(self, id_cliente, nombre, email, carrito, tarjeta=None, telefono=""):
        """
        Inicializa un cliente.

        Args:
            id_cliente (str): ID único del cliente
            nombre (str): Nombre completo del cliente
            email (str): Email del cliente
            telefono (str): Teléfono del cliente (opcional)
            carrito (Carrito): Carrito asociado al cliente
            tarjeta (TarjetaCredito, opcional): Tarjeta de crédito asociada
        """
        # Validaciones básicas
        if not id_cliente:
            raise ValueError("ID del cliente no puede estar vacío")
        if not nombre:
            raise ValueError("Nombre del cliente no puede estar vacío")
        if not email or "@" not in email:
            raise ValueError("Email debe ser válido")
        if tarjeta is not None and not isinstance(tarjeta, TarjetaCredito):
            raise ValueError("Se debe proporcionar una tarjeta de crédito válida")

        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.activo = True
        self.carrito = carrito
        # Nueva funcionalidad: Lista de órdenes del cliente
        self.ordenes = Lista()  # Lista para almacenar el historial de órdenes
        self.metodo_pago = tarjeta  # Tarjeta de crédito asociada al cliente
    
    def agregar_orden(self, orden):
        """
        Agrega una orden al historial del cliente.
        
        Args:
            orden (Orden): Orden a agregar al historial
            
        Returns:
            bool: True si se agregó correctamente
        """
        try:
            if orden and hasattr(orden, 'id'):
                self.ordenes.agregar(orden)
                return True
            return False
        except Exception:
            return False
    
    def obtener_ordenes(self):
        """
        Obtiene todas las órdenes del cliente.
        
        Returns:
            list: Lista de órdenes del cliente
        """
        return self.ordenes.copy()  # Retorna una copia para evitar modificaciones externas
    
    def obtener_orden_por_id(self, id_orden):
        """
        Busca una orden específica por su ID.
        
        Args:
            id_orden: ID de la orden a buscar
            
        Returns:
            Orden: La orden encontrada o None si no existe
        """
        for orden in self.ordenes:
            if hasattr(orden, 'id') and orden.id == id_orden:
                return orden
        return None
    
    def obtener_ordenes_activas(self):
        """
        Obtiene las órdenes que están en proceso (no entregadas).
        
        Returns:
            list: Lista de órdenes activas
        """
        ordenes_activas = []
        for orden in self.ordenes:
            if hasattr(orden, 'estado') and orden.estado in ['Pendiente', 'Procesando', 'Enviado']:
                ordenes_activas.agregar(orden)
        return ordenes_activas
    
    def obtener_total_gastado(self):
        """
        Calcula el total gastado por el cliente en todas sus órdenes.
        
        Returns:
            float: Total gastado por el cliente
        """
        total_gastado = 0.0
        for orden in self.ordenes:
            if hasattr(orden, 'total'):
                total_gastado += orden.total
        return total_gastado
    
    def contar_ordenes(self):
        """
        Cuenta el número total de órdenes del cliente.
        
        Returns:
            int: Número de órdenes
        """
        return len(self.ordenes)
    
    def obtener_ultima_orden(self):
        """
        Obtiene la orden más reciente del cliente.
        
        Returns:
            Orden: La orden más reciente o None si no hay órdenes
        """
        if self.ordenes:
            return self.ordenes[-1]  # La última orden agregada
        return None
    
    def actualizar_info(self, nombre=None, email=None, telefono=None):
        """
        Actualiza información del cliente.
        
        Args:
            nombre (str, optional): Nuevo nombre
            email (str, optional): Nuevo email
            telefono (str, optional): Nuevo teléfono
            
        Returns:
            bool: True si se actualizó correctamente
        """
        try:
            if nombre:
                self.nombre = nombre
            if email and "@" in email:
                self.email = email
            if telefono is not None:  # Permite vacío
                self.telefono = telefono
            return True
        except:
            return False
    
    def obtener_carrito(self):
        """
        Obtiene el carrito del cliente.
        
        Returns:
            Carrito: Carrito asociado al cliente
        """
        return self.carrito
    def agregar_producto_al_carrito(self, producto):
        """
        Agrega un producto al carrito del cliente.
        Args:
            producto (Producto): Producto a agregar
        Returns:
            bool: True si se agregó correctamente
        """
        if self.carrito:
            return self.carrito.agregar_producto(producto)
        return False
    def eliminar_producto_del_carrito(self, producto):
        """
        Elimina un producto del carrito del cliente.
        Args:
            producto (Producto): Producto a eliminar
        Returns:
            bool: True si se eliminó correctamente 
        """
        if self.carrito:
            return self.carrito.eliminar_producto(producto)
        return False
    def mostrar_carrito(self):
        """
        Muestra los productos en el carrito del cliente.
        Returns:
            Lista: Lista de productos en el carrito
        """
        if self.carrito:
            return self.carrito.mostrar_carrito()
        return None
    def vaciar_carrito(self):
        """
        Vacía el carrito del cliente.
        
        Returns:
            bool: True si se vació correctamente
        """
        # En lugar de productos encargarse de limpiar deberia ser el carrito.
        if self.carrito:
            self.carrito.productos.limpiar()
            return True
        return False
    def get_id_cliente(self):
        """
        Obtiene el ID del cliente.
        
        Returns:
            str: ID del cliente
        """
        return self.id_cliente
    def get_nombre(self):
        """
        Obtiene el nombre del cliente.
        Returns:
            str: Nombre del cliente
        """
        return self.nombre
    def get_email(self):
        """
        Obtiene el email del cliente.
        Returns:
            str: Email del cliente
        """
        return self.email
    def get_telefono(self):
        """
        Obtiene el teléfono del cliente.
        Returns:
            str: Teléfono del cliente
        """
        return self.telefono
    def get_metodo_pago(self):
        """
        Obtiene el método de pago del cliente.
        Returns:
            obj: Tarjeta de Credito
        """
        return self.metodo_pago
    
    def set_telefono(self, telefono):
        """
        Actualiza el teléfono del cliente.
        Args:
            telefono (str): Nuevo teléfono
        """
        if telefono:
            self.telefono = telefono
        else:
            raise ValueError("Teléfono no puede estar vacío")
    def set_email(self, email):
        """
        Actualiza el email del cliente.
        
        Args:
            email (str): Nuevo email
        """
        if "@" in email:
            self.email = email
        else:
            raise ValueError("Email debe ser válido")
    def set_nombre(self, nombre):
        """
        Actualiza el nombre del cliente.
        
        Args:
            nombre (str): Nuevo nombre
        """
        if nombre:
            self.nombre = nombre
        else:
            raise ValueError("Nombre no puede estar vacío")
    def set_id_cliente(self, id_cliente):
        """
        Actualiza el ID del cliente.
        
        Args:
            id_cliente (str): Nuevo ID del cliente
        """
        if id_cliente:
            self.id_cliente = id_cliente
        else:
            raise ValueError("ID del cliente no puede estar vacío")

    def set_metodo_pago(self, tarjeta):
        """
        Asigna o actualiza la tarjeta de crédito del cliente.
        Args:
            tarjeta (TarjetaCredito): Tarjeta de crédito válida
        """
        # Validación flexible: acepta cualquier objeto con los métodos requeridos
        if not (hasattr(tarjeta, 'validar') and hasattr(tarjeta, 'autorizar_pago')):
            raise ValueError("Se debe proporcionar una tarjeta de crédito válida")
        self.metodo_pago = tarjeta

    def desactivar(self):
        """Desactiva el cliente."""
        self.activo = False

    def activar(self):
        """Activa el cliente."""
        self.activo = True
    
    def esta_activo(self):
        """Verifica si el cliente está activo."""
        return self.activo
    
    def obtener_info(self):
        """
        Obtiene información del cliente.
        
        Returns:
            dict: Información del cliente
        """
        # Deberia implementarse un metodo de confirmacion de que no haya objetos vacios antes de mandar la informacion
        return {
            'id': self.id_cliente,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'activo': self.activo,
            'total_ordenes': self.contar_ordenes(),
            'total_gastado': self.obtener_total_gastado(),
            'ordenes_activas': len(self.obtener_ordenes_activas()),
            'metodo_pago': self.metodo_pago.get_numero()
        }
    
    def __repr__(self):
        """Representación técnica del cliente."""
        return f"Cliente(id='{self.id_cliente}', nombre='{self.nombre}', email='{self.email}', ordenes={self.contar_ordenes()})"
    
    def __eq__(self, otro):
        """Compara clientes por ID."""
        if not isinstance(otro, Cliente):
            return False
        return self.id_cliente == otro.id_cliente
    
    def __hash__(self):
        """Hash basado en el ID del cliente."""
        return hash(self.id_cliente)
