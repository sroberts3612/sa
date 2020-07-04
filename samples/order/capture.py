from paypalrestsdk import Order
import logging
logging.basicConfig(level=logging.INFO)

order = Order.find("<ORDER_ID>")
capture = order.capture({
    "amount": {
        "currency": "USD",
        "total": "4.54"},
    "is_final_capture": True})

if capture.success():
    print("Capture[%s] successfully" % (capture.id))
else:
    print(capture.error)
