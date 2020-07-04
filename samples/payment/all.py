# GetPaymentList Sample
# This sample code demonstrate how you can
# retrieve a list of all Payment resources
# you've created using the Payments API.
# Note various query parameters that you can
# use to filter, and paginate through the
# payments list.
# API used: GET /v1/payments/payments
from paypalrestsdk import Payment
import logging
logging.basicConfig(level=logging.INFO)

# Retrieve
# Retrieve the PaymentHistory  by calling the
# `all` method
# on the Payment class
# Refer the API documentation
# for valid values for keys
# Supported paramters are :count, :next_id
payment_history = Payment.all({"count": 2})

# List Payments
print("List Payment:")
for payment in payment_history.payments:
    print("  -> Payment[%s]" % (payment.id))
