import customtkinter as ctk
from PIL import Image
import os
import sys

def obtener_directorio_proyecto():
    """Obtener directorio base del proyecto de manera robusta"""
    try:
        # Intentar varias estrategias para encontrar el directorio del proyecto
        
        # Estrategia 1: Desde el archivo actual (InterfazCompras.py)
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        
        # Desde Src/Interfaz/ subir 2 niveles al proyecto base
        proyecto_dir = os.path.dirname(os.path.dirname(current_dir))
        if os.path.exists(os.path.join(proyecto_dir, 'Src')):
            return proyecto_dir
        
        # Estrategia 2: Buscar desde el working directory
        cwd = os.getcwd()
        if 'Proyecto-Estructuras-de-Datos' in cwd:
            # Encontrar la parte del path que contiene el proyecto
            parts = cwd.split(os.sep)
            for i, part in enumerate(parts):
                if 'Proyecto-Estructuras-de-Datos' in part:
                    proyecto_dir = os.sep.join(parts[:i+1])
                    if os.path.exists(os.path.join(proyecto_dir, 'Src')):
                        return proyecto_dir
        
        # Estrategia 3: Buscar en sys.path
        for path in sys.path:
            if 'Proyecto-Estructuras-de-Datos' in path:
                if os.path.exists(os.path.join(path, 'Src')):
                    return path
                # Si path apunta a Src/, subir un nivel
                parent = os.path.dirname(path)
                if os.path.exists(os.path.join(parent, 'Src')):
                    return parent
        
        # Estrategia 4: Usar BASE_DIR como fallback
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
        if os.path.exists(os.path.join(base_dir, 'Src')):
            return base_dir
            
        # Si nada funciona, usar directorio actual
        print("⚠️ No se pudo determinar directorio del proyecto, usando directorio actual")
        return os.getcwd()
        
    except Exception as e:
        print(f"❌ Error determinando directorio del proyecto: {e}")
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def obtener_directorio_imagenes(tipo="productos"):
    """Obtener directorio de imágenes de manera robusta"""
    try:
        proyecto_dir = obtener_directorio_proyecto()
        
        # Rutas posibles para las imágenes
        rutas_posibles = [
            os.path.join(proyecto_dir, 'Src', 'Images', tipo),
            os.path.join(proyecto_dir, 'Images', tipo),
            os.path.join(proyecto_dir, 'Src', 'Interfaz', 'Images', tipo),
            os.path.join(proyecto_dir, 'assets', tipo),
            os.path.join(proyecto_dir, 'static', tipo)
        ]
        
        for ruta in rutas_posibles:
            if os.path.exists(ruta):
                print(f"📁 Directorio de imágenes encontrado: {ruta}")
                return ruta
        
        # Si no existe, crear el directorio estándar
        ruta_estandar = os.path.join(proyecto_dir, 'Src', 'Images', tipo)
        os.makedirs(ruta_estandar, exist_ok=True)
        print(f"📁 Directorio de imágenes creado: {ruta_estandar}")
        return ruta_estandar
        
    except Exception as e:
        print(f"❌ Error obteniendo directorio de imágenes: {e}")
        return None

# Configurar ruta base del proyecto de manera robusta
BASE_DIR = obtener_directorio_proyecto()
IMAGES_DIR = obtener_directorio_imagenes("productos")

# Agregar al sys.path si no está
src_dir = os.path.join(BASE_DIR, 'Src')
if src_dir not in sys.path:
    sys.path.append(src_dir)
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

print(f"🔧 Configuración de rutas:")
print(f"   BASE_DIR: {BASE_DIR}")
print(f"   IMAGES_DIR: {IMAGES_DIR}")
print(f"   SRC_DIR: {src_dir}")

