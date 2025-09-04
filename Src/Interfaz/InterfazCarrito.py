import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
import os
import sys

def obtener_directorio_proyecto():
    """Obtener directorio base del proyecto de manera robusta"""
    try:
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        proyecto_dir = os.path.dirname(os.path.dirname(current_dir))
        if os.path.exists(os.path.join(proyecto_dir, 'Src')):
            return proyecto_dir
        
        cwd = os.getcwd()
        if 'Proyecto-Estructuras-de-Datos' in cwd:
            parts = cwd.split(os.sep)
            for i, part in enumerate(parts):
                if 'Proyecto-Estructuras-de-Datos' in part:
                    proyecto_dir = os.sep.join(parts[:i+1])
                    if os.path.exists(os.path.join(proyecto_dir, 'Src')):
                        return proyecto_dir
        
        for path in sys.path:
            if 'Proyecto-Estructuras-de-Datos' in path:
                if os.path.exists(os.path.join(path, 'Src')):
                    return path
                parent = os.path.dirname(path)
                if os.path.exists(os.path.join(parent, 'Src')):
                    return parent
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
        if os.path.exists(os.path.join(base_dir, 'Src')):
            return base_dir
            
        return os.getcwd()
        
    except Exception as e:
        print(f"Error determinando directorio del proyecto: {e}")
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def obtener_directorio_imagenes(tipo="productos"):
    """Obtener directorio de imágenes de manera robusta"""
    try:
        proyecto_dir = obtener_directorio_proyecto()
        
        rutas_posibles = [
            os.path.join(proyecto_dir, 'Src', 'Images', tipo),
            os.path.join(proyecto_dir, 'Images', tipo),
            os.path.join(proyecto_dir, 'Src', 'Interfaz', 'Images', tipo),
            os.path.join(proyecto_dir, 'assets', tipo),
            os.path.join(proyecto_dir, 'static', tipo)
        ]
        
        for ruta in rutas_posibles:
            if os.path.exists(ruta):
                return ruta
        
        ruta_estandar = os.path.join(proyecto_dir, 'Src', 'Images', tipo)
        os.makedirs(ruta_estandar, exist_ok=True)
        return ruta_estandar
        
    except Exception as e:
        print(f"Error obteniendo directorio de imágenes: {e}")
        return None

# Configurar rutas
BASE_DIR = obtener_directorio_proyecto()
IMAGES_DIR = obtener_directorio_imagenes("productos")

