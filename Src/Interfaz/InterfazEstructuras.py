import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

class InterfazEstructuras(ctk.CTkFrame):
    """Interfaz mejorada para visualizar las estructuras de datos del sistema"""
    
    def __init__(self, parent, sistema_ecommerce, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.sistema = sistema_ecommerce
        
        # VERIFICAR E INICIALIZAR ESTRUCTURAS
        self.verificar_estructuras()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Variables de control
        self.auto_refresh = tk.BooleanVar(value=True)
        self.refresh_interval = 5000  # 5 segundos
        self.refresh_job = None
        
        self.crear_interfaz()
        self.actualizar_visualizaciones()
        self.iniciar_auto_refresh()
    
    def verificar_estructuras(self):
        """Verificar e inicializar estructuras de datos si no existen"""
        try:
            # VERIFICAR PILA DE ÓRDENES
            if not hasattr(self.sistema, 'pila_ordenes') or self.sistema.pila_ordenes is None:
                from estructuras.Pila import Pila
                self.sistema.pila_ordenes = Pila()
                print("🔧 Pila de órdenes inicializada")
            
            # VERIFICAR COLA DE PAGOS
            if not hasattr(self.sistema, 'cola_pagos') or self.sistema.cola_pagos is None:
                from estructuras.Cola import Cola
                self.sistema.cola_pagos = Cola()
                print("🔧 Cola de pagos inicializada")
            
            # VERIFICAR INVENTARIO
            if not hasattr(self.sistema, 'inventario') or self.sistema.inventario is None:
                from Inventario import Inventario
                self.sistema.inventario = Inventario()
                print("🔧 Inventario inicializado")
            
            # VERIFICAR CARRITO
            if not hasattr(self.sistema, 'carrito') or self.sistema.carrito is None:
                from Carrito import Carrito
                self.sistema.carrito = Carrito("estructuras_viewer")
                print("🔧 Carrito inicializado")
                
            print("✅ Todas las estructuras verificadas/inicializadas")
            
        except Exception as e:
            print(f"Error verificando estructuras: {e}")
            import traceback
            traceback.print_exc()
    
    def crear_interfaz(self):
        """Crear la interfaz de estructuras mejorada"""
        # HEADER MEJORADO
        self.crear_header()

        # NOTEBOOK CON PESTAÑAS MEJORADAS
        self.notebook = ctk.CTkTabview(self, height=500)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Crear pestañas mejoradas
        self.crear_tab_inventario()
        self.crear_tab_carrito()
        self.crear_tab_pila_ordenes()
        self.crear_tab_cola_pagos()
        self.crear_tab_estadisticas()

        # PANEL DE CONTROL MEJORADO
        self.crear_panel_control()
    
    def crear_header(self):
        """Crear header mejorado con información general"""
        header_frame = ctk.CTkFrame(self, fg_color="#1e40af", height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)

        # TÍTULO E ICONO
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        ctk.CTkLabel(
            title_frame,
            text="📊 Visualizador de Estructuras de Datos",
            font=("Arial Black", 22),
            text_color="white"
        ).pack()
        
        # INFORMACIÓN GENERAL EN TIEMPO REAL
        self.info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        self.info_frame.grid(row=0, column=1, sticky="e", padx=20, pady=15)
        
        self.lbl_estado_general = ctk.CTkLabel(
            self.info_frame,
            text="⏳ Cargando...",
            font=("Arial Bold", 12),
            text_color="#fbbf24"
        )
        self.lbl_estado_general.pack()
        
        # CONTROL DE AUTO-REFRESH
        refresh_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        refresh_frame.grid(row=0, column=2, sticky="e", padx=20, pady=15)
        
        self.switch_auto_refresh = ctk.CTkSwitch(
            refresh_frame,
            text="🔄 Auto-refresh",
            variable=self.auto_refresh,
            command=self.toggle_auto_refresh,
            font=("Arial Bold", 10),
            text_color="white"
        )
        self.switch_auto_refresh.pack()
    
    def crear_tab_inventario(self):
        """Crear pestaña mejorada del inventario"""
        tab = self.notebook.add("📦 Inventario")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # INFO PANEL MEJORADO
        info_frame = ctk.CTkFrame(tab, fg_color="#f3f4f6")
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        info_container = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_container.pack(fill="x", padx=15, pady=15)
        info_container.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Información de la estructura
        ctk.CTkLabel(
            info_container,
            text="📋 Lista Enlazada de Productos",
            font=("Arial Black", 16),
            text_color="#1f2937"
        ).grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # ESTADÍSTICAS EN TIEMPO REAL
        self.lbl_total_productos = ctk.CTkLabel(
            info_container,
            text="📦 Productos: 0",
            font=("Arial Bold", 12),
            text_color="#059669"
        )
        self.lbl_total_productos.grid(row=1, column=0, padx=10)
        
        self.lbl_valor_total = ctk.CTkLabel(
            info_container,
            text="💰 Valor Total: $0.00",
            font=("Arial Bold", 12),
            text_color="#3b82f6"
        )
        self.lbl_valor_total.grid(row=1, column=1, padx=10)
        
        self.lbl_stock_total = ctk.CTkLabel(
            info_container,
            text="📊 Stock Total: 0",
            font=("Arial Bold", 12),
            text_color="#f59e0b"
        )
        self.lbl_stock_total.grid(row=1, column=2, padx=10)

        # ÁREA DE VISUALIZACIÓN MEJORADA
        self.text_inventario = ctk.CTkTextbox(
            tab, 
            font=("Courier New", 10),
            wrap="word"
        )
        self.text_inventario.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def crear_tab_carrito(self):
        """Crear pestaña mejorada del carrito"""
        tab = self.notebook.add("🛒 Carrito")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # INFO PANEL DEL CARRITO
        info_frame = ctk.CTkFrame(tab, fg_color="#f0fdf4")
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        info_container = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_container.pack(fill="x", padx=15, pady=15)
        info_container.grid_columnconfigure((0, 1, 2), weight=1)
        
        ctk.CTkLabel(
            info_container,
            text="🛍️ Estructura Dinámica del Carrito",
            font=("Arial Black", 16),
            text_color="#1f2937"
        ).grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # ESTADÍSTICAS DEL CARRITO
        self.lbl_items_carrito = ctk.CTkLabel(
            info_container,
            text="📦 Items: 0",
            font=("Arial Bold", 12),
            text_color="#059669"
        )
        self.lbl_items_carrito.grid(row=1, column=0, padx=10)
        
        self.lbl_total_carrito = ctk.CTkLabel(
            info_container,
            text="💰 Total: $0.00",
            font=("Arial Bold", 12),
            text_color="#3b82f6"
        )
        self.lbl_total_carrito.grid(row=1, column=1, padx=10)
        
        self.lbl_productos_unicos = ctk.CTkLabel(
            info_container,
            text="🔢 Únicos: 0",
            font=("Arial Bold", 12),
            text_color="#f59e0b"
        )
        self.lbl_productos_unicos.grid(row=1, column=2, padx=10)
        
        # ÁREA DE VISUALIZACIÓN DEL CARRITO
        self.text_carrito = ctk.CTkTextbox(
            tab,
            font=("Courier New", 10),
            wrap="word"
        )
        self.text_carrito.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def crear_tab_pila_ordenes(self):
        """Crear pestaña mejorada de la pila de órdenes"""
        tab = self.notebook.add("🗂️ Pila LIFO")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # INFO PANEL DE LA PILA
        info_frame = ctk.CTkFrame(tab, fg_color="#fef3c7")
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        info_container = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_container.pack(fill="x", padx=15, pady=15)
        info_container.grid_columnconfigure((0, 1, 2), weight=1)
        
        ctk.CTkLabel(
            info_container,
            text="📚 Pila de Órdenes (LIFO - Last In, First Out)",
            font=("Arial Black", 16),
            text_color="#1f2937"
        ).grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # ESTADÍSTICAS DE LA PILA
        self.lbl_ordenes_pila = ctk.CTkLabel(
            info_container,
            text="📋 Órdenes: 0",
            font=("Arial Bold", 12),
            text_color="#f59e0b"
        )
        self.lbl_ordenes_pila.grid(row=1, column=0, padx=10)
        
        self.lbl_valor_ordenes = ctk.CTkLabel(
            info_container,
            text="💰 Valor Total: $0.00",
            font=("Arial Bold", 12),
            text_color="#3b82f6"
        )
        self.lbl_valor_ordenes.grid(row=1, column=1, padx=10)
        
        self.lbl_ultima_orden = ctk.CTkLabel(
            info_container,
            text="🔝 Tope: N/A",
            font=("Arial Bold", 12),
            text_color="#dc2626"
        )
        self.lbl_ultima_orden.grid(row=1, column=2, padx=10)
        
        # ÁREA DE VISUALIZACIÓN DE LA PILA
        self.text_pila = ctk.CTkTextbox(
            tab,
            font=("Courier New", 10),
            wrap="word"
        )
        self.text_pila.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def crear_tab_cola_pagos(self):
        """Crear pestaña mejorada de la cola de pagos"""
        tab = self.notebook.add("🏃 Cola FIFO")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # INFO PANEL DE LA COLA
        info_frame = ctk.CTkFrame(tab, fg_color="#e0f2fe")
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        info_container = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_container.pack(fill="x", padx=15, pady=15)
        info_container.grid_columnconfigure((0, 1, 2), weight=1)
        
        ctk.CTkLabel(
            info_container,
            text="🚶 Cola de Pagos (FIFO - First In, First Out)",
            font=("Arial Black", 16),
            text_color="#1f2937"
        ).grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # ESTADÍSTICAS DE LA COLA
        self.lbl_pagos_cola = ctk.CTkLabel(
            info_container,
            text="💳 Pagos: 0",
            font=("Arial Bold", 12),
            text_color="#3b82f6"
        )
        self.lbl_pagos_cola.grid(row=1, column=0, padx=10)
        
        self.lbl_monto_total = ctk.CTkLabel(
            info_container,
            text="💰 Monto Total: $0.00",
            font=("Arial Bold", 12),
            text_color="#059669"
        )
        self.lbl_monto_total.grid(row=1, column=1, padx=10)
        
        self.lbl_proximo_pago = ctk.CTkLabel(
            info_container,
            text="⏭️ Siguiente: N/A",
            font=("Arial Bold", 12),
            text_color="#dc2626"
        )
        self.lbl_proximo_pago.grid(row=1, column=2, padx=10)
        
        # ÁREA DE VISUALIZACIÓN DE LA COLA
        self.text_cola = ctk.CTkTextbox(
            tab,
            font=("Courier New", 10),
            wrap="word"
        )
        self.text_cola.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def crear_tab_estadisticas(self):
        """Crear pestaña de estadísticas generales"""
        tab = self.notebook.add("📈 Estadísticas")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # PANEL DE ESTADÍSTICAS GLOBALES
        stats_frame = ctk.CTkFrame(tab)
        stats_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        ctk.CTkLabel(
            stats_frame,
            text="📊 Resumen General del Sistema",
            font=("Arial Black", 18),
            text_color="#1f2937"
        ).grid(row=0, column=0, columnspan=3, pady=15)

        # MÉTRICAS DEL SISTEMA
        # Columna 1: Inventario
        inv_frame = ctk.CTkFrame(stats_frame, fg_color="#f0fdf4")
        inv_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(inv_frame, text="📦 INVENTARIO", font=("Arial Bold", 14)).pack(pady=5)
        self.lbl_stat_productos = ctk.CTkLabel(inv_frame, text="Productos: 0", font=("Arial", 12))
        self.lbl_stat_productos.pack()
        self.lbl_stat_valor_inv = ctk.CTkLabel(inv_frame, text="Valor: $0.00", font=("Arial", 12))
        self.lbl_stat_valor_inv.pack()
        self.lbl_stat_stock = ctk.CTkLabel(inv_frame, text="Stock: 0", font=("Arial", 12))
        self.lbl_stat_stock.pack(pady=(0, 10))
        
        # Columna 2: Carrito
        cart_frame = ctk.CTkFrame(stats_frame, fg_color="#fef3c7")
        cart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(cart_frame, text="🛒 CARRITO", font=("Arial Bold", 14)).pack(pady=5)
        self.lbl_stat_items_cart = ctk.CTkLabel(cart_frame, text="Items: 0", font=("Arial", 12))
        self.lbl_stat_items_cart.pack()
        self.lbl_stat_total_cart = ctk.CTkLabel(cart_frame, text="Total: $0.00", font=("Arial", 12))
        self.lbl_stat_total_cart.pack()
        self.lbl_stat_unique_cart = ctk.CTkLabel(cart_frame, text="Únicos: 0", font=("Arial", 12))
        self.lbl_stat_unique_cart.pack(pady=(0, 10))
        
        # Columna 3: Actividad
        activity_frame = ctk.CTkFrame(stats_frame, fg_color="#e0f2fe")
        activity_frame.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(activity_frame, text="📈 ACTIVIDAD", font=("Arial Bold", 14)).pack(pady=5)
        self.lbl_stat_ordenes = ctk.CTkLabel(activity_frame, text="Órdenes: 0", font=("Arial", 12))
        self.lbl_stat_ordenes.pack()
        self.lbl_stat_pagos = ctk.CTkLabel(activity_frame, text="Pagos: 0", font=("Arial", 12))
        self.lbl_stat_pagos.pack()
        self.lbl_stat_ultima_act = ctk.CTkLabel(activity_frame, text="Última: N/A", font=("Arial", 12))
        self.lbl_stat_ultima_act.pack(pady=(0, 10))

        # ÁREA DE LOGS DEL SISTEMA
        ctk.CTkLabel(
            tab,
            text="📋 Log de Actividad del Sistema",
            font=("Arial Bold", 16)
        ).grid(row=1, column=0, pady=(20, 5), sticky="w", padx=10)
        
        self.text_logs = ctk.CTkTextbox(
            tab,
            font=("Consolas", 9),
            wrap="word"
        )
        self.text_logs.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tab.grid_rowconfigure(2, weight=1)
    
    def crear_panel_control(self):
        """Crear panel de control mejorado"""
        panel = ctk.CTkFrame(self, height=70)
        panel.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        panel.pack_propagate(False)
        panel.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # BOTONES DE CONTROL MEJORADOS
        btn_actualizar = ctk.CTkButton(
            panel,
            text="🔄 Actualizar",
            command=self.actualizar_visualizaciones,
            font=("Arial Bold", 12),
            height=35,
            fg_color="#3b82f6",
            hover_color="#2563eb"
        )
        btn_actualizar.grid(row=0, column=0, padx=5, pady=15, sticky="ew")
        
        btn_limpiar = ctk.CTkButton(
            panel,
            text="🧹 Limpiar",
            command=self.limpiar_estructuras,
            font=("Arial Bold", 12),
            height=35,
            fg_color="#dc2626",
            hover_color="#b91c1c"
        )
        btn_limpiar.grid(row=0, column=1, padx=5, pady=15, sticky="ew")
        
        btn_exportar = ctk.CTkButton(
            panel,
            text="💾 Exportar",
            command=self.exportar_estructuras,
            font=("Arial Bold", 12),
            height=35,
            fg_color="#059669",
            hover_color="#047857"
        )
        btn_exportar.grid(row=0, column=2, padx=5, pady=15, sticky="ew")
        
        btn_simulacion = ctk.CTkButton(
            panel,
            text="🎮 Simulación",
            command=self.mostrar_simulacion,
            font=("Arial Bold", 12),
            height=35,
            fg_color="#7c3aed",
            hover_color="#6d28d9"
        )
        btn_simulacion.grid(row=0, column=3, padx=5, pady=15, sticky="ew")
        
        btn_cerrar = ctk.CTkButton(
            panel,
            text="❌ Cerrar",
            command=self.cerrar_ventana,
            font=("Arial Bold", 12),
            height=35,
            fg_color="#6b7280",
            hover_color="#4b5563"
        )
        btn_cerrar.grid(row=0, column=4, padx=5, pady=15, sticky="ew")
    
    def actualizar_visualizaciones(self):
        """Actualizar todas las visualizaciones"""
        try:
            self.actualizar_estado_general()
            self.actualizar_inventario()
            self.actualizar_carrito()
            self.actualizar_pila_ordenes()
            self.actualizar_cola_pagos()
            self.actualizar_estadisticas()
            self.actualizar_logs()
            
        except Exception as e:
            print(f"Error actualizando visualizaciones: {e}")
            import traceback
            traceback.print_exc()
    
    def actualizar_estado_general(self):
        """Actualizar estado general en el header"""
        try:
            # CALCULAR ESTADÍSTICAS GENERALES
            total_productos = len(self.sistema.inventario.obtener_productos()) if hasattr(self.sistema.inventario, 'obtener_productos') else 0
            items_carrito = self.sistema.carrito.obtener_cantidad_items() if hasattr(self.sistema.carrito, 'obtener_cantidad_items') else 0
            ordenes_pila = len(self.obtener_elementos_seguros(self.sistema.pila_ordenes))
            pagos_cola = len(self.obtener_elementos_seguros(self.sistema.cola_pagos))
            
            estado_texto = f"📦 {total_productos} productos | 🛒 {items_carrito} en carrito | 📋 {ordenes_pila} órdenes | 💳 {pagos_cola} pagos"
            
            self.lbl_estado_general.configure(
                text=estado_texto,
                text_color="#10b981"
            )
            
        except Exception as e:
            self.lbl_estado_general.configure(
                text="❌ Error actualizando estado",
                text_color="#dc2626"
            )
    
    def obtener_elementos_seguros(self, estructura):
        """Obtener elementos de una estructura de manera segura"""
        try:
            if estructura is None:
                return []
            
            if hasattr(estructura, 'obtener_elementos'):
                return estructura.obtener_elementos()
            elif hasattr(estructura, 'elementos'):
                return estructura.elementos
            elif hasattr(estructura, '_elementos'):
                return estructura._elementos
            else:
                return []
        except Exception as e:
            print(f"Error obteniendo elementos: {e}")
            return []
    
    def actualizar_inventario(self):
        """Actualizar visualización del inventario"""
        try:
            self.text_inventario.delete("1.0", tk.END)
            
            productos = self.sistema.inventario.obtener_productos() if hasattr(self.sistema.inventario, 'obtener_productos') else []
            
            # CALCULAR ESTADÍSTICAS
            total_productos = len(productos)
            valor_total = sum(p.precio * p.stock for p in productos)
            stock_total = sum(p.stock for p in productos)
            
            # ACTUALIZAR LABELS DE ESTADÍSTICAS
            self.lbl_total_productos.configure(text=f"📦 Productos: {total_productos}")
            self.lbl_valor_total.configure(text=f"💰 Valor Total: ${valor_total:.2f}")
            self.lbl_stock_total.configure(text=f"📊 Stock Total: {stock_total}")

            # CONTENIDO MEJORADO
            contenido = "═" * 80 + "\n"
            contenido += "                        📦 INVENTARIO DE PRODUCTOS\n"
            contenido += "═" * 80 + "\n\n"
            
            if productos:
                contenido += f"📊 Total de productos: {total_productos}\n"
                contenido += f"💰 Valor total del inventario: ${valor_total:,.2f}\n"
                contenido += f"📦 Stock total disponible: {stock_total:,} unidades\n"
                contenido += "─" * 80 + "\n\n"
                
                for i, producto in enumerate(productos, 1):
                    contenido += f"[{i:3d}] 🏷️  ID: {getattr(producto, 'id', getattr(producto, 'id_producto', 'N/A'))}\n"
                    contenido += f"      📝 Nombre: {producto.nombre}\n"
                    contenido += f"      💰 Precio: ${producto.precio:.2f}\n"
                    contenido += f"      📦 Stock: {producto.stock:,} unidades\n"
                    contenido += f"      💵 Valor en stock: ${producto.precio * producto.stock:.2f}\n"
                    if hasattr(producto, 'descripcion') and producto.descripcion:
                        contenido += f"      📋 Descripción: {producto.descripcion[:50]}{'...' if len(producto.descripcion) > 50 else ''}\n"
                    contenido += "─" * 80 + "\n"
            else:
                contenido += "❌ No hay productos en el inventario\n"
                contenido += "ℹ️  Los productos aparecerán aquí una vez que se carguen en el sistema\n"
            
            contenido += "\n═" * 80 + "\n"
            self.text_inventario.insert("1.0", contenido)
            
        except Exception as e:
            self.text_inventario.delete("1.0", tk.END)
            self.text_inventario.insert("1.0", f"❌ Error cargando inventario: {e}")
    
    def actualizar_carrito(self):
        """Actualizar visualización del carrito"""
        try:
            self.text_carrito.delete("1.0", tk.END)

            # OBTENER DATOS DEL CARRITO MEJORADO
            items_agrupados = []
            total_carrito = 0
            items_count = 0
            
            if hasattr(self.sistema.carrito, 'obtener_items_agrupados'):
                items_agrupados = self.sistema.carrito.obtener_items_agrupados()
                total_carrito = self.sistema.carrito.calcular_total()
                items_count = self.sistema.carrito.obtener_cantidad_items()

            # ACTUALIZAR ESTADÍSTICAS
            productos_unicos = len(items_agrupados)
            self.lbl_items_carrito.configure(text=f"📦 Items: {items_count}")
            self.lbl_total_carrito.configure(text=f"💰 Total: ${total_carrito:.2f}")
            self.lbl_productos_unicos.configure(text=f"🔢 Únicos: {productos_unicos}")
            
            # CONTENIDO DEL CARRITO
            contenido = "═" * 80 + "\n"
            contenido += "                        🛒 CARRITO DE COMPRAS\n"
            contenido += "═" * 80 + "\n\n"
            
            if items_agrupados:
                contenido += f"📊 Total de items: {items_count}\n"
                contenido += f"🔢 Productos únicos: {productos_unicos}\n"
                contenido += f"💰 Total del carrito: ${total_carrito:.2f}\n"
                contenido += "─" * 80 + "\n\n"
                
                for i, item in enumerate(items_agrupados, 1):
                    producto = item.producto
                    cantidad = item.cantidad
                    subtotal = producto.precio * cantidad
                    
                    contenido += f"[{i:2d}] 📦 {producto.nombre}\n"
                    contenido += f"     💰 Precio unitario: ${producto.precio:.2f}\n"
                    contenido += f"     📊 Cantidad: {cantidad}\n"
                    contenido += f"     💵 Subtotal: ${subtotal:.2f}\n"
                    if hasattr(item, 'fecha_agregado'):
                        contenido += f"     📅 Agregado: {item.fecha_agregado.strftime('%d/%m/%Y %H:%M')}\n"
                    contenido += "─" * 80 + "\n"
            else:
                contenido += "❌ El carrito está vacío\n"
                contenido += "ℹ️  Agrega productos desde la tienda para verlos aquí\n"
            
            contenido += "\n═" * 80 + "\n"
            self.text_carrito.insert("1.0", contenido)
            
        except Exception as e:
            self.text_carrito.delete("1.0", tk.END)
            self.text_carrito.insert("1.0", f"❌ Error cargando carrito: {e}")
    
    def actualizar_pila_ordenes(self):
        """Actualizar visualización de la pila de órdenes"""
        try:
            self.text_pila.delete("1.0", tk.END)
            
            ordenes = self.obtener_elementos_seguros(self.sistema.pila_ordenes)

            # CALCULAR ESTADÍSTICAS
            total_ordenes = len(ordenes)
            valor_total = 0
            ultima_orden = "N/A"
            
            if ordenes:
                valor_total = sum(getattr(orden, 'total', 0) for orden in ordenes)
                ultima_orden = f"#{getattr(ordenes[-1], 'id', 'N/A')}" if ordenes else "N/A"

            # ACTUALIZAR ESTADÍSTICAS
            self.lbl_ordenes_pila.configure(text=f"📋 Órdenes: {total_ordenes}")
            self.lbl_valor_ordenes.configure(text=f"💰 Valor Total: ${valor_total:.2f}")
            self.lbl_ultima_orden.configure(text=f"🔝 Tope: {ultima_orden}")
            
            # CONTENIDO DE LA PILA
            contenido = "═" * 80 + "\n"
            contenido += "                      🗂️ PILA DE ÓRDENES (LIFO)\n"
            contenido += "═" * 80 + "\n\n"
            
            if ordenes:
                contenido += f"📊 Total de órdenes: {total_ordenes}\n"
                contenido += f"💰 Valor total: ${valor_total:.2f}\n"
                contenido += "🔝 TOP (Última agregada - Primera en procesarse)\n"
                contenido += "─" * 80 + "\n\n"
                
                # Mostrar en orden LIFO
                for i, orden in enumerate(reversed(ordenes)):
                    posicion = len(ordenes) - i
                    contenido += f"[{posicion:2d}] 🏷️  Orden #{getattr(orden, 'id', 'N/A')}\n"
                    
                    if hasattr(orden, 'fecha'):
                        contenido += f"     📅 Fecha: {orden.fecha.strftime('%d/%m/%Y %H:%M:%S')}\n"
                    if hasattr(orden, 'total'):
                        contenido += f"     💰 Total: ${orden.total:.2f}\n"
                    if hasattr(orden, 'estado'):
                        contenido += f"     📊 Estado: {orden.estado}\n"
                    if hasattr(orden, 'cliente_id'):
                        contenido += f"     👤 Cliente: {orden.cliente_id}\n"
                    if hasattr(orden, 'productos'):
                        contenido += f"     📦 Items: {len(orden.productos)} productos\n"
                    
                    contenido += "─" * 80 + "\n"
                
                contenido += "\n🔻 BOTTOM (Primera agregada - Última en procesarse)\n"
            else:
                contenido += "❌ No hay órdenes en la pila\n"
                contenido += "ℹ️  Las órdenes se agregarán aquí cuando se generen compras\n"
            
            contenido += "\n═" * 80 + "\n"
            self.text_pila.insert("1.0", contenido)
            
        except Exception as e:
            self.text_pila.delete("1.0", tk.END)
            self.text_pila.insert("1.0", f"❌ Error cargando pila de órdenes: {e}")
    
    def actualizar_cola_pagos(self):
        """Actualizar visualización de la cola de pagos"""
        try:
            self.text_cola.delete("1.0", tk.END)
            
            pagos = self.obtener_elementos_seguros(self.sistema.cola_pagos)

            # CALCULAR ESTADÍSTICAS
            total_pagos = len(pagos)
            monto_total = 0
            proximo_pago = "N/A"
            
            if pagos:
                monto_total = sum(getattr(pago, 'monto', 0) for pago in pagos)
                proximo_pago = f"#{getattr(pagos[0], 'id_pago', 'N/A')}" if pagos else "N/A"
            
            # ACTUALIZAR ESTADÍSTICAS
            self.lbl_pagos_cola.configure(text=f"💳 Pagos: {total_pagos}")
            self.lbl_monto_total.configure(text=f"💰 Monto Total: ${monto_total:.2f}")
            self.lbl_proximo_pago.configure(text=f"⏭️ Siguiente: {proximo_pago}")
            
            # CONTENIDO DE LA COLA
            contenido = "═" * 80 + "\n"
            contenido += "                       🏃 COLA DE PAGOS (FIFO)\n"
            contenido += "═" * 80 + "\n\n"
            
            if pagos:
                contenido += f"📊 Total de pagos: {total_pagos}\n"
                contenido += f"💰 Monto total: ${monto_total:.2f}\n"
                contenido += "➡️ FRONT (Primero en entrar - Primero en procesarse)\n"
                contenido += "─" * 80 + "\n\n"
                
                # Mostrar en orden FIFO
                for i, pago in enumerate(pagos, 1):
                    contenido += f"[{i:2d}] 🏷️  Pago ID: {getattr(pago, 'id_pago', 'N/A')}\n"
                    
                    if hasattr(pago, 'cliente'):
                        contenido += f"     👤 Cliente: {pago.cliente}\n"
                    if hasattr(pago, 'monto'):
                        contenido += f"     💰 Monto: ${pago.monto:.2f}\n"
                    if hasattr(pago, 'metodo'):
                        contenido += f"     💳 Método: {pago.metodo}\n"
                    if hasattr(pago, 'fecha'):
                        contenido += f"     📅 Fecha: {pago.fecha.strftime('%d/%m/%Y %H:%M:%S')}\n"
                    if hasattr(pago, 'estado'):
                        contenido += f"     📊 Estado: {pago.estado}\n"
                    
                    contenido += "─" * 80 + "\n"
                
                contenido += "\n⬅️ REAR (Último en entrar - Último en procesarse)\n"
            else:
                contenido += "❌ No hay pagos en la cola\n"
                contenido += "ℹ️  Los pagos se agregarán aquí cuando se procesen compras\n"
            
            contenido += "\n═" * 80 + "\n"
            self.text_cola.insert("1.0", contenido)
            
        except Exception as e:
            self.text_cola.delete("1.0", tk.END)
            self.text_cola.insert("1.0", f"❌ Error cargando cola de pagos: {e}")
    
    def actualizar_estadisticas(self):
        """Actualizar estadísticas generales"""
        try:
            # ESTADÍSTICAS DE INVENTARIO
            productos = self.sistema.inventario.obtener_productos() if hasattr(self.sistema.inventario, 'obtener_productos') else []
            total_productos = len(productos)
            valor_inventario = sum(p.precio * p.stock for p in productos)
            stock_total = sum(p.stock for p in productos)
            
            self.lbl_stat_productos.configure(text=f"Productos: {total_productos}")
            self.lbl_stat_valor_inv.configure(text=f"Valor: ${valor_inventario:,.2f}")
            self.lbl_stat_stock.configure(text=f"Stock: {stock_total:,}")
            
            # ESTADÍSTICAS DE CARRITO
            items_carrito = self.sistema.carrito.obtener_cantidad_items() if hasattr(self.sistema.carrito, 'obtener_cantidad_items') else 0
            total_carrito = self.sistema.carrito.calcular_total() if hasattr(self.sistema.carrito, 'calcular_total') else 0
            unicos_carrito = len(self.sistema.carrito.obtener_items_agrupados()) if hasattr(self.sistema.carrito, 'obtener_items_agrupados') else 0
            
            self.lbl_stat_items_cart.configure(text=f"Items: {items_carrito}")
            self.lbl_stat_total_cart.configure(text=f"Total: ${total_carrito:.2f}")
            self.lbl_stat_unique_cart.configure(text=f"Únicos: {unicos_carrito}")
            
            # ESTADÍSTICAS DE ACTIVIDAD
            ordenes = self.obtener_elementos_seguros(self.sistema.pila_ordenes)
            pagos = self.obtener_elementos_seguros(self.sistema.cola_pagos)
            
            self.lbl_stat_ordenes.configure(text=f"Órdenes: {len(ordenes)}")
            self.lbl_stat_pagos.configure(text=f"Pagos: {len(pagos)}")
            
            # Última actividad
            ultima_actividad = "N/A"
            if ordenes:
                ultima_actividad = "Orden creada"
            elif pagos:
                ultima_actividad = "Pago procesado"
            elif items_carrito > 0:
                ultima_actividad = "Items en carrito"
            
            self.lbl_stat_ultima_act.configure(text=f"Última: {ultima_actividad}")
            
        except Exception as e:
            print(f"Error actualizando estadísticas: {e}")
    
    def actualizar_logs(self):
        """Actualizar logs del sistema"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # INFORMACIÓN DE ÚLTIMA ACTUALIZACIÓN
            log_entry = f"[{timestamp}] 🔄 Estructuras actualizadas\n"
            
            # Información del estado actual
            productos_count = len(self.sistema.inventario.obtener_productos()) if hasattr(self.sistema.inventario, 'obtener_productos') else 0
            carrito_count = self.sistema.carrito.obtener_cantidad_items() if hasattr(self.sistema.carrito, 'obtener_cantidad_items') else 0
            ordenes_count = len(self.obtener_elementos_seguros(self.sistema.pila_ordenes))
            pagos_count = len(self.obtener_elementos_seguros(self.sistema.cola_pagos))
            
            log_entry += f"[{timestamp}] 📊 Estado: {productos_count} productos, {carrito_count} en carrito, {ordenes_count} órdenes, {pagos_count} pagos\n"
            
            # MANTENER SOLO LAS ÚLTIMAS 50 LÍNEAS
            current_content = self.text_logs.get("1.0", tk.END)
            lines = current_content.strip().split('\n')
            
            if len(lines) > 50:
                lines = lines[-45:]  # Mantener las últimas 45 líneas
            
            lines.append(log_entry.strip())
            
            self.text_logs.delete("1.0", tk.END)
            self.text_logs.insert("1.0", '\n'.join(lines))
            
            # Scroll to bottom
            self.text_logs.see(tk.END)
            
        except Exception as e:
            print(f"Error actualizando logs: {e}")

    def iniciar_auto_refresh(self):
        """Iniciar auto-refresh si está habilitado"""
        if self.auto_refresh.get():
            self.actualizar_visualizaciones()
            self.refresh_job = self.after(self.refresh_interval, self.iniciar_auto_refresh)
    
    def toggle_auto_refresh(self):
        """Alternar auto-refresh"""
        if self.auto_refresh.get():
            self.iniciar_auto_refresh()
        else:
            if self.refresh_job:
                self.after_cancel(self.refresh_job)
                self.refresh_job = None
    
    def limpiar_estructuras(self):
        """Limpiar todas las estructuras de datos"""
        respuesta = messagebox.askyesno(
            "Confirmar Limpieza",
            "¿Está seguro de que desea limpiar todas las estructuras?\n\n"
            "⚠️ Esto eliminará:\n"
            "• Todas las órdenes de la pila\n"
            "• Todos los pagos de la cola\n"
            "• El contenido del carrito actual\n\n"
            "❌ Esta acción NO se puede deshacer"
        )
        
        if respuesta:
            try:
                # LIMPIAR ESTRUCTURAS DE MANERA SEGURA
                if hasattr(self.sistema.pila_ordenes, 'vaciar'):
                    self.sistema.pila_ordenes.vaciar()
                elif hasattr(self.sistema.pila_ordenes, 'limpiar'):
                    self.sistema.pila_ordenes.limpiar()
                
                if hasattr(self.sistema.cola_pagos, 'vaciar'):
                    self.sistema.cola_pagos.vaciar()
                elif hasattr(self.sistema.cola_pagos, 'limpiar'):
                    self.sistema.cola_pagos.limpiar()
                
                if hasattr(self.sistema.carrito, 'limpiar'):
                    self.sistema.carrito.limpiar()
                elif hasattr(self.sistema.carrito, 'vaciar'):
                    self.sistema.carrito.vaciar()
                
                # Actualizar visualizaciones
                self.actualizar_visualizaciones()
                
                # Log de limpieza
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_entry = f"[{timestamp}] 🧹 Todas las estructuras limpiadas\n"
                self.text_logs.insert(tk.END, log_entry)
                
                messagebox.showinfo("Éxito", "Todas las estructuras han sido limpiadas correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al limpiar estructuras: {str(e)}")
    
    def exportar_estructuras(self):
        """Exportar el estado actual de las estructuras"""
        try:
            # CREAR DIRECTORIO DE EXPORTACIÓN
            project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            export_dir = os.path.join(project_dir, 'Exports')
            os.makedirs(export_dir, exist_ok=True)

            # NOMBRE DEL ARCHIVO
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"estructuras_datos_{timestamp}.txt"
            filepath = os.path.join(export_dir, filename)

            # GENERAR CONTENIDO COMPLETO
            contenido = self.generar_reporte_completo()

            # GUARDAR ARCHIVO
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(contenido)
            
            messagebox.showinfo(
                "✅ Exportación Exitosa",
                f"Estructuras exportadas correctamente:\n\n"
                f"📁 Archivo: {filename}\n"
                f"📍 Ubicación: {export_dir}\n"
                f"📊 Tamaño: {os.path.getsize(filepath):,} bytes"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar estructuras:\n{str(e)}")

    def generar_reporte_completo(self):
        """Generar reporte completo de todas las estructuras"""
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        contenido = f"""
═══════════════════════════════════════════════════════════════════════════════
                        📊 REPORTE DE ESTRUCTURAS DE DATOS
                           Sistema de E-commerce Universitario
═══════════════════════════════════════════════════════════════════════════════

📅 Fecha de generación: {timestamp}
🔧 Sistema: Proyecto de Estructuras de Datos
👨‍💻 Generado por: Visualizador de Estructuras

═══════════════════════════════════════════════════════════════════════════════
                                📦 INVENTARIO
═══════════════════════════════════════════════════════════════════════════════

"""
        
        # AGREGAR DATOS DEL INVENTARIO
        try:
            productos = self.sistema.inventario.obtener_productos() if hasattr(self.sistema.inventario, 'obtener_productos') else []
            contenido += f"Total de productos: {len(productos)}\n"
            contenido += f"Valor total del inventario: ${sum(p.precio * p.stock for p in productos):,.2f}\n"
            contenido += f"Stock total: {sum(p.stock for p in productos):,} unidades\n\n"
            
            for i, producto in enumerate(productos, 1):
                contenido += f"{i:3d}. {producto.nombre} | ${producto.precio:.2f} | Stock: {producto.stock}\n"
        except Exception as e:
            contenido += f"Error obteniendo inventario: {e}\n"
        
        # AGREGAR CARRITO
        contenido += f"""
═══════════════════════════════════════════════════════════════════════════════
                               🛒 CARRITO ACTUAL
═══════════════════════════════════════════════════════════════════════════════

"""
        try:
            items_carrito = self.sistema.carrito.obtener_items_agrupados() if hasattr(self.sistema.carrito, 'obtener_items_agrupados') else []
            total_carrito = self.sistema.carrito.calcular_total() if hasattr(self.sistema.carrito, 'calcular_total') else 0
            
            contenido += f"Items en carrito: {len(items_carrito)}\n"
            contenido += f"Total del carrito: ${total_carrito:.2f}\n\n"
            
            for i, item in enumerate(items_carrito, 1):
                contenido += f"{i:2d}. {item.producto.nombre} x{item.cantidad} = ${item.producto.precio * item.cantidad:.2f}\n"
        except Exception as e:
            contenido += f"Error obteniendo carrito: {e}\n"
        
        # AGREGAR MÁS SECCIONES...
        contenido += f"""
═══════════════════════════════════════════════════════════════════════════════
                              🗂️ PILA DE ÓRDENES
═══════════════════════════════════════════════════════════════════════════════

"""
        try:
            ordenes = self.obtener_elementos_seguros(self.sistema.pila_ordenes)
            contenido += f"Órdenes en pila: {len(ordenes)}\n"
            for i, orden in enumerate(reversed(ordenes), 1):
                contenido += f"{i:2d}. Orden #{getattr(orden, 'id', 'N/A')} - ${getattr(orden, 'total', 0):.2f}\n"
        except Exception as e:
            contenido += f"Error obteniendo órdenes: {e}\n"
        
        contenido += f"""
═══════════════════════════════════════════════════════════════════════════════
                               🏃 COLA DE PAGOS
═══════════════════════════════════════════════════════════════════════════════

"""
        try:
            pagos = self.obtener_elementos_seguros(self.sistema.cola_pagos)
            contenido += f"Pagos en cola: {len(pagos)}\n"
            for i, pago in enumerate(pagos, 1):
                contenido += f"{i:2d}. Pago #{getattr(pago, 'id_pago', 'N/A')} - ${getattr(pago, 'monto', 0):.2f}\n"
        except Exception as e:
            contenido += f"Error obteniendo pagos: {e}\n"
        
        contenido += f"""
═══════════════════════════════════════════════════════════════════════════════
                               📈 RESUMEN FINAL
═══════════════════════════════════════════════════════════════════════════════

Reporte generado exitosamente
Timestamp: {timestamp}
Sistema: Activo y funcionando

═══════════════════════════════════════════════════════════════════════════════
"""
        
        return contenido
    
    def mostrar_simulacion(self):
        """Mostrar ventana de simulación de estructuras integrada"""
        try:
            # ARREGLO: Crear simulación integrada sin importar archivo externo
            ventana_sim = ctk.CTkToplevel(self)
            ventana_sim.title("🎮 Simulación de Estructuras de Datos")
            ventana_sim.geometry("900x700")
            ventana_sim.transient(self)
            ventana_sim.grab_set()  # Modal
            
            # CREAR SIMULACIÓN COMPLETA INTEGRADA
            self.crear_simulacion_integrada(ventana_sim)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo simulación: {str(e)}")

    def crear_simulacion_integrada(self, ventana):
        """Crear simulación completa integrada"""
        # Frame principal
        main_frame = ctk.CTkFrame(ventana)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.grid_columnconfigure((0, 1), weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        # TÍTULO
        titulo = ctk.CTkLabel(
            main_frame,
            text="🎮 Simulador de Estructuras de Datos",
            font=("Arial Black", 24),
            text_color="#1f2937"
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=20)

        # PANEL DE PILA (IZQUIERDA)
        pila_frame = ctk.CTkFrame(main_frame, fg_color="#fef3c7")
        pila_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            pila_frame,
            text="📚 PILA (LIFO)",
            font=("Arial Bold", 18),
            text_color="#92400e"
        ).pack(pady=10)
        
        # Controles de pila
        pila_controls = ctk.CTkFrame(pila_frame, fg_color="transparent")
        pila_controls.pack(pady=10)
        
        self.pila_entry = ctk.CTkEntry(
            pila_controls,
            placeholder_text="Valor para la pila",
            width=150
        )
        self.pila_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            pila_controls,
            text="⬆️ PUSH",
            command=self.simular_push,
            width=80,
            fg_color="#059669"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            pila_controls,
            text="⬇️ POP",
            command=self.simular_pop,
            width=80,
            fg_color="#dc2626"
        ).pack(side="left", padx=2)
        
        # Visualización de pila
        self.pila_visual = ctk.CTkTextbox(
            pila_frame,
            height=200,
            font=("Courier New", 12),
            fg_color="#fef3c7"
        )
        self.pila_visual.pack(fill="both", expand=True, padx=10, pady=10)

        # PANEL DE COLA (DERECHA)
        cola_frame = ctk.CTkFrame(main_frame, fg_color="#e0f2fe")
        cola_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            cola_frame,
            text="🏃 COLA (FIFO)",
            font=("Arial Bold", 18),
            text_color="#0369a1"
        ).pack(pady=10)
        
        # Controles de cola
        cola_controls = ctk.CTkFrame(cola_frame, fg_color="transparent")
        cola_controls.pack(pady=10)
        
        self.cola_entry = ctk.CTkEntry(
            cola_controls,
            placeholder_text="Valor para la cola",
            width=150
        )
        self.cola_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            cola_controls,
            text="➡️ ENQUEUE",
            command=self.simular_enqueue,
            width=100,
            fg_color="#059669"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            cola_controls,
            text="⬅️ DEQUEUE",
            command=self.simular_dequeue,
            width=100,
            fg_color="#dc2626"
        ).pack(side="left", padx=2)
        
        # Visualización de cola
        self.cola_visual = ctk.CTkTextbox(
            cola_frame,
            height=200,
            font=("Courier New", 12),
            fg_color="#e0f2fe"
        )
        self.cola_visual.pack(fill="both", expand=True, padx=10, pady=10)

        # PANEL DE LOGS (ABAJO)
        logs_frame = ctk.CTkFrame(main_frame)
        logs_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            logs_frame,
            text="📋 Log de Operaciones",
            font=("Arial Bold", 16)
        ).pack(pady=5)
        
        self.sim_logs = ctk.CTkTextbox(
            logs_frame,
            height=150,
            font=("Courier New", 10)
        )
        self.sim_logs.pack(fill="both", expand=True, padx=10, pady=10)

        # PANEL DE BOTONES
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="🔄 Actualizar Vista",
            command=self.actualizar_simulacion,
            fg_color="#3b82f6"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="🧹 Limpiar Todo",
            command=self.limpiar_simulacion,
            fg_color="#f59e0b"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="🎯 Auto-Demo",
            command=self.ejecutar_demo_automatico,
            fg_color="#7c3aed"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="❌ Cerrar",
            command=ventana.destroy,
            fg_color="#6b7280"
        ).pack(side="left", padx=10)

        # INICIALIZAR VISUALIZACIÓN
        self.actualizar_simulacion()
        self.log_simulacion("🎮 Simulador iniciado - ¡Prueba las operaciones!")
    
    def simular_push(self):
        """Simular operación PUSH en la pila"""
        try:
            valor = self.pila_entry.get().strip()
            if not valor:
                valor = f"Orden_{len(self.obtener_elementos_seguros(self.sistema.pila_ordenes)) + 1}"

            # CREAR ORDEN SIMULADA
            from datetime import datetime
            orden_sim = type('Orden', (), {
                'id': valor,
                'total': 50.0 + len(self.obtener_elementos_seguros(self.sistema.pila_ordenes)) * 10,
                'fecha': datetime.now(),
                'estado': 'Simulada'
            })()
            
            # Agregar a la pila real
            if hasattr(self.sistema.pila_ordenes, 'apilar'):
                self.sistema.pila_ordenes.apilar(orden_sim)
            elif hasattr(self.sistema.pila_ordenes, 'push'):
                self.sistema.pila_ordenes.push(orden_sim)
            
            self.log_simulacion(f"📚 PUSH: '{valor}' agregado al TOPE de la pila")
            self.actualizar_simulacion()
            self.pila_entry.delete(0, 'end')
            
        except Exception as e:
            self.log_simulacion(f"Error en PUSH: {e}")
    
    def simular_pop(self):
        """Simular operación POP en la pila"""
        try:
            # Obtener elemento del tope
            elemento = None
            if hasattr(self.sistema.pila_ordenes, 'desapilar'):
                elemento = self.sistema.pila_ordenes.desapilar()
            elif hasattr(self.sistema.pila_ordenes, 'pop'):
                elemento = self.sistema.pila_ordenes.pop()
            
            if elemento:
                self.log_simulacion(f"📚 POP: '{getattr(elemento, 'id', str(elemento))}' removido del TOPE")
            else:
                self.log_simulacion("📚 POP: La pila está vacía")
            
            self.actualizar_simulacion()
            
        except Exception as e:
            self.log_simulacion(f"Error en POP: {e}")

    def simular_enqueue(self):
        """Simular operación ENQUEUE en la cola"""
        try:
            valor = self.cola_entry.get().strip()
            if not valor:
                valor = f"Pago_{len(self.obtener_elementos_seguros(self.sistema.cola_pagos)) + 1}"
            
            # ✅ CREAR PAGO SIMULADO
            from datetime import datetime
            pago_sim = type('Pago', (), {
                'id_pago': valor,
                'monto': 25.0 + len(self.obtener_elementos_seguros(self.sistema.cola_pagos)) * 5,
                'fecha': datetime.now(),
                'metodo': 'Simulado',
                'estado': 'Pendiente'
            })()
            
            # Agregar a la cola real
            if hasattr(self.sistema.cola_pagos, 'encolar'):
                self.sistema.cola_pagos.encolar(pago_sim)
            elif hasattr(self.sistema.cola_pagos, 'enqueue'):
                self.sistema.cola_pagos.enqueue(pago_sim)
            
            self.log_simulacion(f"🏃 ENQUEUE: '{valor}' agregado al FINAL de la cola")
            self.actualizar_simulacion()
            self.cola_entry.delete(0, 'end')
            
        except Exception as e:
            self.log_simulacion(f"Error en ENQUEUE: {e}")
    
    def simular_dequeue(self):
        """Simular operación DEQUEUE en la cola"""
        try:
            # Obtener elemento del frente
            elemento = None
            if hasattr(self.sistema.cola_pagos, 'desencolar'):
                elemento = self.sistema.cola_pagos.desencolar()
            elif hasattr(self.sistema.cola_pagos, 'dequeue'):
                elemento = self.sistema.cola_pagos.dequeue()
            
            if elemento:
                self.log_simulacion(f"🏃 DEQUEUE: '{getattr(elemento, 'id_pago', str(elemento))}' removido del FRENTE")
            else:
                self.log_simulacion("🏃 DEQUEUE: La cola está vacía")
            
            self.actualizar_simulacion()
            
        except Exception as e:
            self.log_simulacion(f"Error en DEQUEUE: {e}")

    def actualizar_simulacion(self):
        """Actualizar visualización de la simulación"""
        try:
            # ACTUALIZAR PILA
            self.pila_visual.delete("1.0", tk.END)
            ordenes = self.obtener_elementos_seguros(self.sistema.pila_ordenes)
            
            pila_content = "╔══════ PILA (LIFO) ══════╗\n"
            pila_content += "║  ⬆️  TOPE (Último)      ║\n"
            pila_content += "╠═════════════════════════╣\n"
            
            if ordenes:
                for i, orden in enumerate(reversed(ordenes)):
                    pila_content += f"║ [{len(ordenes)-i:2d}] {getattr(orden, 'id', 'N/A'):<15} ║\n"
            else:
                pila_content += "║       (Vacía)           ║\n"
            
            pila_content += "╠═════════════════════════╣\n"
            pila_content += "║  ⬇️  BASE (Primero)     ║\n"
            pila_content += "╚═════════════════════════╝\n"
            
            self.pila_visual.insert("1.0", pila_content)

            # ACTUALIZAR COLA
            self.cola_visual.delete("1.0", tk.END)
            pagos = self.obtener_elementos_seguros(self.sistema.cola_pagos)
            
            cola_content = "╔══════ COLA (FIFO) ══════╗\n"
            cola_content += "║ ➡️ FRENTE (Sale primero) ║\n"
            cola_content += "╠═════════════════════════╣\n"
            
            if pagos:
                for i, pago in enumerate(pagos):
                    cola_content += f"║ [{i+1:2d}] {getattr(pago, 'id_pago', 'N/A'):<15} ║\n"
            else:
                cola_content += "║       (Vacía)           ║\n"
            
            cola_content += "╠═════════════════════════╣\n"
            cola_content += "║ ⬅️ FINAL (Entra último)  ║\n"
            cola_content += "╚═════════════════════════╝\n"
            
            self.cola_visual.insert("1.0", cola_content)

            # ACTUALIZAR ESTRUCTURAS PRINCIPALES
            self.actualizar_visualizaciones()
            
        except Exception as e:
            self.log_simulacion(f"Error actualizando simulación: {e}")

    def limpiar_simulacion(self):
        """Limpiar todas las estructuras de la simulación"""
        try:
            # Limpiar pila
            if hasattr(self.sistema.pila_ordenes, 'vaciar'):
                self.sistema.pila_ordenes.vaciar()
            elif hasattr(self.sistema.pila_ordenes, 'limpiar'):
                self.sistema.pila_ordenes.limpiar()
            
            # Limpiar cola
            if hasattr(self.sistema.cola_pagos, 'vaciar'):
                self.sistema.cola_pagos.vaciar()
            elif hasattr(self.sistema.cola_pagos, 'limpiar'):
                self.sistema.cola_pagos.limpiar()
            
            self.log_simulacion("🧹 Todas las estructuras limpiadas")
            self.actualizar_simulacion()
            
        except Exception as e:
            self.log_simulacion(f"Error limpiando: {e}")

    def ejecutar_demo_automatico(self):
        """Ejecutar demostración automática"""
        try:
            self.log_simulacion("🎯 Iniciando demostración automática...")
            
            # Simular secuencia de operaciones
            demos = [
                ("PUSH", "Orden_A"),
                ("PUSH", "Orden_B"), 
                ("ENQUEUE", "Pago_1"),
                ("PUSH", "Orden_C"),
                ("ENQUEUE", "Pago_2"),
                ("POP", ""),
                ("DEQUEUE", ""),
                ("ENQUEUE", "Pago_3")
            ]
            
            for i, (operacion, valor) in enumerate(demos):
                self.after(i * 1000, lambda op=operacion, val=valor: self.ejecutar_operacion_demo(op, val))
            
        except Exception as e:
            self.log_simulacion(f"Error en demo: {e}")

    def ejecutar_operacion_demo(self, operacion, valor):
        """Ejecutar una operación específica del demo"""
        try:
            if operacion == "PUSH":
                self.pila_entry.delete(0, 'end')
                self.pila_entry.insert(0, valor)
                self.simular_push()
            elif operacion == "POP":
                self.simular_pop()
            elif operacion == "ENQUEUE":
                self.cola_entry.delete(0, 'end')
                self.cola_entry.insert(0, valor)
                self.simular_enqueue()
            elif operacion == "DEQUEUE":
                self.simular_dequeue()
                
        except Exception as e:
            self.log_simulacion(f"Error en operación demo {operacion}: {e}")

    def log_simulacion(self, mensaje):
        """Agregar mensaje al log de simulación"""
        try:
            if hasattr(self, 'sim_logs'):
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_msg = f"[{timestamp}] {mensaje}\n"
                self.sim_logs.insert(tk.END, log_msg)
                self.sim_logs.see(tk.END)
        except Exception as e:
            print(f"Error en log simulación: {e}")
    
    def cerrar_ventana(self):
        """Cerrar la ventana de estructuras"""
        # CANCELAR AUTO-REFRESH ANTES DE CERRAR
        if self.refresh_job:
            self.after_cancel(self.refresh_job)

        # NOTIFICAR AL LOG
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 🚪 Cerrando visualizador de estructuras")

        # CERRAR VENTANA
        if hasattr(self.master, 'destroy'):
            self.master.destroy()
        else:
            self.destroy()
    
    def __del__(self):
        """Destructor para limpiar recursos"""
        try:
            if hasattr(self, 'refresh_job') and self.refresh_job:
                self.after_cancel(self.refresh_job)
        except:
            pass

# FUNCIÓN AUXILIAR PARA CREAR VENTANA INDEPENDIENTE
def mostrar_visualizador_estructuras(sistema_ecommerce):
    """Función para mostrar el visualizador en una ventana independiente"""
    try:
        ventana = ctk.CTkToplevel()
        ventana.title("📊 Visualizador de Estructuras de Datos")
        ventana.geometry("1200x800")
        ventana.minsize(800, 600)

        # CONFIGURAR ÍCONO Y TEMA
        ventana.resizable(True, True)
        
        visualizador = InterfazEstructuras(ventana, sistema_ecommerce)
        visualizador.pack(fill="both", expand=True, padx=10, pady=10)
        
        # CENTRAR VENTANA
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (1200 // 2)
        y = (ventana.winfo_screenheight() // 2) - (800 // 2)
        ventana.geometry(f"1200x800+{x}+{y}")
        
        return ventana
        
    except Exception as e:
        print(f"Error creando visualizador: {e}")
        import traceback
        traceback.print_exc()
        return None