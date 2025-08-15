import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Src', 'estructuras'))

from ListaDoble import ListaDoble

def test_lista_doble():
    print("=== TEST LISTA DOBLE ===")
    
    # Crear lista doble
    lista = ListaDoble()
    print(f"Lista doble creada: {lista}")
    print(f"¿Está vacía? {lista.esta_vacia()}")
    print(f"Tamaño: {lista.obtener_tamaño()}")
    
    # Agregar al inicio
    print("\n--- Agregando al inicio ---")
    lista.agregar_inicio("B")
    lista.agregar_inicio("A")
    print(f"Después de agregar_inicio(B, A): {lista}")
    
    # Agregar al final
    print("\n--- Agregando al final ---")
    lista.agregar_final("C")
    lista.agregar_final("D")
    print(f"Después de agregar_final(C, D): {lista}")
    print(f"Tamaño: {lista.obtener_tamaño()}")
    
    # Buscar elementos
    print("\n--- Buscando elementos ---")
    pos_a = lista.buscar("A")
    pos_d = lista.buscar("D")
    pos_z = lista.buscar("Z")
    print(f"Posición de 'A': {pos_a}")
    print(f"Posición de 'D': {pos_d}")
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
    lista.agregar_inicio("X")
    lista.agregar_final("Y")
    print(f"Después de agregar X al inicio e Y al final: {lista}")
    print(f"Elementos: {lista.obtener_elementos()}")
    
    # Eliminar todos
    print("\n--- Eliminando todos ---")
    elementos = lista.obtener_elementos().copy()
    for elemento in elementos:
        lista.eliminar(elemento)
        print(f"Eliminado {elemento}, Lista: {lista}")
    
    print(f"¿Lista vacía? {lista.esta_vacia()}")
    print("✅ Test de Lista Doble completado\n")

if __name__ == "__main__":
    test_lista_doble()