class ItemCarrito(ctk.CTkFrame):
    """Widget individual para cada item del carrito"""
    
    def __init__(self, master, item_carrito, carrito, on_update_callback=None, **kwargs):
        super().__init__(master, corner_radius=15, border_width=1, 
                         border_color="#e5e7eb", fg_color="white", **kwargs)
        
        self.item_carrito = item_carrito
        self.carrito = carrito
        self.on_update_callback = on_update_callback
        self._imagen_widget = None
        self._photo_image = None
        
        # Configurar tamaño
        self.configure(height=140)
        self.pack_propagate(False)
        
        self.crear_contenido()
    
    def crear_contenido(self):
        """Crear el contenido del item del carrito"""
        try:
            # Frame principal horizontal
            main_frame = ctk.CTkFrame(self, fg_color="transparent")
            main_frame.pack(fill="both", expand=True, padx=15, pady=10)
            
            # 1. IMAGEN DEL PRODUCTO (Izquierda)
            self.crear_imagen_producto(main_frame)
            
            # 2. INFORMACIÓN DEL PRODUCTO (Centro)
            self.crear_info_producto(main_frame)
            
            # 3. CONTROLES DE CANTIDAD (Centro-Derecha) 
            self.crear_controles_cantidad(main_frame)
            
            # 4. PRECIO Y ELIMINAR (Derecha)
            self.crear_panel_derecho(main_frame)
            
        except Exception as e:
            print(f"Error creando contenido item carrito: {e}")
            self.crear_contenido_fallback()
    
    def crear_imagen_producto(self, parent):
        """Crear widget de imagen del producto"""
        try:
            # Frame para imagen
            img_frame = ctk.CTkFrame(parent, width=100, height=100, 
                                   corner_radius=10, fg_color="#f8f9fa")
            img_frame.pack(side="left", padx=(0, 15))
            img_frame.pack_propagate(False)
            
            # Intentar cargar imagen
            imagen = self.cargar_imagen_producto()
            
            if imagen:
                self._imagen_widget = tk.Label(img_frame, image=imagen, bg="#f8f9fa", bd=0)
                self._imagen_widget.image = imagen  # Mantener referencia
                self._imagen_widget.pack(expand=True)
            else:
                # Fallback con texto
                placeholder = ctk.CTkLabel(
                    img_frame, 
                    text="📦", 
                    font=("Arial", 32),
                    text_color="#6b7280"
                )
                placeholder.pack(expand=True)
                
        except Exception as e:
            print(f"Error creando imagen: {e}")
            # Crear placeholder simple
            placeholder_frame = ctk.CTkFrame(parent, width=100, height=100, 
                                           corner_radius=10, fg_color="#f3f4f6")
            placeholder_frame.pack(side="left", padx=(0, 15))
            placeholder_frame.pack_propagate(False)
            
            placeholder_label = ctk.CTkLabel(
                placeholder_frame, text="📦", font=("Arial", 24), text_color="#9ca3af"
            )
            placeholder_label.pack(expand=True)
    
    def cargar_imagen_producto(self):
        """Cargar imagen del producto de manera robusta"""
        try:
            if not IMAGES_DIR or not os.path.exists(IMAGES_DIR):
                return None
            
            # Obtener nombre de imagen
            imagen_nombre = None
            if hasattr(self.item_carrito.producto, 'imagen_ruta') and self.item_carrito.producto.imagen_ruta:
                imagen_nombre = os.path.basename(self.item_carrito.producto.imagen_ruta)
            elif hasattr(self.item_carrito.producto, 'imagen') and self.item_carrito.producto.imagen:
                imagen_nombre = self.item_carrito.producto.imagen
            
            if not imagen_nombre:
                return None
            
            # Buscar archivo de imagen
            ruta_imagen = self.buscar_imagen(IMAGES_DIR, imagen_nombre)
            if not ruta_imagen:
                return None
            
            # Cargar y procesar imagen
            img_pil = Image.open(ruta_imagen)
            img_pil = self.procesar_imagen(img_pil, (80, 80))
            
            # Crear PhotoImage
            self._photo_image = ImageTk.PhotoImage(img_pil)
            return self._photo_image
            
        except Exception as e:
            print(f"Error cargando imagen del producto: {e}")
            return None
    
    def buscar_imagen(self, directorio, nombre_imagen):
        """Buscar archivo de imagen con múltiples estrategias"""
        try:
            # Extensiones soportadas
            extensiones = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
            
            # Buscar archivo exacto
            ruta_exacta = os.path.join(directorio, nombre_imagen)
            if os.path.exists(ruta_exacta):
                return ruta_exacta
            
            # Buscar sin extensión y agregar extensiones
            nombre_sin_ext = os.path.splitext(nombre_imagen)[0]
            for ext in extensiones:
                ruta_test = os.path.join(directorio, nombre_sin_ext + ext)
                if os.path.exists(ruta_test):
                    return ruta_test
            
            # Buscar imagen por defecto
            for nombre_default in ['producto_default.png', 'default.png', 'placeholder.png']:
                ruta_default = os.path.join(directorio, nombre_default)
                if os.path.exists(ruta_default):
                    return ruta_default
            
            return None
            
        except Exception as e:
            print(f"Error buscando imagen: {e}")
            return None
    
    def procesar_imagen(self, imagen, tamaño_objetivo):
        """Procesar imagen para el tamaño correcto"""
        try:
            # Convertir a RGB si es necesario
            if imagen.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', imagen.size, (255, 255, 255))
                if imagen.mode == 'RGBA':
                    background.paste(imagen, mask=imagen.split()[-1])
                else:
                    background.paste(imagen, mask=imagen.split()[-1])
                imagen = background
            elif imagen.mode != 'RGB':
                imagen = imagen.convert('RGB')
            
            # Redimensionar manteniendo proporción
            ancho_orig, alto_orig = imagen.size
            ancho_obj, alto_obj = tamaño_objetivo
            
            ratio = min(ancho_obj / ancho_orig, alto_obj / alto_orig)
            nuevo_ancho = int(ancho_orig * ratio)
            nuevo_alto = int(alto_orig * ratio)
            
            imagen_redim = imagen.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
            
            # Centrar en canvas si es necesario
            if nuevo_ancho < ancho_obj or nuevo_alto < alto_obj:
                canvas = Image.new('RGB', tamaño_objetivo, (248, 249, 250))
                offset_x = (ancho_obj - nuevo_ancho) // 2
                offset_y = (alto_obj - nuevo_alto) // 2
                canvas.paste(imagen_redim, (offset_x, offset_y))
                return canvas
            
            return imagen_redim
            
        except Exception as e:
            print(f"Error procesando imagen: {e}")
            return imagen.resize(tamaño_objetivo, Image.Resampling.LANCZOS)
    
    def crear_info_producto(self, parent):
        """Crear información del producto"""
        try:
            info_frame = ctk.CTkFrame(parent, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
            
            # Nombre del producto
            nombre_texto = self.item_carrito.producto.nombre
            if len(nombre_texto) > 35:
                nombre_texto = nombre_texto[:35] + "..."
            
            nombre_label = ctk.CTkLabel(
                info_frame,
                text=nombre_texto,
                font=("Arial", 16, "bold"),
                text_color="#1f2937",
                anchor="w"
            )
            nombre_label.pack(anchor="w", pady=(10, 5))
            
            # Descripción del producto
            descripcion = getattr(self.item_carrito.producto, 'descripcion', 'Sin descripción disponible')
            if len(descripcion) > 60:
                descripcion = descripcion[:60] + "..."
            
            desc_label = ctk.CTkLabel(
                info_frame,
                text=descripcion,
                font=("Arial", 12),
                text_color="#6b7280",
                anchor="w",
                wraplength=250
            )
            desc_label.pack(anchor="w", pady=(0, 5))
            
            # Precio unitario
            precio_unitario_label = ctk.CTkLabel(
                info_frame,
                text=f"Precio unitario: ${self.item_carrito.producto.precio:.2f}",
                font=("Arial", 11),
                text_color="#059669",
                anchor="w"
            )
            precio_unitario_label.pack(anchor="w", pady=(0, 10))
            
        except Exception as e:
            print(f"Error creando info producto: {e}")
    
    def crear_controles_cantidad(self, parent):
        """Crear controles de cantidad con diseño moderno"""
        try:
            cantidad_frame = ctk.CTkFrame(parent, fg_color="transparent")
            cantidad_frame.pack(side="left", padx=(0, 15))
            
            # Label "Cantidad"
            cantidad_titulo = ctk.CTkLabel(
                cantidad_frame,
                text="Cantidad:",
                font=("Arial", 12, "bold"),
                text_color="#374151"
            )
            cantidad_titulo.pack(pady=(15, 5))
            
            # Frame para controles de cantidad
            controles_frame = ctk.CTkFrame(cantidad_frame, fg_color="transparent")
            controles_frame.pack(pady=(0, 10))
            
            # Botón disminuir
            self.btn_menos = ctk.CTkButton(
                controles_frame,
                text="−",
                width=35,
                height=35,
                font=("Arial", 18, "bold"),
                command=self.disminuir_cantidad,
                fg_color="#ef4444",
                hover_color="#dc2626",
                corner_radius=8
            )
            self.btn_menos.pack(side="left")
            
            # Display de cantidad
            self.cantidad_label = ctk.CTkLabel(
                controles_frame,
                text=str(self.item_carrito.cantidad),
                font=("Arial", 16, "bold"),
                text_color="#1f2937",
                width=50
            )
            self.cantidad_label.pack(side="left", padx=10)
            
            # Botón aumentar
            self.btn_mas = ctk.CTkButton(
                controles_frame,
                text="+",
                width=35,
                height=35,
                font=("Arial", 16, "bold"),
                command=self.aumentar_cantidad,
                fg_color="#10b981",
                hover_color="#059669",
                corner_radius=8
            )
            self.btn_mas.pack(side="left")
            
            # Verificar límites de stock
            self.actualizar_botones_cantidad()
            
        except Exception as e:
            print(f"Error creando controles cantidad: {e}")
    
    def crear_panel_derecho(self, parent):
        """Crear panel derecho con precio total y botón eliminar"""
        try:
            derecho_frame = ctk.CTkFrame(parent, fg_color="transparent", width=120)
            derecho_frame.pack(side="right", fill="y")
            derecho_frame.pack_propagate(False)
            
            # Precio total
            precio_total = self.item_carrito.cantidad * self.item_carrito.producto.precio
            precio_frame = ctk.CTkFrame(derecho_frame, fg_color="#ecfdf5", 
                                      corner_radius=8, border_width=1, border_color="#10b981")
            precio_frame.pack(pady=(15, 10), padx=5, fill="x")
            
            precio_label = ctk.CTkLabel(
                precio_frame,
                text="Total:",
                font=("Arial", 11),
                text_color="#374151"
            )
            precio_label.pack(pady=(8, 2))
            
            self.precio_total_label = ctk.CTkLabel(
                precio_frame,
                text=f"${precio_total:.2f}",
                font=("Arial", 16, "bold"),
                text_color="#059669"
            )
            self.precio_total_label.pack(pady=(0, 8))
            
            # Botón eliminar con diseño mejorado
            self.btn_eliminar = ctk.CTkButton(
                derecho_frame,
                text="🗑️ Eliminar",
                width=110,
                height=40,
                font=("Arial", 12, "bold"),
                command=self.eliminar_item,
                fg_color="#fca5a5",
                hover_color="#f87171",
                text_color="#7f1d1d",
                corner_radius=10
            )
            self.btn_eliminar.pack(pady=(0, 15), padx=5)
            
        except Exception as e:
            print(f"Error creando panel derecho: {e}")
    
    def aumentar_cantidad(self):
        """Aumentar cantidad del producto"""
        try:
            if self.item_carrito.cantidad < self.item_carrito.producto.stock:
                self.item_carrito.cantidad += 1
                self.actualizar_display()
                
                if self.on_update_callback:
                    self.on_update_callback()
            else:
                print("No se puede agregar más, stock insuficiente")
                
        except Exception as e:
            print(f"Error aumentando cantidad: {e}")
    
    def disminuir_cantidad(self):
        """Disminuir cantidad del producto"""
        try:
            if self.item_carrito.cantidad > 1:
                self.item_carrito.cantidad -= 1
                self.actualizar_display()
                
                if self.on_update_callback:
                    self.on_update_callback()
            else:
                # Si la cantidad es 1, eliminar el item
                self.eliminar_item()
                
        except Exception as e:
            print(f"Error disminuyendo cantidad: {e}")
    
    def eliminar_item(self):
        """Eliminar item completo del carrito"""
        try:
            # Eliminar todas las instancias del producto del carrito
            producto_id = self.item_carrito.producto.id
            self.carrito.eliminar_producto_completo(producto_id)
            
            if self.on_update_callback:
                self.on_update_callback()
                
            print(f"Producto eliminado del carrito: {self.item_carrito.producto.nombre}")
            
        except Exception as e:
            print(f"Error eliminando item: {e}")
    
    def actualizar_display(self):
        """Actualizar displays de cantidad y precio"""
        try:
            # Actualizar cantidad
            if hasattr(self, 'cantidad_label'):
                self.cantidad_label.configure(text=str(self.item_carrito.cantidad))
            
            # Actualizar precio total
            if hasattr(self, 'precio_total_label'):
                precio_total = self.item_carrito.cantidad * self.item_carrito.producto.precio
                self.precio_total_label.configure(text=f"${precio_total:.2f}")
            
            # Actualizar estado de botones
            self.actualizar_botones_cantidad()
            
        except Exception as e:
            print(f"Error actualizando display: {e}")
    
    def actualizar_botones_cantidad(self):
        """Actualizar estado de botones según stock y cantidad"""
        try:
            if hasattr(self, 'btn_mas'):
                # Deshabilitar botón + si se alcanzó el stock máximo
                if self.item_carrito.cantidad >= self.item_carrito.producto.stock:
                    self.btn_mas.configure(state="disabled", fg_color="#9ca3af")
                else:
                    self.btn_mas.configure(state="normal", fg_color="#10b981")
            
            if hasattr(self, 'btn_menos'):
                # El botón - siempre está habilitado (elimina si cantidad = 1)
                if self.item_carrito.cantidad <= 1:
                    self.btn_menos.configure(text="🗑️", fg_color="#fca5a5")
                else:
                    self.btn_menos.configure(text="−", fg_color="#ef4444")
                    
        except Exception as e:
            print(f"Error actualizando botones: {e}")
    
    def crear_contenido_fallback(self):
        """Crear contenido básico en caso de error"""
        try:
            error_label = ctk.CTkLabel(
                self,
                text=f"Error cargando: {self.item_carrito.producto.nombre}",
                font=("Arial", 14),
                text_color="#dc2626"
            )
            error_label.pack(pady=20)
            
        except Exception as e:
            print(f"Error crítico en fallback: {e}")
    
    def destroy(self):
        """Limpiar referencias antes de destruir"""
        try:
            if hasattr(self, '_photo_image'):
                self._photo_image = None
            if hasattr(self, '_imagen_widget'):
                self._imagen_widget = None
        except Exception as e:
            print(f"Error limpiando ItemCarrito: {e}")
        finally:
            super().destroy()

class InterfazCarrito(ctk.CTkFrame):
    """Interfaz principal del carrito de compras mejorada"""
    
    def __init__(self, master, carrito, **kwargs):
        super().__init__(master, **kwargs)
        
        self.carrito = carrito
        self.items_widgets = []
        
        # Configurar interfaz
        self.configure(fg_color="#f8f9fa")
        
        self.crear_interfaz()
        self.actualizar_carrito()
    
    def crear_interfaz(self):
        """Crear la interfaz principal del carrito"""
        try:
            # Header del carrito
            self.crear_header()
            
            # Contenedor principal con scroll
            self.crear_contenedor_scroll()
            
            # Footer con resumen y acciones
            self.crear_footer()
            
        except Exception as e:
            print(f"Error creando interfaz carrito: {e}")
    
    def crear_header(self):
        """Crear header del carrito"""
        try:
            header_frame = ctk.CTkFrame(self, height=80, fg_color="#1e40af")
            header_frame.pack(fill="x", padx=15, pady=(15, 10))
            header_frame.pack_propagate(False)
            
            # Contenedor del header
            header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
            header_content.pack(expand=True, fill="both", padx=20, pady=15)
            
            # Título
            titulo = ctk.CTkLabel(
                header_content,
                text="🛒 Mi Carrito de Compras",
                font=("Arial", 26, "bold"),
                text_color="white"
            )
            titulo.pack(side="left")
            
            # Contador de items
            self.contador_items = ctk.CTkLabel(
                header_content,
                text="0 productos",
                font=("Arial", 14),
                text_color="#bfdbfe"
            )
            self.contador_items.pack(side="right", pady=(5, 0))
            
        except Exception as e:
            print(f"Error creando header: {e}")
    
    def crear_contenedor_scroll(self):
        """Crear contenedor scrollable para items"""
        try:
            # Frame scrollable para los items
            self.scroll_frame = ctk.CTkScrollableFrame(
                self,
                label_text="Productos en el Carrito",
                label_font=("Arial", 16, "bold"),
                label_fg_color="#3b82f6",
                label_text_color="white"
            )
            self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
            
            # Contenedor para los items
            self.items_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            self.items_container.pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            print(f"Error creando contenedor scroll: {e}")
    
    def crear_footer(self):
        """Crear footer con resumen y acciones"""
        try:
            # Frame principal del footer
            footer_frame = ctk.CTkFrame(self, height=120, fg_color="#ffffff", 
                                      border_width=2, border_color="#e5e7eb")
            footer_frame.pack(fill="x", padx=15, pady=(0, 15))
            footer_frame.pack_propagate(False)
            
            # Contenedor del footer
            footer_content = ctk.CTkFrame(footer_frame, fg_color="transparent")
            footer_content.pack(expand=True, fill="both", padx=20, pady=15)
            
            # Panel izquierdo - Resumen
            self.crear_panel_resumen(footer_content)
            
            # Panel derecho - Acciones
            self.crear_panel_acciones(footer_content)
            
        except Exception as e:
            print(f"Error creando footer: {e}")
    
    def crear_panel_resumen(self, parent):
        """Crear panel de resumen del carrito"""
        try:
            resumen_frame = ctk.CTkFrame(parent, fg_color="#f0f9ff", 
                                       corner_radius=10, border_width=1, border_color="#0ea5e9")
            resumen_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
            
            # Título del resumen
            titulo_resumen = ctk.CTkLabel(
                resumen_frame,
                text="📊 Resumen del Pedido",
                font=("Arial", 16, "bold"),
                text_color="#0c4a6e"
            )
            titulo_resumen.pack(pady=(15, 10))
            
            # Frame para estadísticas
            stats_frame = ctk.CTkFrame(resumen_frame, fg_color="transparent")
            stats_frame.pack(pady=(0, 15))
            
            # Cantidad total de items
            self.total_items_label = ctk.CTkLabel(
                stats_frame,
                text="Productos: 0",
                font=("Arial", 12),
                text_color="#374151"
            )
            self.total_items_label.pack(side="left", padx=15)
            
            # Separador visual
            separador = ctk.CTkLabel(stats_frame, text="•", text_color="#9ca3af")
            separador.pack(side="left")
            
            # Total a pagar
            self.total_precio_label = ctk.CTkLabel(
                stats_frame,
                text="Total: $0.00",
                font=("Arial", 14, "bold"),
                text_color="#059669"
            )
            self.total_precio_label.pack(side="left", padx=15)
            
        except Exception as e:
            print(f"Error creando panel resumen: {e}")
    
    def crear_panel_acciones(self, parent):
        """Crear panel de acciones del carrito"""
        try:
            acciones_frame = ctk.CTkFrame(parent, fg_color="transparent")
            acciones_frame.pack(side="right")
            
            # Botón limpiar carrito
            self.btn_limpiar = ctk.CTkButton(
                acciones_frame,
                text="🗑️ Vaciar Carrito",
                width=140,
                height=40,
                font=("Arial", 12, "bold"),
                command=self.limpiar_carrito,
                fg_color="#fca5a5",
                hover_color="#f87171",
                text_color="#7f1d1d",
                corner_radius=10
            )
            self.btn_limpiar.pack(side="left", padx=(0, 10))
            
            # Botón continuar comprando
            self.btn_continuar = ctk.CTkButton(
                acciones_frame,
                text="🛍️ Seguir Comprando",
                width=150,
                height=40,
                font=("Arial", 12, "bold"),
                command=self.continuar_comprando,
                fg_color="#6366f1",
                hover_color="#4f46e5",
                corner_radius=10
            )
            self.btn_continuar.pack(side="left", padx=(0, 10))
            
            # Botón proceder al checkout
            self.btn_checkout = ctk.CTkButton(
                acciones_frame,
                text="💳 Proceder al Pago",
                width=150,
                height=40,
                font=("Arial", 12, "bold"),
                command=self.proceder_checkout,
                fg_color="#059669",
                hover_color="#047857",
                corner_radius=10
            )
            self.btn_checkout.pack(side="left")
            
        except Exception as e:
            print(f"Error creando panel acciones: {e}")
    
    def actualizar_carrito(self):
        """Actualizar visualización del carrito"""
        try:
            # Limpiar items anteriores
            self.limpiar_items_anteriores()
            
            # Obtener items del carrito
            items = self.carrito.obtener_items_agrupados()
            
            if not items:
                self.mostrar_carrito_vacio()
            else:
                self.mostrar_items_carrito(items)
            
            # Actualizar resumen
            self.actualizar_resumen()
            
        except Exception as e:
            print(f"Error actualizando carrito: {e}")
    
    def limpiar_items_anteriores(self):
        """Limpiar widgets de items anteriores"""
        try:
            for item_widget in self.items_widgets:
                try:
                    if item_widget.winfo_exists():
                        item_widget.destroy()
                except Exception as e:
                    print(f"Error limpiando item widget: {e}")
            
            self.items_widgets.clear()
            
            # Limpiar contenedor
            for widget in self.items_container.winfo_children():
                try:
                    widget.destroy()
                except Exception as e:
                    print(f"Error limpiando widget contenedor: {e}")
            
        except Exception as e:
            print(f"Error limpiando items anteriores: {e}")
    
    def mostrar_carrito_vacio(self):
        """Mostrar mensaje cuando el carrito está vacío"""
        try:
            # Frame para mensaje vacío
            vacio_frame = ctk.CTkFrame(self.items_container, fg_color="#f9fafb", 
                                     corner_radius=15, border_width=2, border_color="#e5e7eb")
            vacio_frame.pack(fill="both", expand=True, padx=20, pady=50)
            
            # Icono grande
            icono_label = ctk.CTkLabel(
                vacio_frame,
                text="🛒",
                font=("Arial", 64),
                text_color="#9ca3af"
            )
            icono_label.pack(pady=(50, 20))
            
            # Mensaje principal
            mensaje_label = ctk.CTkLabel(
                vacio_frame,
                text="Tu carrito está vacío",
                font=("Arial", 24, "bold"),
                text_color="#374151"
            )
            mensaje_label.pack(pady=(0, 10))
            
            # Submensaje
            submensaje_label = ctk.CTkLabel(
                vacio_frame,
                text="¡Explora nuestros productos y encuentra algo que te guste!",
                font=("Arial", 14),
                text_color="#6b7280"
            )
            submensaje_label.pack(pady=(0, 30))
            
            # Botón para ir a compras
            btn_explorar = ctk.CTkButton(
                vacio_frame,
                text="🛍️ Explorar Productos",
                width=200,
                height=45,
                font=("Arial", 14, "bold"),
                command=self.continuar_comprando,
                fg_color="#3b82f6",
                hover_color="#2563eb",
                corner_radius=15
            )
            btn_explorar.pack(pady=(0, 50))
            
        except Exception as e:
            print(f"Error mostrando carrito vacío: {e}")
    
    def mostrar_items_carrito(self, items):
        """Mostrar items del carrito"""
        try:
            for item in items:
                # Crear widget para cada item
                item_widget = ItemCarrito(
                    self.items_container,
                    item,
                    self.carrito,
                    on_update_callback=self.actualizar_carrito
                )
                item_widget.pack(fill="x", padx=10, pady=8)
                
                # Agregar a lista de widgets
                self.items_widgets.append(item_widget)
            
            print(f"Mostrando {len(items)} items en el carrito")
            
        except Exception as e:
            print(f"Error mostrando items del carrito: {e}")
    
    def actualizar_resumen(self):
        """Actualizar resumen del carrito"""
        try:
            # Obtener estadísticas del carrito
            cantidad_total = self.carrito.obtener_cantidad_items()
            precio_total = self.carrito.calcular_total()
            
            # Actualizar labels
            if hasattr(self, 'contador_items'):
                texto_items = f"{cantidad_total} producto{'s' if cantidad_total != 1 else ''}"
                self.contador_items.configure(text=texto_items)
            
            if hasattr(self, 'total_items_label'):
                self.total_items_label.configure(text=f"Productos: {cantidad_total}")
            
            if hasattr(self, 'total_precio_label'):
                self.total_precio_label.configure(text=f"Total: ${precio_total:.2f}")
            
            # Habilitar/deshabilitar botón de checkout
            if hasattr(self, 'btn_checkout'):
                if cantidad_total > 0:
                    self.btn_checkout.configure(state="normal", fg_color="#059669")
                else:
                    self.btn_checkout.configure(state="disabled", fg_color="#9ca3af")
            
            # Habilitar/deshabilitar botón limpiar
            if hasattr(self, 'btn_limpiar'):
                if cantidad_total > 0:
                    self.btn_limpiar.configure(state="normal", fg_color="#fca5a5")
                else:
                    self.btn_limpiar.configure(state="disabled", fg_color="#d1d5db")
            
        except Exception as e:
            print(f"Error actualizando resumen: {e}")
    
    def limpiar_carrito(self):
        """Limpiar todos los productos del carrito"""
        try:
            if self.carrito.obtener_cantidad_items() == 0:
                return
            
            # Crear ventana de confirmación
            self.mostrar_confirmacion_limpiar()
            
        except Exception as e:
            print(f"Error limpiando carrito: {e}")
    
    def mostrar_confirmacion_limpiar(self):
        """Mostrar ventana de confirmación para limpiar carrito"""
        try:
            # Crear ventana modal
            confirmacion = ctk.CTkToplevel(self)
            confirmacion.title("Confirmar acción")
            confirmacion.geometry("400x200")
            confirmacion.resizable(False, False)
            confirmacion.transient(self.winfo_toplevel())
            confirmacion.grab_set()
            
            # Centrar ventana
            confirmacion.geometry("+%d+%d" % (
                self.winfo_rootx() + 50,
                self.winfo_rooty() + 50
            ))
            
            # Contenido de la confirmación
            contenido_frame = ctk.CTkFrame(confirmacion, fg_color="transparent")
            contenido_frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            # Icono de advertencia
            icono_label = ctk.CTkLabel(
                contenido_frame,
                text="⚠️",
                font=("Arial", 32),
                text_color="#f59e0b"
            )
            icono_label.pack(pady=(10, 15))
            
            # Mensaje
            mensaje_label = ctk.CTkLabel(
                contenido_frame,
                text="¿Estás seguro de que quieres vaciar tu carrito?",
                font=("Arial", 14, "bold"),
                text_color="#374151"
            )
            mensaje_label.pack(pady=(0, 5))
            
            submensaje_label = ctk.CTkLabel(
                contenido_frame,
                text="Esta acción no se puede deshacer.",
                font=("Arial", 12),
                text_color="#6b7280"
            )
            submensaje_label.pack(pady=(0, 20))
            
            # Botones
            botones_frame = ctk.CTkFrame(contenido_frame, fg_color="transparent")
            botones_frame.pack()
            
            btn_cancelar = ctk.CTkButton(
                botones_frame,
                text="Cancelar",
                width=100,
                command=confirmacion.destroy,
                fg_color="#6b7280",
                hover_color="#4b5563"
            )
            btn_cancelar.pack(side="left", padx=(0, 10))
            
            btn_confirmar = ctk.CTkButton(
                botones_frame,
                text="Sí, vaciar",
                width=100,
                command=lambda: self.confirmar_limpiar_carrito(confirmacion),
                fg_color="#dc2626",
                hover_color="#b91c1c"
            )
            btn_confirmar.pack(side="left")
            
        except Exception as e:
            print(f"Error mostrando confirmación: {e}")
    
    def confirmar_limpiar_carrito(self, ventana_confirmacion):
        """Confirmar y ejecutar limpieza del carrito"""
        try:
            # Cerrar ventana de confirmación
            ventana_confirmacion.destroy()
            
            # Limpiar carrito
            self.carrito.limpiar()
            
            # Actualizar interfaz
            self.actualizar_carrito()
            
            # Notificar a la aplicación principal si es posible
            if hasattr(self.master, 'actualizar_contador_carrito'):
                self.master.actualizar_contador_carrito()
            
            print("Carrito vaciado exitosamente")
            
        except Exception as e:
            print(f"Error confirmando limpiar carrito: {e}")
    
    def continuar_comprando(self):
        """Volver a la vista de compras"""
        try:
            if hasattr(self.master, 'mostrar_compras'):
                self.master.mostrar_compras()
            else:
                print("No se pudo acceder a la función mostrar_compras")
            
        except Exception as e:
            print(f"Error continuando compras: {e}")
    
    def proceder_checkout(self):
        """Proceder al checkout"""
        try:
            if self.carrito.obtener_cantidad_items() == 0:
                print("No se puede proceder al checkout con carrito vacío")
                return
            
            if hasattr(self.master, 'mostrar_checkout'):
                self.master.mostrar_checkout()
            else:
                print("No se pudo acceder a la función mostrar_checkout")
            
        except Exception as e:
            print(f" Error procediendo al checkout: {e}")
    
    def destroy(self):
        """Limpiar recursos antes de destruir"""
        try:
            # Limpiar items widgets
            self.limpiar_items_anteriores()
            
            print("🧹 InterfazCarrito limpiada")
            
        except Exception as e:
            print(f"Error limpiando InterfazCarrito: {e}")
        finally:
            super().destroy()