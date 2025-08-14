import nodo.py

class ListaSimple:
    def __init__(self):
        self.cabeza = None

    def insertar_al_final(self, dato):
        nuevo_nodo = NodoSimple(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(actual.dato, end=" -> ")
            actual = actual.siguiente
        print("None")

#...