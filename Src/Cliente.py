"""
Clase Cliente simplificada para el sistema de e-commerce universitario.
"""

class Cliente:
    """Clase para representar clientes del sistema."""
    
    def __init__(self, id_cliente, nombre, email, telefono=""):
        """
        Inicializa un cliente.
        
        Args:
            id_cliente (str): ID único del cliente
            nombre (str): Nombre completo del cliente
            email (str): Email del cliente
            telefono (str): Teléfono del cliente (opcional)
        """
        # Validaciones básicas
        if not id_cliente:
            raise ValueError("ID del cliente no puede estar vacío")
        if not nombre:
            raise ValueError("Nombre del cliente no puede estar vacío")
        if not email or "@" not in email:
            raise ValueError("Email debe ser válido")
        
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.activo = True
    
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
        return {
            'id': self.id_cliente,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'activo': self.activo
        }
    
    def __str__(self):
        """Representación en cadena del cliente."""
        estado = "✅" if self.activo else "❌"
        return f"{estado} {self.nombre} ({self.email})"
    
    def __repr__(self):
        """Representación técnica del cliente."""
        return f"Cliente(id='{self.id_cliente}', nombre='{self.nombre}', email='{self.email}')"
    
    def __eq__(self, otro):
        """Compara clientes por ID."""
        if not isinstance(otro, Cliente):
            return False
        return self.id_cliente == otro.id_cliente
    
    def __hash__(self):
        """Hash basado en el ID del cliente."""
        return hash(self.id_cliente)
