# Create a PayPal Payment with custom PayPal checkout experience
# For a simple payment example, refer to samples/payment/create_with_paypal.py
#
# Refer to https://developer.paypal.com/docs/integration/direct/rest-experience-overview/
# to see the available options

from paypalrestsdk import WebProfile, Payment
import logging
import random
import string

logging.basicConfig(level=logging.INFO)

# Name needs to be unique so just generating a random one
wpn = ''.join(random.choice(string.ascii_uppercase) for i in range(12))

web_profile = WebProfile({
    "name": wpn,
    "presentation": {
        "brand_name": "YeowZa Paypal",
        "logo_image": "http://s3-ec.buzzfed.com/static/2014-07/18/8/enhanced/webdr02/anigif_enhanced-buzz-21087-1405685585-12.gif",
        "locale_code": "US"
    },
    "input_fields": {
        "allow_note": True,
        "no_shipping": 1,
        "address_override": 1
    },
    "flow_config": {
        "landing_page_type": "billing",
        "bank_txn_pending_url": "http://www.yeowza.com"
    }
})

if web_profile.create():
    print("Web Profile[%s] created successfully" % (web_profile.id))
else:
    print(web_profile.error)

payment = Payment({
    "intent": "sale",
    "experience_profile_id": web_profile.id,
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
