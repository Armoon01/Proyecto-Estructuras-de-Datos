import tkinter as tk
from tkinter import messagebox
from OrderIssue import OrderIssue
from datetime import timedelta

class InterfazOrderIssue(tk.Frame):
	def __init__(self, master, usuario_actual, orders, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.usuario_actual = usuario_actual
		self.orders = orders
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.btn_estado = tk.Button(self, text="Estado de compra", command=self.show_order_info)
		self.btn_estado.pack(pady=20)

	def show_order_info(self):
		user_orders = [order for order in self.orders if order.user_name == self.usuario_actual]
		if user_orders:
			info = ""
			for order in user_orders:
				delivery_date = order.payment_date + timedelta(days=order.delivery_days)
				info += (
					f"Usuario: {order.user_name}\n"
					f"Estado de compra: {order.order_status}\n"
					f"Fecha de pago: {order.payment_date.strftime('%Y-%m-%d')}\n"
					f"Fecha estimada de entrega: {delivery_date.strftime('%Y-%m-%d')}\n\n"
				)
			messagebox.showinfo("Estado de compra", info)
		else:
			messagebox.showinfo("Estado de compra", "No tienes compras registradas.")
