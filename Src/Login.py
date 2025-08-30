"""
Sistema de Login y Autenticación para el sistema de e-commerce universitario.
"""
import hashlib
import csv
import os
from datetime import datetime
from Cliente import Cliente
from Carrito import Carrito

class SistemaLogin:
    """Clase para manejar autenticación y gestión de usuarios."""
    
    def __init__(self):
        self.usuarios_db = {}  # En memoria para acceso rápido
        self.usuario_actual = None
        self.archivo_clientes = os.path.join(os.path.dirname(__file__), '..', 'Data', 'clientes.csv')
        self.archivo_usuarios = os.path.join(os.path.dirname(__file__), '..', 'Data', 'usuarios.csv')
        self.cargar_usuarios()
    
    def hash_password(self, password):
        """Genera hash seguro de la contraseña."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def cargar_usuarios(self):
        """Carga usuarios desde archivos CSV."""
        try:
            # Cargar desde el nuevo archivo de usuarios (formato completo)
            if os.path.exists(self.archivo_usuarios):
                self.cargar_desde_usuarios_csv()
            # Si no existe, migrar desde clientes.csv existente
            elif os.path.exists(self.archivo_clientes):
                self.migrar_desde_clientes_csv()
            else:
                # Crear usuario administrador por defecto
                self.crear_usuario_admin_default()
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")
            self.crear_usuario_admin_default()
    
    def cargar_desde_usuarios_csv(self):
        """Carga usuarios desde el archivo usuarios.csv (formato completo)."""
        with open(self.archivo_usuarios, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.usuarios_db[row['id_usuario']] = {
                    'id_usuario': row['id_usuario'],
                    'nombre': row['nombre'],
                    'email': row['email'],
                    'password_hash': row['password_hash'],
                    'rol': row.get('rol', 'cliente'),
                    'fecha_creacion': row['fecha_creacion'],
                    'activo': row.get('activo', 'True').lower() == 'true',
                    'telefono': row.get('telefono', ''),
                    'intentos_login': int(row.get('intentos_login', '0')),
                    'ultimo_login': row.get('ultimo_login', None)
                }
    
    def migrar_desde_clientes_csv(self):
        """Migra datos desde clientes.csv al nuevo formato."""
        print("Migrando datos desde clientes.csv...")
        
        # Crear admin por defecto
        self.crear_usuario_admin_default()
        
        # Migrar clientes existentes
        with open(self.archivo_clientes, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Generar ID único basado en email
                id_usuario = row['email'].split('@')[0]
                contador = 1
                id_original = id_usuario
                
                while id_usuario in self.usuarios_db:
                    id_usuario = f"{id_original}{contador}"
                    contador += 1
                
                # Migrar usuario
                self.usuarios_db[id_usuario] = {
                    'id_usuario': id_usuario,
                    'nombre': row['nombre'],
                    'email': row['email'],
                    'password_hash': row['password'],  # Asumir que ya está hasheado
                    'rol': 'cliente',
                    'fecha_creacion': row.get('fecha_registro', datetime.now().isoformat()),
                    'activo': True,
                    'telefono': '',
                    'intentos_login': 0,
                    'ultimo_login': row.get('ultimo_login', None)
                }
        
        # Guardar en el nuevo formato
        self.guardar_usuarios()
        print(f"Migración completada. {len(self.usuarios_db)-1} clientes migrados.")
    
    def guardar_usuarios(self):
        """Guarda usuarios en archivo CSV."""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.archivo_usuarios), exist_ok=True)
            
            # Guardar en formato CSV
            with open(self.archivo_usuarios, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['id_usuario', 'nombre', 'email', 'password_hash', 'rol', 
                            'fecha_creacion', 'activo', 'telefono', 'intentos_login', 'ultimo_login']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for usuario_data in self.usuarios_db.values():
                    # Convertir datos para CSV
                    row_data = usuario_data.copy()
                    row_data['activo'] = str(row_data['activo'])  # Convertir boolean a string
                    row_data['intentos_login'] = str(row_data['intentos_login'])
                    if row_data['ultimo_login'] is None:
                        row_data['ultimo_login'] = ''
                    
                    writer.writerow(row_data)
                    
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")
    
    def crear_usuario_admin_default(self):
        """Crea usuario administrador por defecto."""
        admin_data = {
            'id_usuario': 'admin',
            'nombre': 'Administrador',
            'email': 'admin@universidad.edu',
            'password_hash': self.hash_password('admin123'),
            'rol': 'administrador',
            'fecha_creacion': datetime.now().isoformat(),
            'activo': True,
            'telefono': '000-000-0000',
            'intentos_login': 0,
            'ultimo_login': None
        }
        self.usuarios_db['admin'] = admin_data
        self.guardar_usuarios()
        print("Usuario administrador creado: admin/admin123")
    
    def sincronizar_con_clientes_csv(self):
        """Mantiene sincronización con el archivo clientes.csv para compatibilidad."""
        try:
            # Solo sincronizar clientes (no administradores)
            clientes = [user for user in self.usuarios_db.values() if user['rol'] == 'cliente']
            
            with open(self.archivo_clientes, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['email', 'password', 'nombre', 'fecha_registro', 'ultimo_login']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for cliente in clientes:
                    writer.writerow({
                        'email': cliente['email'],
                        'password': cliente['password_hash'],  # Mantener hash
                        'nombre': cliente['nombre'],
                        'fecha_registro': cliente['fecha_creacion'],
                        'ultimo_login': cliente['ultimo_login'] or ''
                    })
                    
        except Exception as e:
            print(f"Error al sincronizar con clientes.csv: {e}")

    def registrar_usuario(self, nombre, email, password, telefono="", rol="cliente"):
        """
        Registra un nuevo usuario en el sistema. El id_usuario se genera automáticamente.
        """
        if not nombre:
            return False, "El nombre es requerido"
        if not email or "@" not in email:
            return False, "Email inválido"
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        # Verificar que el email no esté en uso
        for usuario_data in self.usuarios_db.values():
            if usuario_data['email'] == email:
                return False, "Email ya registrado"
        # Generar id_usuario único basado en email
        id_usuario = email.split('@')[0]
        contador = 1
        id_original = id_usuario
        while id_usuario in self.usuarios_db:
            id_usuario = f"{id_original}{contador}"
            contador += 1
        # Crear nuevo usuario
        nuevo_usuario = {
            'id_usuario': id_usuario,
            'nombre': nombre,
            'email': email,
            'password_hash': self.hash_password(password),
            'rol': rol,
            'fecha_creacion': datetime.now().isoformat(),
            'activo': True,
            'telefono': telefono,
            'intentos_login': 0,
            'ultimo_login': None
        }
        self.usuarios_db[id_usuario] = nuevo_usuario
        self.guardar_usuarios()
        if rol == 'cliente':
            self.sincronizar_con_clientes_csv()
        return True, "Usuario registrado exitosamente"
    
    def autenticar(self, email, password):
        """
        Autentica un usuario con email y contraseña.
        """
        usuario_data = None
        for user in self.usuarios_db.values():
            if user['email'] == email:
                usuario_data = user
                break
        if not usuario_data:
            return False, "Usuario no encontrado", None
        if not usuario_data.get('activo', True):
            return False, "Cuenta desactivada", None
        if usuario_data.get('intentos_login', 0) >= 5:
            return False, "Cuenta bloqueada por múltiples intentos fallidos", None
        password_hash = self.hash_password(password)
        if usuario_data['password_hash'] != password_hash:
            usuario_data['intentos_login'] = usuario_data.get('intentos_login', 0) + 1
            self.guardar_usuarios()
            return False, "Contraseña incorrecta", None
        usuario_data['intentos_login'] = 0
        usuario_data['ultimo_login'] = datetime.now().isoformat()
        self.guardar_usuarios()
        return True, "Autenticación exitosa", usuario_data
    
    def iniciar_sesion(self, email, password):
        """
        Inicia sesión y crea una sesión activa usando el correo.
        """
        exito, mensaje, usuario_data = self.autenticar(email, password)
        if not exito:
            return False, mensaje, None
        carrito_usuario = Carrito(f"carrito_{usuario_data['id_usuario']}")
        cliente = Cliente(
            id_cliente=usuario_data['id_usuario'],
            nombre=usuario_data['nombre'],
            email=usuario_data['email'],
            carrito=carrito_usuario,
            tarjeta=usuario_data.get('tarjeta', None),
            telefono=usuario_data.get('telefono', '')
        )
        self.usuario_actual = cliente
        return True, f"Bienvenido, {cliente.nombre}!", cliente
    
    def cerrar_sesion(self):
        """Cierra la sesión actual."""
        self.usuario_actual = None
        return True, "Sesión cerrada exitosamente"
    
    def esta_autenticado(self):
        """Verifica si hay un usuario autenticado."""
        return self.usuario_actual is not None
    
    def obtener_usuario_actual(self):
        """Obtiene el cliente autenticado actualmente."""
        return self.usuario_actual
    
    def obtener_rol_usuario(self):
        """Obtiene el rol del usuario actual."""
        if not self.esta_autenticado():
            return None
        
        # Buscar el rol en la base de datos de usuarios
        for usuario_id, datos in self.usuarios_db.items():
            if self.usuario_actual and datos['id_usuario'] == self.usuario_actual.id_cliente:
                return datos['rol']
        return 'cliente'  # Rol por defecto
    
    def es_administrador(self):
        """Verifica si el usuario actual es administrador."""
        return self.obtener_rol_usuario() == 'administrador'
    
    def cambiar_password(self, id_usuario, password_actual, password_nueva):
        """
        Cambia la contraseña de un usuario.
        
        Args:
            id_usuario (str): ID del usuario
            password_actual (str): Contraseña actual
            password_nueva (str): Nueva contraseña
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        # Verificar usuario
        if id_usuario not in self.usuarios_db:
            return False, "Usuario no encontrado"
        
        usuario_data = self.usuarios_db[id_usuario]
        
        # Verificar contraseña actual
        if usuario_data['password_hash'] != self.hash_password(password_actual):
            return False, "Contraseña actual incorrecta"
        
        # Validar nueva contraseña
        if len(password_nueva) < 6:
            return False, "La nueva contraseña debe tener al menos 6 caracteres"
        
        # Actualizar contraseña
        usuario_data['password_hash'] = self.hash_password(password_nueva)
        self.guardar_usuarios()
        
        return True, "Contraseña actualizada exitosamente"
    
    def listar_usuarios(self):
        """Lista todos los usuarios (solo para administradores)."""
        if not self.es_administrador():
            return []
        
        usuarios = []
        for id_usuario, data in self.usuarios_db.items():
            usuarios.append({
                'id': id_usuario,
                'nombre': data['nombre'],
                'email': data['email'],
                'rol': data['rol'],
                'activo': data['activo'],
                'ultimo_login': data.get('ultimo_login'),
                'fecha_creacion': data['fecha_creacion']
            })
        
        return usuarios
    
    def activar_desactivar_usuario(self, id_usuario, activo):
        """Activa o desactiva un usuario (solo administradores)."""
        if not self.es_administrador():
            return False, "Permisos insuficientes"
        
        if id_usuario not in self.usuarios_db:
            return False, "Usuario no encontrado"
        
        self.usuarios_db[id_usuario]['activo'] = activo
        self.guardar_usuarios()
        
        estado = "activado" if activo else "desactivado"
        return True, f"Usuario {estado} exitosamente"
    
    def __str__(self):
        """Representación del sistema de login."""
        usuario_actual = self.usuario_actual.nombre if self.usuario_actual else "Ninguno"
        return f"SistemaLogin(usuario_actual='{usuario_actual}', usuarios_registrados={len(self.usuarios_db)})"
