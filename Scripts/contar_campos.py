"""
Script para contar campos únicos en archivos CSV del proyecto
Verificar cumplimiento del requisito de 30+ campos diferentes
"""

import os
import csv

def contar_campos_csv():
    """Contar todos los campos únicos en archivos CSV"""
    directorio_data = r"c:\Users\lunai\OneDrive\Escritorio\Estructura de datos Proyecto\Proyecto-Estructuras-de-Datos\Data"
    
    campos_unicos = set()
    archivos_analizados = []
    
    # Leer todos los archivos CSV
    for archivo in os.listdir(directorio_data):
        if archivo.endswith('.csv'):
            ruta_archivo = os.path.join(directorio_data, archivo)
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    headers = next(reader)  # Primera línea son los headers
                    campos_unicos.update(headers)
                    archivos_analizados.append(archivo)
                    print(f"✅ {archivo}: {len(headers)} campos")
            except Exception as e:
                print(f"❌ Error leyendo {archivo}: {e}")
    
    print(f"\n📊 RESUMEN:")
    print(f"Archivos analizados: {len(archivos_analizados)}")
    print(f"Total campos únicos: {len(campos_unicos)}")
    print(f"Requisito 30+ campos: {'✅ CUMPLIDO' if len(campos_unicos) >= 30 else '❌ FALTANTE'}")
    
    print(f"\n📋 LISTA DE CAMPOS ÚNICOS:")
    for i, campo in enumerate(sorted(campos_unicos), 1):
        print(f"{i:2d}. {campo}")
    
    return len(campos_unicos)

if __name__ == "__main__":
    contar_campos_csv()
