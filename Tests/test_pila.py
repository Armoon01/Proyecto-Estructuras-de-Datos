import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Src', 'estructuras'))

from Pila import Pila

def test_pila():
    print("=== TEST PILA ===")
    
    # Crear pila
    pila = Pila()
    print(f"Pila creada: {pila}")
    print(f"¿Está vacía? {pila.esta_vacia()}")
    print(f"Tamaño: {pila.obtener_tamaño()}")
    
    # Agregar elementos
    print("\n--- Agregando elementos ---")
    pila.push(10)
    pila.push(20)
    pila.push(30)
    print(f"Después de push(10, 20, 30): {pila}")
    print(f"Tamaño: {pila.obtener_tamaño()}")
    print(f"Peek (cima): {pila.peek()}")
    
    # Quitar elementos
    print("\n--- Quitando elementos ---")
    elemento = pila.pop()
    print(f"Pop(): {elemento}")
    print(f"Pila después del pop: {pila}")
    print(f"Nuevo peek: {pila.peek()}")
    
    # Más operaciones
    print("\n--- Más operaciones ---")
    pila.push(40)
    print(f"Después de push(40): {pila}")
    print(f"Elementos: {pila.obtener_elementos()}")
    
    # Vaciar pila
    print("\n--- Vaciando pila ---")
    while not pila.esta_vacia():
        elemento = pila.pop()
        print(f"Pop(): {elemento}, Pila: {pila}")
    
    # Intentar pop en pila vacía
    print(f"Pop en pila vacía: {pila.pop()}")
    print(f"Peek en pila vacía: {pila.peek()}")
    
    print("✅ Test de Pila completado\n")

if __name__ == "__main__":
    test_pila()
