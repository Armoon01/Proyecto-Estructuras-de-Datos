"""
Clase Pago para el sistema de e-commerce universitario.
Maneja el procesamiento de pagos y comunicación con compañías de tarjetas.
Puntos 5 y 6 del flujo de compra.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'estructuras'))

from datetime import datetime
from Cola_Simple import Cola
from cola_prioridad import ColaPrioridad

class Pago:
    """Clase para representar un pago en el sistema."""
    
    def __init__(self, id_pago, id_orden, id_cliente, monto, metodo_pago="tarjeta"):
        """
        Inicializa un pago.
        
        Args:
            id_pago (str): ID único del pago
            id_orden (str): ID de la orden asociada
            id_cliente (str): ID del cliente
            monto (float): Monto a pagar
            metodo_pago (str): Método de pago (tarjeta, efectivo, etc.)
        """
        # Validaciones básicas
        if not id_pago or not id_orden or not id_cliente:
            raise ValueError("IDs de pago, orden y cliente son requeridos")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        
        self.id_pago = id_pago
        self.id_orden = id_orden
        self.id_cliente = id_cliente
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.estado = "Pendiente"  # Pendiente, Procesando, Aprobado, Rechazado
        self.fecha_creacion = datetime.now()
        self.fecha_procesamiento = None
        self.numero_tarjeta = None
        self.codigo_autorizacion = None
        self.mensaje_error = None
    
    def establecer_tarjeta(self, numero_tarjeta, codigo_cvv, fecha_expiracion):
        """
        Establece información de la tarjeta.
        
        Args:
            numero_tarjeta (str): Número de tarjeta (se almacena parcialmente por seguridad)
            codigo_cvv (str): Código CVV
            fecha_expiracion (str): Fecha de expiración MM/YY
            
        Returns:
            bool: True si la información es válida
        """
        # Validación básica de tarjeta
        if not numero_tarjeta or len(numero_tarjeta) < 13:
            self.mensaje_error = "Número de tarjeta inválido"
            return False
        
        if not codigo_cvv or len(codigo_cvv) not in [3, 4]:
            self.mensaje_error = "Código CVV inválido"
            return False
        
        # Almacenar solo los últimos 4 dígitos por seguridad
        self.numero_tarjeta = "**** **** **** " + numero_tarjeta[-4:]
        return True
    
    def procesar(self):
        """Cambia el estado a procesando."""
        if self.estado == "Pendiente":
            self.estado = "Procesando"
            self.fecha_procesamiento = datetime.now()
            return True
        return False
    
    def aprobar(self, codigo_autorizacion):
        """
        Aprueba el pago.
        
        Args:
            codigo_autorizacion (str): Código de autorización del banco
        """
        if self.estado == "Procesando":
            self.estado = "Aprobado"
            self.codigo_autorizacion = codigo_autorizacion
            return True
        return False
    
    def rechazar(self, motivo):
        """
        Rechaza el pago.
        
        Args:
            motivo (str): Motivo del rechazo
        """
        self.estado = "Rechazado"
        self.mensaje_error = motivo
        return True
    
    def esta_aprobado(self):
        """Verifica si el pago está aprobado."""
        return self.estado == "Aprobado"
    
    def esta_rechazado(self):
        """Verifica si el pago está rechazado."""
        return self.estado == "Rechazado"
    
    def obtener_resumen(self):
        """
        Obtiene resumen del pago.
        
        Returns:
            dict: Información del pago
        """
        return {
            'id_pago': self.id_pago,
            'id_orden': self.id_orden,
            'id_cliente': self.id_cliente,
            'monto': self.monto,
            'estado': self.estado,
            'metodo_pago': self.metodo_pago,
            'fecha_creacion': self.fecha_creacion,
            'codigo_autorizacion': self.codigo_autorizacion,
            'tarjeta': self.numero_tarjeta
        }
    
    def __str__(self):
        """Representación en cadena del pago."""
        estado_emoji = {
            "Pendiente": "⏳",
            "Procesando": "🔄",
            "Aprobado": "✅",
            "Rechazado": "❌"
        }
        emoji = estado_emoji.get(self.estado, "❓")
        return f"{emoji} Pago #{self.id_pago} - ${self.monto:.2f} - {self.estado}"
    
    def __repr__(self):
        """Representación técnica del pago."""
        return f"Pago(id='{self.id_pago}', orden='{self.id_orden}', monto={self.monto}, estado='{self.estado}')"

class ProcesadorPagos:
    """
    Procesador de pagos usando Cola para pagos normales y Cola de Prioridad para urgentes.
    Punto 5: Collect Payment
    """
    
    def __init__(self):
        """Inicializa el procesador de pagos."""
        self.cola_pagos = Cola()  # Cola normal para pagos regulares
        self.cola_prioritaria = ColaPrioridad()  # Cola de prioridad para pagos urgentes
        self.pagos_procesados = []
        self.estadisticas = {
            'total_procesados': 0,
            'aprobados': 0,
            'rechazados': 0,
            'monto_total': 0.0
        }
    
    def agregar_pago(self, pago, es_prioritario=False, prioridad=1):
        """
        Agrega un pago a la cola de procesamiento.
        
        Args:
            pago (Pago): Objeto pago
            es_prioritario (bool): Si debe ir a cola prioritaria
            prioridad (int): Nivel de prioridad (1=más alta, 5=más baja)
            
        Returns:
            bool: True si se agregó correctamente
        """
        if not isinstance(pago, Pago):
            return False
        
        if pago.estado != "Pendiente":
            return False
        
        if es_prioritario:
            self.cola_prioritaria.encolar(pago, prioridad)
            print(f"💳 Pago #{pago.id_pago} agregado a cola prioritaria (P{prioridad})")
        else:
            self.cola_pagos.encolar(pago)
            print(f"💳 Pago #{pago.id_pago} agregado a cola regular")
        
        return True
    
    def procesar_siguiente_pago(self):
        """
        Procesa el siguiente pago en las colas.
        Prioriza la cola prioritaria sobre la regular.
        
        Returns:
            Pago: El pago procesado o None si no hay pagos
        """
        pago = None
        
        # Primero revisar cola prioritaria
        if not self.cola_prioritaria.esta_vacia():
            pago = self.cola_prioritaria.desencolar()
            print(f"🔄 Procesando pago prioritario #{pago.id_pago}")
        
        # Si no hay prioritarios, procesar cola regular
        elif not self.cola_pagos.esta_vacia():
            pago = self.cola_pagos.desencolar()
            print(f"🔄 Procesando pago regular #{pago.id_pago}")
        
        if pago:
            pago.procesar()
            # Simular procesamiento automático
            resultado = self._simular_procesamiento_tarjeta(pago)
            self.pagos_procesados.append(pago)
            self._actualizar_estadisticas(pago)
            return pago
        
        return None
    
    def _simular_procesamiento_tarjeta(self, pago):
        """
        Simula el procesamiento con la compañía de tarjetas.
        Punto 6: Post payment (Credit Card Company)
        
        Args:
            pago (Pago): Pago a procesar
            
        Returns:
            bool: True si se aprobó, False si se rechazó
        """
        import random
        
        # Simular diferentes escenarios
        probabilidad_aprobacion = 0.85  # 85% de probabilidad de aprobación
        
        if random.random() < probabilidad_aprobacion:
            # Aprobar pago
            codigo_auth = f"AUTH{random.randint(100000, 999999)}"
            pago.aprobar(codigo_auth)
            print(f"✅ Pago #{pago.id_pago} APROBADO - Código: {codigo_auth}")
            return True
        else:
            # Rechazar pago
            motivos = [
                "Fondos insuficientes",
                "Tarjeta bloqueada",
                "Información incorrecta",
                "Límite de crédito excedido"
            ]
            motivo = random.choice(motivos)
            pago.rechazar(motivo)
            print(f"❌ Pago #{pago.id_pago} RECHAZADO - Motivo: {motivo}")
            return False
    
    def _actualizar_estadisticas(self, pago):
        """Actualiza estadísticas del procesador."""
        self.estadisticas['total_procesados'] += 1
        
        if pago.esta_aprobado():
            self.estadisticas['aprobados'] += 1
            self.estadisticas['monto_total'] += pago.monto
        elif pago.esta_rechazado():
            self.estadisticas['rechazados'] += 1
    
    def obtener_estado_colas(self):
        """Muestra el estado de las colas de procesamiento."""
        print("💳 ESTADO DE COLAS DE PAGO:")
        print("="*40)
        
        print(f"Cola regular: {self.cola_pagos.obtener_tamaño()} pagos")
        print(f"Cola prioritaria: {self.cola_prioritaria.obtener_tamaño()} pagos")
        print(f"Procesados: {len(self.pagos_procesados)} pagos")
        
        if not self.cola_prioritaria.esta_vacia():
            print("\nPAGOS PRIORITARIOS:")
            # Mostrar sin modificar la cola
            temp_items = []
            while not self.cola_prioritaria.esta_vacia():
                item = self.cola_prioritaria.desencolar()
                temp_items.append(item)
                print(f"  P{item[1]}: {item[0]}")
            
            # Restaurar cola
            for item in temp_items:
                self.cola_prioritaria.encolar(item[0], item[1])
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas del procesamiento.
        
        Returns:
            dict: Estadísticas completas
        """
        total = self.estadisticas['total_procesados']
        if total > 0:
            tasa_aprobacion = (self.estadisticas['aprobados'] / total) * 100
            tasa_rechazo = (self.estadisticas['rechazados'] / total) * 100
        else:
            tasa_aprobacion = 0
            tasa_rechazo = 0
        
        return {
            **self.estadisticas,
            'tasa_aprobacion': tasa_aprobacion,
            'tasa_rechazo': tasa_rechazo
        }
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del procesamiento."""
        stats = self.obtener_estadisticas()
        
        print("\n📊 ESTADÍSTICAS DE PAGOS:")
        print("="*40)
        print(f"Total procesados: {stats['total_procesados']}")
        print(f"Aprobados: {stats['aprobados']} ({stats['tasa_aprobacion']:.1f}%)")
        print(f"Rechazados: {stats['rechazados']} ({stats['tasa_rechazo']:.1f}%)")
        print(f"Monto total aprobado: ${stats['monto_total']:.2f}")
        
        # Mostrar últimos pagos procesados
        if self.pagos_procesados:
            print("\nÚLTIMOS PAGOS PROCESADOS:")
            for pago in self.pagos_procesados[-3:]:  # Últimos 3
                print(f"  {pago}")
    
    def __str__(self):
        """Representación del procesador."""
        return f"ProcesadorPagos: {self.cola_pagos.obtener_tamaño()} regular, {self.cola_prioritaria.obtener_tamaño()} prioritarios"
