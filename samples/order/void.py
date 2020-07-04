from paypalrestsdk import Order
import logging
logging.basicConfig(level=logging.INFO)

order = Order.find("O-0FJ734297A068505V")

if order.void():
    print("Void Order successfully")
else:
    print(order.error)
