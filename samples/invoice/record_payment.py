# Example demonstrating creating an invoice, sending it
# (which changes its status from draft to sent)
# and recording a payment on the send invoice

import paypalrestsdk
from paypalrestsdk import Invoice
import logging

logging.basicConfig(level=logging.DEBUG)
paypalrestsdk.configure({
    "mode": "<MODE>",  # sandbox or live
    "client_id": "<CLIENT_ID>",
    "client_secret": "<CLIENT_SECRET>"})

invoice = Invoice({
    "merchant_info": {
        "email": "PPX.DevNet-facilitator@gmail.com",
        "first_name": "Dennis",
        "last_name": "Doctor",
        "business_name": "Medical Professionals, LLC",
        "phone": {
            "country_code": "001",
            "national_number": "5032141716"
        },
        "address": {
            "line1": "1234 Main St.",
            "city": "Portland",
            "state": "OR",
            "postal_code": "97217",
            "country_code": "US"
        }
    },
    "billing_info": [{"email": "example@example.com"}],
    "items": [
        {
            "name": "Sutures",
            "quantity": 100,
            "unit_price": {
                "currency": "USD",
                "value": 5
            }
        }
    ],
    "note": "Medical Invoice 16 Jul, 2013 PST",
    "payment_term": {
        "term_type": "NET_45"
    },
    "shipping_info": {
        "first_name": "Sally",
        "last_name": "Patient",
        "business_name": "Not applicable",
        "phone": {
            "country_code": "001",
            "national_number": "5039871234"
        },
        "address": {
            "line1": "1234 Broad St.",
            "city": "Portland",
            "state": "OR",
            "postal_code": "97216",
            "country_code": "US"
        }
    }
})

if invoice.create():
    print("Invoice[%s] created successfully" % (invoice.id))
else:
    print(invoice.error)

if invoice.send():  # return True or False
    print("Invoice[%s] send successfully" % (invoice.id))
else:
    print(invoice.error)

payment_attr = {
    "method": "CASH",
    "date": "2014-07-10 03:30:00 PST",
    "note": "Cash received."
}

if invoice.record_payment(payment_attr):  # return True or False
    print("Payment record on Invoice[%s] successfully" % (invoice.id))
else:
    print(invoice.error)
