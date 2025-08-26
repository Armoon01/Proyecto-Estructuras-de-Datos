import customtkinter as ctk
import platform
import sys
import traceback
import os

# Configurar tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def configurar_dpi_awareness():
    """Configurar DPI awareness para Windows"""
    if platform.system() == "Windows":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            print(f"⚠️ Error configurando DPI awareness: {e}")

def configurar_rutas():
    """Configurar rutas del proyecto"""
    try:
        # Obtener directorio del proyecto (3 niveles arriba desde Src/main.py)
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Agregar rutas al sys.path
        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)
        
        src_dir = os.path.join(project_dir, 'Src')
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
            
        return project_dir
    except Exception as e:
        print(f"⚠️ Error configurando rutas: {e}")
        return None

# Configurar rutas antes de importar
PROJECT_DIR = configurar_rutas()

try:
    # Importaciones base del sistema
    from Interfaz.InterfazCarrito import InterfazCarrito
    from Interfaz.InterfazCheckout import InterfazCheckout
    from Interfaz.InterfazLogin import mostrar_login
    from Interfaz.InterfazEstructuras import mostrar_visualizador_estructuras  # ✅ LÍNEA CORREGIDA
    from Inventario import Inventario
    from Carrito import Carrito
    from Login import SistemaLogin
    from estructuras.Pila import Pila
    from estructuras.Cola import Cola
    from Pago import Pago
    from Orden import Orden
    from Interfaz.InterfazCompras import InterfazCompras
    print("✅ Todas las importaciones exitosas")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    traceback.print_exc()
    sys.exit(1)

class SistemaEcommerce:
    """Sistema principal de e-commerce"""
    def __init__(self, cliente_autenticado=None):
        self.cliente_autenticado = cliente_autenticado
        
        try:
            # Inicializar componentes del sistema
            self.inventario = Inventario()
            self.pila_ordenes = Pila()
            self.cola_pagos = Cola()
            
            # ✅ ARREGLO: Configurar carrito con el sistema mejorado
            if cliente_autenticado and hasattr(cliente_autenticado, 'carrito'):
                self.carrito = cliente_autenticado.carrito
                print(f"🛒 Carrito del cliente cargado: {self.carrito}")
            else:
                cliente_id = cliente_autenticado.id if cliente_autenticado else "invitado"
                self.carrito = Carrito(cliente_id)
                print(f"🛒 Nuevo carrito creado para: {cliente_id}")
                
            # ✅ DEBUG: Verificar estado inicial del carrito
            print(f"🔍 DEBUG: Carrito inicial - Items: {self.carrito.obtener_cantidad_items()}")
            print(f"🔍 DEBUG: Carrito inicial - Total: ${self.carrito.calcular_total():.2f}")
                
            print(f"🔧 Sistema inicializado correctamente")
            
        except Exception as e:
            print(f"❌ Error inicializando sistema: {e}")
            traceback.print_exc()
            raise

    def obtener_productos(self):
        """Obtener lista de productos del inventario"""
        try:
            return self.inventario.obtener_productos()
        except Exception as e:
            print(f"❌ Error obteniendo productos: {e}")
            return []

