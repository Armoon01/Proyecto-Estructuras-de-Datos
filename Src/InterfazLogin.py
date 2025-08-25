"""
Interfaz gráfica para el sistema de login con diseño moderno.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Login import SistemaLogin

class InterfazLogin:
    """Interfaz gráfica para login y registro de usuarios."""
    
    def __init__(self, callback_login_exitoso=None):
        self.sistema_login = SistemaLogin()
        self.callback_login_exitoso = callback_login_exitoso
        self.ventana = None
        self.cliente_autenticado = None
        
    def mostrar_ventana_login(self):
        """Muestra la ventana principal de login."""
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Login - Universidad")
        self.ventana.geometry("450x650")  # Aumentado la altura
        self.ventana.resizable(False, False)
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear interfaz
        self.crear_interfaz_login()
        
        # Ejecutar loop
        self.ventana.mainloop()
        
        return self.cliente_autenticado
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def crear_interfaz_login(self):
        """Crea la interfaz de login."""
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema de Compras", 
                          font=('Arial', 18, 'bold'), foreground='navy')
        titulo.pack(pady=(0, 10))
        
        subtitulo = ttk.Label(main_frame, text="Universidad - Iniciar Sesión", 
                            font=('Arial', 12), foreground='gray')
        subtitulo.pack(pady=(0, 30))
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Pestaña de Login
        self.crear_pestaña_login()
        
        # Pestaña de Registro
        self.crear_pestaña_registro()
        
        # Información del sistema
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X)
        
        ttk.Label(info_frame, text="Usuario por defecto: admin@universidad.edu / Contraseña: admin123", 
                 font=('Arial', 9), foreground='gray').pack()
        
        # Botón de salir
        ttk.Button(main_frame, text="Salir", command=self.salir).pack(pady=(10, 0))
    
    def crear_pestaña_login(self):
        """Crea la pestaña de inicio de sesión."""
        login_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(login_frame, text="Iniciar Sesión")
        
        # Campos de login
        ttk.Label(login_frame, text="Email:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.entry_usuario = ttk.Entry(login_frame, width=30, font=('Arial', 11))
        self.entry_usuario.pack(pady=(0, 15))
        self.entry_usuario.focus()
        
        ttk.Label(login_frame, text="Contraseña:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.entry_password = ttk.Entry(login_frame, width=30, show="*", font=('Arial', 11))
        self.entry_password.pack(pady=(0, 20))
        
        # Botón de login
        btn_login = ttk.Button(login_frame, text="Iniciar Sesión", command=self.procesar_login)
        btn_login.pack(pady=(0, 15))
        
        # Información adicional
        info_login = ttk.LabelFrame(login_frame, text="Información", padding="10")
        info_login.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(info_login, text="• Use su email universitario").pack(anchor=tk.W)
        ttk.Label(info_login, text="• Si no tiene cuenta, regístrese en la pestaña siguiente").pack(anchor=tk.W)
        ttk.Label(info_login, text="• Para pruebas use: admin@universidad.edu / admin123").pack(anchor=tk.W)
        
        # Eventos de teclado
        self.entry_usuario.bind('<Return>', lambda e: self.entry_password.focus())
        self.entry_password.bind('<Return>', lambda e: self.procesar_login())
    
    def crear_pestaña_registro(self):
        """Crea la pestaña de registro de nuevos usuarios."""
        registro_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(registro_frame, text="Registrarse")
        
        # Crear un frame interno para centrar mejor el contenido
        contenido_frame = ttk.Frame(registro_frame)
        contenido_frame.pack(expand=True, fill='both')
        
        # Campos de registro con espaciado reducido
        ttk.Label(contenido_frame, text="Nombre Completo:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 3))
        self.entry_reg_nombre = ttk.Entry(contenido_frame, width=30)
        self.entry_reg_nombre.pack(pady=(0, 6))
        
        ttk.Label(contenido_frame, text="Email:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 3))
        self.entry_reg_email = ttk.Entry(contenido_frame, width=30)
        self.entry_reg_email.pack(pady=(0, 6))
        
        ttk.Label(contenido_frame, text="Teléfono (opcional):", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 3))
        self.entry_reg_telefono = ttk.Entry(contenido_frame, width=30)
        self.entry_reg_telefono.pack(pady=(0, 6))
        
        ttk.Label(contenido_frame, text="Contraseña:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 3))
        self.entry_reg_password = ttk.Entry(contenido_frame, width=30, show="*")
        self.entry_reg_password.pack(pady=(0, 6))
        
        ttk.Label(contenido_frame, text="Confirmar Contraseña:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 3))
        self.entry_reg_confirm = ttk.Entry(contenido_frame, width=30, show="*")
        self.entry_reg_confirm.pack(pady=(0, 10))
        
        # Botón de registro - más prominente
        btn_registro = ttk.Button(contenido_frame, text="📝 Registrarse", 
                                command=self.procesar_registro, 
                                style='Accent.TButton' if hasattr(ttk, 'Style') else None)
        btn_registro.pack(pady=(5, 10))
        
        # Información compacta
        info_text = "• Mínimo 6 caracteres en la contraseña • Email válido requerido • ID se asigna automáticamente"
        ttk.Label(contenido_frame, text=info_text, font=('Arial', 8), foreground='gray').pack(pady=(0, 5))
        
        # Eventos de teclado para navegación fluida
        self.entry_reg_nombre.bind('<Return>', lambda e: self.entry_reg_email.focus())
        self.entry_reg_email.bind('<Return>', lambda e: self.entry_reg_telefono.focus())
        self.entry_reg_telefono.bind('<Return>', lambda e: self.entry_reg_password.focus())
        self.entry_reg_password.bind('<Return>', lambda e: self.entry_reg_confirm.focus())
        self.entry_reg_confirm.bind('<Return>', lambda e: self.procesar_registro())
    
    def procesar_login(self):
        """Procesa el intento de login."""
        email = self.entry_usuario.get().strip()
        password = self.entry_password.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        # Intentar autenticación
        exito, mensaje, cliente = self.sistema_login.iniciar_sesion(email, password)
        
        if exito:
            self.cliente_autenticado = cliente
            messagebox.showinfo("Éxito", mensaje)
            
            # Llamar callback si existe
            if self.callback_login_exitoso:
                self.callback_login_exitoso(cliente, self.sistema_login)
            
            self.ventana.destroy()
        else:
            messagebox.showerror("Error de Login", mensaje)
            self.entry_password.delete(0, tk.END)
            self.entry_password.focus()
    
    def procesar_registro(self):
        """Procesa el registro de un nuevo usuario."""
        nombre = self.entry_reg_nombre.get().strip()
        email = self.entry_reg_email.get().strip()
        telefono = self.entry_reg_telefono.get().strip()
        password = self.entry_reg_password.get()
        confirm = self.entry_reg_confirm.get()
        
        # Validaciones
        if not all([nombre, email, password, confirm]):
            messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        # Intentar registro
        exito, mensaje = self.sistema_login.registrar_usuario(
            nombre, email, password, telefono
        )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            # Limpiar campos
            self.limpiar_campos_registro()
            # Cambiar a pestaña de login
            self.notebook.select(0)
            self.entry_usuario.delete(0, tk.END)
            self.entry_usuario.insert(0, email)
            self.entry_password.focus()
        else:
            messagebox.showerror("Error de Registro", mensaje)
    
    def limpiar_campos_registro(self):
        """Limpia todos los campos de registro."""
        self.entry_reg_nombre.delete(0, tk.END)
        self.entry_reg_email.delete(0, tk.END)
        self.entry_reg_telefono.delete(0, tk.END)
        self.entry_reg_password.delete(0, tk.END)
        self.entry_reg_confirm.delete(0, tk.END)
    
    def salir(self):
        """Cierra la aplicación."""
        self.ventana.destroy()

def mostrar_login(callback_login_exitoso=None):
    """Función helper para mostrar el login."""
    interfaz = InterfazLogin(callback_login_exitoso)
    return interfaz.mostrar_ventana_login()

if __name__ == "__main__":
    # Test independiente
    def callback_test(cliente, sistema_login):
        print(f"Login exitoso: {cliente.nombre}")
        print(f"Rol: {sistema_login.obtener_rol_usuario()}")
    
    cliente = mostrar_login(callback_test)
    if cliente:
        print(f"Usuario autenticado: {cliente.nombre}")
    else:
        print("Login cancelado")
