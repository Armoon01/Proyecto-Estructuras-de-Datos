import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Src', 'estructuras'))

from Cola import Cola

def test_cola():
    print("=== TEST COLA ===")
    
    # Crear cola
    cola = Cola()
    print(f"Cola creada: {cola}")
    print(f"¿Está vacía? {cola.esta_vacia()}")
    print(f"Tamaño: {cola.obtener_tamaño()}")
    
    # Agregar elementos
    print("\n--- Agregando elementos ---")
    cola.enqueue("Primero")
    cola.enqueue("Segundo")
    cola.enqueue("Tercero")
    print(f"Después de enqueue(Primero, Segundo, Tercero): {cola}")
    print(f"Tamaño: {cola.obtener_tamaño()}")
    print(f"Front (frente): {cola.front()}")
    
    # Quitar elementos
    print("\n--- Quitando elementos ---")
    elemento = cola.dequeue()
    print(f"Dequeue(): {elemento}")
    print(f"Cola después del dequeue: {cola}")
    print(f"Nuevo front: {cola.front()}")
    
    # Más operaciones
    print("\n--- Más operaciones ---")
    cola.enqueue("Cuarto")
    print(f"Después de enqueue(Cuarto): {cola}")
    print(f"Elementos: {cola.obtener_elementos()}")
    
    # Vaciar cola
    print("\n--- Vaciando cola ---")
    while not cola.esta_vacia():
        elemento = cola.dequeue()
        print(f"Dequeue(): {elemento}, Cola: {cola}")
    
    # Intentar dequeue en cola vacía
    print(f"Dequeue en cola vacía: {cola.dequeue()}")
    print(f"Front en cola vacía: {cola.front()}")
    
    print("✅ Test de Cola completado\n")

if __name__ == "__main__":
    test_cola()