class AplicacionPrincipal(ctk.CTk):
    """Aplicación principal con interfaz mejorada"""
    def __init__(self, cliente_autenticado=None):
        super().__init__()
        
        # Configuración de ventana
        self.title("🛒 Sistema de E-commerce - Tienda Universitaria")
        self.geometry("1400x850")
        self.minsize(1200, 700)
        self.resizable(True, True)
        
        # Variables de estado
        self.cliente_autenticado = cliente_autenticado
        self.vista_actual = "compras"
        
        # ✅ VARIABLES PARA GESTIÓN DE INTERFACES
        self.interfaz_compras = None
        self.interfaz_carrito = None
        self.interfaz_checkout = None
        self.interfaz_historial = None
        
        try:
            # Inicializar sistema
            self.sistema = SistemaEcommerce(cliente_autenticado)
            
            # ✅ DEBUG: Verificar sistema después de inicialización
            print(f"🔍 DEBUG: Sistema creado - Carrito: {self.sistema.carrito}")
            print(f"🔍 DEBUG: Productos disponibles: {len(self.sistema.obtener_productos())}")
            
            # Crear interfaz
            self.crear_interfaz()
            
            # Configurar cierre de ventana
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            print("🎉 Aplicación principal iniciada correctamente")
            
        except Exception as e:
            print(f"❌ Error inicializando aplicación: {e}")
            traceback.print_exc()
            self.mostrar_error_critico(str(e))
    
    def crear_interfaz(self):
        """Crear la interfaz principal"""
        try:
            # Header principal
            self.crear_header()
            
            # Contenedor principal con scroll
            self.contenedor_principal = ctk.CTkFrame(self, fg_color="#ffffff")
            self.contenedor_principal.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            # Mostrar vista inicial
            self.mostrar_compras()
            
        except Exception as e:
            print(f"❌ Error creando interfaz: {e}")
            self.mostrar_error_critico(str(e))
    
    def crear_header(self):
        """✅ CORREGIDO: Crear header completo con grid layout"""
        try:
            # Frame principal del header
            self.header_frame = ctk.CTkFrame(self, height=85, fg_color="#1e40af")
            self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
            self.header_frame.pack_propagate(False)
            
            # ✅ CONFIGURAR GRID PARA DISTRIBUCIÓN CORRECTA
            self.header_frame.grid_columnconfigure(1, weight=1)  # Columna central expandible
            
            # ✅ LOGO Y TÍTULO (COLUMNA 0)
            logo_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
            logo_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)
            
            titulo = ctk.CTkLabel(
                logo_frame, 
                text="🛒 Tienda Universitaria", 
                font=("Arial", 26, "bold"),
                text_color="white"
            )
            titulo.pack()
            
            # ✅ NAVEGACIÓN CENTRAL (COLUMNA 1)
            nav_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
            nav_frame.grid(row=0, column=1, pady=20)
            
            # Botones de navegación
            self.crear_botones_navegacion(nav_frame)
            
            # ✅ PANEL DE USUARIO (COLUMNA 2)
            self.crear_panel_usuario()
            
        except Exception as e:
            print(f"❌ Error creando header: {e}")
            traceback.print_exc()
    
    def crear_botones_navegacion(self, parent):
        """✅ MEJORADO: Crear botones de navegación con historial"""
        try:
            # Botón Productos
            self.btn_compras = ctk.CTkButton(
                parent,
                text="🛍️ Productos",
                command=self.mostrar_compras,
                width=130,
                height=40,
                font=("Arial", 14, "bold"),
                fg_color="#3b82f6",
                hover_color="#2563eb",
                corner_radius=20
            )
            self.btn_compras.pack(side="left", padx=8)
            
            # Botón Carrito con contador
            self.btn_carrito = ctk.CTkButton(
                parent,
                text="🛒 Mi Carrito",
                command=self.mostrar_carrito,
                width=130,
                height=40,
                font=("Arial", 14, "bold"),
                fg_color="#059669",
                hover_color="#047857",
                corner_radius=20
            )
            self.btn_carrito.pack(side="left", padx=8)
            
            # ✅ NUEVO: Botón Historial
            self.btn_historial = ctk.CTkButton(
                parent,
                text="📋 Historial",
                command=self.mostrar_historial,
                width=130,
                height=40,
                font=("Arial", 14, "bold"),
                fg_color="#f59e0b",
                hover_color="#d97706",
                corner_radius=20
            )
            self.btn_historial.pack(side="left", padx=8)
            
            # Botón Checkout
            self.btn_checkout = ctk.CTkButton(
                parent,
                text="💳 Checkout",
                command=self.mostrar_checkout,
                width=130,
                height=40,
                font=("Arial", 14, "bold"),
                fg_color="#7c3aed",
                hover_color="#6d28d9",
                corner_radius=20
            )
            self.btn_checkout.pack(side="left", padx=8)
            
        except Exception as e:
            print(f"❌ Error creando botones: {e}")
    
    def crear_panel_usuario(self):
        """✅ CORREGIDO: Crear panel de usuario completo con estructuras y logout"""
        try:
            # Frame para el panel de usuario (columna 2 del grid)
            user_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
            user_frame.grid(row=0, column=2, sticky="e", padx=20, pady=15)
            
            # ✅ INFORMACIÓN DEL USUARIO
            if self.cliente_autenticado:
                usuario_text = f"👤 {self.cliente_autenticado.nombre}"
            else:
                usuario_text = "👤 Usuario Invitado"
            
            usuario_label = ctk.CTkLabel(
                user_frame,
                text=usuario_text,
                font=("Arial", 14, "bold"),
                text_color="white"
            )
            usuario_label.pack(side="left", padx=(0, 15))
            
            # ✅ BOTÓN VER ESTRUCTURAS
            self.btn_estructuras = ctk.CTkButton(
                user_frame,
                text="📊 Estructuras",
                command=self.mostrar_estructuras,
                width=110,
                height=35,
                font=("Arial", 12, "bold"),
                fg_color="#8b5cf6",
                hover_color="#7c3aed",
                corner_radius=15
            )
            self.btn_estructuras.pack(side="left", padx=5)
            
            # ✅ BOTÓN LOGOUT
            self.btn_logout = ctk.CTkButton(
                user_frame,
                text="🚪 Cerrar Sesión",
                command=self.logout,
                width=120,
                height=35,
                font=("Arial", 12, "bold"),
                fg_color="#dc2626",
                hover_color="#b91c1c",
                corner_radius=15
            )
            self.btn_logout.pack(side="left", padx=(10, 0))
            
            print("✅ Panel de usuario creado con botones de Estructuras y Logout")
            
        except Exception as e:
            print(f"❌ Error creando panel usuario: {e}")
            traceback.print_exc()
    
    def limpiar_contenedor(self):
        """Limpiar contenedor principal"""
        try:
            print("🧹 Contenedor principal limpiado")
            
            if hasattr(self, 'contenedor_principal') and self.contenedor_principal.winfo_exists():
                for widget in self.contenedor_principal.winfo_children():
                    try:
                        widget.destroy()
                    except Exception as e:
                        print(f"⚠️ Warning destruyendo widget: {e}")
                        
            # ✅ LIMPIAR REFERENCIAS DE INTERFACES
            self.interfaz_compras = None
            self.interfaz_carrito = None
            self.interfaz_checkout = None
            self.interfaz_historial = None
                        
        except Exception as e:
            print(f"❌ Error limpiando contenedor: {e}")
    
    def limpiar_recursos(self):
        """Limpiar todos los recursos antes de cerrar"""
        try:
            print("🧹 Limpiando recursos...")
            
            # ✅ LIMPIAR INTERFACES ESPECÍFICAS DE MANERA SEGURA
            interfaces_a_limpiar = [
                ('interfaz_compras', 'InterfazCompras'),
                ('interfaz_carrito', 'InterfazCarrito'), 
                ('interfaz_checkout', 'InterfazCheckout'),
                ('interfaz_historial', 'InterfazHistorial')
            ]
            
            for attr_name, interface_name in interfaces_a_limpiar:
                if hasattr(self, attr_name):
                    try:
                        interfaz = getattr(self, attr_name)
                        if interfaz and hasattr(interfaz, 'winfo_exists') and interfaz.winfo_exists():
                            interfaz.destroy()
                            print(f"✅ {interface_name} limpiada")
                        setattr(self, attr_name, None)
                    except Exception as e:
                        print(f"⚠️ Warning limpiando {interface_name}: {e}")
            
            # Limpiar contenedor
            self.limpiar_contenedor()
            
            print("✅ Recursos limpiados exitosamente")
            
        except Exception as e:
            print(f"❌ Error limpiando recursos: {e}")
    
    def actualizar_botones_navegacion(self, vista_activa):
        """✅ MEJORADO: Actualizar estado visual de botones de navegación con historial"""
        try:
            # Resetear colores
            self.btn_compras.configure(fg_color="#3b82f6")
            self.btn_carrito.configure(fg_color="#059669")
            if hasattr(self, 'btn_historial'):
                self.btn_historial.configure(fg_color="#f59e0b")
            self.btn_checkout.configure(fg_color="#7c3aed")
            
            # Activar botón correspondiente
            if vista_activa == "compras":
                self.btn_compras.configure(fg_color="#1d4ed8")
            elif vista_activa == "carrito":
                self.btn_carrito.configure(fg_color="#047857")
            elif vista_activa == "historial" and hasattr(self, 'btn_historial'):
                self.btn_historial.configure(fg_color="#d97706")
            elif vista_activa == "checkout":
                self.btn_checkout.configure(fg_color="#6d28d9")
                
        except Exception as e:
            print(f"❌ Error actualizando botones de navegación: {e}")
    
    def mostrar_compras(self):
        """✅ MÉTODO ACTUALIZADO: Mostrar interfaz de compras con callbacks mejorados"""
        try:
            self.vista_actual = "compras"
            self.limpiar_contenedor()
            self.actualizar_botones_navegacion("compras")
            
            print("🛍️ Iniciando carga de vista de compras...")
            
            # Crear interfaz de compras
            self.interfaz_compras = InterfazCompras(
                self.contenedor_principal,
                self.sistema.inventario,
                self.sistema.carrito
            )
            self.interfaz_compras.pack(fill="both", expand=True)
            
            # ✅ CONFIGURAR CALLBACK PERSONALIZADO MEJORADO
            def on_producto_agregado_callback(producto, cantidad):
                try:
                    print(f"🔄 Callback: Producto agregado - {cantidad}x {producto.nombre}")
                    print(f"📊 Estado del carrito después de agregar:")
                    print(f"   - Items totales: {self.sistema.carrito.obtener_cantidad_items()}")
                    print(f"   - Total precio: ${self.sistema.carrito.calcular_total():.2f}")
                    
                    # Actualizar contador del carrito
                    self.actualizar_contador_carrito()
                    
                    # Si la vista del carrito está activa, actualizarla
                    if self.vista_actual == "carrito" and self.interfaz_carrito:
                        print("🔄 Actualizando vista del carrito...")
                        self.interfaz_carrito.actualizar_carrito()
                    
                    # Mostrar notificación
                    self.mostrar_notificacion(
                        f"✅ {cantidad}x {producto.nombre} agregado al carrito",
                        tipo="success",
                        duracion=2000
                    )
                    
                except Exception as e:
                    print(f"❌ Error en callback producto agregado: {e}")
                    import traceback
                    traceback.print_exc()
            
            # ✅ CONFIGURAR CALLBACK EN LA INTERFAZ DE COMPRAS
            if hasattr(self.interfaz_compras, 'set_callback_producto_agregado'):
                self.interfaz_compras.set_callback_producto_agregado(on_producto_agregado_callback)
                print("🔗 Callback de producto agregado configurado exitosamente")
            else:
                print("⚠️ La interfaz de compras no tiene método set_callback_producto_agregado")
            
            # Establecer referencia para otros callbacks
            self.interfaz_compras.master = self
            
            # Actualizar contador del carrito
            self.actualizar_contador_carrito()
            
            print("🛍️ Vista de compras cargada exitosamente")
            
        except Exception as e:
            print(f"❌ Error mostrando compras: {e}")
            traceback.print_exc()
            self.mostrar_error("Error cargando productos")
    
    def mostrar_carrito(self):
        """✅ MÉTODO ACTUALIZADO: Mostrar interfaz del carrito con debugging"""
        try:
            self.vista_actual = "carrito"
            self.limpiar_contenedor()
            self.actualizar_botones_navegacion("carrito")
            
            print("🛒 Iniciando carga de vista del carrito...")
            print(f"📊 Estado actual del carrito:")
            print(f"   - Items: {self.sistema.carrito.obtener_cantidad_items()}")
            print(f"   - Total: ${self.sistema.carrito.calcular_total():.2f}")
            print(f"   - Items agrupados: {len(self.sistema.carrito.obtener_items_agrupados())}")
            
            # Crear interfaz del carrito
            self.interfaz_carrito = InterfazCarrito(
                self.contenedor_principal, 
                self.sistema.carrito
            )
            self.interfaz_carrito.pack(fill="both", expand=True)
            
            # ✅ ESTABLECER REFERENCIA PARA CALLBACKS
            self.interfaz_carrito.master = self
            
            print("🛒 Vista de carrito cargada exitosamente")
            
        except Exception as e:
            print(f"❌ Error mostrando carrito: {e}")
            traceback.print_exc()
            self.mostrar_error("Error cargando carrito")
    
    def mostrar_historial(self):
        """✅ NUEVO: Mostrar interfaz de historial de compras"""
        try:
            self.vista_actual = "historial"
            self.limpiar_contenedor()
            self.actualizar_botones_navegacion("historial")
            
            print("📋 Iniciando carga de vista de historial...")
            
            # ✅ CREAR INTERFAZ DE HISTORIAL MEJORADA
            historial_frame = ctk.CTkFrame(self.contenedor_principal, fg_color="#ffffff")
            historial_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Header del historial
            header_frame = ctk.CTkFrame(historial_frame, fg_color="#f8fafc", height=100)
            header_frame.pack(fill="x", padx=20, pady=(20, 10))
            header_frame.pack_propagate(False)
            
            # Título principal
            titulo = ctk.CTkLabel(
                header_frame,
                text="📋 Historial de Compras",
                font=("Arial Black", 28),
                text_color="#1f2937"
            )
            titulo.pack(pady=(20, 5))
            
            # Subtítulo con información del usuario
            if self.cliente_autenticado:
                subtitulo = f"Historial de compras para {self.cliente_autenticado.nombre}"
            else:
                subtitulo = "Historial de compras - Usuario Invitado"
            
            subtitulo_label = ctk.CTkLabel(
                header_frame,
                text=subtitulo,
                font=("Arial", 14),
                text_color="#6b7280"
            )
            subtitulo_label.pack()
            
            # ✅ CONTENIDO PRINCIPAL DEL HISTORIAL
            contenido_frame = ctk.CTkFrame(historial_frame, fg_color="#ffffff")
            contenido_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            # ✅ SIMULAR DATOS DE HISTORIAL (PLACEHOLDER)
            self.crear_historial_simulado(contenido_frame)
            
            # ✅ PANEL DE ACCIONES
            acciones_frame = ctk.CTkFrame(historial_frame, fg_color="#f8fafc", height=80)
            acciones_frame.pack(fill="x", padx=20, pady=(10, 20))
            acciones_frame.pack_propagate(False)
            
            # Botones de acción
            btn_frame = ctk.CTkFrame(acciones_frame, fg_color="transparent")
            btn_frame.pack(expand=True, pady=20)
            
            btn_actualizar = ctk.CTkButton(
                btn_frame,
                text="🔄 Actualizar",
                command=self.actualizar_historial,
                font=("Arial", 14, "bold"),
                fg_color="#3b82f6",
                hover_color="#2563eb",
                width=140,
                height=40
            )
            btn_actualizar.pack(side="left", padx=10)
            
            btn_exportar = ctk.CTkButton(
                btn_frame,
                text="📄 Exportar PDF",
                command=self.exportar_historial,
                font=("Arial", 14, "bold"),
                fg_color="#059669",
                hover_color="#047857",
                width=140,
                height=40
            )
            btn_exportar.pack(side="left", padx=10)
            
            btn_volver = ctk.CTkButton(
                btn_frame,
                text="🔙 Volver a Tienda",
                command=self.mostrar_compras,
                font=("Arial", 14, "bold"),
                fg_color="#f59e0b",
                hover_color="#d97706",
                width=140,
                height=40
            )
            btn_volver.pack(side="left", padx=10)
            
            print("📋 Vista de historial cargada exitosamente")
            
        except Exception as e:
            print(f"❌ Error mostrando historial: {e}")
            traceback.print_exc()
            self.mostrar_error("Error cargando historial")
    
    def crear_historial_simulado(self, parent):
        """✅ CREAR HISTORIAL SIMULADO PARA DEMOSTRACIÓN"""
        try:
            # Scroll frame para el historial
            scroll_frame = ctk.CTkScrollableFrame(
                parent,
                label_text="📦 Órdenes Recientes",
                label_font=("Arial Bold", 16)
            )
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # ✅ SIMULAR ÓRDENES DE EJEMPLO
            ordenes_ejemplo = [
                {
                    "id": "ORD-2024-001",
                    "fecha": "2024-01-15",
                    "productos": ["Laptop Gaming", "Mouse Gamer"],
                    "total": 1299.99,
                    "estado": "Entregado"
                },
                {
                    "id": "ORD-2024-002", 
                    "fecha": "2024-01-20",
                    "productos": ["Audífonos Bluetooth", "Cargador USB-C"],
                    "total": 89.99,
                    "estado": "En Tránsito"
                },
                {
                    "id": "ORD-2024-003",
                    "fecha": "2024-01-25", 
                    "productos": ["Smartphone", "Funda Protectora"],
                    "total": 699.99,
                    "estado": "Procesando"
                }
            ]
            
            # ✅ CREAR CARDS PARA CADA ORDEN
            for orden in ordenes_ejemplo:
                self.crear_card_orden(scroll_frame, orden)
            
            # ✅ MENSAJE INFORMATIVO
            info_frame = ctk.CTkFrame(scroll_frame, fg_color="#e0f2fe")
            info_frame.pack(fill="x", pady=20)
            
            info_label = ctk.CTkLabel(
                info_frame,
                text="ℹ️ Este es un historial de demostración.\nEn la versión completa, aquí aparecerían tus compras reales.",
                font=("Arial", 12),
                text_color="#0369a1",
                justify="center"
            )
            info_label.pack(pady=15)
            
        except Exception as e:
            print(f"❌ Error creando historial simulado: {e}")
    
    def crear_card_orden(self, parent, orden):
        """✅ CREAR CARD INDIVIDUAL PARA UNA ORDEN"""
        try:
            # Determinar color según estado
            colores_estado = {
                "Entregado": "#10b981",
                "En Tránsito": "#f59e0b", 
                "Procesando": "#3b82f6",
                "Cancelado": "#ef4444"
            }
            
            color_estado = colores_estado.get(orden["estado"], "#6b7280")
            
            # Frame principal de la orden
            orden_frame = ctk.CTkFrame(parent, fg_color="#ffffff", border_width=2, border_color="#e5e7eb")
            orden_frame.pack(fill="x", pady=10, padx=5)
            
            # ✅ HEADER DE LA ORDEN
            header_frame = ctk.CTkFrame(orden_frame, fg_color="#f9fafb")
            header_frame.pack(fill="x", padx=15, pady=(15, 5))
            
            # ID y fecha
            id_label = ctk.CTkLabel(
                header_frame,
                text=f"📋 Orden: {orden['id']}",
                font=("Arial Bold", 14),
                text_color="#1f2937"
            )
            id_label.pack(side="left")
            
            fecha_label = ctk.CTkLabel(
                header_frame,
                text=f"📅 {orden['fecha']}",
                font=("Arial", 12),
                text_color="#6b7280"
            )
            fecha_label.pack(side="right")
            
            # ✅ CONTENIDO DE LA ORDEN
            contenido_frame = ctk.CTkFrame(orden_frame, fg_color="transparent")
            contenido_frame.pack(fill="x", padx=15, pady=5)
            contenido_frame.grid_columnconfigure((0, 1, 2), weight=1)
            
            # Productos
            productos_text = "\n".join([f"• {prod}" for prod in orden["productos"]])
            productos_label = ctk.CTkLabel(
                contenido_frame,
                text=f"📦 Productos:\n{productos_text}",
                font=("Arial", 11),
                text_color="#374151",
                justify="left"
            )
            productos_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            
            # Total
            total_label = ctk.CTkLabel(
                contenido_frame,
                text=f"💰 Total:\n${orden['total']:.2f}",
                font=("Arial Bold", 13),
                text_color="#059669"
            )
            total_label.grid(row=0, column=1, padx=10, pady=5)
            
            # Estado
            estado_frame = ctk.CTkFrame(contenido_frame, fg_color=color_estado, corner_radius=15)
            estado_frame.grid(row=0, column=2, padx=10, pady=5, sticky="e")
            
            estado_label = ctk.CTkLabel(
                estado_frame,
                text=f"📊 {orden['estado']}",
                font=("Arial Bold", 11),
                text_color="white"
            )
            estado_label.pack(padx=15, pady=8)
            
            # ✅ BOTONES DE ACCIÓN
            acciones_frame = ctk.CTkFrame(orden_frame, fg_color="transparent")
            acciones_frame.pack(fill="x", padx=15, pady=(5, 15))
            
            btn_detalles = ctk.CTkButton(
                acciones_frame,
                text="👁️ Ver Detalles",
                command=lambda: self.ver_detalles_orden(orden),
                font=("Arial", 10),
                fg_color="#6b7280",
                hover_color="#4b5563",
                width=100,
                height=30
            )
            btn_detalles.pack(side="left", padx=5)
            
            if orden["estado"] == "Entregado":
                btn_factura = ctk.CTkButton(
                    acciones_frame,
                    text="📄 Factura",
                    command=lambda: self.descargar_factura(orden),
                    font=("Arial", 10),
                    fg_color="#3b82f6",
                    hover_color="#2563eb",
                    width=100,
                    height=30
                )
                btn_factura.pack(side="left", padx=5)
            
        except Exception as e:
            print(f"❌ Error creando card de orden: {e}")
    
    def actualizar_historial(self):
        """✅ ACTUALIZAR HISTORIAL"""
        print("🔄 Actualizando historial...")
        self.mostrar_notificacion("🔄 Historial actualizado", tipo="info")
    
    def exportar_historial(self):
        """✅ EXPORTAR HISTORIAL A PDF"""
        print("📄 Exportando historial...")
        self.mostrar_notificacion("📄 Historial exportado exitosamente", tipo="success")
    
    def ver_detalles_orden(self, orden):
        """✅ VER DETALLES DE UNA ORDEN"""
        print(f"👁️ Viendo detalles de orden {orden['id']}")
        self.mostrar_notificacion(f"👁️ Mostrando detalles de {orden['id']}", tipo="info")
    
    def descargar_factura(self, orden):
        """✅ DESCARGAR FACTURA"""
        print(f"📄 Descargando factura de orden {orden['id']}")
        self.mostrar_notificacion(f"📄 Factura descargada: {orden['id']}", tipo="success")
    
    def mostrar_estructuras(self):
        """✅ MÉTODO CORREGIDO: Mostrar visualizador de estructuras de datos"""
        try:
            print("📊 Abriendo visualizador de estructuras...")
            
            # ✅ VERIFICAR QUE LAS ESTRUCTURAS EXISTAN
            if not hasattr(self.sistema, 'pila_ordenes') or self.sistema.pila_ordenes is None:
                self.sistema.pila_ordenes = Pila()
                print("🔧 Pila de órdenes inicializada")
            
            if not hasattr(self.sistema, 'cola_pagos') or self.sistema.cola_pagos is None:
                self.sistema.cola_pagos = Cola()
                print("🔧 Cola de pagos inicializada")
            
            # ✅ CREAR VENTANA DE ESTRUCTURAS
            ventana_estructuras = mostrar_visualizador_estructuras(self.sistema)
            
            if ventana_estructuras:
                print("✅ Visualizador de estructuras abierto exitosamente")
                
                # ✅ CONFIGURAR VENTANA COMO MODAL
                ventana_estructuras.transient(self)  # Asociar con ventana principal
                ventana_estructuras.grab_set()  # Hacer modal
                
                # ✅ CONFIGURAR CIERRE APROPIADO
                def on_close():
                    try:
                        ventana_estructuras.grab_release()  # Liberar modal
                        ventana_estructuras.destroy()
                        print("🚪 Visualizador de estructuras cerrado")
                    except Exception as e:
                        print(f"⚠️ Error cerrando estructuras: {e}")
                
                ventana_estructuras.protocol("WM_DELETE_WINDOW", on_close)
                
                # ✅ LOG DE LA ACCIÓN
                self.mostrar_notificacion(
                    "📊 Visualizador de estructuras abierto",
                    tipo="info",
                    duracion=2000
                )
                
                # ✅ CENTRAR VENTANA MEJOR
                ventana_estructuras.focus_set()
                
            else:
                self.mostrar_error("Error abriendo visualizador de estructuras")
                
        except ImportError as e:
            print(f"❌ Error importando InterfazEstructuras: {e}")
            self.mostrar_error("Módulo de estructuras no disponible")
        except Exception as e:
            print(f"❌ Error mostrando estructuras: {e}")
            traceback.print_exc()
            self.mostrar_error("Error abriendo visualizador de estructuras")
    
    def mostrar_checkout(self):
        """✅ MÉTODO ACTUALIZADO: Mostrar interfaz de checkout con validaciones"""
        try:
            # Verificar si hay productos en el carrito
            cantidad_items = self.sistema.carrito.obtener_cantidad_items()
            if cantidad_items == 0:
                self.mostrar_error("El carrito está vacío. Agrega productos antes de hacer checkout.")
                return
            
            self.vista_actual = "checkout"
            self.limpiar_contenedor()
            self.actualizar_botones_navegacion("checkout")
            
            print(f"💳 Iniciando checkout con {cantidad_items} items...")
            
            self.interfaz_checkout = InterfazCheckout(
                self.contenedor_principal, 
                self.sistema
            )
            self.interfaz_checkout.pack(fill="both", expand=True)
            
            # ✅ CONFIGURAR CALLBACK PARA COMPLETAR CHECKOUT
            def on_checkout_complete():
                try:
                    print("✅ Checkout completado, actualizando interfaz...")
                    
                    # Actualizar contador del carrito
                    self.actualizar_contador_carrito()
                    
                    # Actualizar carrito si está visible
                    if self.vista_actual == "carrito" and self.interfaz_carrito:
                        self.interfaz_carrito.actualizar_carrito()
                    
                    # Mostrar notificación de éxito
                    self.mostrar_notificacion(
                        "🎉 ¡Compra realizada exitosamente!",
                        tipo="success",
                        duracion=3000
                    )
                    
                    # Redirigir a compras después de un delay
                    self.after(2000, self.mostrar_compras)
                    
                except Exception as e:
                    print(f"❌ Error en callback checkout: {e}")
            
            # Configurar callback si está disponible
            if hasattr(self.interfaz_checkout, 'set_callback'):
                self.interfaz_checkout.set_callback(on_checkout_complete)
                
            print("💳 Vista de checkout cargada exitosamente")
            
        except Exception as e:
            print(f"❌ Error mostrando checkout: {e}")
            traceback.print_exc()
            self.mostrar_error("Error cargando checkout")
            self.mostrar_compras()  # Fallback a compras
    
    def actualizar_contador_carrito(self):
        """✅ MÉTODO ACTUALIZADO: Actualizar contador de productos en el carrito"""
        try:
            if hasattr(self, 'btn_carrito') and self.btn_carrito.winfo_exists():
                cantidad = self.sistema.carrito.obtener_cantidad_items()
                
                print(f"🔄 Actualizando contador carrito: {cantidad} items")
                
                if cantidad > 0:
                    texto_carrito = f"🛒 Mi Carrito ({cantidad})"
                    # Cambiar color para indicar que hay productos
                    if self.vista_actual != "carrito":
                        self.btn_carrito.configure(
                            text=texto_carrito,
                            fg_color="#059669"
                        )
                    else:
                        self.btn_carrito.configure(text=texto_carrito)
                        
                    # ✅ HABILITAR BOTÓN DE CHECKOUT SI HAY PRODUCTOS
                    if hasattr(self, 'btn_checkout'):
                        self.btn_checkout.configure(state="normal")
                        
                else:
                    texto_carrito = "🛒 Mi Carrito"
                    if self.vista_actual != "carrito":
                        self.btn_carrito.configure(
                            text=texto_carrito,
                            fg_color="#6b7280"  # Gris cuando está vacío
                        )
                    else:
                        self.btn_carrito.configure(text=texto_carrito)
                        
                    # ✅ DESHABILITAR BOTÓN DE CHECKOUT SI NO HAY PRODUCTOS
                    if hasattr(self, 'btn_checkout'):
                        self.btn_checkout.configure(state="disabled", fg_color="#9ca3af")
                
        except Exception as e:
            print(f"❌ Error actualizando contador carrito: {e}")
            try:
                if hasattr(self, 'btn_carrito'):
                    self.btn_carrito.configure(text="🛒 Mi Carrito")
            except:
                pass
    
    def mostrar_notificacion(self, mensaje, tipo="success", duracion=3000):
        """✅ MÉTODO MEJORADO: Mostrar notificación temporal"""
        try:
            # Colores según el tipo
            colores = {
                "success": "#10b981",
                "warning": "#f59e0b", 
                "error": "#ef4444",
                "info": "#3b82f6"
            }
            
            iconos = {
                "success": "✅",
                "warning": "⚠️",
                "error": "❌", 
                "info": "ℹ️"
            }
            
            # Crear frame de notificación
            notif_frame = ctk.CTkFrame(
                self,
                fg_color=colores.get(tipo, "#3b82f6"),
                corner_radius=10
            )
            
            # Posicionar en la esquina superior derecha
            notif_frame.place(relx=0.95, rely=0.15, anchor="ne")
            
            # Mensaje
            mensaje_label = ctk.CTkLabel(
                notif_frame,
                text=f"{iconos.get(tipo, 'ℹ️')} {mensaje}",
                font=("Arial", 12, "bold"),
                text_color="white"
            )
            mensaje_label.pack(padx=15, pady=8)
            
            # ✅ ANIMACIÓN DE ENTRADA
            def animar_entrada():
                try:
                    # Efecto de fade-in
                    notif_frame.lift()
                except:
                    pass
            
            self.after(50, animar_entrada)
            
            # ✅ AUTO DESTRUIR DESPUÉS DE LA DURACIÓN ESPECIFICADA
            def destruir_notificacion():
                try:
                    if notif_frame.winfo_exists():
                        notif_frame.destroy()
                except:
                    pass
            
            self.after(duracion, destruir_notificacion)
            
        except Exception as e:
            print(f"❌ Error mostrando notificación: {e}")
    
    def mostrar_error(self, mensaje):
        """Mostrar mensaje de error en el contenedor principal"""
        try:
            self.limpiar_contenedor()
            
            error_frame = ctk.CTkFrame(self.contenedor_principal, fg_color="#fee2e2")
            error_frame.pack(fill="both", expand=True, padx=50, pady=100)
            
            error_label = ctk.CTkLabel(
                error_frame,
                text=f"❌ {mensaje}",
                font=("Arial", 18, "bold"),
                text_color="#dc2626"
            )
            error_label.pack(pady=50)
            
            retry_btn = ctk.CTkButton(
                error_frame,
                text="🔄 Reintentar",
                command=self.mostrar_compras,
                font=("Arial", 14, "bold"),
                fg_color="#3b82f6",
                hover_color="#2563eb"
            )
            retry_btn.pack(pady=20)
            
        except Exception as e:
            print(f"❌ Error mostrando error: {e}")
    
    def mostrar_error_critico(self, mensaje):
        """Mostrar error crítico y cerrar aplicación"""
        print(f"💥 Error crítico: {mensaje}")
        # Aquí podrías mostrar una ventana de error antes de cerrar
        self.quit()
    
    def logout(self):
        """Cerrar sesión y volver al login"""
        try:
            print("🚪 Iniciando proceso de logout...")
            print(f"📊 Estado actual: vista={self.vista_actual}")
            
            # Limpiar recursos antes de cerrar
            try:
                self.limpiar_recursos()
            except Exception as e:
                print(f"⚠️ Warning limpiando recursos: {e}")
            
            # Destruir la ventana actual
            print("🗑️ Destruyendo ventana principal...")
            self.destroy()
            
            # Pequeña pausa para asegurar limpieza
            import time
            time.sleep(0.2)
            print("⏱️ Pausa de limpieza completada")
            
            # Función callback para el nuevo login
            def reiniciar_aplicacion(cliente, sistema_login):
                try:
                    print(f"🔄 Reiniciando aplicación para {cliente.nombre}")
                    configurar_dpi_awareness()
                    
                    # Crear nueva instancia de la aplicación
                    print("🆕 Creando nueva instancia de aplicación...")
                    nueva_app = AplicacionPrincipal(cliente_autenticado=cliente)
                    print("▶️ Iniciando mainloop...")
                    nueva_app.mainloop()
                    
                except Exception as e:
                    print(f"❌ Error reiniciando aplicación: {e}")
                    traceback.print_exc()
            
            # Mostrar login con callback
            print("🔐 Mostrando pantalla de login...")
            mostrar_login(reiniciar_aplicacion)
            
            print("🏁 Proceso de logout completado")
                
        except Exception as e:
            print(f"❌ Error crítico en logout: {e}")
            traceback.print_exc()
            # En caso de error crítico, salir
            print("💥 Saliendo por error crítico...")
            sys.exit(1)
    
    def on_closing(self):
        """Manejar cierre de ventana"""
        try:
            print("👋 Cerrando aplicación...")
            
            # Limpiar recursos
            try:
                self.limpiar_recursos()
            except Exception as e:
                print(f"⚠️ Warning limpiando recursos en cierre: {e}")
            
            # Destruir ventana
            self.destroy()
            
            # Salir del programa completamente
            print("🏁 Aplicación cerrada exitosamente")
            sys.exit(0)
            
        except Exception as e:
            print(f"❌ Error cerrando aplicación: {e}")
            self.quit()
            sys.exit(1)

def main():
    """Función principal"""
    print("🚀 Iniciando Sistema de E-commerce...")
    
    def iniciar_aplicacion(cliente, sistema_login):
        """Callback para iniciar aplicación tras login exitoso"""
        try:
            print(f"🎉 Bienvenido, {cliente.nombre}!")
            configurar_dpi_awareness()
            
            app = AplicacionPrincipal(cliente_autenticado=cliente)
            app.mainloop()
            
        except Exception as e:
            print(f"❌ Error iniciando aplicación: {e}")
            traceback.print_exc()
    
    try:
        # Intentar mostrar login
        cliente = mostrar_login(iniciar_aplicacion)
        
    except Exception as e:
        print(f"⚠️ Error con el sistema de login: {e}")
        traceback.print_exc()
        
        # Modo invitado como fallback
        print("🔄 Iniciando en modo invitado...")
        try:
            configurar_dpi_awareness()
            app = AplicacionPrincipal()
            app.mainloop()
        except Exception as fallback_error:
            print(f"💥 Error crítico en modo invitado: {fallback_error}")
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    main()