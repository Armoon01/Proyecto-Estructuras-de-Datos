import tkinter as tk

class Interfaz:
    def __init__(self):
        self.window = tk.tk() #para crear la ventana
        self.window.title("Proyecto - Estructuras de Datos") #titulo de la ventana
        self.window.geometry("400x600") #dimensiones de la ventana

        self.label = tk.label(self.window, text="Prueba, nerfeen al horno") #una etiqueta inicial
        self.label.pack(pady=20)

        self.button = tk.Button(self.window, text="Cerrar", command=self.quit()) #Aqui crea un boton para cerra la ventana
        self.button.pack()

    def ejecutar(self):
        self.window.mainloop()