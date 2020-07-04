from paypalrestsdk import Payment
import logging

logging.basicConfig(level=logging.INFO)

# Payment
# A Payment Resource of type order; intent set as 'order'
payment = Payment({
    "intent": "order",
    "payer": {
        "payment_method": "paypal"
    },
    "redirect_urls": {
        "return_url": "http://return.url",
        "cancel_url": "http://cancel.url"
    },
    "transactions": [{
        "item_list": {
            "items": [{
                "name": "item",
                "sku": "item",
                "price": "1.00",
                "currency": "USD",
                "quantity": 1
            }]
        },
        "amount": {
            "currency": "USD",
            "total": "1.00"
        },
        "description": "This is the payment description."
    }]
})

# Create Payment and return status
if payment.create():
    print("Payment[%s] created successfully" % (payment.id))
    # Redirect the user to given approval url
    for link in payment.links:
        if link.rel == "approval_url":
            approval_url = str(link.href)
            print("Redirect for approval: %s" % (approval_url))
else:
    print("Error while creating payment:")
    print(payment.error)
