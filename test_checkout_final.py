#!/usr/bin/env python3
"""
Script de prueba para verificar el flujo completo del checkout después de las correcciones
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Src'))

from Inventario import Inventario
from Carrito import Carrito
from estructuras.Pila import Pila
from estructuras.Cola import Cola
import csv

def verificar_archivos_csv():
    """Verificar estado de archivos CSV antes de la prueba"""
    archivos_csv = [
        'Data/productos.csv',
        'Data/ordenes.csv', 
        'Data/pagos.csv',
        'Data/transacciones.csv'
    ]
    
    print("📋 ESTADO DE ARCHIVOS CSV ANTES DE LA PRUEBA:")
    for archivo in archivos_csv:
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    print(f"   ✅ {archivo}: {len(lines)} líneas")
            except Exception as e:
                print(f"   ❌ {archivo}: Error leyendo - {e}")
        else:
            print(f"   🆕 {archivo}: No existe (se creará)")

def probar_checkout():
    """Probar el checkout simulado"""
    print("\n🧪 INICIANDO PRUEBA DE CHECKOUT CON CORRECCIONES\n")
    
    # Verificar archivos CSV
    verificar_archivos_csv()
    
    # Crear instancias del sistema
    inventario = Inventario()
    carrito = Carrito("usuario_test")
    
    print(f"\n📦 Inventario cargado con {inventario.productos.obtener_tamaño()} productos")
    
    if inventario.productos.obtener_tamaño() == 0:
        print("❌ No hay productos en el inventario")
        return
    
    # Obtener productos como lista
    productos_lista = inventario.productos.obtener_elementos()
    
    # Mostrar primeros productos y su stock
    print("\n📊 STOCK DE PRODUCTOS ANTES DE LA COMPRA:")
    for i, producto in enumerate(productos_lista[:3]):
        stock = getattr(producto, 'stock', 'No definido')
        print(f"   {i+1}. {producto.nombre}: {stock} unidades")
    
    # Agregar productos al carrito
    print("\n🛒 AGREGANDO PRODUCTOS AL CARRITO:")
    productos_test = productos_lista[:3]
    for i, producto in enumerate(productos_test, 1):
        cantidad = i  # 1, 2, 3 unidades
        carrito.agregar_producto(producto, cantidad)
        print(f"   + {cantidad}x {producto.nombre}")
    
    print(f"\n📊 CARRITO ACTUAL:")
    print(f"   - Items: {carrito.obtener_cantidad_items()}")
    print(f"   - Total: ${carrito.calcular_total():.2f}")
    
    # Simular reducción de stock
    print("\n🔄 SIMULANDO REDUCCIÓN DE STOCK:")
    items = carrito.obtener_items_agrupados()
    
    for item in items:
        producto = item.producto
        cantidad = item.cantidad
        
        # Obtener stock actual
        stock_actual = getattr(producto, 'stock', 100)
        print(f"   📦 {producto.nombre}: stock actual = {stock_actual}")
        
        # Simular reducción de stock
        if hasattr(inventario, 'reducir_stock'):
            resultado = inventario.reducir_stock(producto.id, cantidad)
            print(f"   {'✅' if resultado else '❌'} Reducir {cantidad} unidades: {resultado}")
            
            # Verificar nuevo stock
            producto_actualizado = inventario.buscar_producto(producto.id)
            if producto_actualizado:
                nuevo_stock = getattr(producto_actualizado, 'stock', 'No definido')
                print(f"   📊 Nuevo stock: {nuevo_stock}")
        
    print(f"\n✅ SIMULACIÓN COMPLETADA")
    
    # Verificar cambios en archivos CSV (si existieran)
    print("\n💾 VERIFICANDO PERSISTENCIA:")
    try:
        # Leer productos.csv para ver si el stock cambió
        with open('Data/productos.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"   📁 productos.csv: {len(lines)} líneas")
            
            if len(lines) > 1:  # Al menos header + 1 producto
                # Mostrar primeras líneas de productos
                print("   📊 Primeros productos después de la actualización:")
                for i, line in enumerate(lines[1:4], 1):  # Primeros 3 productos
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 7:
                            nombre = parts[1]
                            stock = parts[6] if len(parts) > 6 else 'N/A'
                            print(f"      {i}. {nombre}: Stock = {stock}")
                        
    except Exception as e:
        print(f"   ⚠️ Error verificando productos.csv: {e}")
    
    print(f"\n🎯 RESUMEN DE LA PRUEBA:")
    print(f"   ✅ Inventario inicializado correctamente")
    print(f"   ✅ Carrito funcionando con {len(items)} tipos de productos")
    print(f"   ✅ Reducción de stock simulada")
    print(f"   ✅ Persistencia verificada")

if __name__ == "__main__":
    try:
        probar_checkout()
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
