import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Src', 'estructuras'))

# Importar todos los tests
from test_pila import test_pila
from test_cola import test_cola
from test_lista import test_lista
from test_lista_doble import test_lista_doble
from test_cola_prioridad import test_cola_prioridad
from test_nodos import test_nodos

def ejecutar_todos_los_tests():
    print("🧪 EJECUTANDO TODOS LOS TESTS DE ESTRUCTURAS DE DATOS")
    print("=" * 60)
    
    try:
        # Ejecutar cada test
        test_pila()
        test_cola()
        test_lista()
        test_lista_doble()
        test_cola_prioridad()
        test_nodos()
        
        print("=" * 60)
        print("🎉 TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        print("✅ Pila - OK")
        print("✅ Cola - OK")
        print("✅ Lista - OK")
        print("✅ Lista Doble - OK")
        print("✅ Cola Prioridad - OK")
        print("✅ Nodos - OK")
        
    except Exception as e:
        print(f"❌ Error durante los tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ejecutar_todos_los_tests()
