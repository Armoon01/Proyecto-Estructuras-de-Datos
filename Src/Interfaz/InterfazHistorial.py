import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class InterfazHistorial(ctk.CTkFrame):
    """Interfaz para mostrar el historial de órdenes del cliente"""
    
    def __init__(self, parent, sistema_ecommerce, nombre_cliente, email_cliente, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.sistema = sistema_ecommerce
        self.nombre_cliente = nombre_cliente
        self.email_cliente = email_cliente
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.crear_interfaz()
        self.cargar_historial()
    
    def crear_interfaz(self):
        """Crear la interfaz del historial"""
        # Título
        titulo = ctk.CTkLabel(
            self, 
            text="📋 Historial de Órdenes", 
            font=("Arial Bold", 24),
            text_color=("#1f2937", "#f9fafb")
        )
        titulo.grid(row=0, column=0, pady=(10, 20), sticky="ew")
        
        # Información del cliente
        self.crear_info_cliente()
        
        # Lista de órdenes
        self.crear_lista_ordenes()
        
        # Resumen
        self.crear_resumen()
        
        # Botones
        self.crear_botones()
    
    def crear_info_cliente(self):
        """Crear sección de información del cliente"""
        frame_info = ctk.CTkFrame(self)
        frame_info.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 20))
        frame_info.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Información del cliente
        ctk.CTkLabel(
            frame_info,
            text=f"👤 Cliente: {self.nombre_cliente}",
            font=("Arial Bold", 16),
            text_color=("#1f2937", "#f9fafb")
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        ctk.CTkLabel(
            frame_info,
            text=f"📧 Email: {self.email_cliente}",
            font=("Arial", 14),
            text_color=("#4b5563", "#9ca3af")
        ).grid(row=0, column=1, padx=20, pady=15, sticky="w")
        
        # Contador de órdenes (se actualizará)
        self.lbl_total_ordenes = ctk.CTkLabel(
            frame_info,
            text="📦 Total de órdenes: 0",
            font=("Arial", 14),
            text_color=("#059669", "#10b981")
        )
        self.lbl_total_ordenes.grid(row=0, column=2, padx=20, pady=15, sticky="e")
    
    def crear_lista_ordenes(self):
        """Crear lista scrollable de órdenes"""
        # Frame contenedor
        frame_lista = ctk.CTkFrame(self)
        frame_lista.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 20))
        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_rowconfigure(1, weight=1)
        
        # Título de la sección
        titulo_lista = ctk.CTkLabel(
            frame_lista,
            text="📋 Lista de Órdenes",
            font=("Arial Bold", 18),
            text_color=("#1f2937", "#f9fafb")
        )
        titulo_lista.grid(row=0, column=0, pady=15, sticky="ew")
        
        # Scrollable frame para órdenes
        self.scroll_ordenes = ctk.CTkScrollableFrame(frame_lista)
        self.scroll_ordenes.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scroll_ordenes.grid_columnconfigure(0, weight=1)
    
    def crear_resumen(self):
        """Crear sección de resumen"""
        frame_resumen = ctk.CTkFrame(self)
        frame_resumen.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 20))
        frame_resumen.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Total gastado
        self.lbl_total_gastado = ctk.CTkLabel(
            frame_resumen,
            text="💰 Total gastado: $0.00",
            font=("Arial Bold", 16),
            text_color=("#059669", "#10b981")
        )
        self.lbl_total_gastado.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Promedio por orden
        self.lbl_promedio = ctk.CTkLabel(
            frame_resumen,
            text="📊 Promedio por orden: $0.00",
            font=("Arial", 14),
            text_color=("#4b5563", "#9ca3af")
        )
        self.lbl_promedio.grid(row=0, column=1, padx=20, pady=15)
        
        # Fecha última compra
        self.lbl_ultima_compra = ctk.CTkLabel(
            frame_resumen,
            text="📅 Última compra: N/A",
            font=("Arial", 14),
            text_color=("#4b5563", "#9ca3af")
        )
        self.lbl_ultima_compra.grid(row=0, column=2, padx=20, pady=15, sticky="e")
    
    def crear_botones(self):
        """Crear botones de acción"""
        frame_botones = ctk.CTkFrame(self)
        frame_botones.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 20))
        frame_botones.grid_columnconfigure((0, 1), weight=1)
        
        # Botón actualizar
        btn_actualizar = ctk.CTkButton(
            frame_botones,
            text="🔄 Actualizar",
            command=self.cargar_historial,
            font=("Arial Bold", 14),
            height=40,
            fg_color="#3b82f6",
            hover_color="#2563eb"
        )
        btn_actualizar.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        
        # Botón cerrar
        btn_cerrar = ctk.CTkButton(
            frame_botones,
            text="❌ Cerrar",
            command=self.master.destroy,
            font=("Arial Bold", 14),
            height=40,
            fg_color="#6b7280",
            hover_color="#4b5563"
        )
        btn_cerrar.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
    
    def cargar_historial(self):
        """Cargar y mostrar el historial de órdenes"""
        # Limpiar órdenes anteriores
        for widget in self.scroll_ordenes.winfo_children():
            widget.destroy()
        
        # Obtener órdenes del sistema
        ordenes_historial = []
        if hasattr(self.sistema, 'pila_ordenes'):
            ordenes_historial = self.sistema.pila_ordenes.obtener_elementos()
        
        if not ordenes_historial:
            # Mostrar mensaje de sin órdenes
            frame_vacio = ctk.CTkFrame(self.scroll_ordenes, fg_color="transparent")
            frame_vacio.grid(row=0, column=0, sticky="ew", pady=20)
            
            ctk.CTkLabel(
                frame_vacio,
                text="📭 No hay órdenes en el historial",
                font=("Arial", 16),
                text_color=("#6b7280", "#9ca3af")
            ).pack(pady=20)
            
            ctk.CTkLabel(
                frame_vacio,
                text="Las órdenes aparecerán aquí después de realizar compras",
                font=("Arial", 12),
                text_color=("#9ca3af", "#6b7280")
            ).pack()
        else:
            # Mostrar órdenes
            total_gastado = 0
            
            for i, orden in enumerate(reversed(ordenes_historial)):
                self.crear_card_orden(orden, i)
                if hasattr(orden, 'total'):
                    total_gastado += orden.total
            
            # Actualizar estadísticas
            self.actualizar_estadisticas(ordenes_historial, total_gastado)
    
    def crear_card_orden(self, orden, index):
        """Crear card para una orden individual"""
        # Frame principal de la orden
        frame_orden = ctk.CTkFrame(self.scroll_ordenes)
        frame_orden.grid(row=index, column=0, sticky="ew", pady=5, padx=5)
        frame_orden.grid_columnconfigure(1, weight=1)
        
        # Información principal
        frame_info = ctk.CTkFrame(frame_orden, fg_color="transparent")
        frame_info.grid(row=0, column=0, columnspan=3, sticky="ew", padx=15, pady=10)
        frame_info.grid_columnconfigure(1, weight=1)
        
        # ID de orden
        ctk.CTkLabel(
            frame_info,
            text=f"🏷️ Orden #{orden.id}",
            font=("Arial Bold", 16),
            text_color=("#1f2937", "#f9fafb")
        ).grid(row=0, column=0, sticky="w")
        
        # Estado
        estado_color = self.get_color_estado(orden.estado if hasattr(orden, 'estado') else 'Pendiente')
        ctk.CTkLabel(
            frame_info,
            text=f"📊 {orden.estado if hasattr(orden, 'estado') else 'Pendiente'}",
            font=("Arial Bold", 12),
            text_color=estado_color
        ).grid(row=0, column=1, padx=20)
        
        # Total
        ctk.CTkLabel(
            frame_info,
            text=f"💰 ${orden.total:.2f}" if hasattr(orden, 'total') else "💰 $0.00",
            font=("Arial Bold", 16),
            text_color=("#059669", "#10b981")
        ).grid(row=0, column=2, sticky="e")
        
        # Fecha
        fecha_str = orden.fecha.strftime('%d/%m/%Y %H:%M') if hasattr(orden, 'fecha') else 'N/A'
        ctk.CTkLabel(
            frame_info,
            text=f"📅 {fecha_str}",
            font=("Arial", 12),
            text_color=("#4b5563", "#9ca3af")
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))
        
        # Productos
        if hasattr(orden, 'productos') and orden.productos:
            frame_productos = ctk.CTkFrame(frame_orden, fg_color="transparent")
            frame_productos.grid(row=1, column=0, columnspan=3, sticky="ew", padx=15, pady=(0, 10))
            
            productos_text = "🛍️ Productos: "
            if len(orden.productos) <= 3:
                # Mostrar todos los productos si son pocos
                nombres = []
                for item in orden.productos:
                    if hasattr(item, 'producto'):
                        nombres.append(f"{item.producto.nombre} (x{item.cantidad})")
                    else:
                        nombres.append(item.nombre)
                productos_text += ", ".join(nombres)
            else:
                # Mostrar solo algunos productos si son muchos
                productos_text += f"{len(orden.productos)} productos"
            
            ctk.CTkLabel(
                frame_productos,
                text=productos_text,
                font=("Arial", 11),
                text_color=("#6b7280", "#9ca3af"),
                wraplength=600
            ).pack(anchor="w")
        
        # Fechas de entrega y envío
        if hasattr(orden, 'fecha_entrega') or hasattr(orden, 'fecha_envio'):
            frame_fechas = ctk.CTkFrame(frame_orden, fg_color="transparent")
            frame_fechas.grid(row=2, column=0, columnspan=3, sticky="ew", padx=15, pady=(0, 10))
            frame_fechas.grid_columnconfigure((0, 1), weight=1)
            
            if hasattr(orden, 'fecha_envio'):
                envio_str = orden.fecha_envio.strftime('%d/%m/%Y') if orden.fecha_envio else 'N/A'
                ctk.CTkLabel(
                    frame_fechas,
                    text=f"📦 Envío: {envio_str}",
                    font=("Arial", 10),
                    text_color=("#6b7280", "#9ca3af")
                ).grid(row=0, column=0, sticky="w")
            
            if hasattr(orden, 'fecha_entrega'):
                entrega_str = orden.fecha_entrega.strftime('%d/%m/%Y') if orden.fecha_entrega else 'N/A'
                ctk.CTkLabel(
                    frame_fechas,
                    text=f"🏠 Entrega: {entrega_str}",
                    font=("Arial", 10),
                    text_color=("#6b7280", "#9ca3af")
                ).grid(row=0, column=1, sticky="w")
    
    def get_color_estado(self, estado):
        """Obtener color según el estado de la orden"""
        colores = {
            "Pendiente": ("#f59e0b", "#fbbf24"),
            "Procesando": ("#3b82f6", "#60a5fa"),
            "Enviado": ("#8b5cf6", "#a78bfa"),
            "Entregado": ("#059669", "#10b981"),
            "Cancelado": ("#dc2626", "#ef4444")
        }
        return colores.get(estado, ("#6b7280", "#9ca3af"))
    
    def actualizar_estadisticas(self, ordenes, total_gastado):
        """Actualizar las estadísticas del historial"""
        # Total de órdenes
        self.lbl_total_ordenes.configure(text=f"📦 Total de órdenes: {len(ordenes)}")
        
        # Total gastado
        self.lbl_total_gastado.configure(text=f"💰 Total gastado: ${total_gastado:.2f}")
        
        # Promedio por orden
        promedio = total_gastado / len(ordenes) if ordenes else 0
        self.lbl_promedio.configure(text=f"📊 Promedio por orden: ${promedio:.2f}")
        
        # Última compra
        if ordenes:
            ultima_orden = max(ordenes, key=lambda o: o.fecha if hasattr(o, 'fecha') else datetime.min)
            if hasattr(ultima_orden, 'fecha'):
                fecha_str = ultima_orden.fecha.strftime('%d/%m/%Y')
                self.lbl_ultima_compra.configure(text=f"📅 Última compra: {fecha_str}")
        else:
            self.lbl_ultima_compra.configure(text="📅 Última compra: N/A")
