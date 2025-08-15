"""
Interfaz Gráfica para el Sistema de E-commerce
Implementa los puntos 1-6 del flujo de compra
Autor: Sistema de E-commerce Universitario
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import sys
import os
from datetime import datetime

# Agregar paths para importar nuestras clases
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Para llegar a Src/
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estructuras'))

# Importar las clases existentes del proyecto
from Producto import Producto
from Cliente import Cliente
from Carrito import Carrito
from Cola import Cola

class ColaPagos:
    """Cola FIFO para el procesamiento de pagos usando la estructura Cola original."""
    
    def __init__(self):
        self.cola = Cola()  # Usar la Cola original implementada
    
    def agregar_pago(self, pago):
        """Agrega un pago al final de la cola."""
        return self.cola.enqueue(pago)
    
    def procesar_pago(self):
        """Procesa el primer pago de la cola (FIFO)."""
        return self.cola.dequeue()
    
    def esta_vacia(self):
        """Verifica si la cola está vacía."""
        return self.cola.esta_vacia()
    
    def obtener_siguiente(self):
        """Obtiene el siguiente pago sin procesarlo."""
        return self.cola.front()
    
    def tamaño(self):
        """Obtiene el tamaño de la cola."""
        return self.cola.obtener_tamaño()

class PagoOnline:
    """Clase para representar un pago online (Punto 6)."""
    
    def __init__(self, id_pago, monto, metodo="tarjeta"):
        self.id_pago = id_pago
        self.monto = monto
        self.metodo = metodo
        self.estado = "Pendiente"
        self.fecha = datetime.now()
        self.codigo_autorizacion = None
        self.mensaje = ""

class Interfaz:
    """Interfaz gráfica principal del sistema de e-commerce."""
    
    def __init__(self):
        self.window = tk.Tk()  # Corregir Tk() en lugar de tk()
        self.window.title("Sistema E-commerce - Puntos 1-6")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f0f0f0')
        
        # Datos del sistema
        self.productos = self._crear_productos_demo()
        self.cliente_actual = Cliente("CLI001", "Usuario Demo", "demo@email.com", "555-1234")
        self.carrito = Carrito(self.cliente_actual.id_cliente)
        self.cola_pagos = ColaPagos()
        
        # Variables de control
        self.producto_seleccionado = None
        self.contador_pagos = 0
        
        # Crear interfaz
        self._crear_interfaz()
        self._mostrar_productos()
        self._log("🚀 Sistema iniciado - Puntos 1-6 del flujo de compra")
    
    def _crear_productos_demo(self):
        """Crea productos de demostración para el catálogo."""
        productos = [
            Producto("P001", "Laptop Gaming ASUS ROG", 1500.00, "Electrónicos", 5),
            Producto("P002", "Mouse Logitech G502", 45.99, "Periféricos", 20),
            Producto("P003", "Teclado Mecánico RGB", 89.99, "Periféricos", 15),
            Producto("P004", "Monitor 4K Samsung 27''", 350.00, "Monitores", 8),
            Producto("P005", "Auriculares Sony WH-1000XM4", 120.00, "Audio", 12),
            Producto("P006", "Webcam Logitech C920", 75.00, "Accesorios", 18),
            Producto("P007", "SSD Samsung 1TB", 180.00, "Almacenamiento", 10),
            Producto("P008", "Memoria RAM Corsair 16GB", 95.00, "Componentes", 25)
        ]
        return productos
    
    def _crear_interfaz(self):
        """Crea todos los componentes de la interfaz gráfica."""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        titulo = ttk.Label(main_frame, text="🛒 Sistema E-commerce - Flujo de Compra (Puntos 1-6)", 
                          font=('Arial', 16, 'bold'))
        titulo.pack(pady=(0, 20))
        
        # Frame superior para catálogo y carrito
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Panel del catálogo (Punto 1: Select Item)
        self._crear_panel_catalogo(top_frame)
        
        # Panel del carrito (Puntos 2-3: Cart Item, Item Details)
        self._crear_panel_carrito(top_frame)
        
        # Frame inferior para checkout y pagos
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel de checkout (Punto 4: Checkout)
        self._crear_panel_checkout(bottom_frame)
        
        # Panel de pagos (Puntos 5-6: Collect Payment, Post Payment)
        self._crear_panel_pagos(bottom_frame)
        
        # Panel de log del sistema
        self._crear_panel_log(main_frame)
    
    def _crear_panel_catalogo(self, parent):
        """Crea el panel del catálogo de productos (Punto 1: Select Item)."""
        # Frame del catálogo
        catalogo_frame = ttk.LabelFrame(parent, text="📋 Punto 1: Select Item - Catálogo de Productos", padding="10")
        catalogo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Treeview para mostrar productos
        columns = ('ID', 'Nombre', 'Precio', 'Categoría', 'Stock')
        self.tree_productos = ttk.Treeview(catalogo_frame, columns=columns, show='headings', height=10)
        
        # Configurar columnas
        for col in columns:
            self.tree_productos.heading(col, text=col)
        
        self.tree_productos.column('ID', width=50)
        self.tree_productos.column('Nombre', width=180)
        self.tree_productos.column('Precio', width=70)
        self.tree_productos.column('Categoría', width=100)
        self.tree_productos.column('Stock', width=50)
        
        self.tree_productos.pack(fill=tk.BOTH, expand=True)
        
        # Frame para controles
        controles_frame = ttk.Frame(catalogo_frame)
        controles_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Control de cantidad
        ttk.Label(controles_frame, text="Cantidad:").pack(side=tk.LEFT)
        self.cantidad_var = tk.StringVar(value="1")
        cantidad_spin = ttk.Spinbox(controles_frame, from_=1, to=10, width=5, textvariable=self.cantidad_var)
        cantidad_spin.pack(side=tk.LEFT, padx=(5, 10))
        
        # Botón agregar al carrito
        btn_agregar = ttk.Button(controles_frame, text="🛒 Agregar al Carrito", 
                                command=self._agregar_al_carrito)
        btn_agregar.pack(side=tk.LEFT)
        
        # Evento de selección
        self.tree_productos.bind('<<TreeviewSelect>>', self._on_producto_select)
    
    def _crear_panel_carrito(self, parent):
        """Crea el panel del carrito (Puntos 2-3: Cart Item, Item Details)."""
        carrito_frame = ttk.LabelFrame(parent, text="🛒 Puntos 2-3: Cart Item & Item Details", padding="10")
        carrito_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Treeview para items del carrito
        columns_carrito = ('Producto', 'Cantidad', 'Precio Unit.', 'Subtotal')
        self.tree_carrito = ttk.Treeview(carrito_frame, columns=columns_carrito, show='headings', height=8)
        
        for col in columns_carrito:
            self.tree_carrito.heading(col, text=col)
        
        self.tree_carrito.column('Producto', width=150)
        self.tree_carrito.column('Cantidad', width=70)
        self.tree_carrito.column('Precio Unit.', width=80)
        self.tree_carrito.column('Subtotal', width=80)
        
        self.tree_carrito.pack(fill=tk.BOTH, expand=True)
        
        # Frame para total
        total_frame = ttk.Frame(carrito_frame)
        total_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.total_label = ttk.Label(total_frame, text="Total: $0.00", 
                                   font=('Arial', 12, 'bold'), foreground='blue')
        self.total_label.pack(side=tk.RIGHT)
        
        # Frame para botones del carrito
        botones_frame = ttk.Frame(carrito_frame)
        botones_frame.pack(fill=tk.X, pady=(5, 0))
        
        btn_actualizar = ttk.Button(botones_frame, text="📝 Actualizar", 
                                   command=self._actualizar_cantidad)
        btn_actualizar.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_eliminar = ttk.Button(botones_frame, text="🗑️ Eliminar", 
                                 command=self._eliminar_del_carrito)
        btn_eliminar.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_limpiar = ttk.Button(botones_frame, text="🧹 Limpiar Todo", 
                                command=self._limpiar_carrito)
        btn_limpiar.pack(side=tk.RIGHT)
    
    def _crear_panel_checkout(self, parent):
        """Crea el panel de checkout (Punto 4: Checkout)."""
        checkout_frame = ttk.LabelFrame(parent, text="💳 Punto 4: Checkout", padding="10")
        checkout_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Información del cliente
        cliente_info = ttk.Frame(checkout_frame)
        cliente_info.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(cliente_info, text="👤 Cliente:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(cliente_info, text=f"Nombre: {self.cliente_actual.nombre}").pack(anchor=tk.W)
        ttk.Label(cliente_info, text=f"Email: {self.cliente_actual.email}").pack(anchor=tk.W)
        
        # Método de pago
        metodo_frame = ttk.Frame(checkout_frame)
        metodo_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(metodo_frame, text="💳 Método de Pago:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.metodo_pago = tk.StringVar(value="tarjeta")
        ttk.Radiobutton(metodo_frame, text="Tarjeta de Crédito", 
                       variable=self.metodo_pago, value="tarjeta").pack(anchor=tk.W)
        ttk.Radiobutton(metodo_frame, text="Efectivo", 
                       variable=self.metodo_pago, value="efectivo").pack(anchor=tk.W)
        
        # Resumen del carrito
        resumen_frame = ttk.Frame(checkout_frame)
        resumen_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(resumen_frame, text="📋 Resumen:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.resumen_text = tk.Text(resumen_frame, height=5, width=30)
        self.resumen_text.pack(fill=tk.BOTH, expand=True)
        
        # Botón de checkout
        btn_checkout = ttk.Button(checkout_frame, text="🛒 Proceder al Checkout", 
                                 command=self._procesar_checkout)
        btn_checkout.pack(fill=tk.X, pady=(10, 0))
    
    def _crear_panel_pagos(self, parent):
        """Crea el panel de pagos (Puntos 5-6: Collect Payment, Post Payment)."""
        pagos_frame = ttk.LabelFrame(parent, text="🏦 Puntos 5-6: Collect & Post Payment", padding="10")
        pagos_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Cola de pagos (Punto 5)
        ttk.Label(pagos_frame, text="📋 Cola de Pagos (FIFO):", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.lista_pagos = tk.Listbox(pagos_frame, height=6)
        self.lista_pagos.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Botones de procesamiento
        botones_pagos = ttk.Frame(pagos_frame)
        botones_pagos.pack(fill=tk.X)
        
        btn_procesar = ttk.Button(botones_pagos, text="🏦 Procesar Siguiente Pago", 
                                 command=self._procesar_pago)
        btn_procesar.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_procesar_todos = ttk.Button(botones_pagos, text="⚡ Procesar Todos", 
                                       command=self._procesar_todos_pagos)
        btn_procesar_todos.pack(side=tk.RIGHT)
        
        # Estadísticas
        stats_frame = ttk.Frame(pagos_frame)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(stats_frame, text="📊 Estadísticas:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.stats_label = ttk.Label(stats_frame, text="Pagos procesados: 0\nTotal procesado: $0.00")
        self.stats_label.pack(anchor=tk.W)
    
    def _crear_panel_log(self, parent):
        """Crea el panel de log del sistema."""
        log_frame = ttk.LabelFrame(parent, text="📋 Log del Sistema", padding="5")
        log_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6)
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def _mostrar_productos(self):
        """Muestra los productos en el catálogo."""
        for producto in self.productos:
            estado = "✅" if producto.stock > 0 else "❌"
            self.tree_productos.insert('', 'end', values=(
                producto.id_producto,
                f"{estado} {producto.nombre}",
                f"${producto.precio:.2f}",
                producto.categoria,
                producto.stock
            ))
    
    def _on_producto_select(self, event):
        """Maneja la selección de un producto."""
        selection = self.tree_productos.selection()
        if selection:
            item = self.tree_productos.item(selection[0])
            producto_id = item['values'][0]
            self.producto_seleccionado = next(p for p in self.productos if p.id_producto == producto_id)
            self._log(f"📋 Punto 1: Producto seleccionado - {self.producto_seleccionado.nombre}")
    
    def _agregar_al_carrito(self):
        """Agrega el producto seleccionado al carrito (Punto 2: Cart Item)."""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor selecciona un producto del catálogo")
            return
        
        try:
            cantidad = int(self.cantidad_var.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
            
            if cantidad > self.producto_seleccionado.stock:
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {self.producto_seleccionado.stock}")
                return
            
            # Agregar al carrito
            self.carrito.agregar_producto(self.producto_seleccionado, cantidad)
            
            # Reducir stock
            self.producto_seleccionado.reducir_stock(cantidad)
            
            # Actualizar visualizaciones
            self._actualizar_carrito()
            self._actualizar_catalogo()
            self._actualizar_resumen_checkout()
            
            self._log(f"🛒 Punto 2: Item agregado al carrito - {self.producto_seleccionado.nombre} x{cantidad}")
            
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")
    
    def _actualizar_carrito(self):
        """Actualiza la visualización del carrito (Punto 3: Item Details)."""
        # Limpiar carrito actual
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        
        # Agregar items usando la clase Carrito original
        productos_carrito = self.carrito.obtener_productos()
        for item in productos_carrito:
            self.tree_carrito.insert('', 'end', values=(
                item.producto.nombre,
                item.cantidad,
                f"${item.producto.precio:.2f}",
                f"${item.subtotal:.2f}"
            ))
        
        # Actualizar total
        self.total_label.config(text=f"Total: ${self.carrito.obtener_total():.2f}")
        
        if not self.carrito.esta_vacio():
            self._log(f"📋 Punto 3: Detalles del carrito actualizados - {self.carrito.obtener_cantidad_items()} items, Total: ${self.carrito.obtener_total():.2f}")
    
    def _actualizar_catalogo(self):
        """Actualiza la visualización del catálogo."""
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        self._mostrar_productos()
    
    def _actualizar_resumen_checkout(self):
        """Actualiza el resumen para checkout."""
        self.resumen_text.delete(1.0, tk.END)
        
        if self.carrito.esta_vacio():
            self.resumen_text.insert(tk.END, "Carrito vacío")
        else:
            productos_carrito = self.carrito.obtener_productos()
            texto = f"Items: {self.carrito.obtener_cantidad_items()}\n"
            texto += f"Total: ${self.carrito.obtener_total():.2f}\n\n"
            texto += "Productos:\n"
            for item in productos_carrito:
                texto += f"• {item.producto.nombre} x{item.cantidad}\n"
            self.resumen_text.insert(tk.END, texto)
    
    def _actualizar_cantidad(self):
        """Actualiza la cantidad de un item en el carrito."""
        selection = self.tree_carrito.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un item del carrito")
            return
        
        item_values = self.tree_carrito.item(selection[0])['values']
        nombre_producto = item_values[0]
        
        # Buscar item en carrito usando la clase original
        productos_carrito = self.carrito.obtener_productos()
        item_carrito = None
        for item in productos_carrito:
            if item.producto.nombre == nombre_producto:
                item_carrito = item
                break
        
        if not item_carrito:
            return
        
        nueva_cantidad = simpledialog.askinteger("Actualizar Cantidad", 
                                                f"Nueva cantidad para {nombre_producto}:",
                                                initialvalue=item_carrito.cantidad,
                                                minvalue=0, maxvalue=50)
        
        if nueva_cantidad is not None:
            if nueva_cantidad == 0:
                self._eliminar_item_especifico(item_carrito.producto.id_producto)
            else:
                diferencia = nueva_cantidad - item_carrito.cantidad
                if diferencia > 0:
                    if diferencia > item_carrito.producto.stock:
                        messagebox.showerror("Error", "Stock insuficiente")
                        return
                    item_carrito.producto.reducir_stock(diferencia)
                else:
                    item_carrito.producto.agregar_stock(abs(diferencia))
                
                self.carrito.actualizar_cantidad(item_carrito.producto.id_producto, nueva_cantidad)
                
                self._actualizar_carrito()
                self._actualizar_catalogo()
                self._actualizar_resumen_checkout()
                self._log(f"📝 Cantidad actualizada: {nombre_producto} → {nueva_cantidad}")
    
    def _eliminar_del_carrito(self):
        """Elimina un item del carrito."""
        selection = self.tree_carrito.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un item del carrito")
            return
        
        item_values = self.tree_carrito.item(selection[0])['values']
        nombre_producto = item_values[0]
        
        # Buscar y eliminar usando la clase original
        productos_carrito = self.carrito.obtener_productos()
        for item in productos_carrito:
            if item.producto.nombre == nombre_producto:
                # Devolver stock
                item.producto.agregar_stock(item.cantidad)
                self._eliminar_item_especifico(item.producto.id_producto)
                break
        
        self._actualizar_carrito()
        self._actualizar_catalogo()
        self._actualizar_resumen_checkout()
        self._log(f"🗑️ Eliminado del carrito: {nombre_producto}")
    
    def _eliminar_item_especifico(self, id_producto):
        """Elimina un item específico del carrito."""
        self.carrito.eliminar_producto(id_producto)
    
    def _limpiar_carrito(self):
        """Limpia todo el carrito."""
        if self.carrito.esta_vacio():
            messagebox.showinfo("Info", "El carrito ya está vacío")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de limpiar todo el carrito?"):
            # Devolver stock usando la clase original
            productos_carrito = self.carrito.obtener_productos()
            for item in productos_carrito:
                item.producto.agregar_stock(item.cantidad)
            
            self.carrito.limpiar()
            self._actualizar_carrito()
            self._actualizar_catalogo()
            self._actualizar_resumen_checkout()
            self._log("🧹 Carrito limpiado completamente")
    
    def _procesar_checkout(self):
        """Procesa el checkout y crea pago (Punto 4: Checkout)."""
        if self.carrito.esta_vacio():
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        # Crear pago
        self.contador_pagos += 1
        id_pago = f"PAY{self.contador_pagos:03d}"
        pago = PagoOnline(id_pago, self.carrito.obtener_total(), self.metodo_pago.get())
        
        # Agregar a cola de pagos (Punto 5)
        self.cola_pagos.agregar_pago(pago)
        
        # Actualizar lista de pagos
        self.lista_pagos.insert(tk.END, f"⏳ {pago.id_pago} - ${pago.monto:.2f} ({pago.metodo})")
        
        # Limpiar carrito
        self.carrito.limpiar()
        self._actualizar_carrito()
        self._actualizar_resumen_checkout()
        
        self._log(f"💳 Punto 4: Checkout completado - {pago.id_pago} por ${pago.monto:.2f}")
        self._log(f"📋 Punto 5: Pago agregado a cola de procesamiento")
        
        messagebox.showinfo("Checkout Exitoso", 
                           f"Checkout completado!\n\nPago {pago.id_pago} creado por ${pago.monto:.2f}\nMétodo: {pago.metodo.title()}")
    
    def _procesar_pago(self):
        """Procesa el siguiente pago en la cola (Punto 6: Post Payment)."""
        if self.cola_pagos.esta_vacia():
            messagebox.showinfo("Info", "No hay pagos pendientes en la cola")
            return
        
        # Obtener el siguiente pago (FIFO)
        pago = self.cola_pagos.procesar_pago()
        
        # Simular procesamiento bancario
        import random
        if random.random() < 0.85:  # 85% probabilidad de aprobación
            pago.estado = "Aprobado"
            pago.codigo_autorizacion = f"AUTH{random.randint(100000, 999999)}"
            pago.mensaje = "Transacción aprobada exitosamente"
            self._log(f"✅ Punto 6: Pago {pago.id_pago} APROBADO - Código: {pago.codigo_autorizacion}")
            messagebox.showinfo("Pago Aprobado", 
                               f"Pago {pago.id_pago} aprobado\n\nCódigo de autorización: {pago.codigo_autorizacion}\nMonto: ${pago.monto:.2f}")
        else:
            pago.estado = "Rechazado"
            motivos = ["Fondos insuficientes", "Tarjeta bloqueada", "Error del banco", "Límite excedido"]
            pago.mensaje = random.choice(motivos)
            self._log(f"❌ Punto 6: Pago {pago.id_pago} RECHAZADO - {pago.mensaje}")
            messagebox.showerror("Pago Rechazado", 
                                f"Pago {pago.id_pago} rechazado\n\nMotivo: {pago.mensaje}\nMonto: ${pago.monto:.2f}")
        
        # Actualizar lista de pagos
        if self.lista_pagos.size() > 0:
            self.lista_pagos.delete(0)
        
        # Actualizar estadísticas
        self._actualizar_estadisticas()
        
        self._log(f"🏦 Procesamiento bancario completado para {pago.id_pago}")
    
    def _procesar_todos_pagos(self):
        """Procesa todos los pagos pendientes en la cola."""
        if self.cola_pagos.esta_vacia():
            messagebox.showinfo("Info", "No hay pagos pendientes")
            return
        
        cantidad_procesados = 0
        while not self.cola_pagos.esta_vacia():
            self._procesar_pago()
            cantidad_procesados += 1
        
        self._log(f"⚡ Procesamiento masivo completado: {cantidad_procesados} pagos procesados")
    
    def _actualizar_estadisticas(self):
        """Actualiza las estadísticas de pagos."""
        # Aquí se podrían agregar estadísticas reales
        # Por simplicidad, mostramos info básica
        cola_size = self.cola_pagos.tamaño()
        self.stats_label.config(text=f"Pagos en cola: {cola_size}\nSistema operativo")
    
    def _log(self, mensaje):
        """Agrega un mensaje al log del sistema."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.log_text.see(tk.END)
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        self._log("🎯 Interfaz lista - Implementando puntos 1-6 del flujo de compra")
        self.window.mainloop()

# Función para ejecutar la aplicación
def main():
    """Función principal para ejecutar la interfaz."""
    try:
        app = Interfaz()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()