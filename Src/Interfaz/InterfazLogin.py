from customtkinter import *
from PIL import Image
from tkinter import messagebox

import os
import sys
from datetime import datetime

# Agregar el directorio padre al path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Login import SistemaLogin
# Imports explícitos de las clases principales del flujo de checkout
from Src.Carrito import Carrito
from Src.Checkout import Checkout
from Src.Cliente import Cliente
from Src.Pago import Pago
from Src.Recibo import Recibo

class LoginApp(CTk):
    def __init__(self, callback_login_exitoso=None):
        super().__init__()
        
        # Configurar apariencia para consistencia entre sistemas
        set_appearance_mode("light")  # Forzar modo claro
        set_default_color_theme("blue")  # Tema consistente
        
        # Sistema de login
        self.sistema_login = SistemaLogin()
        self.callback_login_exitoso = callback_login_exitoso    
        self.cliente_autenticado = None
        self._callback_ejecutado = False  # Flag para evitar doble ejecución
        
        # Configuración de ventana más robusta (tamaño original que se veía bien)
        self.geometry("750x580")  # Mantener tamaño original
        self.resizable(False, False)  # No redimensionable
        self.title("Sistema Ecomerce - Login")
        
        # Configurar escalado DPI como originalmente (sin forzar límites)
        try:
            import ctypes
            # Usar configuración DPI original que funcionaba bien
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Volver a la configuración original
        except:
            pass  # En caso de que no esté en Windows
        
        # Configurar cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Cargar imágenes
        self.cargar_imagenes()
        
        # Mostrar interfaz de login inicial
        self.mostrar_login()
        
        # NO forzar tamaño - dejar que se muestre naturalmente
    
    def on_closing(self):
        """Manejar cierre de ventana de login"""
        try:
            print("🚪 Cerrando ventana de login...")
            self.cliente_autenticado = None
            # Cancelar todos los afters pendientes
            if hasattr(self, '_after_ids'):
                for after_id in self._after_ids:
                    try:
                        self.after_cancel(after_id)
                    except Exception as e:
                        print(f"Warning cancelando after: {e}")
                self._after_ids.clear()
            # Limpia widgets explícitamente antes de destruir
            self.limpiar_interfaz()
            # Elimina referencias a imágenes para evitar errores de pyimage
            self.side_img = None
            self.email_icon = None
            self.password_icon = None
            self.google_icon = None
            self.avatar_icon = None
            self.destroy()
        except Exception as e:
            print(f"Error cerrando login: {e}")
            self.quit()
    
    def after(self, ms, func=None, *args):
        """Sobrescribe after para registrar los afters y poder cancelarlos todos al cerrar."""
        if not hasattr(self, '_after_ids'):
            self._after_ids = set()
        after_id = super().after(ms, func, *args)
        self._after_ids.add(after_id)
        return after_id

    def after_cancel(self, after_id):
        """Sobrescribe after_cancel para mantener la lista limpia."""
        if hasattr(self, '_after_ids') and after_id in self._after_ids:
            self._after_ids.remove(after_id)
        return super().after_cancel(after_id)

    def centrar_ventana(self):
        """Centra la ventana en la pantalla con mejor compatibilidad."""
        self.update_idletasks()
        
        # Obtener dimensiones reales de la ventana
        ancho = 750  # Usar valor fijo actualizado
        alto = 580   # Usar valor fijo en lugar de winfo_height()
        
        # Obtener dimensiones de la pantalla
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        
        # Calcular posición centrada
        x = max(0, (pantalla_ancho - ancho) // 2)
        y = max(0, (pantalla_alto - alto) // 2)
        
        # Aplicar geometría con validación
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        # Forzar actualización
        self.update()
    
    def cargar_imagenes(self):
        """Carga las imágenes necesarias con mejor manejo de errores."""
        try:
            # Obtener directorio actual del script (Src/Interfaz/)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Subir un nivel para llegar a Src/ y luego entrar a Images/
            src_dir = os.path.dirname(current_dir)
            images_dir = os.path.join(src_dir, "Images")
            
            # Verificar que existe la carpeta
            if not os.path.exists(images_dir):
                print(f"Advertencia: No se encontró la carpeta Images en {images_dir}")
                self.crear_imagenes_fallback()
                return

            # Cargar imágenes desde la carpeta Images con tamaños fijos
            self.side_img_data = Image.open(os.path.join(images_dir, "side-img.png"))
            self.email_icon_data = Image.open(os.path.join(images_dir, "email-icon.png"))
            self.password_icon_data = Image.open(os.path.join(images_dir, "password-icon.png"))
            self.google_icon_data = Image.open(os.path.join(images_dir, "google-icon.png"))
            self.avatar_icon_data = Image.open(os.path.join(images_dir, "avatar (1).png"))
            
            # Crear CTkImages con tamaños consistentes y escalado DPI
            scale_factor = self.tk.call('tk', 'scaling')  # Detectar escalado del sistema
            
            self.side_img = CTkImage(
                dark_image=self.side_img_data, 
                light_image=self.side_img_data, 
                size=(int(300 * scale_factor), int(580 * scale_factor))
            )
            self.email_icon = CTkImage(
                dark_image=self.email_icon_data, 
                light_image=self.email_icon_data, 
                size=(20, 20)
            )
            self.password_icon = CTkImage(
                dark_image=self.password_icon_data, 
                light_image=self.password_icon_data, 
                size=(17, 17)
            )
            self.google_icon = CTkImage(
                dark_image=self.google_icon_data, 
                light_image=self.google_icon_data, 
                size=(17, 17)
            )
            self.avatar_icon = CTkImage(
                dark_image=self.avatar_icon_data, 
                light_image=self.avatar_icon_data, 
                size=(20, 20)
            )

        except Exception as e:
            print(f"Error cargando imágenes: {e}")
            self.crear_imagenes_fallback()
    
    def crear_imagenes_fallback(self):
        """Crear imágenes de respaldo cuando fallan las originales."""
        # Crear imágenes de respaldo
        fallback_img = Image.new('RGB', (300, 580), (96, 30, 136))
        fallback_icon = Image.new('RGBA', (20, 20), (96, 30, 136, 255))

        self.side_img = CTkImage(dark_image=fallback_img, light_image=fallback_img, size=(300, 580))
        self.email_icon = CTkImage(dark_image=fallback_icon, light_image=fallback_icon, size=(20,20))
        self.password_icon = CTkImage(dark_image=fallback_icon, light_image=fallback_icon, size=(17,17))
        self.google_icon = CTkImage(dark_image=fallback_icon, light_image=fallback_icon, size=(17,17))
        self.avatar_icon = CTkImage(dark_image=fallback_icon, light_image=fallback_icon, size=(20,20))

    def limpiar_interfaz(self):
        """Limpia la interfaz actual."""
        for widget in self.winfo_children():
            widget.destroy()
    
    def mostrar_login(self):
        """Muestra la interfaz de login."""
        self.limpiar_interfaz()
        
        # Crear frame principal para mejor distribución
        main_frame = CTkFrame(master=self, fg_color="#ffffff")  # Fondo blanco explícito
        main_frame.pack(fill="both", expand=True)
        
        # Lado izquierdo - Imagen
        left_frame = CTkFrame(master=main_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        CTkLabel(master=left_frame, text="", image=self.side_img).pack(expand=True)
        
        # Lado derecho - Formulario de login
        self.frame = CTkFrame(master=main_frame, width=450, height=580, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(side="right", padx=(0, 30), pady=0)  # Margen solo del lado derecho
        
        # Título
        CTkLabel(master=self.frame, text="¡Bienvenido!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(40, 0))
        CTkLabel(master=self.frame, text="Inicia sesión en tu cuenta", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(40, 0))
        
        # Email
        CTkLabel(master=self.frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(40, 0))
        self.email_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", placeholder_text="usuario@universidad.edu")
        self.email_entry.pack(anchor="w", padx=(40, 0))

        # Contraseña
        CTkLabel(master=self.frame, text="  Contraseña:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(40, 0))
        self.password_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*", placeholder_text="Contraseña")
        self.password_entry.pack(anchor="w", padx=(40, 0))
        
        # Botón Iniciar Sesión
        self.login_btn = CTkButton(master=self.frame, text="Iniciar Sesión", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=350, command=self.procesar_login)
        self.login_btn.pack(anchor="w", pady=(40, 0), padx=(40, 0))

        # Botón Cambiar Contraseña
        CTkButton(master=self.frame, text="Cambiar Contraseña", fg_color="transparent", hover_color="#F0F0F0", font=("Arial Bold", 10), text_color="#E44982", width=350, command=self.mostrar_cambio_contrasena).pack(anchor="w", pady=(8, 0), padx=(40, 0))

        # Botón Registro
        CTkButton(master=self.frame, text="Crear Nueva Cuenta", fg_color="transparent", hover_color="#F0F0F0", font=("Arial Bold", 11), text_color="#601E88", width=350, command=self.mostrar_registro).pack(anchor="w", pady=(10, 0), padx=(40, 0))

        # Información del admin
        CTkLabel(master=self.frame, text="Admin: admin@universidad.edu / admin123", text_color="#999999", font=("Arial", 8)).pack(pady=(15, 0), padx=(40, 0))

        # Eventos de teclado
        self.email_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.procesar_login())

        # Focus inicial
        self.email_entry.focus()

    def mostrar_cambio_contrasena(self):
        """Muestra la interfaz para cambiar la contraseña."""
        self.limpiar_interfaz()

        main_frame = CTkFrame(master=self, fg_color="#ffffff")
        main_frame.pack(fill="both", expand=True)

        left_frame = CTkFrame(master=main_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        CTkLabel(master=left_frame, text="", image=self.side_img).pack(expand=True)

        self.frame = CTkFrame(master=main_frame, width=450, height=580, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(side="right", padx=(0, 30), pady=0)

        CTkLabel(master=self.frame, text="Restablecer Contraseña", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 22)).pack(anchor="w", pady=(25, 5), padx=(40, 0))
        CTkLabel(master=self.frame, text="Ingrese los datos para cambiar su contraseña", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(40, 0))

        # Email
        CTkLabel(master=self.frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12), image=self.email_icon, compound="left").pack(anchor="w", pady=(20, 5), padx=(40, 0))
        self.cambio_email_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", placeholder_text="usuario@universidad.edu")
        self.cambio_email_entry.pack(anchor="w", padx=(40, 0))

        # Contraseña actual
        CTkLabel(master=self.frame, text="  Contraseña actual:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12), image=self.password_icon, compound="left").pack(anchor="w", pady=(12, 5), padx=(40, 0))
        self.cambio_actual_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*", placeholder_text="Contraseña actual")
        self.cambio_actual_entry.pack(anchor="w", padx=(40, 0))

        # Nueva contraseña
        CTkLabel(master=self.frame, text="  Nueva contraseña:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12), image=self.password_icon, compound="left").pack(anchor="w", pady=(12, 5), padx=(40, 0))
        self.cambio_nueva_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*", placeholder_text="Nueva contraseña")
        self.cambio_nueva_entry.pack(anchor="w", padx=(40, 0))

        # Confirmar nueva contraseña
        CTkLabel(master=self.frame, text="  Confirmar nueva contraseña:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12), image=self.password_icon, compound="left").pack(anchor="w", pady=(12, 5), padx=(40, 0))
        self.cambio_confirmar_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*", placeholder_text="Confirmar nueva contraseña")
        self.cambio_confirmar_entry.pack(anchor="w", padx=(40, 0))

        # Botón Cambiar
        CTkButton(master=self.frame, text="Cambiar Contraseña", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=350, command=self.procesar_cambio_contrasena).pack(anchor="w", pady=(20, 0), padx=(40, 0))

        # Botón Volver
        CTkButton(master=self.frame, text="← Volver al Login", fg_color="transparent", hover_color="#F0F0F0", font=("Arial Bold", 10), text_color="#601E88", width=350, command=self.mostrar_login).pack(anchor="w", pady=(8, 0), padx=(40, 0))

        self.cambio_email_entry.focus()

    def procesar_cambio_contrasena(self):
        """Procesa el cambio de contraseña desde la interfaz."""
        email = self.cambio_email_entry.get().strip()
        actual = self.cambio_actual_entry.get()
        nueva = self.cambio_nueva_entry.get()
        confirmar = self.cambio_confirmar_entry.get()

        if not all([email, actual, nueva, confirmar]):
            messagebox.showerror("❌ Error", "Por favor complete todos los campos")
            return
        if nueva != confirmar:
            messagebox.showerror("❌ Error", "Las nuevas contraseñas no coinciden")
            return
        if len(nueva) < 6:
            messagebox.showerror("❌ Error", "La nueva contraseña debe tener al menos 6 caracteres")
            return

        # Buscar id_usuario por email
        id_usuario = None
        for user in self.sistema_login.usuarios_db.values():
            if user['email'] == email:
                id_usuario = user['id_usuario']
                break
        if not id_usuario:
            messagebox.showerror("❌ Error", "Usuario no encontrado")
            return

        exito, mensaje = self.sistema_login.cambiar_password(id_usuario, actual, nueva)
        if exito:
            messagebox.showinfo("✅ Contraseña cambiada", "¡Contraseña actualizada exitosamente!")
            self.mostrar_login()
        else:
            messagebox.showerror("❌ Error", mensaje)
    
    def mostrar_registro(self):
        """Muestra la interfaz de registro."""
        self.limpiar_interfaz()
        
        # Crear frame principal para mejor distribución
        main_frame = CTkFrame(master=self, fg_color="#ffffff")  # Fondo blanco explícito
        main_frame.pack(fill="both", expand=True)
        
        # Lado izquierdo - Imagen
        left_frame = CTkFrame(master=main_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        CTkLabel(master=left_frame, text="", image=self.side_img).pack(expand=True)
        
        # Lado derecho - Formulario de registro
        self.frame = CTkFrame(master=main_frame, width=450, height=580, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(side="right", padx=(0, 30), pady=0)  # Margen solo del lado derecho
        
        # Título
        CTkLabel(master=self.frame, text="¡Regístrate!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 22)).pack(anchor="w", pady=(25, 5), padx=(40, 0))
        CTkLabel(master=self.frame, text="Crea tu nueva cuenta", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(40, 0))
        
        # Nombre Completo
        CTkLabel(master=self.frame, text="  Nombre:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12), image=self.avatar_icon, compound="left").pack(anchor="w", pady=(20, 5), padx=(40, 0))
        self.nombre_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", placeholder_text="Nombre completo")
        self.nombre_entry.pack(anchor="w", padx=(40, 0))
        
        # Email
        CTkLabel(master=self.frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12), image=self.email_icon, compound="left").pack(anchor="w", pady=(12, 5), padx=(40, 0))
        self.reg_email_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", placeholder_text="usuario@universidad.edu")
        self.reg_email_entry.pack(anchor="w", padx=(40, 0))
        
        # Teléfono
        CTkLabel(master=self.frame, text="📱  Teléfono:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", pady=(12, 5), padx=(40, 0))
        self.telefono_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", placeholder_text="Opcional")
        self.telefono_entry.pack(anchor="w", padx=(40, 0))
        
        # Password
        CTkLabel(master=self.frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12), image=self.password_icon, compound="left").pack(anchor="w", pady=(12, 5), padx=(40, 0))
        self.reg_password_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*", placeholder_text="Mínimo 6 caracteres")
        self.reg_password_entry.pack(anchor="w", padx=(40, 0))
        
        # Confirmar Password
        CTkLabel(master=self.frame, text="🔒  Confirmar:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", pady=(12, 5), padx=(40, 0))
        self.confirm_password_entry = CTkEntry(master=self.frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*", placeholder_text="Confirma contraseña")
        self.confirm_password_entry.pack(anchor="w", padx=(40, 0))
        
        # Botón Crear Cuenta
        self.register_btn = CTkButton(master=self.frame, text="Crear Cuenta", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=350, command=self.procesar_registro)
        self.register_btn.pack(anchor="w", pady=(20, 0), padx=(40, 0))
        
        # Botón Volver
        CTkButton(master=self.frame, text="← Volver al Login", fg_color="transparent", hover_color="#F0F0F0", font=("Arial Bold", 10), text_color="#601E88", width=350, command=self.mostrar_login).pack(anchor="w", pady=(8, 0), padx=(40, 0))
        
        # Focus inicial
        self.nombre_entry.focus()
    
    def procesar_login(self):
        """Procesa el intento de login."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("❌ Error", "Por favor complete todos los campos")
            return
        
        # Cambiar estado del botón
        self.login_btn.configure(state="disabled", text="Verificando...")
        self.update()
        
        try:
            # Intentar autenticación
            exito, mensaje, cliente_base = self.sistema_login.iniciar_sesion(email, password)
            if exito:
                # Crear solo el carrito para el cliente, sin tarjeta
                carrito = Carrito(cliente_id=cliente_base.id_cliente if hasattr(cliente_base, 'id_cliente') else cliente_base.nombre)
                cliente = Cliente(
                    id_cliente=cliente_base.id_cliente if hasattr(cliente_base, 'id_cliente') else cliente_base.nombre,
                    nombre=cliente_base.nombre,
                    email=cliente_base.email,
                    carrito=carrito,
                    telefono=getattr(cliente_base, 'telefono', "")
                )
                self.cliente_autenticado = cliente
                messagebox.showinfo("✅ Login Exitoso", f"¡Bienvenido, {cliente.nombre}!")
                # Ejecutar callback si existe
                if self.callback_login_exitoso:
                    self.withdraw()
                    self.after(100, lambda: self._ejecutar_callback_y_cerrar(cliente))
                else:
                    self.destroy()
            else:
                messagebox.showerror("❌ Error de Login", mensaje)
                self.password_entry.delete(0, "end")
                self.password_entry.focus()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error inesperado: {str(e)}")
            print(f"Error en login: {e}")
        
        finally:
            # Restaurar botón si la ventana aún existe
            try:
                self.login_btn.configure(state="normal", text="Iniciar Sesión")
            except:
                pass
    
    def _ejecutar_callback_y_cerrar(self, cliente):
        """Ejecutar callback y cerrar login de forma segura"""
        try:
            if self.callback_login_exitoso and not self._callback_ejecutado:
                self._callback_ejecutado = True
                print(f"Ejecutando callback para {cliente.nombre}")
                self.callback_login_exitoso(cliente, self.sistema_login)
            
            # Cerrar ventana de login
            self.destroy()
            
        except Exception as e:
            print(f"Error ejecutando callback: {e}")
            try:
                self.destroy()
            except:
                self.quit()
    
    def procesar_registro(self):
        """Procesa el registro de un nuevo usuario."""
        nombre = self.nombre_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validaciones
        if not all([nombre, email, password, confirm_password]):
            messagebox.showerror("❌ Error", "Por favor complete todos los campos obligatorios")
            return
        
        if password != confirm_password:
            messagebox.showerror("❌ Error", "Las contraseñas no coinciden")
            return
        
        if len(password) < 6:
            messagebox.showerror("❌ Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        if "@" not in email:
            messagebox.showerror("❌ Error", "Email inválido")
            return
        
        # Cambiar estado del botón
        self.register_btn.configure(state="disabled", text="Creando cuenta...")
        self.update()
        
        try:
            # Intentar registro
            exito, mensaje = self.sistema_login.registrar_usuario(nombre, email, password, telefono)
            
            if exito:
                messagebox.showinfo("✅ Registro Exitoso", "¡Cuenta creada exitosamente!\nAhora puedes iniciar sesión.")
                # Volver al login y pre-llenar email
                self.mostrar_login()
                self.email_entry.insert(0, email)
                self.password_entry.focus()
            else:
                messagebox.showerror("❌ Error de Registro", mensaje)
        
        finally:
            # Restaurar botón
            self.register_btn.configure(state="normal", text="Crear Cuenta")
    
    def obtener_cliente(self):
        """Retorna el cliente autenticado."""
        return self.cliente_autenticado

def mostrar_login(callback_login_exitoso=None):
    """Función principal para mostrar el login."""
    try:
        # Configurar CustomTkinter para login (configuración ligera)
        set_appearance_mode("light")
        set_default_color_theme("blue")
        print("Iniciando ventana de login...")
        # Siempre crear una nueva instancia de LoginApp y sus imágenes
        app = LoginApp(callback_login_exitoso)
        # Forzar garbage collection para limpiar imágenes viejas
        import gc
        gc.collect()
        # Si hay callback, no necesitamos el retorno del mainloop
        if callback_login_exitoso:
            app.mainloop()
            return None
        else:
            # Solo para uso directo sin callback
            app.mainloop()
            return app.obtener_cliente()
    except Exception as e:
        print(f"Error en mostrar_login: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Prueba independiente
    def callback_prueba(cliente, sistema_login):
        print(f"Login exitoso: {cliente.nombre}")
        print(f"Email: {cliente.email}")
        print(f"Rol: {sistema_login.obtener_rol_usuario()}")
    
    cliente = mostrar_login(callback_prueba)
    if cliente:
        print(f"\n Usuario autenticado: {cliente.nombre}")
    else:
        print("\nLogin cancelado")