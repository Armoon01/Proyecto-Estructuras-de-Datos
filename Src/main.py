#IMPORTANTE ESTA CLASE MAIN SE CREO CON IA, PORQUE NO SE NADA DE GRAFICAR, 
#hay que mover la parte de gui de esta clase a su respectiva clase


import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime, timedelta
import os
import sys

# Agregar el directorio actual al path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from Carrito import Carrito
from Producto import Producto
from Pago import Pago
from Orden import Orden
from estructuras.Cola import Cola
from estructuras.Pila import Pila
from Login import SistemaLogin
from InterfazLogin import mostrar_login

class SistemaCompras:
    def __init__(self, root, cliente_autenticado=None, sistema_login=None):
        self.root = root
        self.root.title("Sistema de Compras - Universidad")
        self.root.geometry("1200x800")
        
        # Sistema de autenticación
        self.sistema_login = sistema_login
        self.cliente_autenticado = cliente_autenticado
        
        # Inicializar estructuras de datos
        if cliente_autenticado:
            self.carrito = cliente_autenticado.carrito  # Usar carrito del cliente autenticado
        else:
            self.carrito = Carrito("carrito_invitado")  # Carrito temporal para invitados
            
        self.lista_productos = []
        self.pila_ordenes = Pila()
        self.cola_pagos = Cola()
        
        # Cargar productos desde CSV
        self.cargar_productos()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Configurar cierre de aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
    
    def cargar_productos(self):
        """Cargar productos desde archivo CSV"""
        try:
            # Construir la ruta correcta al archivo CSV
            data_path = os.path.join(os.path.dirname(current_dir), 'Data', 'productos.csv')
            with open(data_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    producto = Producto(
                        id_producto=row['id_producto'],
                        nombre=row['nombre'],
                        descripcion=row['descripcion'],
                        precio=float(row['precio']),
                        stock=int(row['stock'])
                    )
                    self.lista_productos.append(producto)
        except FileNotFoundError:
            # Crear productos de ejemplo si no existe el archivo
            self.crear_productos_ejemplo()
    
    def crear_productos_ejemplo(self):
        """Crear productos de ejemplo y guardar en CSV"""
        productos_ejemplo = [
            {'id_producto': '1', 'nombre': 'Laptop HP', 'precio': 899.99, 'descripcion': 'Laptop HP 15 pulgadas', 'stock': 10},
            {'id_producto': '2', 'nombre': 'Mouse Inalámbrico', 'precio': 25.50, 'descripcion': 'Mouse inalámbrico Logitech', 'stock': 50},
            {'id_producto': '3', 'nombre': 'Teclado Mecánico', 'precio': 89.99, 'descripcion': 'Teclado mecánico RGB', 'stock': 20},
            {'id_producto': '4', 'nombre': 'Monitor 24"', 'precio': 199.99, 'descripcion': 'Monitor LED 24 pulgadas', 'stock': 15},
            {'id_producto': '5', 'nombre': 'Auriculares', 'precio': 45.00, 'descripcion': 'Auriculares con micrófono', 'stock': 30}
        ]
        
        # Crear directorio Data si no existe
        data_dir = os.path.join(os.path.dirname(current_dir), 'Data')
        os.makedirs(data_dir, exist_ok=True)
        
        data_path = os.path.join(data_dir, 'productos.csv')
        with open(data_path, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['id_producto', 'nombre', 'precio', 'descripcion', 'stock']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(productos_ejemplo)
        
        for prod in productos_ejemplo:
            producto = Producto(
                id_producto=prod['id_producto'],
                nombre=prod['nombre'],
                descripcion=prod['descripcion'],
                precio=prod['precio'],
                stock=prod['stock']
            )
            self.lista_productos.append(producto)
    
    def crear_interfaz(self):
        """Crear la interfaz gráfica principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(3, weight=1)
        
        # Título con información del usuario
        if self.cliente_autenticado:
            usuario_info = f"Sistema de Compras - Bienvenido, {self.cliente_autenticado.nombre}"
            if self.sistema_login and self.sistema_login.es_administrador():
                usuario_info += " (Administrador)"
        else:
            usuario_info = "Sistema de Compras - Modo Invitado"
            
        titulo = ttk.Label(main_frame, text=usuario_info, font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Panel izquierdo - Productos
        self.crear_panel_productos(main_frame)
        
        # Panel central - Carrito
        self.crear_panel_carrito(main_frame)
        
        # Panel derecho - Estructuras de datos
        self.crear_panel_estructuras(main_frame)
        
        # Panel inferior - Checkout
        self.crear_panel_checkout(main_frame)
    
    def crear_panel_productos(self, parent):
        """Crear panel de productos"""
        frame = ttk.LabelFrame(parent, text="Productos Disponibles", padding="10")
        frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Treeview para productos
        columns = ('ID', 'Nombre', 'Precio', 'Stock')
        self.tree_productos = ttk.Treeview(frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.tree_productos.heading(col, text=col)
            self.tree_productos.column(col, width=100)
        
        self.tree_productos.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_productos.yview)
        scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.tree_productos.configure(yscrollcommand=scrollbar.set)
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Agregar al Carrito", command=self.agregar_al_carrito).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Ver Detalles", command=self.ver_detalles_producto).pack(side=tk.LEFT)
        
        # Cargar productos en el treeview
        self.actualizar_lista_productos()
    
    def crear_panel_carrito(self, parent):
        """Crear panel del carrito"""
        frame = ttk.LabelFrame(parent, text="Carrito de Compras", padding="10")
        frame.grid(row=1, column=2, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Treeview para carrito
        columns = ('Producto', 'Cantidad', 'Precio Unit.', 'Subtotal')
        self.tree_carrito = ttk.Treeview(frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.tree_carrito.heading(col, text=col)
            self.tree_carrito.column(col, width=100)
        
        self.tree_carrito.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_carrito.yview)
        scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.tree_carrito.configure(yscrollcommand=scrollbar.set)
        
        # Botones del carrito
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Eliminar Item", command=self.eliminar_del_carrito).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Modificar Cantidad", command=self.modificar_cantidad).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Vaciar Carrito", command=self.vaciar_carrito).pack(side=tk.LEFT)
        
        # Total
        self.lbl_total = ttk.Label(frame, text="Total: $0.00", font=('Arial', 12, 'bold'))
        self.lbl_total.grid(row=2, column=0, columnspan=2, pady=(10, 0))
    
    def crear_panel_estructuras(self, parent):
        """Crear panel para mostrar estructuras de datos"""
        frame = ttk.LabelFrame(parent, text="Visualización de Estructuras", padding="10")
        frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Notebook para pestañas
        notebook = ttk.Notebook(frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña Lista de Productos
        frame_lista = ttk.Frame(notebook)
        notebook.add(frame_lista, text="Lista de Productos")
        
        self.text_lista = tk.Text(frame_lista, height=6, width=50)
        self.text_lista.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña Pila de Órdenes
        frame_pila = ttk.Frame(notebook)
        notebook.add(frame_pila, text="Pila de Órdenes")
        
        self.text_pila = tk.Text(frame_pila, height=6, width=50)
        self.text_pila.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña Cola de Pagos
        frame_cola = ttk.Frame(notebook)
        notebook.add(frame_cola, text="Cola de Pagos")
        
        self.text_cola = tk.Text(frame_cola, height=6, width=50)
        self.text_cola.pack(fill=tk.BOTH, expand=True)
        
        # Actualizar visualizaciones
        self.actualizar_visualizaciones()
    
    def crear_panel_checkout(self, parent):
        """Crear panel de checkout"""
        frame = ttk.LabelFrame(parent, text="Checkout y Pago", padding="10")
        frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Información del cliente
        cliente_frame = ttk.Frame(frame)
        cliente_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(cliente_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.entry_nombre = ttk.Entry(cliente_frame, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=(5, 10))
        
        ttk.Label(cliente_frame, text="Email:").grid(row=0, column=2, sticky=tk.W)
        self.entry_email = ttk.Entry(cliente_frame, width=30)
        self.entry_email.grid(row=0, column=3, padx=(5, 0))
        
        # Información de pago
        pago_frame = ttk.Frame(frame)
        pago_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(pago_frame, text="Número de Tarjeta:").grid(row=0, column=0, sticky=tk.W)
        self.entry_tarjeta = ttk.Entry(pago_frame, width=20)
        self.entry_tarjeta.grid(row=0, column=1, padx=(5, 10))
        
        ttk.Label(pago_frame, text="CVV:").grid(row=0, column=2, sticky=tk.W)
        self.entry_cvv = ttk.Entry(pago_frame, width=10)
        self.entry_cvv.grid(row=0, column=3, padx=(5, 10))
        
        ttk.Label(pago_frame, text="Fecha Vencimiento:").grid(row=0, column=4, sticky=tk.W)
        self.entry_fecha = ttk.Entry(pago_frame, width=10)
        self.entry_fecha.grid(row=0, column=5, padx=(5, 0))
        
        # Botones de checkout
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Procesar Pago", command=self.procesar_pago).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Generar Orden", command=self.generar_orden).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Checkout Completo", command=self.procesar_checkout_completo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Ver Historial", command=self.mostrar_historial_cliente).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Limpiar Formulario", command=self.limpiar_formulario).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Cerrar Sesión", command=self.cerrar_sesion).pack(side=tk.LEFT)
        
        # Si hay cliente autenticado, rellenar campos
        if self.cliente_autenticado:
            self.rellenar_campos_cliente()
    
    def mostrar_historial_cliente(self):
        """Mostrar historial de órdenes del cliente actual"""
        if not self.entry_nombre.get() or not self.entry_email.get():
            messagebox.showwarning("Advertencia", "Por favor complete los campos del cliente")
            return
        
        try:
            from Cliente import Cliente
            
            # Crear un cliente temporal para mostrar historial
            # En una aplicación real, buscaríamos el cliente en una base de datos
            cliente_temp = Cliente(
                id_cliente="temp",
                nombre=self.entry_nombre.get(),
                email=self.entry_email.get(),
                carrito=self.carrito,
                telefono=""
            )
            
            # Simular órdenes del historial (en una app real, se cargarían de la BD)
            # Por ahora, mostraremos las órdenes de la pila actual
            ordenes_historial = self.pila_ordenes.obtener_elementos()
            
            # Crear ventana de historial
            ventana_historial = tk.Toplevel(self.root)
            ventana_historial.title(f"Historial de Órdenes - {cliente_temp.nombre}")
            ventana_historial.geometry("800x600")
            ventana_historial.transient(self.root)
            ventana_historial.grab_set()
            
            # Información del cliente
            info_frame = ttk.LabelFrame(ventana_historial, text="Información del Cliente", padding="10")
            info_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(info_frame, text=f"Nombre: {cliente_temp.nombre}").pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Email: {cliente_temp.email}").pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Total de órdenes: {len(ordenes_historial)}").pack(anchor=tk.W)
            
            # Lista de órdenes
            ordenes_frame = ttk.LabelFrame(ventana_historial, text="Historial de Órdenes", padding="10")
            ordenes_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Treeview para órdenes
            columns = ('Orden', 'Fecha', 'Estado', 'Total', 'Items')
            tree_ordenes = ttk.Treeview(ordenes_frame, columns=columns, show='headings', height=15)
            
            for col in columns:
                tree_ordenes.heading(col, text=col)
                tree_ordenes.column(col, width=120)
            
            tree_ordenes.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
            
            # Scrollbar
            scrollbar_ordenes = ttk.Scrollbar(ordenes_frame, orient=tk.VERTICAL, command=tree_ordenes.yview)
            scrollbar_ordenes.pack(side=tk.RIGHT, fill=tk.Y)
            tree_ordenes.configure(yscrollcommand=scrollbar_ordenes.set)
            
            # Llenar con órdenes
            if ordenes_historial:
                total_gastado = 0
                for orden in ordenes_historial:
                    items_count = len(orden.productos) if hasattr(orden, 'productos') else 0
                    tree_ordenes.insert('', 'end', values=(
                        f"#{orden.id}",
                        orden.fecha.strftime('%Y-%m-%d %H:%M') if hasattr(orden, 'fecha') else 'N/A',
                        orden.estado if hasattr(orden, 'estado') else 'Pendiente',
                        f"${orden.total:.2f}" if hasattr(orden, 'total') else '$0.00',
                        items_count
                    ))
                    if hasattr(orden, 'total'):
                        total_gastado += orden.total
                
                # Resumen
                resumen_frame = ttk.Frame(ventana_historial)
                resumen_frame.pack(fill=tk.X, padx=10, pady=5)
                
                ttk.Label(resumen_frame, text=f"Total gastado: ${total_gastado:.2f}", 
                         font=('Arial', 12, 'bold')).pack(anchor=tk.W)
            else:
                tree_ordenes.insert('', 'end', values=("Sin órdenes", "", "", "", ""))
            
            # Botón cerrar
            ttk.Button(ventana_historial, text="Cerrar", 
                      command=ventana_historial.destroy).pack(pady=10)
                      
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar historial: {str(e)}")

    def actualizar_lista_productos(self):
        """Actualizar la lista de productos en el treeview"""
        # Limpiar treeview
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        # Agregar productos
        for producto in self.lista_productos:
            self.tree_productos.insert('', 'end', values=(
                producto.getIdProducto(),
                producto.nombre,
                f"${producto.precio:.2f}",
                producto.stock
            ))
    
    def agregar_al_carrito(self):
        """Agregar producto seleccionado al carrito"""
        selection = self.tree_productos.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto")
            return
        
        item = self.tree_productos.item(selection[0])
        producto_id = item['values'][0]
        
        # Buscar producto
        producto = None
        for p in self.lista_productos:
            if str(p.getIdProducto()) == str(producto_id):
                producto = p
                break
        
        if producto:
            # Agregar al carrito
            resultado = self.carrito.agregar_producto_con_cantidad(producto, 1)
            self.actualizar_carrito()
            if resultado:
                messagebox.showinfo("Éxito", f"Producto '{producto.nombre}' agregado al carrito")
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto al carrito")
        else:
            messagebox.showerror("Error", f"No se encontró el producto con ID: {producto_id}")
    
    def actualizar_carrito(self):
        """Actualizar la visualización del carrito"""
        # Limpiar treeview
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        
        # Agregar items del carrito
        elementos = self.carrito.productos.obtener_elementos()
        for item in elementos:
            if hasattr(item, 'producto'):
                # Es un ItemCarrito
                subtotal = item.producto.precio * item.cantidad
                self.tree_carrito.insert('', 'end', values=(
                    item.producto.nombre,
                    item.cantidad,
                    f"${item.producto.precio:.2f}",
                    f"${subtotal:.2f}"
                ))
            else:
                # Es un producto directo
                self.tree_carrito.insert('', 'end', values=(
                    item.nombre,
                    1,
                    f"${item.precio:.2f}",
                    f"${item.precio:.2f}"
                ))
        
        # Actualizar total
        total = self.carrito.calcular_total()
        self.lbl_total.config(text=f"Total: ${total:.2f}")
    
    def eliminar_del_carrito(self):
        """Eliminar item seleccionado del carrito"""
        selection = self.tree_carrito.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un item del carrito")
            return
        
        index = self.tree_carrito.index(selection[0])
        self.carrito.eliminar_item(index)
        self.actualizar_carrito()
        messagebox.showinfo("Éxito", "Item eliminado del carrito")
    
    def modificar_cantidad(self):
        """Modificar cantidad de un item del carrito"""
        selection = self.tree_carrito.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un item del carrito")
            return
        
        index = self.tree_carrito.index(selection[0])
        
        # Ventana de diálogo para nueva cantidad
        dialog = tk.Toplevel(self.root)
        dialog.title("Modificar Cantidad")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nueva cantidad:").pack(pady=10)
        entry_cantidad = ttk.Entry(dialog)
        entry_cantidad.pack(pady=5)
        
        elementos = self.carrito.productos.obtener_elementos()
        if 0 <= index < len(elementos):
            if hasattr(elementos[index], 'cantidad'):
                entry_cantidad.insert(0, str(elementos[index].cantidad))
            else:
                entry_cantidad.insert(0, "1")
        
        def confirmar():
            try:
                nueva_cantidad = int(entry_cantidad.get())
                if nueva_cantidad > 0:
                    self.carrito.modificar_cantidad(index, nueva_cantidad)
                    self.actualizar_carrito()
                    dialog.destroy()
                    messagebox.showinfo("Éxito", "Cantidad modificada")
                else:
                    messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")
        
        ttk.Button(dialog, text="Confirmar", command=confirmar).pack(pady=10)
    
    def vaciar_carrito(self):
        """Vaciar todo el carrito"""
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea vaciar el carrito?"):
            self.carrito.vaciar()
            self.actualizar_carrito()
            messagebox.showinfo("Éxito", "Carrito vaciado")
    
    def ver_detalles_producto(self):
        """Mostrar detalles del producto seleccionado"""
        selection = self.tree_productos.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto")
            return
        
        item = self.tree_productos.item(selection[0])
        producto_id = item['values'][0]
        
        # Buscar producto
        producto = None
        for p in self.lista_productos:
            if p.getIdProducto() == producto_id:
                producto = p
                break
        
        if producto:
            detalles = f"""
Detalles del Producto:
ID: {producto.getIdProducto()}
Nombre: {producto.nombre}
Precio: ${producto.precio:.2f}
Descripción: {producto.descripcion}
Stock disponible: {producto.stock}
            """
            messagebox.showinfo("Detalles del Producto", detalles)
    
    def actualizar_visualizaciones(self):
        """Actualizar las visualizaciones de las estructuras de datos"""
        # Lista de productos
        self.text_lista.delete(1.0, tk.END)
        for producto in self.lista_productos:
            self.text_lista.insert(tk.END, f"{producto.getIdProducto()}. {producto.nombre} - ${producto.precio:.2f}\n")
        
        # Pila de órdenes
        self.text_pila.delete(1.0, tk.END)
        ordenes = self.pila_ordenes.obtener_elementos()
        for orden in reversed(ordenes):
            self.text_pila.insert(tk.END, f"Orden #{orden.id} - {orden.fecha.strftime('%Y-%m-%d %H:%M:%S')} - ${orden.total:.2f}\n")
        
        # Cola de pagos
        self.text_cola.delete(1.0, tk.END)
        pagos = self.cola_pagos.obtener_elementos()
        for pago in pagos:
            self.text_cola.insert(tk.END, f"Pago ${pago.monto:.2f} - {pago.fecha}\n")
    
    def procesar_pago(self):
        """Procesar el pago del carrito"""
        if self.carrito.esta_vacio():
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        # Validar campos
        if not self.entry_nombre.get() or not self.entry_email.get():
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        # Crear pago
        pago = Pago(
            id_pago=len(self.cola_pagos.obtener_elementos()) + 1,
            monto=self.carrito.calcular_total(),
            metodo="Tarjeta de Crédito" if self.entry_tarjeta.get() else "Efectivo",
            cliente=self.entry_nombre.get(),
            fecha=datetime.now()
        )
        
        # Agregar a la cola de pagos
        self.cola_pagos.enqueue(pago)
        
        # Guardar pago en CSV
        self.guardar_pago_csv(pago)
        
        # Actualizar visualizaciones
        self.actualizar_visualizaciones()
        
        messagebox.showinfo("Éxito", f"Pago procesado por ${pago.monto:.2f}")
    
    def generar_orden(self):
        """Generar orden de compra"""
        if self.carrito.esta_vacio():
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        # Crear orden
        fecha_actual = datetime.now()
        orden = Orden(
            id_orden=len(self.pila_ordenes.obtener_elementos()) + 1,
            fecha_compra=fecha_actual,
            productos=self.carrito.productos.obtener_elementos().copy(),
            recibo=None,  # Se generará después
            fecha_entrega=fecha_actual + timedelta(days=5),
            fecha_envio=fecha_actual + timedelta(days=2),
            total=self.carrito.calcular_total()
        )
        
        # Agregar a la pila de órdenes
        self.pila_ordenes.push(orden)
        
        # Actualizar visualizaciones
        self.actualizar_visualizaciones()
        
        # Guardar orden en CSV
        self.guardar_orden_csv(orden)
        
        messagebox.showinfo("Éxito", f"Orden #{orden.id} generada exitosamente")
        
        # Vaciar carrito después de generar orden
        self.carrito.vaciar()
        self.actualizar_carrito()
    
    def guardar_orden_csv(self, orden):
        """Guardar orden en archivo CSV"""
        try:
            # Crear directorio Data si no existe
            data_dir = os.path.join(os.path.dirname(current_dir), 'Data')
            os.makedirs(data_dir, exist_ok=True)
            
            data_path = os.path.join(data_dir, 'ordenes.csv')
            with open(data_path, 'a', newline='', encoding='utf-8') as file:
                fieldnames = ['id_orden', 'fecha', 'cliente', 'producto', 'cantidad', 'precio_unitario', 'subtotal', 'total_orden']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Escribir header si el archivo está vacío
                if file.tell() == 0:
                    writer.writeheader()
                
                # Escribir cada item de la orden
                for item in orden.productos:
                    if hasattr(item, 'producto'):
                        # Es un ItemCarrito
                        writer.writerow({
                            'id_orden': orden.id,
                            'fecha': orden.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                            'cliente': self.entry_nombre.get(),
                            'producto': item.producto.nombre,
                            'cantidad': item.cantidad,
                            'precio_unitario': item.producto.precio,
                            'subtotal': item.producto.precio * item.cantidad,
                            'total_orden': orden.total
                        })
                    else:
                        # Es un producto directo
                        writer.writerow({
                            'id_orden': orden.id,
                            'fecha': orden.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                            'cliente': self.entry_nombre.get(),
                            'producto': item.nombre,
                            'cantidad': 1,
                            'precio_unitario': item.precio,
                            'subtotal': item.precio,
                            'total_orden': orden.total
                        })
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la orden: {str(e)}")
    
    def guardar_pago_csv(self, pago):
        """Guardar pago en archivo CSV"""
        try:
            # Crear directorio Data si no existe
            data_dir = os.path.join(os.path.dirname(current_dir), 'Data')
            os.makedirs(data_dir, exist_ok=True)
            
            data_path = os.path.join(data_dir, 'pagos.csv')
            
            # Verificar si el archivo existe para escribir header
            file_exists = os.path.exists(data_path)
            
            with open(data_path, 'a', newline='', encoding='utf-8') as file:
                fieldnames = ['id_pago', 'fecha', 'cliente', 'email', 'monto', 'metodo', 'numero_tarjeta', 'estado']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Escribir header si el archivo es nuevo
                if not file_exists:
                    writer.writeheader()
                
                # Escribir datos del pago
                writer.writerow({
                    'id_pago': pago.id_pago,
                    'fecha': pago.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                    'cliente': self.entry_nombre.get(),
                    'email': self.entry_email.get(),
                    'monto': pago.monto,
                    'metodo': pago.metodo,
                    'numero_tarjeta': self.entry_tarjeta.get()[-4:] if self.entry_tarjeta.get() else 'N/A',  # Solo últimos 4 dígitos
                    'estado': 'Completado'
                })
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el pago: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpiar formulario de checkout"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_tarjeta.delete(0, tk.END)
        self.entry_cvv.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
    
    def procesar_checkout_completo(self):
        """Procesar checkout completo usando la clase Checkout"""
        if self.carrito.esta_vacio():
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        try:
            from Cliente import Cliente
            from Checkout import Checkout
            from TarjetaCredito import TarjetaCredito
            
            # Usar cliente autenticado o crear uno temporal
            if self.cliente_autenticado:
                cliente = self.cliente_autenticado
            else:
                # Validar campos para usuario invitado
                if not self.entry_nombre.get() or not self.entry_email.get():
                    messagebox.showerror("Error", "Por favor complete todos los campos del cliente")
                    return
                
                # Crear cliente temporal
                cliente = Cliente(
                    id_cliente="invitado",
                    nombre=self.entry_nombre.get(),
                    email=self.entry_email.get(),
                    carrito=self.carrito,
                    telefono=""
                )
            
            # Crear tarjeta de crédito si se proporciona
            tarjeta = None
            if self.entry_tarjeta.get() and self.entry_cvv.get() and self.entry_fecha.get():
                from datetime import datetime
                try:
                    fecha_exp = datetime.strptime(self.entry_fecha.get(), "%m/%y").date()
                    tarjeta = TarjetaCredito(
                        numero=self.entry_tarjeta.get(),
                        titular=self.entry_nombre.get(),
                        fecha_expiracion=fecha_exp,
                        cvv=self.entry_cvv.get()
                    )
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inválido. Use MM/YY")
                    return
            
            # Crear checkout
            checkout = Checkout(self.carrito, cliente, tarjeta)
            
            # Procesar checkout
            metodo_pago = "Tarjeta de Crédito" if tarjeta else "Efectivo"
            direccion_envio = "Dirección predeterminada"  # Se podría agregar un campo para esto
            
            checkout.procesar_checkout(direccion_envio, metodo_pago)
            
            # Agregar orden al historial del cliente
            cliente.agregar_orden(checkout.orden)
            
            # Agregar orden a la pila
            self.pila_ordenes.push(checkout.orden)
            
            # Crear y agregar pago a la cola
            pago = Pago(
                id_pago=len(self.cola_pagos.obtener_elementos()) + 1,
                monto=checkout.total,
                metodo=metodo_pago,
                cliente=cliente.nombre,
                fecha=datetime.now()
            )
            self.cola_pagos.enqueue(pago)
            
            # Guardar pago en CSV
            self.guardar_pago_csv(pago)
            
            # Actualizar visualizaciones
            self.actualizar_carrito()
            self.actualizar_visualizaciones()
            
            messagebox.showinfo("Éxito", f"Checkout completado exitosamente. Total: ${checkout.total:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el checkout: {str(e)}")
    
    def cerrar_sesion(self):
        """Cerrar la sesión actual y volver al login."""
        if self.sistema_login:
            self.sistema_login.cerrar_sesion()
        
        # Limpiar datos de la sesión
        self.cliente_autenticado = None
        self.carrito.vaciar()
        
        messagebox.showinfo("Sesión Cerrada", "Sesión cerrada exitosamente")
        
        # Cerrar ventana actual
        self.root.destroy()
        
        # Mostrar login nuevamente
        iniciar_aplicacion_con_login()
    
    def cerrar_aplicacion(self):
        """Manejar el cierre de la aplicación."""
        if self.sistema_login and self.sistema_login.esta_autenticado():
            if messagebox.askyesno("Cerrar", "¿Está seguro de que desea cerrar la aplicación?"):
                self.sistema_login.cerrar_sesion()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def rellenar_campos_cliente(self):
        """Rellena los campos del formulario con datos del cliente autenticado."""
        if hasattr(self, 'entry_nombre') and self.cliente_autenticado:
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, self.cliente_autenticado.nombre)
            
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, self.cliente_autenticado.email)
            
            # Deshabilitar campos para usuarios autenticados
            self.entry_nombre.config(state='readonly')
            self.entry_email.config(state='readonly')

def callback_login_exitoso(cliente, sistema_login):
    """Callback ejecutado cuando el login es exitoso."""
    # Cerrar cualquier ventana existente
    for widget in tk._default_root.winfo_children() if tk._default_root else []:
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
    
    # Crear nueva ventana principal
    root = tk.Tk()
    app = SistemaCompras(root, cliente, sistema_login)
    root.mainloop()

def iniciar_aplicacion_con_login():
    """Inicia la aplicación mostrando primero el login."""
    # Crear ventana root temporal (se destruirá después del login)
    temp_root = tk.Tk()
    temp_root.withdraw()  # Ocultar ventana temporal
    
    try:
        # Mostrar login
        cliente = mostrar_login(callback_login_exitoso)
        
        if not cliente:
            # Usuario canceló el login
            temp_root.destroy()
            return
            
    except Exception as e:
        messagebox.showerror("Error", f"Error en el sistema de login: {str(e)}")
        temp_root.destroy()
        return
    
    temp_root.destroy()

def main():
    """Función principal que inicia con login."""
    iniciar_aplicacion_con_login()

if __name__ == "__main__":
    main()
