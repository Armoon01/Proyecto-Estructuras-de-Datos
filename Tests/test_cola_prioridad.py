import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Src', 'estructuras'))

from cola_prioridad import ColaPrioridad

def test_cola_prioridad():
    print("=== TEST COLA PRIORIDAD ===")
    
    # Crear cola de prioridad
    cola = ColaPrioridad()
    print(f"Cola de prioridad creada: {cola}")
    print(f"¿Está vacía? {cola.esta_vacia()}")
    print(f"Tamaño: {cola.obtener_tamaño()}")
    
    # Agregar elementos con prioridad
    print("\n--- Agregando elementos con prioridad ---")
    cola.enqueue("Tarea Baja", 1)
    cola.enqueue("Tarea Alta", 5)
    cola.enqueue("Tarea Media", 3)
    cola.enqueue("Tarea Crítica", 10)
    print(f"Después de agregar tareas: {cola}")
    print(f"Tamaño: {cola.obtener_tamaño()}")
    print(f"Peek (mayor prioridad): {cola.peek()}")
    
    # Quitar elementos por prioridad
    print("\n--- Quitando elementos por prioridad ---")
    while not cola.esta_vacia():
        elemento = cola.dequeue()
        print(f"Dequeue(): {elemento}")
        print(f"Cola actual: {cola}")
        if not cola.esta_vacia():
            print(f"Siguiente en peek: {cola.peek()}")
    
    # Agregar más elementos
    print("\n--- Agregando más elementos ---")
    cola.enqueue("Emergencia", 9)
    cola.enqueue("Normal", 2)
    cola.enqueue("Urgente", 7)
    print(f"Nueva cola: {cola}")
    print(f"Elementos: {cola.obtener_elementos()}")
    
    # Operaciones en cola vacía
    print("\n--- Vaciando cola ---")
    while not cola.esta_vacia():
        cola.dequeue()
    
    print(f"Dequeue en cola vacía: {cola.dequeue()}")
    print(f"Peek en cola vacía: {cola.peek()}")
    
    print("✅ Test de Cola Prioridad completado\n")

if __name__ == "__main__":
    test_cola_prioridad()
