# Execute an approved PayPal payment
# Use this call to execute (complete) a PayPal payment that has been approved by the payer.
# You can optionally update transaction information by passing in one or more transactions.
# API used: /v1/payments/payment
from paypalrestsdk import Payment
import logging
logging.basicConfig(level=logging.INFO)

# ID of the payment. This ID is provided when creating payment.
payment = Payment.find("PAY-28103131SP722473WKFD7VGQ")

# PayerID is required to approve the payment.
if payment.execute({"payer_id": "DUFRQ8GWYMJXC"}):  # return True or False
    print("Payment[%s] execute successfully" % (payment.id))
else:
    print(payment.error)
