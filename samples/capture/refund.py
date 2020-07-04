from paypalrestsdk import Capture
import logging
logging.basicConfig(level=logging.INFO)

capture = Capture.find("8F148933LY9388354")
refund = capture.refund({
    "amount": {
        "currency": "USD",
        "total": "110.54"}})

if refund.success():
    print("Refund[%s] Success" % (refund.id))
else:
    print("Unable to Refund")
    print(refund.error)
