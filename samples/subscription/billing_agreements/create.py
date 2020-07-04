from paypalrestsdk import BillingAgreement
import logging

logging.basicConfig(level=logging.INFO)

billing_agreement = BillingAgreement({
    "name": "Fast Speed Agreement",
    "description": "Agreement for Fast Speed Plan",
    "start_date": "2015-02-19T00:37:04Z",
    "plan": {
        "id": "P-0NJ10521L3680291SOAQIVTQ"
    },
    "payer": {
        "payment_method": "paypal"
    },
    "shipping_address": {
        "line1": "StayBr111idge Suites",
        "line2": "Cro12ok Street",
        "city": "San Jose",
        "state": "CA",
        "postal_code": "95112",
        "country_code": "US"
    }
})

if billing_agreement.create():
    print("Billing Agreement created successfully")
else:
    print(billing_agreement.error)
