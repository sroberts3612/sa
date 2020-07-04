# SaleRefund Sample
# This sample code demonstrate how you can
# process a refund on a sale transaction created
# using the Payments API.
# API used: /v1/payments/sale/{sale-id}/refund
from paypalrestsdk import Sale
import logging
logging.basicConfig(level=logging.INFO)

sale = Sale.find("7DY409201T7922549")

# Make Refund API call
# Set amount only if the refund is partial
refund = sale.refund({
    "amount": {
        "total": "0.01",
        "currency": "USD"}})

# Check refund status
if refund.success():
    print("Refund[%s] Success" % (refund.id))
else:
    print("Unable to Refund")
    print(refund.error)
