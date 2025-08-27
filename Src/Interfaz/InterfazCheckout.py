import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import uuid
import re

class InterfazCheckout(ctk.CTkFrame):
    """Interfaz de checkout con scroll funcional y botón en formulario"""
    
    def __init__(self, parent, sistema_ecommerce, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.sistema = sistema_ecommerce
        self.carrito = sistema_ecommerce.carrito
        
        self.orden_id = None
        self.procesando = False
        self.total_final = 0
        
        if self.carrito.obtener_cantidad_items() == 0:
            self.mostrar_carrito_vacio()
            return
        
        self.crear_interfaz()
    
    def mostrar_carrito_vacio(self):
        """Mostrar mensaje cuando el carrito está vacío"""
        mensaje_frame = ctk.CTkFrame(self, fg_color="#fef2f2")
        mensaje_frame.pack(fill="both", expand=True, padx=50, pady=100)
        
        ctk.CTkLabel(mensaje_frame, text="🛒", font=("Arial", 64)).pack(pady=(50, 20))
        ctk.CTkLabel(mensaje_frame, text="Tu carrito está vacío", font=("Arial Black", 24), text_color="#dc2626").pack(pady=10)
        ctk.CTkButton(mensaje_frame, text="🛍️ Ir a Compras", command=self.ir_a_compras, font=("Arial Bold", 16), fg_color="#3b82f6", height=50, width=200).pack(pady=30)
    
    def crear_interfaz(self):
        """Crear interfaz principal"""
        # Header
        header = ctk.CTkFrame(self, fg_color="#1e40af", height=80)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text="💳 Finalizar Compra", font=("Arial Black", 24), text_color="white").pack(side="left", padx=30, pady=20)
        
        # Usuario info
        if hasattr(self.sistema, 'cliente_autenticado') and self.sistema.cliente_autenticado:
            user_label = ctk.CTkLabel(header, text=f"👤 {self.sistema.cliente_autenticado.nombre}", font=("Arial", 14), text_color="white")
            user_label.pack(side="right", padx=30, pady=20)
        
        # Contenedor principal
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        main_container.grid_columnconfigure((0, 1), weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Formulario con scroll (lado izquierdo)
        self.crear_formulario_scroll(main_container)
        
        # Resumen SIN botón de pago (lado derecho)
        self.crear_resumen(main_container)
    
    def crear_formulario_scroll(self, parent):
        """Crear formulario con scroll funcional"""
        form_container = ctk.CTkFrame(parent, fg_color="#f8fafc")
        form_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        # Título del formulario
        ctk.CTkLabel(form_container, text="💳 Datos de Pago", font=("Arial Black", 18), text_color="#1f2937").pack(pady=(20, 10))
        
        # Frame scrollable - ESTE ES EL CLAVE PARA QUE FUNCIONE EL SCROLL
        self.form_frame = ctk.CTkScrollableFrame(
            form_container,
            width=480,
            height=550,  # Altura fija para activar scroll
            fg_color="#ffffff"
        )
        self.form_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Info del método de pago
        info_frame = ctk.CTkFrame(self.form_frame, fg_color="#f0f9ff", corner_radius=15)
        info_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(info_frame, text="🔐 Pago Seguro con Tarjeta", font=("Arial Bold", 16), text_color="#1e40af").pack(pady=(15, 5))
        ctk.CTkLabel(info_frame, text="Aceptamos Visa, MasterCard, American Express", font=("Arial", 12), text_color="#64748b").pack(pady=(0, 15))
        
        # Campos de tarjeta
        self.crear_campos_tarjeta(self.form_frame)
        
        # BOTÓN DE PAGO AQUÍ - EN VEZ DE LA INFORMACIÓN DE SEGURIDAD
        boton_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        boton_frame.pack(fill="x", padx=20, pady=(30, 50))
        
        self.btn_finalizar = ctk.CTkButton(
            boton_frame,
            text="💳 PAGAR AHORA",
            command=self.finalizar_compra,
            height=70,
            font=("Arial", 18, "bold"),
            fg_color="#10b981",
            hover_color="#059669",
            text_color="white",
            corner_radius=20
        )
        self.btn_finalizar.pack(fill="x", pady=10)
        
        # Información de seguridad pequeña debajo del botón
        info_seguridad = ctk.CTkLabel(
            boton_frame, 
            text="🔒 Pago seguro con encriptación SSL de 256 bits", 
            font=("Arial", 11), 
            text_color="#6b7280"
        )
        info_seguridad.pack(pady=(10, 0))
    
    def crear_campos_tarjeta(self, parent):
        """Crear campos de tarjeta dentro del scroll - VERSIÓN CORREGIDA"""
        frame_tarjeta = ctk.CTkFrame(parent, fg_color="#ffffff", corner_radius=15, border_width=2, border_color="#e5e7eb")
        frame_tarjeta.pack(fill="x", padx=20, pady=20)
        
        # Título de la sección
        titulo_frame = ctk.CTkFrame(frame_tarjeta, fg_color="#f9fafb", corner_radius=10)
        titulo_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(titulo_frame, text="💳 Datos de la Tarjeta", font=("Arial Bold", 16), text_color="#1f2937").pack(pady=15)
        
        # Contenedor de campos
        campos_frame = ctk.CTkFrame(frame_tarjeta, fg_color="transparent")
        campos_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Número de tarjeta - SIN TEXTVARIABLE
        ctk.CTkLabel(campos_frame, text="Número de Tarjeta *", font=("Arial Bold", 13), text_color="#374151").pack(anchor="w", pady=(15, 5))
        self.entry_num_tarjeta = ctk.CTkEntry(
            campos_frame, 
            placeholder_text="1234 5678 9012 3456", 
            height=45, 
            font=("Arial", 14),
            corner_radius=8
        )
        self.entry_num_tarjeta.pack(fill="x", pady=(0, 15))
        self.entry_num_tarjeta.bind('<KeyRelease>', self.formatear_numero_tarjeta)
        
        # Nombre del titular - SIN TEXTVARIABLE
        ctk.CTkLabel(campos_frame, text="Nombre del Titular *", font=("Arial Bold", 13), text_color="#374151").pack(anchor="w", pady=(0, 5))
        self.entry_titular = ctk.CTkEntry(
            campos_frame, 
            placeholder_text="Como aparece en la tarjeta", 
            height=45, 
            font=("Arial", 14),
            corner_radius=8
        )
        self.entry_titular.pack(fill="x", pady=(0, 15))
        
        # Fila para CVV y Expiración
        fila_datos = ctk.CTkFrame(campos_frame, fg_color="transparent")
        fila_datos.pack(fill="x", pady=(0, 20))
        fila_datos.grid_columnconfigure((0, 1), weight=1)
        
        # CVV - SIN TEXTVARIABLE
        cvv_frame = ctk.CTkFrame(fila_datos, fg_color="transparent")
        cvv_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ctk.CTkLabel(cvv_frame, text="CVV *", font=("Arial Bold", 13), text_color="#374151").pack(anchor="w", pady=(0, 5))
        self.entry_cvv = ctk.CTkEntry(
            cvv_frame, 
            placeholder_text="123", 
            height=45, 
            font=("Arial", 14), 
            show="*",
            corner_radius=8,
            width=120
        )
        self.entry_cvv.pack(fill="x")
        
        # Fecha de Expiración
        exp_frame = ctk.CTkFrame(fila_datos, fg_color="transparent")
        exp_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        ctk.CTkLabel(exp_frame, text="Fecha de Expiración *", font=("Arial Bold", 13), text_color="#374151").pack(anchor="w", pady=(0, 5))
        
        exp_container = ctk.CTkFrame(exp_frame, fg_color="transparent")
        exp_container.pack(fill="x")
        
        # Combo de mes - SIN VARIABLE
        self.combo_mes = ctk.CTkComboBox(
            exp_container, 
            values=[f"{i:02d}" for i in range(1, 13)], 
            width=80, 
            height=45, 
            state="readonly",
            corner_radius=8
        )
        self.combo_mes.pack(side="left", padx=(0, 5))
        self.combo_mes.set("")  # Valor inicial vacío
        
        # Separador
        ctk.CTkLabel(exp_container, text="/", font=("Arial Bold", 18), text_color="#6b7280").pack(side="left", padx=5)
        
        # Combo de año - SIN VARIABLE
        anio_actual = datetime.now().year
        self.combo_anio = ctk.CTkComboBox(
            exp_container, 
            values=[str(anio_actual + i) for i in range(10)], 
            width=100, 
            height=45, 
            state="readonly",
            corner_radius=8
        )
        self.combo_anio.pack(side="left", padx=(5, 0))
        self.combo_anio.set("")  # Valor inicial vacío
    
    def formatear_numero_tarjeta(self, event):
        """Formatear número de tarjeta automáticamente - VERSIÓN CORREGIDA"""
        try:
            # Obtener valor directamente del widget
            valor = self.entry_num_tarjeta.get()
            
            # Quitar todo lo que no sean números
            solo_numeros = re.sub(r'[^\d]', '', valor)
            
            # Limitar a 19 dígitos máximo
            if len(solo_numeros) > 19:
                solo_numeros = solo_numeros[:19]
            
            # Formatear con espacios cada 4 dígitos
            formateado = ' '.join([solo_numeros[i:i+4] for i in range(0, len(solo_numeros), 4)])
            
            # Actualizar solo si cambió
            if formateado != valor:
                # Guardar posición del cursor
                cursor_pos = self.entry_num_tarjeta.index(ctk.INSERT)
                
                # Actualizar valor
                self.entry_num_tarjeta.delete(0, ctk.END)
                self.entry_num_tarjeta.insert(0, formateado)
                
                # Restaurar cursor al final
                self.entry_num_tarjeta.icursor(len(formateado))
                
        except Exception as e:
            print(f"❌ Error formateando tarjeta: {e}")
    
    def crear_resumen(self, parent):
        """Crear panel de resumen SIN botón de pago"""
        resumen_frame = ctk.CTkFrame(parent, fg_color="#f8fafc")
        resumen_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        # Título del resumen
        titulo_frame = ctk.CTkFrame(resumen_frame, fg_color="#ffffff", corner_radius=15)
        titulo_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(titulo_frame, text="📋 Resumen del Pedido", font=("Arial Black", 18), text_color="#1f2937").pack(pady=15)
        
        # Lista de productos (scrollable)
        productos_frame = ctk.CTkScrollableFrame(resumen_frame, height=250, fg_color="#ffffff", corner_radius=15)
        productos_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        try:
            items = self.carrito.obtener_items_agrupados()
            if items:
                for item in items:
                    self.crear_item_resumen(productos_frame, item)
            else:
                ctk.CTkLabel(productos_frame, text="No hay productos", text_color="#6b7280").pack(pady=20)
        except Exception as e:
            print(f"Error cargando productos en resumen: {e}")
            ctk.CTkLabel(productos_frame, text="Error cargando productos", text_color="#dc2626").pack(pady=20)
        
        # Panel de totales
        self.crear_totales(resumen_frame)
        
        # Botones adicionales
        botones_frame = ctk.CTkFrame(resumen_frame, fg_color="transparent")
        botones_frame.pack(fill="x", padx=15, pady=(20, 15))
        
        # Botón volver
        ctk.CTkButton(
            botones_frame, 
            text="🔙 Volver al Carrito", 
            command=self.ir_a_carrito, 
            height=40, 
            font=("Arial", 12, "bold"),
            fg_color="#f59e0b",
            hover_color="#d97706",
            corner_radius=10
        ).pack(fill="x", pady=(0, 5))
        
        # Botón seguir comprando
        ctk.CTkButton(
            botones_frame, 
            text="🛍️ Seguir Comprando", 
            command=self.ir_a_compras, 
            height=35, 
            font=("Arial", 11),
            fg_color="#6b7280",
            hover_color="#4b5563",
            corner_radius=10
        ).pack(fill="x")
    
    def crear_item_resumen(self, parent, item):
        """Crear item individual del resumen"""
        try:
            item_frame = ctk.CTkFrame(parent, fg_color="#f9fafb", corner_radius=10)
            item_frame.pack(fill="x", pady=5, padx=5)
            
            # Contenedor principal del item
            contenido_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            contenido_frame.pack(fill="x", padx=15, pady=12)
            contenido_frame.grid_columnconfigure(0, weight=1)
            
            # Nombre del producto
            nombre_label = ctk.CTkLabel(
                contenido_frame, 
                text=f"{item.producto.nombre}", 
                font=("Arial Bold", 13), 
                text_color="#1f2937",
                anchor="w"
            )
            nombre_label.grid(row=0, column=0, sticky="w", columnspan=2)
            
            # Cantidad y precio unitario
            detalle_frame = ctk.CTkFrame(contenido_frame, fg_color="transparent")
            detalle_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0))
            detalle_frame.grid_columnconfigure(0, weight=1)
            
            cantidad_label = ctk.CTkLabel(
                detalle_frame, 
                text=f"Cantidad: {item.cantidad}", 
                font=("Arial", 11), 
                text_color="#6b7280",
                anchor="w"
            )
            cantidad_label.grid(row=0, column=0, sticky="w")
            
            precio_unit_label = ctk.CTkLabel(
                detalle_frame, 
                text=f"${item.producto.precio:.2f} c/u", 
                font=("Arial", 11), 
                text_color="#6b7280",
                anchor="e"
            )
            precio_unit_label.grid(row=0, column=1, sticky="e")
            
            # Precio total del item
            precio_total = item.producto.precio * item.cantidad
            precio_label = ctk.CTkLabel(
                contenido_frame, 
                text=f"${precio_total:.2f}", 
                font=("Arial Bold", 14), 
                text_color="#059669"
            )
            precio_label.grid(row=0, column=1, rowspan=2, sticky="e", padx=(10, 0))
            
        except Exception as e:
            print(f"Error creando item resumen: {e}")
            # Item de error simple
            error_frame = ctk.CTkFrame(parent, fg_color="#fee2e2")
            error_frame.pack(fill="x", pady=2)
            ctk.CTkLabel(error_frame, text="Error cargando item", text_color="#dc2626").pack(pady=5)
    
    def crear_totales(self, parent):
        """Crear panel de totales del pedido"""
        totales_frame = ctk.CTkFrame(parent, fg_color="#ffffff", corner_radius=15)
        totales_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        try:
            # Calcular totales
            subtotal = self.carrito.calcular_total()
            impuestos = subtotal * 0.16  # IVA 16%
            envio = 50.0 if subtotal < 500 else 0  # Envío gratis si compra > $500
            total = subtotal + impuestos + envio
            
            self.total_final = total
            
            # Lista de conceptos y montos
            conceptos = [
                ("Subtotal:", f"${subtotal:.2f}", False),
                ("IVA (16%):", f"${impuestos:.2f}", False),
                ("Envío:", "GRATIS" if envio == 0 else f"${envio:.2f}", False),
                ("TOTAL:", f"${total:.2f}", True)
            ]
            
            # Crear filas de totales
            for i, (concepto, monto, es_total) in enumerate(conceptos):
                fila_frame = ctk.CTkFrame(totales_frame, fg_color="#f9fafb" if es_total else "transparent")
                fila_frame.pack(fill="x", padx=10, pady=2)
                
                # Configurar grid
                fila_frame.grid_columnconfigure(0, weight=1)
                
                # Estilos según si es el total
                if es_total:
                    font_concepto = ("Arial Bold", 16)
                    font_monto = ("Arial Bold", 16)
                    color_concepto = "#1f2937"
                    color_monto = "#059669"
                    pady_interno = 15
                else:
                    font_concepto = ("Arial", 13)
                    font_monto = ("Arial", 13)
                    color_concepto = "#6b7280"
                    color_monto = "#374151"
                    pady_interno = 8
                
                # Etiqueta del concepto
                concepto_label = ctk.CTkLabel(
                    fila_frame,
                    text=concepto,
                    font=font_concepto,
                    text_color=color_concepto,
                    anchor="w"
                )
                concepto_label.grid(row=0, column=0, sticky="w", padx=(15, 5), pady=pady_interno)
                
                # Etiqueta del monto
                monto_label = ctk.CTkLabel(
                    fila_frame,
                    text=monto,
                    font=font_monto,
                    text_color=color_monto,
                    anchor="e"
                )
                monto_label.grid(row=0, column=1, sticky="e", padx=(5, 15), pady=pady_interno)
                
                # Separador antes del total
                if i == len(conceptos) - 2:  # Antes del último elemento (total)
                    separador = ctk.CTkFrame(totales_frame, height=2, fg_color="#e5e7eb")
                    separador.pack(fill="x", padx=10, pady=5)
                    
        except Exception as e:
            print(f"Error calculando totales: {e}")
            # Totales de error
            error_label = ctk.CTkLabel(
                totales_frame, 
                text="Error calculando totales", 
                text_color="#dc2626"
            )
            error_label.pack(pady=20)
            self.total_final = 0
    
    def validar_formulario(self):
        """Validar todos los campos del formulario - VERSIÓN CORREGIDA"""
        errores = []
        
        try:
            # Obtener valores directamente de los widgets en lugar de las variables
            num_tarjeta = self.entry_num_tarjeta.get().strip().replace(" ", "")
            titular = self.entry_titular.get().strip()
            cvv = self.entry_cvv.get().strip()
            mes = self.combo_mes.get().strip()
            anio = self.combo_anio.get().strip()
            
            print(f"🔍 DEBUG Validación:")
            print(f"   - Número tarjeta: '{num_tarjeta}' (len: {len(num_tarjeta)})")
            print(f"   - Titular: '{titular}' (len: {len(titular)})")
            print(f"   - CVV: '{cvv}' (len: {len(cvv)})")
            print(f"   - Mes: '{mes}'")
            print(f"   - Año: '{anio}'")
            
            # Validar número de tarjeta
            if not num_tarjeta:
                errores.append("• El número de tarjeta es requerido")
            elif not re.match(r'^\d{13,19}$', num_tarjeta):
                errores.append("• El número de tarjeta debe tener entre 13 y 19 dígitos")
            
            # Validar titular
            if not titular:
                errores.append("• El nombre del titular es requerido")
            elif len(titular) < 3:
                errores.append("• El nombre del titular debe tener al menos 3 caracteres")
            
            # Validar CVV
            if not cvv:
                errores.append("• El CVV es requerido")
            elif not re.match(r'^\d{3,4}$', cvv):
                errores.append("• El CVV debe tener 3 o 4 dígitos")
            
            # Validar fecha de expiración
            if not mes or not anio:
                errores.append("• La fecha de expiración es requerida")
            else:
                try:
                    mes_int = int(mes)
                    anio_int = int(anio)
                    fecha_actual = datetime.now()
                    
                    # Verificar que no esté vencida
                    if anio_int < fecha_actual.year or (anio_int == fecha_actual.year and mes_int < fecha_actual.month):
                        errores.append("• La tarjeta está vencida")
                        
                except ValueError:
                    errores.append("• Fecha de expiración inválida")
            
            # Debug de errores
            if errores:
                print(f"❌ Errores encontrados: {errores}")
            else:
                print("✅ Validación exitosa")
            
            # Mostrar errores si los hay
            if errores:
                messagebox.showerror("Errores en el Formulario", "\n".join(errores))
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            messagebox.showerror("Error", "Error validando el formulario")
            return False
    
    def finalizar_compra(self):
        """Procesar el pago y finalizar la compra"""
        if self.procesando:
            return
        
        # Validar formulario
        if not self.validar_formulario():
            return
        
        try:
            # Cambiar estado del botón
            self.procesando = True
            self.btn_finalizar.configure(
                text="🔄 Procesando Pago...", 
                state="disabled",
                fg_color="#6b7280"
            )
            
            # Actualizar interfaz para mostrar el cambio
            self.update()
            
            # Simular tiempo de procesamiento
            self.after(1000, self._procesar_pago)
            
        except Exception as e:
            print(f"❌ Error iniciando procesamiento: {e}")
            self._restaurar_boton()
            messagebox.showerror("Error", f"Error procesando la compra: {str(e)}")
    
    def _procesar_pago(self):
        """Procesar el pago (segunda parte del proceso) - VERSIÓN COMPLETA CON PERSISTENCIA"""
        try:
            # Generar ID de orden único
            self.orden_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            
            # Información del pago
            fecha_actual = datetime.now()
            numero_tarjeta_completo = self.entry_num_tarjeta.get().replace(" ", "")
            numero_enmascarado = "****" + numero_tarjeta_completo[-4:]
            
            # ✅ OBTENER CLIENTE ID CORRECTAMENTE
            if hasattr(self.sistema, 'cliente_autenticado') and self.sistema.cliente_autenticado:
                if hasattr(self.sistema.cliente_autenticado, 'id'):
                    cliente_id = self.sistema.cliente_autenticado.id
                elif hasattr(self.sistema.cliente_autenticado, 'nombre'):
                    cliente_id = self.sistema.cliente_autenticado.nombre
                else:
                    cliente_id = "CLIENTE_AUTENTICADO"
            else:
                cliente_id = "GUEST"
            
            # ✅ OBTENER ITEMS DEL CARRITO ANTES DE LIMPIAR
            items_carrito = self.carrito.obtener_items_agrupados()
            productos_detalle = []
            
            print(f"🔍 Procesando {len(items_carrito)} tipos de productos en el carrito...")
            
            # ✅ ACTUALIZAR STOCK DE PRODUCTOS Y CREAR DETALLE
            for item in items_carrito:
                try:
                    producto = item.producto
                    cantidad = item.cantidad
                    
                    print(f"📦 Procesando: {cantidad}x {producto.nombre}")
                    
                    # ✅ ACTUALIZAR STOCK EN EL INVENTARIO
                    if hasattr(self.sistema, 'inventario'):
                        # Usar reducir_stock que es más apropiado
                        stock_reducido = self.sistema.inventario.reducir_stock(producto.id, cantidad)
                        if stock_reducido:
                            print(f"📊 Stock reducido para {producto.nombre}: -{cantidad} unidades")
                        else:
                            print(f"⚠️ No se pudo reducir stock para {producto.nombre}")
                    
                    # ✅ AGREGAR AL DETALLE DE PRODUCTOS
                    productos_detalle.append({
                        'producto_id': producto.id,
                        'nombre': producto.nombre,
                        'cantidad': cantidad,
                        'precio_unitario': producto.precio,
                        'subtotal': producto.precio * cantidad
                    })
                    
                except Exception as e:
                    print(f"⚠️ Error procesando producto {item}: {e}")
            
            # ✅ CREAR DATOS COMPLETOS DE LA ORDEN
            orden_data = {
                'id': self.orden_id,
                'fecha': fecha_actual.strftime("%Y-%m-%d %H:%M:%S"),
                'cliente_id': cliente_id,
                'titular_tarjeta': self.entry_titular.get(),
                'numero_tarjeta': numero_enmascarado,
                'metodo_pago': 'Tarjeta de Crédito',
                'subtotal': self.carrito.calcular_total(),
                'impuestos': self.carrito.calcular_total() * 0.16,
                'total': self.total_final,
                'estado': 'Pagado',
                'cantidad_productos': len(items_carrito),
                'productos_detalle': productos_detalle
            }
            
            # ✅ CREAR DATOS DEL PAGO
            pago_data = {
                'id': f"PAY-{uuid.uuid4().hex[:8].upper()}",
                'orden_id': self.orden_id,
                'fecha': fecha_actual.strftime("%Y-%m-%d %H:%M:%S"),
                'metodo': 'Tarjeta de Crédito',
                'monto': self.total_final,
                'estado': 'Completado',
                'referencia': numero_enmascarado
            }
            
            # ✅ AGREGAR A ESTRUCTURAS DEL SISTEMA
            if hasattr(self.sistema, 'pila_ordenes'):
                orden_obj = type('Orden', (), orden_data)()
                self.sistema.pila_ordenes.push(orden_obj)
                print(f"📊 Orden agregada a la pila: {self.orden_id}")
            
            if hasattr(self.sistema, 'cola_pagos'):
                pago_obj = type('Pago', (), pago_data)()
                self.sistema.cola_pagos.enqueue(pago_obj)
                print(f"💳 Pago agregado a la cola: {pago_data['id']}")
            
            # ✅ GUARDAR EN ARCHIVOS CSV
            try:
                self.guardar_orden_csv(orden_data)
                self.guardar_pago_csv(pago_data)
                self.guardar_transaccion_csv(orden_data, pago_data)
                print("💾 Datos guardados en archivos CSV exitosamente")
            except Exception as e:
                print(f"⚠️ Error guardando en CSV: {e}")
            
            # ✅ LIMPIAR CARRITO DESPUÉS DE PROCESAR TODO
            self.carrito.limpiar()
            print(f"🛒 Carrito limpiado después de la compra")
            
            # ✅ ACTUALIZAR CONTADOR DEL CARRITO EN LA INTERFAZ PRINCIPAL
            if hasattr(self, 'master') and hasattr(self.master, 'actualizar_contador_carrito'):
                self.master.actualizar_contador_carrito()
                print("🔄 Contador del carrito actualizado en interfaz principal")
            
            # ✅ LOGS DETALLADOS DE ÉXITO
            print(f"\n✅ COMPRA PROCESADA EXITOSAMENTE:")
            print(f"   🆔 Orden: {self.orden_id}")
            print(f"   💰 Total: ${self.total_final:.2f}")
            print(f"   💳 Tarjeta: {numero_enmascarado}")
            print(f"   👤 Cliente: {cliente_id}")
            print(f"   📦 Productos: {len(productos_detalle)} tipos")
            print(f"   📊 Stock actualizado para {len(productos_detalle)} productos")
            print(f"   💾 Datos persistidos en CSV y estructuras")
            
            # Mostrar confirmación
            self.mostrar_confirmacion()
            
        except Exception as e:
            print(f"❌ Error procesando pago: {e}")
            import traceback
            traceback.print_exc()
            self._restaurar_boton()
            messagebox.showerror("Error de Pago", f"Error procesando el pago: {str(e)}")
    
    def _restaurar_boton(self):
        """Restaurar estado normal del botón"""
        self.procesando = False
        if hasattr(self, 'btn_finalizar') and self.btn_finalizar.winfo_exists():
            self.btn_finalizar.configure(
                text="💳 PAGAR AHORA", 
                state="normal",
                fg_color="#10b981"
            )
    
    def mostrar_confirmacion(self):
        """Mostrar pantalla de confirmación de compra exitosa"""
        # Limpiar toda la interfaz
        for widget in self.winfo_children():
            widget.destroy()
        
        # Frame principal de confirmación
        confirmacion_frame = ctk.CTkFrame(self, fg_color="#ecfdf5", corner_radius=20)
        confirmacion_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Icono de éxito
        ctk.CTkLabel(confirmacion_frame, text="🎉", font=("Arial", 100)).pack(pady=(60, 20))
        
        # Título de éxito
        ctk.CTkLabel(
            confirmacion_frame, 
            text="¡Compra Realizada Exitosamente!", 
            font=("Arial Black", 32), 
            text_color="#065f46"
        ).pack(pady=(0, 10))
        
        # Subtítulo
        ctk.CTkLabel(
            confirmacion_frame, 
            text="Tu pedido ha sido procesado y confirmado", 
            font=("Arial", 16), 
            text_color="#047857"
        ).pack(pady=(0, 30))
        
        # Panel de detalles
        detalles_frame = ctk.CTkFrame(confirmacion_frame, fg_color="#ffffff", corner_radius=15)
        detalles_frame.pack(padx=60, pady=(0, 30))
        
        # Título de detalles
        ctk.CTkLabel(
            detalles_frame, 
            text="📋 Detalles de tu Orden", 
            font=("Arial Bold", 18), 
            text_color="#1f2937"
        ).pack(pady=(20, 15))
        
        # Información de la orden
        info_frame = ctk.CTkFrame(detalles_frame, fg_color="#f9fafb")
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        detalles_texto = f"""
🔖 Número de Orden: {self.orden_id}
💰 Total Pagado: ${self.total_final:.2f}
💳 Método de Pago: Tarjeta de Crédito
📅 Fecha: {datetime.now().strftime("%d/%m/%Y %H:%M")}
📧 Se ha enviado un recibo por email
        """.strip()
        
        ctk.CTkLabel(
            info_frame, 
            text=detalles_texto, 
            font=("Arial", 14), 
            text_color="#374151",
            justify="left"
        ).pack(pady=20)
        
        # Botones de acción
        botones_frame = ctk.CTkFrame(confirmacion_frame, fg_color="transparent")
        botones_frame.pack(pady=(0, 40))
        
        # Botón principal
        ctk.CTkButton(
            botones_frame, 
            text="🛍️ Seguir Comprando", 
            command=self.ir_a_compras, 
            font=("Arial Bold", 16), 
            width=220, 
            height=50,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            corner_radius=25
        ).pack(side="left", padx=10)
        
        # Botón secundario
        ctk.CTkButton(
            botones_frame, 
            text="📋 Ver Historial", 
            command=self.ir_a_historial, 
            font=("Arial Bold", 16), 
            width=220, 
            height=50,
            fg_color="#059669",
            hover_color="#047857",
            corner_radius=25
        ).pack(side="left", padx=10)
        
        # Mensaje adicional
        ctk.CTkLabel(
            confirmacion_frame, 
            text="¡Gracias por tu compra! Recibirás una confirmación por email.", 
            font=("Arial", 12), 
            text_color="#6b7280"
        ).pack()
    
    def ir_a_compras(self):
        """Navegar a la tienda"""
        if hasattr(self.master, 'mostrar_compras'):
            self.master.mostrar_compras()
    
    def ir_a_carrito(self):
        """Navegar al carrito"""
        if hasattr(self.master, 'mostrar_carrito'):
            self.master.mostrar_carrito()
    
    def ir_a_historial(self):
        """Navegar al historial"""
        if hasattr(self.master, 'mostrar_historial'):
            self.master.mostrar_historial()
        else:
            # Fallback si no existe el método
            self.ir_a_compras()
    
    def guardar_orden_csv(self, orden_data):
        """✅ GUARDAR ORDEN EN ARCHIVO CSV"""
        try:
            import csv
            import os
            
            # Ruta del archivo de órdenes (CORREGIDA: 3 niveles arriba desde Src/Interfaz/)
            ordenes_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Data', 'ordenes.csv')
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(ordenes_file), exist_ok=True)
            
            # Verificar si el archivo existe para escribir header
            file_exists = os.path.exists(ordenes_file) and os.path.getsize(ordenes_file) > 0
            
            with open(ordenes_file, 'a', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'fecha', 'cliente_id', 'titular_tarjeta', 'metodo_pago', 
                             'subtotal', 'impuestos', 'total', 'estado', 'cantidad_productos']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Escribir header si es archivo nuevo
                if not file_exists:
                    writer.writeheader()
                
                # Escribir datos de la orden
                orden_csv = {
                    'id': orden_data['id'],
                    'fecha': orden_data['fecha'],
                    'cliente_id': orden_data['cliente_id'],
                    'titular_tarjeta': orden_data['titular_tarjeta'],
                    'metodo_pago': orden_data['metodo_pago'],
                    'subtotal': orden_data['subtotal'],
                    'impuestos': orden_data['impuestos'],
                    'total': orden_data['total'],
                    'estado': orden_data['estado'],
                    'cantidad_productos': orden_data['cantidad_productos']
                }
                writer.writerow(orden_csv)
                
            print(f"📁 Orden {orden_data['id']} guardada en ordenes.csv")
            
        except Exception as e:
            print(f"❌ Error guardando orden en CSV: {e}")
            raise
    
    def guardar_pago_csv(self, pago_data):
        """✅ GUARDAR PAGO EN ARCHIVO CSV"""
        try:
            import csv
            import os
            
            # Ruta del archivo de pagos (CORREGIDA: 3 niveles arriba desde Src/Interfaz/)
            pagos_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Data', 'pagos.csv')
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(pagos_file), exist_ok=True)
            
            # Verificar si el archivo existe para escribir header
            file_exists = os.path.exists(pagos_file) and os.path.getsize(pagos_file) > 0
            
            with open(pagos_file, 'a', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'orden_id', 'fecha', 'metodo', 'monto', 'estado', 'referencia']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Escribir header si es archivo nuevo
                if not file_exists:
                    writer.writeheader()
                
                # Escribir datos del pago
                writer.writerow(pago_data)
                
            print(f"💳 Pago {pago_data['id']} guardado en pagos.csv")
            
        except Exception as e:
            print(f"❌ Error guardando pago en CSV: {e}")
            raise
    
    def guardar_transaccion_csv(self, orden_data, pago_data):
        """✅ GUARDAR TRANSACCIÓN COMPLETA EN ARCHIVO CSV"""
        try:
            import csv
            import os
            
            # Ruta del archivo de transacciones (CORREGIDA: 3 niveles arriba desde Src/Interfaz/)
            transacciones_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Data', 'transacciones.csv')
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(transacciones_file), exist_ok=True)
            
            # Verificar si el archivo existe para escribir header
            file_exists = os.path.exists(transacciones_file) and os.path.getsize(transacciones_file) > 0
            
            with open(transacciones_file, 'a', newline='', encoding='utf-8') as file:
                fieldnames = ['transaccion_id', 'orden_id', 'pago_id', 'fecha', 'cliente_id', 
                             'total', 'metodo_pago', 'estado', 'productos_cantidad']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Escribir header si es archivo nuevo
                if not file_exists:
                    writer.writeheader()
                
                # Escribir datos de la transacción
                transaccion_data = {
                    'transaccion_id': f"TXN-{uuid.uuid4().hex[:8].upper()}",
                    'orden_id': orden_data['id'],
                    'pago_id': pago_data['id'],
                    'fecha': orden_data['fecha'],
                    'cliente_id': orden_data['cliente_id'],
                    'total': orden_data['total'],
                    'metodo_pago': orden_data['metodo_pago'],
                    'estado': 'Completada',
                    'productos_cantidad': orden_data['cantidad_productos']
                }
                writer.writerow(transaccion_data)
                
            print(f"📋 Transacción completa guardada en transacciones.csv")
            
        except Exception as e:
            print(f"❌ Error guardando transacción en CSV: {e}")
            raise