class ProductoCard(ctk.CTkFrame):
    def __init__(self, master, producto, carrito, on_agregar=None, **kwargs):
        super().__init__(master, corner_radius=15, border_width=2, fg_color="white", **kwargs)
        
        self.producto = producto
        self.carrito = carrito
        self.on_agregar = on_agregar
        
        # ✅ ARREGLO: Diccionario para mantener referencias de imágenes
        self._imagenes_refs = {}
        self._widgets_refs = {}  # Para mantener referencias de widgets
        self._imagen_cargada = False
        
        # Configurar tamaño fijo
        self.configure(width=300, height=420)
        self.grid_propagate(False)
        
        # Crear contenido con manejo de errores robusto
        try:
            self.crear_contenido()
            print(f"✅ ProductoCard creada exitosamente: {self.producto.nombre}")
        except Exception as e:
            print(f"❌ Error creando ProductoCard para {self.producto.nombre}: {e}")
            import traceback
            traceback.print_exc()
            # Crear una tarjeta básica en caso de error
            self.crear_contenido_basico()
    
    def cargar_imagen_producto(self):
        """Cargar imagen del producto con sistema robusto de rutas"""
        try:
            # Usar el sistema robusto de detección de directorios
            productos_dir = IMAGES_DIR
            
            if not productos_dir or not os.path.exists(productos_dir):
                print(f"❌ Directorio de productos no encontrado: {productos_dir}")
                return self.crear_imagen_fallback()
            
            # Obtener nombre de imagen del producto
            imagen_nombre = None
            if hasattr(self.producto, 'imagen_ruta') and self.producto.imagen_ruta:
                imagen_ruta = self.producto.imagen_ruta
                
                # Limpiar ruta - extraer solo el nombre del archivo
                if any(sep in imagen_ruta for sep in ['\\', '/', 'Src', 'Images', 'productos']):
                    imagen_nombre = os.path.basename(imagen_ruta)
                else:
                    imagen_nombre = imagen_ruta
                    
            elif hasattr(self.producto, 'imagen') and self.producto.imagen:
                imagen_nombre = self.producto.imagen
            
            if not imagen_nombre:
                print(f"⚠️ Producto {self.producto.nombre} no tiene imagen asignada")
                return self.crear_imagen_fallback()
            
            # Verificar cache global primero
            cache_key = f"{imagen_nombre}_{260}x{180}"
            if cache_key in InterfazCompras._cache_imagenes_global:
                print(f"🗄️ Imagen desde cache: {imagen_nombre}")
                # ✅ ARREGLO: Mantener referencia local también
                imagen_cache = InterfazCompras._cache_imagenes_global[cache_key]
                self._imagenes_refs[cache_key] = imagen_cache
                return imagen_cache
            
            # Buscar imagen con múltiples estrategias
            imagen_encontrada = self.buscar_imagen_multiple(productos_dir, imagen_nombre)
            
            if not imagen_encontrada:
                print(f"❌ No se encontró imagen para: {self.producto.nombre}")
                return self.crear_imagen_fallback()
            
            # Cargar y procesar imagen
            img_pil = Image.open(imagen_encontrada)
            img_pil = self.redimensionar_imagen(img_pil, (260, 180))
            img_pil = self.convertir_a_rgb(img_pil)
            
            # ✅ ARREGLO: Crear CTkImage y mantener múltiples referencias
            ctk_image = ctk.CTkImage(img_pil, size=(260, 180))
            
            # Cache global
            InterfazCompras._cache_imagenes_global[cache_key] = ctk_image
            # Cache local en la tarjeta
            self._imagenes_refs[cache_key] = ctk_image
            
            print(f"✅ Imagen cargada y cacheada: {os.path.basename(imagen_encontrada)}")
            return ctk_image
            
        except Exception as e:
            print(f"❌ Error cargando imagen para {self.producto.nombre}: {e}")
            return self.crear_imagen_fallback()
    
    def buscar_imagen_multiple(self, directorio, nombre_imagen):
        """Buscar imagen usando múltiples estrategias"""
        try:
            # Lista de nombres posibles para buscar
            nombres_busqueda = [
                nombre_imagen,  # Nombre original
                os.path.splitext(nombre_imagen)[0],  # Sin extensión
                self.normalizar_nombre_archivo(self.producto.nombre)  # Normalizado
            ]
            
            # Extensiones a probar
            extensiones = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
            
            # Buscar en el directorio
            for nombre_base in nombres_busqueda:
                # Primero buscar con extensión original si la tiene
                if '.' in nombre_base:
                    ruta_test = os.path.join(directorio, nombre_base)
                    if os.path.exists(ruta_test):
                        print(f"🎯 Imagen encontrada (exacta): {ruta_test}")
                        return ruta_test
                
                # Luego buscar agregando extensiones
                nombre_sin_ext = os.path.splitext(nombre_base)[0]
                for ext in extensiones:
                    ruta_test = os.path.join(directorio, nombre_sin_ext + ext)
                    if os.path.exists(ruta_test):
                        print(f"🎯 Imagen encontrada (con extensión): {ruta_test}")
                        return ruta_test
            
            # Búsqueda fuzzy - buscar archivos que contengan parte del nombre
            archivos_directorio = os.listdir(directorio)
            nombre_producto_limpio = self.normalizar_nombre_archivo(self.producto.nombre)
            
            for archivo in archivos_directorio:
                if any(ext in archivo.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']):
                    archivo_limpio = os.path.splitext(archivo)[0].lower()
                    # Si el archivo contiene palabras del producto
                    palabras_producto = nombre_producto_limpio.split('_')
                    if len(palabras_producto) > 1:
                        if any(palabra in archivo_limpio for palabra in palabras_producto if len(palabra) > 3):
                            ruta_test = os.path.join(directorio, archivo)
                            print(f"🎯 Imagen encontrada (fuzzy): {ruta_test}")
                            return ruta_test
            
            return None
            
        except Exception as e:
            print(f"❌ Error en búsqueda múltiple: {e}")
            return None
    
    def convertir_a_rgb(self, imagen):
        """Convertir imagen a RGB manejando transparencias"""
        try:
            if imagen.mode in ('RGBA', 'LA'):
                # Crear fondo blanco para transparencias
                background = Image.new('RGB', imagen.size, (255, 255, 255))
                if imagen.mode == 'RGBA':
                    background.paste(imagen, mask=imagen.split()[-1])
                else:
                    background.paste(imagen, mask=imagen.split()[-1])
                return background
            elif imagen.mode != 'RGB':
                return imagen.convert('RGB')
            return imagen
            
        except Exception as e:
            print(f"❌ Error convirtiendo imagen: {e}")
            return imagen.convert('RGB')
    
    def normalizar_nombre_archivo(self, nombre):
        """Normalizar nombre de producto para buscar archivo de imagen"""
        import re
        # Convertir a minúsculas y reemplazar caracteres especiales
        nombre_norm = nombre.lower()
        nombre_norm = re.sub(r'[^\w\s-]', '', nombre_norm)  # Remover caracteres especiales
        nombre_norm = re.sub(r'[-\s]+', '_', nombre_norm)   # Reemplazar espacios y guiones con _
        return nombre_norm
    
    def redimensionar_imagen(self, imagen, tamano_objetivo):
        """Redimensionar imagen manteniendo proporción"""
        try:
            # Calcular proporción
            ancho_orig, alto_orig = imagen.size
            ancho_obj, alto_obj = tamano_objetivo
            
            # Calcular ratio para mantener proporción
            ratio = min(ancho_obj / ancho_orig, alto_obj / alto_orig)
            
            # Nuevo tamaño manteniendo proporción
            nuevo_ancho = int(ancho_orig * ratio)
            nuevo_alto = int(alto_orig * ratio)
            
            # Redimensionar
            imagen_redim = imagen.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
            
            # Si la imagen es más pequeña que el objetivo, centrarla en un canvas
            if nuevo_ancho < ancho_obj or nuevo_alto < alto_obj:
                canvas = Image.new('RGB', tamano_objetivo, (255, 255, 255))
                offset_x = (ancho_obj - nuevo_ancho) // 2
                offset_y = (alto_obj - nuevo_alto) // 2
                canvas.paste(imagen_redim, (offset_x, offset_y))
                return canvas
            
            return imagen_redim
            
        except Exception as e:
            print(f"Error redimensionando imagen: {e}")
            return imagen.resize(tamano_objetivo, Image.Resampling.LANCZOS)
    
    def crear_imagen_fallback(self):
        """Crear imagen de respaldo cuando no se puede cargar la original"""
        try:
            # Verificar cache de fallback primero
            fallback_key = f"fallback_{self.producto.nombre[:10]}"
            if fallback_key in self._imagenes_refs:
                return self._imagenes_refs[fallback_key]
            
            # Crear imagen de respaldo con el nombre del producto
            fallback_img = Image.new('RGB', (260, 180), (240, 240, 240))
            
            # Intentar agregar texto con PIL (opcional)
            try:
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(fallback_img)
                
                # Intentar usar fuente del sistema
                try:
                    font = ImageFont.truetype("arial.ttf", 16)
                except:
                    try:
                        font = ImageFont.truetype("calibri.ttf", 16)
                    except:
                        font = ImageFont.load_default()
                
                # Texto del producto (truncado)
                texto = self.producto.nombre[:20] + "..." if len(self.producto.nombre) > 20 else self.producto.nombre
                
                # Centrar texto
                bbox = draw.textbbox((0, 0), texto, font=font)
                ancho_texto = bbox[2] - bbox[0]
                alto_texto = bbox[3] - bbox[1]
                
                x = (260 - ancho_texto) // 2
                y = (180 - alto_texto) // 2
                
                draw.text((x, y), texto, fill=(100, 100, 100), font=font)
                
            except Exception as e:
                print(f"Error agregando texto a imagen fallback: {e}")
            
            # ✅ ARREGLO: Crear CTkImage y mantener referencia del fallback
            ctk_fallback = ctk.CTkImage(fallback_img, size=(260, 180))
            self._imagenes_refs[fallback_key] = ctk_fallback
            
            return ctk_fallback
            
        except Exception as e:
            print(f"Error creando imagen fallback: {e}")
            # Retorno de emergencia - sin imagen
            return None
    
    def crear_contenido(self):
        """Crear contenido de la tarjeta de producto - MÉTODO DIFERIDO"""
        try:
            # Frame para imagen
            img_frame = ctk.CTkFrame(self, width=280, height=200, corner_radius=10)
            img_frame.pack(pady=15, padx=10)
            img_frame.pack_propagate(False)
            
            # ✅ SOLUCIÓN FINAL: Crear label placeholder primero
            self.img_label_placeholder = ctk.CTkLabel(
                img_frame, 
                text="⏳ Cargando...", 
                font=("Arial", 16),
                text_color="#666666"
            )
            self.img_label_placeholder.pack(expand=True)
            
            # ✅ Guardar referencias de widgets críticos
            self._img_frame = img_frame
            self._widgets_refs['img_frame'] = img_frame
            self._widgets_refs['img_label_placeholder'] = self.img_label_placeholder
            
            # Frame de información del producto
            info_frame = ctk.CTkFrame(self, fg_color="transparent")
            info_frame.pack(fill="x", padx=15, pady=(0, 15))
            self._widgets_refs['info_frame'] = info_frame
            
            # Crear resto del contenido primero
            try:
                self.crear_info_producto(info_frame)
            except Exception as info_error:
                print(f"⚠️ Error creando info del producto: {info_error}")
                # Crear información básica en caso de error
                try:
                    error_label = ctk.CTkLabel(
                        info_frame,
                        text=f"⚠️ Error cargando info: {self.producto.nombre}",
                        font=("Arial", 12),
                        text_color="#dc2626"
                    )
                    error_label.pack(pady=10)
                except Exception as critical_error:
                    print(f"💥 Error crítico creando info básica: {critical_error}")
            
            # ✅ CARGAR IMAGEN DE FORMA DIFERIDA usando after()
            # Esto evita el conflicto de pyimage en el thread principal
            self.after(100, self.cargar_imagen_diferida)
                
        except Exception as critical_error:
            print(f"💥 Error crítico en crear_contenido para {self.producto.nombre}: {critical_error}")
            import traceback
            traceback.print_exc()
            # En caso de error crítico, crear contenido mínimo
            try:
                self.crear_contenido_emergencia()
            except Exception as emergency_error:
                print(f"💥💥 Error de emergencia: {emergency_error}")
                raise
    
    def cargar_imagen_diferida(self):
        """Cargar imagen de forma diferida para evitar conflictos de pyimage"""
        try:
            if self._imagen_cargada:
                return  # Ya se cargó la imagen
            
            print(f"🔄 Cargando imagen diferida para: {self.producto.nombre}")
            
            # PASO 1: Cargar imagen PIL directamente desde archivo
            img_pil = self.cargar_imagen_pil_directa()
            
            if img_pil:
                try:
                    # PASO 2: Crear CTkImage en el contexto correcto del thread principal
                    imagen_ctk = ctk.CTkImage(img_pil, size=(260, 180))
                    
                    # PASO 3: Verificar que el placeholder aún existe
                    if hasattr(self, 'img_label_placeholder') and self.img_label_placeholder.winfo_exists():
                        # PASO 4: Destruir placeholder
                        self.img_label_placeholder.destroy()
                        
                        # PASO 5: Crear nuevo label con imagen
                        self.img_label = ctk.CTkLabel(self._img_frame, image=imagen_ctk, text="")
                        
                        # PASO 6: Mantener referencias fuertes
                        self._imagen_producto = imagen_ctk
                        self.img_label._imagen_ref = imagen_ctk
                        self._img_frame._imagen_ref = imagen_ctk
                        self._widgets_refs['img_label'] = self.img_label
                        
                        # PASO 7: Mostrar label
                        self.img_label.pack(expand=True)
                        
                        # PASO 8: Marcar como cargada
                        self._imagen_cargada = True
                        
                        print(f"✅ Imagen diferida cargada exitosamente para: {self.producto.nombre}")
                        return
                    
                except Exception as label_error:
                    print(f"❌ Error creando label diferido: {label_error}")
            
            # Si llegamos aquí, falló la carga - usar fallback
            self.cargar_fallback_diferido()
            
        except Exception as e:
            print(f"❌ Error en carga diferida para {self.producto.nombre}: {e}")
            self.cargar_fallback_diferido()
    
    def cargar_fallback_diferido(self):
        """Cargar fallback de forma diferida"""
        try:
            if self._imagen_cargada:
                return
            
            print(f"🔄 Cargando fallback diferido para: {self.producto.nombre}")
            
            # Crear imagen fallback agresiva
            imagen_fallback = self.crear_imagen_fallback_agresiva()
            
            if imagen_fallback and hasattr(self, 'img_label_placeholder') and self.img_label_placeholder.winfo_exists():
                # Reemplazar placeholder
                self.img_label_placeholder.destroy()
                
                self.img_label = ctk.CTkLabel(self._img_frame, image=imagen_fallback, text="")
                self.img_label._imagen_ref = imagen_fallback
                self._imagen_producto = imagen_fallback
                self._img_frame._imagen_ref = imagen_fallback
                self._widgets_refs['img_label'] = self.img_label
                
                self.img_label.pack(expand=True)
                self._imagen_cargada = True
                
                print(f"✅ Fallback diferido cargado para: {self.producto.nombre}")
            else:
                # Último recurso - cambiar texto del placeholder
                if hasattr(self, 'img_label_placeholder') and self.img_label_placeholder.winfo_exists():
                    self.img_label_placeholder.configure(text="📦\nSin Imagen")
                    self._imagen_cargada = True
                    print(f"⚠️ Placeholder final para: {self.producto.nombre}")
            
        except Exception as e:
            print(f"❌ Error en fallback diferido: {e}")
            # Dejar el placeholder como está
            self._imagen_cargada = True

    def crear_imagen_fallback_agresiva(self):
        """Crear imagen de respaldo más agresiva (sin cache)"""
        try:
            # Crear imagen de respaldo única para esta tarjeta
            fallback_img = Image.new('RGB', (260, 180), (245, 245, 245))
            
            # Agregar información visual del producto
            try:
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(fallback_img)
                
                # Intentar usar fuente del sistema
                font = None
                for font_name in ["arial.ttf", "calibri.ttf", "segoeui.ttf"]:
                    try:
                        font = ImageFont.truetype(font_name, 14)
                        break
                    except:
                        continue
                
                if not font:
                    font = ImageFont.load_default()
                
                # Dibujar información del producto
                producto_info = [
                    self.producto.nombre[:25] + "..." if len(self.producto.nombre) > 25 else self.producto.nombre,
                    f"${self.producto.precio:.2f}",
                    f"Stock: {self.producto.stock}"
                ]
                
                y_offset = 40
                for line in producto_info:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    x = (260 - text_width) // 2
                    draw.text((x, y_offset), line, fill=(80, 80, 80), font=font)
                    y_offset += 25
                
                # Agregar decoración
                draw.rectangle([20, 20, 240, 160], outline=(200, 200, 200), width=2)
                
            except Exception as draw_error:
                print(f"⚠️ Error dibujando en fallback: {draw_error}")
            
            # Crear CTkImage única (sin cache)
            ctk_fallback = ctk.CTkImage(fallback_img, size=(260, 180))
            
            # Mantener referencia local únicamente
            fallback_key = f"fallback_agresivo_{id(self)}_{id(ctk_fallback)}"
            self._imagenes_refs[fallback_key] = ctk_fallback
            
            return ctk_fallback
            
        except Exception as e:
            print(f"❌ Error creando fallback agresivo: {e}")
            return None

    def cargar_imagen_pil_directa(self):
        """Cargar imagen PIL directamente desde archivo - VERSIÓN AGRESIVA"""
        try:
            productos_dir = IMAGES_DIR
            if not productos_dir or not os.path.exists(productos_dir):
                print(f"❌ Directorio no disponible: {productos_dir}")
                return None
            
            # Buscar imagen usando múltiples estrategias
            imagen_nombre = None
            if hasattr(self.producto, 'imagen_ruta') and self.producto.imagen_ruta:
                imagen_nombre = os.path.basename(self.producto.imagen_ruta)
            elif hasattr(self.producto, 'imagen') and self.producto.imagen:
                imagen_nombre = self.producto.imagen
            
            if not imagen_nombre:
                print(f"⚠️ No hay nombre de imagen para: {self.producto.nombre}")
                return None
            
            # Buscar archivo de imagen
            imagen_encontrada = self.buscar_imagen_multiple(productos_dir, imagen_nombre)
            if not imagen_encontrada:
                print(f"❌ Archivo de imagen no encontrado para: {self.producto.nombre}")
                return None
            
            # Cargar imagen PIL directamente
            print(f"📂 Cargando imagen directa desde: {imagen_encontrada}")
            img_pil = Image.open(imagen_encontrada)
            
            # Procesar imagen (redimensionar y convertir)
            img_pil = self.redimensionar_imagen(img_pil, (260, 180))
            img_pil = self.convertir_a_rgb(img_pil)
            
            print(f"✅ Imagen PIL cargada directamente para: {self.producto.nombre}")
            return img_pil
            
        except Exception as e:
            print(f"❌ Error cargando imagen PIL directa para {self.producto.nombre}: {e}")
            return None

    def crear_contenido_emergencia(self):
        """Crear contenido de emergencia mínimo"""
        try:
            # Frame de emergencia con color distintivo
            emergency_frame = ctk.CTkFrame(self, fg_color="#fff3cd", border_color="#ffc107", border_width=2)
            emergency_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Título de emergencia
            emergency_title = ctk.CTkLabel(
                emergency_frame,
                text="⚠️ MODO EMERGENCIA",
                font=("Arial", 12, "bold"),
                text_color="#856404"
            )
            emergency_title.pack(pady=5)
            
            # Nombre del producto
            nombre_label = ctk.CTkLabel(
                emergency_frame,
                text=self.producto.nombre,
                font=("Arial", 14, "bold"),
                text_color="#212529",
                wraplength=280
            )
            nombre_label.pack(pady=5)
            
            # Información básica
            info_text = f"Precio: ${self.producto.precio:.2f}\nStock: {self.producto.stock}"
            info_label = ctk.CTkLabel(
                emergency_frame,
                text=info_text,
                font=("Arial", 12),
                text_color="#495057"
            )
            info_label.pack(pady=5)
            
            # Botón básico si hay stock
            if self.producto.stock > 0:
                btn_simple = ctk.CTkButton(
                    emergency_frame,
                    text="Agregar al Carrito",
                    command=lambda: self.agregar_al_carrito_simple(),
                    font=("Arial", 12),
                    width=200,
                    fg_color="#007bff"
                )
                btn_simple.pack(pady=10)
            
            print(f"🆘 Contenido de emergencia creado para: {self.producto.nombre}")
            
        except Exception as e:
            print(f"💥 Error crítico en contenido de emergencia: {e}")
            raise

    def agregar_al_carrito_simple(self):
        """Versión simplificada para agregar al carrito"""
        try:
            # ✅ ARREGLO: Usar método mejorado del carrito
            exito = self.carrito.agregar_producto(self.producto, 1)
            
            if exito and self.on_agregar:
                self.on_agregar(self.producto, 1)
                
            print(f"✅ Producto agregado (modo simple): {self.producto.nombre}")
        except Exception as e:
            print(f"❌ Error agregando producto simple: {e}")
    
    def crear_info_producto(self, parent):
        """Crear información del producto"""
        try:
            # Nombre del producto
            nombre_text = self.producto.nombre[:35] + "..." if len(self.producto.nombre) > 35 else self.producto.nombre
            nombre_label = ctk.CTkLabel(
                parent,
                text=nombre_text,
                font=("Arial", 16, "bold"),
                text_color="#2c3e50",
                wraplength=270
            )
            nombre_label.pack(anchor="w", pady=(0, 5))
            self._widgets_refs['nombre_label'] = nombre_label
            
            # Descripción
            descripcion_text = getattr(self.producto, 'descripcion', 'Sin descripción')
            if len(descripcion_text) > 60:
                descripcion_text = descripcion_text[:60] + "..."
            
            desc_label = ctk.CTkLabel(
                parent,
                text=descripcion_text,
                font=("Arial", 12),
                text_color="#7f8c8d",
                wraplength=270
            )
            desc_label.pack(anchor="w", pady=(0, 10))
            self._widgets_refs['desc_label'] = desc_label
            
            # Frame para precio y stock
            precio_frame = ctk.CTkFrame(parent, fg_color="transparent")
            precio_frame.pack(fill="x", pady=(0, 10))
            self._widgets_refs['precio_frame'] = precio_frame
            
            # Precio
            precio_label = ctk.CTkLabel(
                precio_frame,
                text=f"${self.producto.precio:,.2f}",
                font=("Arial", 20, "bold"),
                text_color="#27ae60"
            )
            precio_label.pack(side="left")
            self._widgets_refs['precio_label'] = precio_label
            
            # Stock
            stock_text = f"Stock: {self.producto.stock}"
            stock_color = "#27ae60" if self.producto.stock > 5 else "#e74c3c" if self.producto.stock > 0 else "#95a5a6"
            stock_label = ctk.CTkLabel(
                precio_frame,
                text=stock_text,
                font=("Arial", 12),
                text_color=stock_color
            )
            stock_label.pack(side="right")
            self._widgets_refs['stock_label'] = stock_label
            
            # Frame para cantidad y botón
            accion_frame = ctk.CTkFrame(parent, fg_color="transparent")
            accion_frame.pack(fill="x")
            self._widgets_refs['accion_frame'] = accion_frame
            
            if self.producto.stock > 0:
                self.crear_controles_agregar(accion_frame)
            else:
                self.crear_boton_sin_stock(accion_frame)
                
        except Exception as e:
            print(f"❌ Error creando info producto: {e}")
            raise
    
    def crear_controles_agregar(self, parent):
        """Crear controles para agregar producto"""
        try:
            # Entry para cantidad
            cantidad_frame = ctk.CTkFrame(parent, fg_color="transparent")
            cantidad_frame.pack(side="left", fill="x", expand=True)
            self._widgets_refs['cantidad_frame'] = cantidad_frame
            
            cantidad_label = ctk.CTkLabel(cantidad_frame, text="Cantidad:", font=("Arial", 12))
            cantidad_label.pack(side="left")
            self._widgets_refs['cantidad_label'] = cantidad_label
            
            self.cantidad_entry = ctk.CTkEntry(cantidad_frame, width=60, placeholder_text="1")
            self.cantidad_entry.pack(side="left", padx=(5, 10))
            self.cantidad_entry.insert(0, "1")
            self._widgets_refs['cantidad_entry'] = self.cantidad_entry
            
            # Botón agregar
            btn_agregar = ctk.CTkButton(
                parent,
                text="🛒 Agregar",
                command=self.agregar_al_carrito,
                font=("Arial", 12, "bold"),
                width=100,
                fg_color="#3498db",
                hover_color="#2980b9"
            )
            btn_agregar.pack(side="right")
            self._widgets_refs['btn_agregar'] = btn_agregar
            
        except Exception as e:
            print(f"❌ Error creando controles agregar: {e}")
            raise
    
    def crear_boton_sin_stock(self, parent):
        """Crear botón para producto sin stock"""
        try:
            btn_sin_stock = ctk.CTkButton(
                parent,
                text="Sin Stock",
                state="disabled",
                font=("Arial", 12, "bold"),
                width=200,
                fg_color="#95a5a6"
            )
            btn_sin_stock.pack(fill="x")
            self._widgets_refs['btn_sin_stock'] = btn_sin_stock
            
        except Exception as e:
            print(f"❌ Error creando botón sin stock: {e}")
            raise
    
    def crear_contenido_basico(self):
        """Crear contenido básico en caso de error"""
        try:
            # Frame simple con solo el nombre del producto
            basic_frame = ctk.CTkFrame(self, fg_color="#fee2e2")
            basic_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Nombre del producto
            nombre_label = ctk.CTkLabel(
                basic_frame,
                text=f"❌ Error: {self.producto.nombre}",
                font=("Arial", 14, "bold"),
                text_color="#dc2626"
            )
            nombre_label.pack(pady=20)
            
            # Precio básico
            precio_label = ctk.CTkLabel(
                basic_frame,
                text=f"${self.producto.precio:.2f}",
                font=("Arial", 16),
                text_color="#374151"
            )
            precio_label.pack(pady=10)
            
            print(f"⚠️ Contenido básico creado para: {self.producto.nombre}")
            
        except Exception as e:
            print(f"❌ Error crítico creando contenido básico: {e}")
    
    def agregar_al_carrito(self):
        """✅ MÉTODO ACTUALIZADO: Agregar producto al carrito usando el sistema mejorado"""
        try:
            cantidad_str = self.cantidad_entry.get().strip()
            if not cantidad_str:
                cantidad = 1
            else:
                cantidad = int(cantidad_str)
            
            if cantidad <= 0:
                cantidad = 1
            
            if cantidad > self.producto.stock:
                cantidad = self.producto.stock
                self.cantidad_entry.delete(0, 'end')
                self.cantidad_entry.insert(0, str(cantidad))
            
            # ✅ ARREGLO: Usar el método mejorado del carrito
            exito = self.carrito.agregar_producto(self.producto, cantidad)
            
            if exito:
                # Callback opcional
                if self.on_agregar:
                    self.on_agregar(self.producto, cantidad)
                
                print(f"✅ Agregado {cantidad}x {self.producto.nombre} al carrito")
                print(f"📊 Total items en carrito: {self.carrito.obtener_cantidad_items()}")
            else:
                print(f"❌ Error agregando producto al carrito")
            
        except ValueError:
            # Si no es un número válido, usar 1
            try:
                self.cantidad_entry.delete(0, 'end')
                self.cantidad_entry.insert(0, "1")
                self.agregar_al_carrito()
            except Exception as e:
                print(f"Error corrigiendo cantidad: {e}")
        except Exception as e:
            print(f"Error agregando al carrito: {e}")
    
    def destroy(self):
        """Override destroy para limpiar referencias antes de destruir"""
        try:
            # Limpiar referencias de imágenes antes de destruir
            if hasattr(self, '_imagenes_refs'):
                self._imagenes_refs.clear()
            if hasattr(self, '_widgets_refs'):
                self._widgets_refs.clear()
            if hasattr(self, '_imagen_producto'):
                delattr(self, '_imagen_producto')
            print(f"🧹 ProductoCard destruida: {self.producto.nombre}")
        except Exception as e:
            print(f"Error limpiando ProductoCard: {e}")
        finally:
            super().destroy()

class InterfazCompras(ctk.CTkFrame):
    # ✅ Cache global más robusto
    _cache_imagenes_global = {}
    _cache_referencias_fuertes = {}
    
    def __init__(self, master, inventario, carrito, **kwargs):
        super().__init__(master, **kwargs)
        
        self.inventario = inventario
        self.carrito = carrito
        
        # ✅ CALLBACK PERSONALIZADO para la aplicación principal
        self._callback_producto_agregado = None
        
        # ✅ Cache local adicional para esta instancia
        self._cache_local = {}
        self._widgets_con_imagenes = []
        self._tarjetas_productos = []
        
        # Configurar interfaz
        self.configure(fg_color="#f8f9fa")
        
        # Cargar iconos de la interfaz
        self.cargar_iconos_interfaz()
        
        self.crear_interfaz()
        
        # ✅ CARGAR PRODUCTOS DE FORMA DIFERIDA para evitar conflictos
        self.after(50, self.cargar_productos)
    
    def set_callback_producto_agregado(self, callback):
        """✅ NUEVO: Configurar callback para cuando se agrega un producto"""
        self._callback_producto_agregado = callback
        print(f"🔗 Callback de producto agregado configurado")
    
    def cargar_iconos_interfaz(self):
        """Cargar iconos para la interfaz usando sistema robusto de rutas"""
        try:
            # Usar el sistema robusto para encontrar el directorio de imágenes
            images_dir = obtener_directorio_imagenes("")  # Sin subdirectorio
            if images_dir:
                images_dir = os.path.dirname(images_dir)  # Subir un nivel desde productos/
            
            if not images_dir or not os.path.exists(images_dir):
                print(f"⚠️ Directorio de imágenes no encontrado: {images_dir}")
                self.crear_iconos_fallback()
                return
            
            # Iconos que podríamos usar en la interfaz
            iconos_config = {
                'carrito_icono': ('carrito-icon.png', (24, 24)),
                'buscar_icono': ('search-icon.png', (20, 20)),
                'filtro_icono': ('filter-icon.png', (20, 20))
            }
            
            self.iconos = {}
            
            for nombre_icono, (archivo, tamaño) in iconos_config.items():
                try:
                    ruta_icono = os.path.join(images_dir, archivo)
                    if os.path.exists(ruta_icono):
                        img_data = Image.open(ruta_icono)
                        # Redimensionar si es necesario
                        if img_data.size != tamaño:
                            img_data = img_data.resize(tamaño, Image.Resampling.LANCZOS)
                        
                        # Convertir a RGB si es necesario
                        if img_data.mode != 'RGB':
                            img_data = img_data.convert('RGB')
                        
                        # ✅ Mantener referencia del icono
                        icono_ctk = ctk.CTkImage(img_data, size=tamaño)
                        self.iconos[nombre_icono] = icono_ctk
                        self._cache_local[nombre_icono] = icono_ctk
                        
                        print(f"✅ Icono cargado: {nombre_icono}")
                    else:
                        print(f"⚠️ No se encontró icono: {archivo}")
                        
                except Exception as e:
                    print(f"❌ Error cargando icono {nombre_icono}: {e}")
            
            # Si no se cargaron iconos, crear fallbacks
            if not self.iconos:
                self.crear_iconos_fallback()
                
        except Exception as e:
            print(f"❌ Error general cargando iconos: {e}")
            self.crear_iconos_fallback()
    
    def crear_iconos_fallback(self):
        """Crear iconos de respaldo"""
        try:
            self.iconos = {}
            
            # Crear iconos simples de respaldo
            iconos_fallback = {
                'carrito_icono': (24, 24, (52, 152, 219)),
                'buscar_icono': (20, 20, (46, 204, 113)),
                'filtro_icono': (20, 20, (155, 89, 182))
            }
            
            for nombre, (ancho, alto, color) in iconos_fallback.items():
                img_fallback = Image.new('RGB', (ancho, alto), color)
                icono_ctk = ctk.CTkImage(img_fallback, size=(ancho, alto))
                self.iconos[nombre] = icono_ctk
                self._cache_local[nombre] = icono_ctk
            
            print("✅ Iconos fallback creados")
            
        except Exception as e:
            print(f"❌ Error creando iconos fallback: {e}")
            self.iconos = {}
    
    def crear_interfaz(self):
        """Crear la interfaz principal"""
        # Título
        titulo_frame = ctk.CTkFrame(self, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        titulo = ctk.CTkLabel(
            titulo_frame,
            text="🛍️ Catálogo de Productos",
            font=("Arial", 24, "bold"),
            text_color="#2c3e50"
        )
        titulo.pack()
        
        # Frame scrollable para productos
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            label_text="Productos Disponibles",
            label_font=("Arial", 16, "bold")
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Configurar grid del scroll frame
        self.productos_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.productos_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def cargar_productos(self):
        """Cargar y mostrar productos en grid"""
        try:
            productos = self.inventario.obtener_productos()
            print(f"📦 Cargando {len(productos)} productos...")
            
            if not productos:
                self.mostrar_mensaje("No hay productos disponibles", "info")
                return
            
            # Limpiar tarjetas anteriores si existen
            self.limpiar_tarjetas_anteriores()
            
            # Configurar grid
            columnas = 3  # 3 productos por fila
            
            # ✅ CARGAR PRODUCTOS CON DELAY PROGRESIVO
            for idx, producto in enumerate(productos):
                # Usar after() para espaciar la creación de tarjetas
                delay = idx * 150  # 150ms entre cada tarjeta
                self.after(delay, lambda p=producto, i=idx, c=columnas: self.crear_tarjeta_diferida(p, i, c))
            
            # Configurar columnas después de un delay
            total_delay = len(productos) * 150 + 500
            self.after(total_delay, lambda: self.configurar_grid_columnas(columnas))
            
            print(f"📅 Programadas {len(productos)} tarjetas con delay progresivo")
                
        except Exception as e:
            print(f"❌ Error crítico cargando productos: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_error("Error crítico cargando productos")
    
    def crear_tarjeta_diferida(self, producto, idx, columnas):
        """✅ MÉTODO ACTUALIZADO: Crear tarjeta de producto de forma diferida"""
        try:
            row = idx // columnas
            col = idx % columnas
            
            print(f"🔨 Creando tarjeta diferida para producto {idx+1}: {producto.nombre}")
            
            # ✅ ARREGLO: Usar callback personalizado mejorado
            def on_agregar_wrapper(producto, cantidad):
                try:
                    # Callback original de la tarjeta
                    self.on_producto_agregado(producto, cantidad)
                    
                    # ✅ NUEVO: Callback personalizado de la aplicación principal
                    if self._callback_producto_agregado:
                        self._callback_producto_agregado(producto, cantidad)
                        
                except Exception as e:
                    print(f"❌ Error en wrapper callback: {e}")
            
            # Crear tarjeta de producto
            card = ProductoCard(
                self.productos_frame,
                producto=producto,
                carrito=self.carrito,
                on_agregar=on_agregar_wrapper  # ✅ Usar wrapper mejorado
            )
            
            # ✅ Mantener referencia de la tarjeta
            self._tarjetas_productos.append(card)
            
            # Posicionar en grid
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            print(f"✅ Tarjeta diferida {idx+1} creada y posicionada")
            
        except Exception as e:
            print(f"❌ Error creando tarjeta diferida para {producto.nombre}: {e}")
            import traceback
            traceback.print_exc()
    
    def configurar_grid_columnas(self, columnas):
        """Configurar columnas del grid"""
        try:
            for col in range(columnas):
                self.productos_frame.grid_columnconfigure(col, weight=1)
            print(f"✅ Grid configurado con {columnas} columnas")
        except Exception as e:
            print(f"❌ Error configurando grid: {e}")
    
    def limpiar_tarjetas_anteriores(self):
        """Limpiar tarjetas de productos anteriores"""
        try:
            for tarjeta in self._tarjetas_productos:
                try:
                    if tarjeta.winfo_exists():
                        tarjeta.destroy()
                except Exception as e:
                    print(f"Error limpiando tarjeta: {e}")
            self._tarjetas_productos.clear()
            print("🧹 Tarjetas anteriores limpiadas")
        except Exception as e:
            print(f"Error limpiando tarjetas anteriores: {e}")
    
    def on_producto_agregado(self, producto, cantidad):
        """✅ MÉTODO ACTUALIZADO: Callback cuando se agrega un producto al carrito"""
        try:
            # Mostrar notificación visual (opcional)
            print(f"🛒 Producto agregado: {cantidad}x {producto.nombre}")
            print(f"📊 Total en carrito: {self.carrito.obtener_cantidad_items()} items")
            
            # Aquí se puede notificar a la aplicación principal
            # Si hay un callback parent definido
            if hasattr(self.master, 'actualizar_contador_carrito'):
                self.master.actualizar_contador_carrito()
                
        except Exception as e:
            print(f"Error en callback producto agregado: {e}")
    
    def mostrar_mensaje(self, mensaje, tipo="info"):
        """Mostrar mensaje informativo"""
        try:
            color = "#3498db" if tipo == "info" else "#e74c3c"
            icono = "ℹ️" if tipo == "info" else "❌"
            
            mensaje_label = ctk.CTkLabel(
                self.productos_frame,
                text=f"{icono} {mensaje}",
                font=("Arial", 16),
                text_color=color
            )
            mensaje_label.pack(pady=50)
            
        except Exception as e:
            print(f"Error mostrando mensaje: {e}")
    
    def mostrar_error(self, mensaje):
        """Mostrar mensaje de error"""
        self.mostrar_mensaje(mensaje, "error")
    
    def destroy(self):
        """Override destroy para limpiar referencias antes de destruir"""
        try:
            print("🧹 Limpiando InterfazCompras...")
            
            # Limpiar tarjetas de productos
            self.limpiar_tarjetas_anteriores()
            
            # Limpiar cache local
            if hasattr(self, '_cache_local'):
                self._cache_local.clear()
            
            # Limpiar iconos
            if hasattr(self, 'iconos'):
                self.iconos.clear()
            
            print("✅ InterfazCompras limpiada")
            
        except Exception as e:
            print(f"Error limpiando InterfazCompras: {e}")
        finally:
            super().destroy()