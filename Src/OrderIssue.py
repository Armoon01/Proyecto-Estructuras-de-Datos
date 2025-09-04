from datetime import datetime, timedelta

class OrderIssue:
    def __init__(self, user_name, order_status, payment_date):
        self.user_name = user_name
        self.order_status = order_status
        self.payment_date = datetime.strptime(payment_date, '%Y-%m-%d')
        self.delivery_days = 30

    def show_order_status(self):
        delivery_date = self.payment_date + timedelta(days=self.delivery_days)
        print(f"Usuario: {self.user_name}")
        print(f"Estado de compra: {self.order_status}")
        print(f"Fecha de pago: {self.payment_date.strftime('%Y-%m-%d')}")
        print(f"Fecha estimada de entrega: {delivery_date.strftime('%Y-%m-%d')}")