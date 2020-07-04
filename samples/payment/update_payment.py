from paypalrestsdk import Payment
import logging

logging.basicConfig(level=logging.INFO)

payment = Payment.find("<PAYMENT_ID>")

# e.g. Update the amount, shipping address, invoice ID, or custom data after payment creation
# You cannot update a payment after the payment executes.
# https://developer.paypal.com/docs/api/payments/#payment_update
update_payment_json = [
    {
        "op": "replace", 
        "path": "/transactions/0/amount", 
        "value": {
            "total": "4.50", 
            "currency": "USD",
            "details": {
                "subtotal": "5.00",
                "shipping_discount": "-0.50"
            }
        }
    }
];


if payment.replace(update_payment_json):
    print("Payment[%s] updated successfully"%(payment.id))
else:
    print(payment.error)
    
