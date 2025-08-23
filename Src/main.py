#IMPORTANTE ESTA CLASE MAIN SE CREO CON IA, PORQUE NO SE NADA DE GRAFICAR, 
#hay que mover la parte de gui de esta clase a su respectiva clase


import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os
import sys

# Agregar el directorio actual al path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from Carrito import Carrito
from Producto import Producto
from Pago import Pago
from Orden import Orden
from estructuras.Cola import ColaPagos
from estructuras.Pila import PilaOrdenes

class SistemaCompras:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Compras - Universidad")
        self.root.geometry("1200x800")
        
        # Inicializar estructuras de datos
        self.carrito = Carrito("carrito_principal")
        self.lista_productos = []
        self.pila_ordenes = PilaOrdenes()
        self.cola_pagos = ColaPagos()
        
        # Cargar productos desde CSV
        self.cargar_productos()
        
        # Crear interfaz
        self.crear_interfaz()
        
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
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema de Compras", font=('Arial', 16, 'bold'))
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
        
        ttk.Button(btn_frame, text="Procesar Pago", command=self.procesar_pago).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Generar Orden", command=self.generar_orden).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Limpiar Formulario", command=self.limpiar_formulario).pack(side=tk.LEFT)
    
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
        ordenes = self.pila_ordenes.obtener_todas()
        for orden in reversed(ordenes):
            self.text_pila.insert(tk.END, f"Orden #{orden.id} - {orden.fecha} - ${orden.total:.2f}\n")
        
        # Cola de pagos
        self.text_cola.delete(1.0, tk.END)
        pagos = self.cola_pagos.obtener_todos()
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
            monto=self.carrito.calcular_total(),
            fecha=datetime.now(),
            cliente=self.entry_nombre.get(),
            email=self.entry_email.get()
        )
        
        # Agregar a la cola de pagos
        self.cola_pagos.enqueue(pago)
        
        # Actualizar visualizaciones
        self.actualizar_visualizaciones()
        
        messagebox.showinfo("Éxito", f"Pago procesado por ${pago.monto:.2f}")
    
    def generar_orden(self):
        """Generar orden de compra"""
        if self.carrito.esta_vacio():
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        # Crear orden
        orden = Orden(
            id=len(self.pila_ordenes.obtener_todas()) + 1,
            items=self.carrito.productos.obtener_elementos().copy(),
            total=self.carrito.calcular_total(),
            fecha=datetime.now(),
            cliente=self.entry_nombre.get()
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
                for item in orden.items:
                    if hasattr(item, 'producto'):
                        # Es un ItemCarrito
                        writer.writerow({
                            'id_orden': orden.id,
                            'fecha': orden.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                            'cliente': orden.cliente,
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
                            'cliente': orden.cliente,
                            'producto': item.nombre,
                            'cantidad': 1,
                            'precio_unitario': item.precio,
                            'subtotal': item.precio,
                            'total_orden': orden.total
                        })
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la orden: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpiar formulario de checkout"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_tarjeta.delete(0, tk.END)
        self.entry_cvv.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = SistemaCompras(root)
    root.mainloop()

if __name__ == "__main__":
    main()
