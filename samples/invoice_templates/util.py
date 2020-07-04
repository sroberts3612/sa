from paypalrestsdk import InvoiceTemplate
import random
import string

def sample_invoice_template():
    return InvoiceTemplate({
        "name": "Hours Template_".join([random.choice(string.letters) for i in range(10)]),
        "default": True,
        "unit_of_measure": "HOURS",
        "template_data": {
            "items": [{
                    "name": "Nutri Bullet",
                    "quantity": 1,
                    "unit_price": {
                        "currency": "USD",
                        "value": "50.00"
                    }
                }
            ],
            "merchant_info": {
                "email": "stevendcoffey-facilitator@gmail.com"
            },
            "tax_calculated_after_discount": False,
            "tax_inclusive": False,
            "note": "Thank you for your business.",
            "logo_url": "https://pics.paypal.com/v1/images/redDot.jpeg"
        },
        "settings": [
            {
                "field_name": "items.date",
                "display_preference": {
                    "hidden": True
                }
            },
            {
                "field_name": "custom",
                "display_preference": {
                    "hidden": True
                }
            }
        ]
    })
