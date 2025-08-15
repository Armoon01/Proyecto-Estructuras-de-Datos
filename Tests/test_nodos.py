import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Src', 'estructuras'))

from nodo import Nodo, NodoDoble

def test_nodos():
    print("=== TEST NODOS ===")
    
    # Test Nodo Simple
    print("\n--- Test Nodo Simple ---")
    nodo1 = Nodo("Dato 1")
    nodo2 = Nodo("Dato 2")
    nodo3 = Nodo("Dato 3")
    
    print(f"Nodo 1: dato={nodo1.dato}, siguiente={nodo1.siguiente}")
    
    # Conectar nodos
    nodo1.siguiente = nodo2
    nodo2.siguiente = nodo3
    
    print(f"Después de conectar:")
    print(f"Nodo 1: dato={nodo1.dato}, siguiente={nodo1.siguiente.dato if nodo1.siguiente else None}")
    print(f"Nodo 2: dato={nodo2.dato}, siguiente={nodo2.siguiente.dato if nodo2.siguiente else None}")
    print(f"Nodo 3: dato={nodo3.dato}, siguiente={nodo3.siguiente}")
    
    # Test Nodo Doble
    print("\n--- Test Nodo Doble ---")
    nodo_doble1 = NodoDoble("A")
    nodo_doble2 = NodoDoble("B")
    nodo_doble3 = NodoDoble("C")
    
    print(f"Nodo Doble 1: dato={nodo_doble1.dato}, anterior={nodo_doble1.anterior}, siguiente={nodo_doble1.siguiente}")
    
    # Conectar nodos dobles
    nodo_doble1.siguiente = nodo_doble2
    nodo_doble2.anterior = nodo_doble1
    nodo_doble2.siguiente = nodo_doble3
    nodo_doble3.anterior = nodo_doble2
    
    print(f"Después de conectar:")
    print(f"Nodo 1: dato={nodo_doble1.dato}, anterior={nodo_doble1.anterior}, siguiente={nodo_doble1.siguiente.dato if nodo_doble1.siguiente else None}")
    print(f"Nodo 2: dato={nodo_doble2.dato}, anterior={nodo_doble2.anterior.dato if nodo_doble2.anterior else None}, siguiente={nodo_doble2.siguiente.dato if nodo_doble2.siguiente else None}")
    print(f"Nodo 3: dato={nodo_doble3.dato}, anterior={nodo_doble3.anterior.dato if nodo_doble3.anterior else None}, siguiente={nodo_doble3.siguiente}")
    
    print("✅ Test de Nodos completado\n")

if __name__ == "__main__":
    test_nodos()
