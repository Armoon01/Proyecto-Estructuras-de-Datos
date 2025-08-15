import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Src', 'estructuras'))

from Lista import Lista

def test_lista():
    print("=== TEST LISTA ===")
    
    # Crear lista
    lista = Lista()
    print(f"Lista creada: {lista}")
    print(f"¿Está vacía? {lista.esta_vacia()}")
    print(f"Tamaño: {lista.obtener_tamaño()}")
    
    # Agregar elementos
    print("\n--- Agregando elementos ---")
    lista.agregar("A")
    lista.agregar("B")
    lista.agregar("C")
    print(f"Después de agregar(A, B, C): {lista}")
    print(f"Tamaño: {lista.obtener_tamaño()}")
    
    # Buscar elementos
    print("\n--- Buscando elementos ---")
    pos_b = lista.buscar("B")
    pos_z = lista.buscar("Z")
    print(f"Posición de 'B': {pos_b}")
    print(f"Posición de 'Z' (no existe): {pos_z}")
    
    # Eliminar elementos
    print("\n--- Eliminando elementos ---")
    eliminado = lista.eliminar("B")
    print(f"Eliminar 'B': {eliminado}")
    print(f"Lista después de eliminar 'B': {lista}")
    
    eliminado_inexistente = lista.eliminar("Z")
    print(f"Eliminar 'Z' (no existe): {eliminado_inexistente}")
    
    # Más operaciones
    print("\n--- Más operaciones ---")
    lista.agregar("D")
    lista.agregar("E")
    print(f"Después de agregar D, E: {lista}")
    print(f"Elementos: {lista.obtener_elementos()}")
    
    # Eliminar todos
    print("\n--- Eliminando todos ---")
    elementos = lista.obtener_elementos().copy()
    for elemento in elementos:
        lista.eliminar(elemento)
        print(f"Eliminado {elemento}, Lista: {lista}")
    
    print(f"¿Lista vacía? {lista.esta_vacia()}")
    print("✅ Test de Lista completado\n")

if __name__ == "__main__":
    test_lista()
