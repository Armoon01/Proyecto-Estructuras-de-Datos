"""
Clase Orden simplificada para el sistema de e-commerce.
Usa Pila para historial y Cola para procesamiento.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'estructuras'))

from datetime import datetime
from estructuras import Pila
from estructuras import Cola

class Orden:
    """Orden de compra simplificada."""
    
    def __init__(self, id_orden, id_cliente, carrito):
        """
        Inicializa una orden.
        
        Args:
            id_orden (str): ID único de la orden
            id_cliente (str): ID del cliente
            carrito: Objeto Carrito con los productos
        """
        if not id_orden or not id_cliente:
            raise ValueError("ID de orden e ID de cliente son requeridos")
        
        if carrito.esta_vacio():
            raise ValueError("No se puede crear orden con carrito vacío")
        
        self.id_orden = id_orden
        self.id_cliente = id_cliente
        self.productos = carrito.obtener_productos()
        self.total = carrito.obtener_total()
        self.fecha_creacion = datetime.now()
        self.estado = "Pendiente"
        self.historial = Pila()  # Para cambios de estado
        
        # Registrar creación en historial
        self.historial.push(f"Orden creada - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado de la orden.
        
        Args:
            nuevo_estado (str): Nuevo estado de la orden
            
        Returns:
            bool: True si se cambió correctamente
        """
        estados_validos = ["Pendiente", "Procesando", "Enviado", "Entregado", "Cancelado"]
        
        if nuevo_estado not in estados_validos:
            return False
        
        estado_anterior = self.estado
        self.estado = nuevo_estado
        
        # Registrar cambio en historial
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cambio = f"{estado_anterior} -> {nuevo_estado} - {timestamp}"
        self.historial.push(cambio)
        
        return True
    
    def procesar(self):
        """Marca la orden como procesando."""
        return self.cambiar_estado("Procesando")
    
    def enviar(self):
        """Marca la orden como enviada."""
        return self.cambiar_estado("Enviado")
    
    def entregar(self):
        """Marca la orden como entregada."""
        return self.cambiar_estado("Entregado")
    
    def cancelar(self):
        """Cancela la orden."""
        return self.cambiar_estado("Cancelado")
    
    def obtener_historial(self):
        """
        Obtiene el historial de cambios.
        
        Returns:
            list: Lista con el historial
        """
        historial_lista = []
        
        # Crear una copia temporal de la pila para no modificar la original
        pila_temp = Pila()
        
        # Vaciar pila original a temporal
        while not self.historial.esta_vacia():
            item = self.historial.pop()
            pila_temp.push(item)
            historial_lista.append(item)
        
        # Restaurar pila original
        while not pila_temp.esta_vacia():
            self.historial.push(pila_temp.pop())
        
        historial_lista.reverse()  # Para mostrar cronológicamente
        return historial_lista
    
    def esta_completada(self):
        """Verifica si la orden está completada."""
        return self.estado in ["Entregado", "Cancelado"]
    
    def puede_cancelarse(self):
        """Verifica si la orden puede cancelarse."""
        return self.estado in ["Pendiente", "Procesando"]
    
    def obtener_resumen(self):
        """
        Obtiene resumen de la orden.
        
        Returns:
            dict: Resumen de la orden
        """
        return {
            'id_orden': self.id_orden,
            'id_cliente': self.id_cliente,
            'total': self.total,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion,
            'cantidad_productos': len(self.productos),
            'completada': self.esta_completada()
        }
    
    def mostrar_orden(self):
        """Muestra detalles completos de la orden."""
        print(f"📋 ORDEN #{self.id_orden}")
        print("="*50)
        print(f"Cliente: {self.id_cliente}")
        print(f"Estado: {self.estado}")
        print(f"Fecha: {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total: ${self.total:.2f}")
        print()
        
        print("PRODUCTOS:")
        for item in self.productos:
            print(f"  • {item}")
        
        print()
        print("HISTORIAL:")
        for cambio in self.obtener_historial():
            print(f"  📅 {cambio}")
        
        print("="*50)
    
    def __str__(self):
        """Representación en cadena de la orden."""
        return f"Orden #{self.id_orden} - {self.estado} - ${self.total:.2f}"
    
    def __repr__(self):
        """Representación técnica de la orden."""
        return f"Orden(id='{self.id_orden}', cliente='{self.id_cliente}', estado='{self.estado}')"

class ProcesadorOrdenes:
    """Procesador de órdenes usando Cola FIFO."""
    
    def __init__(self):
        """Inicializa el procesador con una cola vacía."""
        self.cola_ordenes = Cola()
        self.ordenes_procesadas = []
    
    def agregar_orden(self, orden):
        """
        Agrega una orden a la cola de procesamiento.
        
        Args:
            orden: Objeto Orden
            
        Returns:
            bool: True si se agregó correctamente
        """
        if not isinstance(orden, Orden):
            return False
        
        if orden.estado != "Pendiente":
            return False
        
        self.cola_ordenes.encolar(orden)
        print(f"✅ Orden #{orden.id_orden} agregada a cola de procesamiento")
        return True
    
    def procesar_siguiente(self):
        """
        Procesa la siguiente orden en la cola.
        
        Returns:
            Orden: La orden procesada o None si no hay órdenes
        """
        if self.cola_ordenes.esta_vacia():
            print("No hay órdenes pendientes de procesar")
            return None
        
        orden = self.cola_ordenes.desencolar()
        orden.procesar()
        self.ordenes_procesadas.append(orden)
        
        print(f"🔄 Procesando orden #{orden.id_orden}")
        return orden
    
    def obtener_cola_estado(self):
        """Muestra el estado de la cola de procesamiento."""
        if self.cola_ordenes.esta_vacia():
            print("Cola de procesamiento vacía")
            return
        
        print("📋 COLA DE PROCESAMIENTO:")
        print("="*40)
        
        # Crear lista temporal para mostrar sin modificar la cola
        ordenes_temp = []
        
        # Guardar órdenes en lista temporal
        while not self.cola_ordenes.esta_vacia():
            orden = self.cola_ordenes.desencolar()
            ordenes_temp.append(orden)
            print(f"  {len(ordenes_temp)}. Orden #{orden.id_orden} - ${orden.total:.2f}")
        
        # Restaurar cola
        for orden in ordenes_temp:
            self.cola_ordenes.encolar(orden)
        
        print(f"Total en cola: {len(ordenes_temp)} órdenes")
    
    def __str__(self):
        """Representación del procesador."""
        return f"Procesador: {self.cola_ordenes.obtener_tamaño()} órdenes en cola, {len(self.ordenes_procesadas)} procesadas"
