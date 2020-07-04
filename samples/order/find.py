from paypalrestsdk import Order, ResourceNotFound
import logging
logging.basicConfig(level=logging.INFO)

try:
    order = Order.find("99M58264FG144833V")
    print("Got Order details for Order[%s]" % (order.id))

except ResourceNotFound as error:
    print("Order Not Found")
