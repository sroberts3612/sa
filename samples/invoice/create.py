from paypalrestsdk import Invoice
import logging
import json

logging.basicConfig(level=logging.INFO)

invoice = Invoice({
    "merchant_info": {
        "email": "jaypatel512-facilitator@hotmail.com",  # You must change this to your sandbox email account
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
    },
    "shipping_cost": {
        "amount": {
            "currency": "USD",
            "value": 10
        }
    }
})

if invoice.create():
    print(json.dumps(invoice.to_dict(), sort_keys=False, indent=4))
else:
    print(invoice.error)
