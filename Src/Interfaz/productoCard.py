from customtkinter import *
from PIL import Image

class ProductoCard(CTkFrame):
    def __init__(self, master, nombre, descripcion, precio, imagen_path, descuento=None, badge=None, on_agregar=None, **kwargs):
        super().__init__(master, fg_color="#fff", corner_radius=15, **kwargs)
        self.configure(width=230, height=340)
        self.pack_propagate(0)
        try:
            img = Image.open(imagen_path)
        except Exception:
            img = Image.new('RGB', (150, 150), (220, 220, 220))
        self.imagen = CTkImage(light_image=img, dark_image=img, size=(150, 150))
        CTkLabel(self, image=self.imagen, text="").pack(pady=(15,0))
        if badge:
            badge_label = CTkLabel(self, text=badge, fg_color="#FFCC00", text_color="#C60A1D", corner_radius=5, font=("Arial Bold", 10))
            badge_label.place(x=10, y=10)
        elif descuento:
            desc_text = f"-{int(descuento*100)}%"
            badge_label = CTkLabel(self, text=desc_text, fg_color="#FFCC00", text_color="#C60A1D", corner_radius=5, font=("Arial Bold", 10))
            badge_label.place(x=10, y=10)
        CTkButton(self, text="+ Agregar", fg_color="#2063E4", hover_color="#0E3B8A", text_color="#fff", width=150, command=on_agregar).pack(pady=(10,0))
        precio_frame = CTkFrame(self, fg_color="transparent")
        precio_frame.pack(pady=(10,0))
        if descuento and precio:
            CTkLabel(precio_frame, text=f"₡{precio}", text_color="#999", font=("Arial", 14, "overstrike")).pack(side="left")
            precio_final = int(precio * (1-descuento))
            CTkLabel(precio_frame, text=f"₡{precio_final}", text_color="#222", font=("Arial Bold", 16)).pack(side="left", padx=(8,0))
        else:
            CTkLabel(precio_frame, text=f"₡{precio}", text_color="#222", font=("Arial Bold", 16)).pack(side="left")
        CTkLabel(self, text=nombre, text_color="#222", font=("Arial", 13), anchor="w", justify="left", wraplength=210).pack(fill="x", padx=10)
        CTkLabel(self, text=descripcion, text_color="#555", font=("Arial", 11), anchor="w", justify="left", wraplength=210).pack(fill="x", padx=10, pady=(0,5))