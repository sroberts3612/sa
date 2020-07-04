from paypalrestsdk import Order
import logging
logging.basicConfig(level=logging.INFO)

order = Order.find("<ORDER_ID>")

response = order.authorize({
    "amount": {
        "currency": "USD",
        "total": "0.08"
    }
})

if order.success():
    print("Authorized[%s] successfully" % (order.id))
else:
    print(order.error)
