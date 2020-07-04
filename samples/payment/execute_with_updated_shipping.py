from paypalrestsdk import Payment
import logging

logging.basicConfig(level=logging.INFO)

payment = Payment.find("<PAYMENT_ID>")

# e.g. Update shipping amount in the transactions array after payment creation
# and calling payment execute
# https://developer.paypal.com/webapps/developer/docs/api/#transaction-object
execute_payment_json = {
    "payer_id": "HCXTE7DLHVTDN",
    "transactions": [{
        "amount": {
            "total": "35.07",
            "currency": "USD",
            "details": {
                "subtotal": "30.00",
                "tax": "0.07",
                "shipping": "2.00",
                "handling_fee": "1.00",
                "shipping_discount": "1.00",
                "insurance": "1.00"
            }
        }
    }]
};

if payment.execute(execute_payment_json):  # return True or False
  print("Payment[%s] execute successfully"%(payment.id))
else:
  print(payment.error)
