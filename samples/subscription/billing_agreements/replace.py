from paypalrestsdk import BillingAgreement
import logging

BILLING_AGREEMENT_ID = "I-HT38K76XPMGJ"

try:
    billing_agreement = BillingAgreement.find(BILLING_AGREEMENT_ID)
    print("Got Billing Agreement Details for Billing Agreement[%s]"
          % (billing_agreement.id))

    billing_agreement_update_attributes = [
        {
            "op": "replace",
            "path": "/",
            "value": {
                "description": "New Description",
                "name": "New Name",
                "shipping_address": {
                    "line1": "StayBr111idge Suites",
                    "line2": "Cro12ok Street",
                    "city": "San Jose",
                    "state": "CA",
                    "postal_code": "95112",
                    "country_code": "US"
                }
            }
        }
    ]

    if billing_agreement.replace(billing_agreement_update_attributes):
        print("Billing Agreement [%s] name changed to [%s]"
              % (billing_agreement.id, billing_agreement.name))
        print("Billing Agreement [%s] description changed to [%s]"
              % (billing_agreement.id, billing_agreement.description))
    else:
        print(billing_agreement.error)

except ResourceNotFound as error:
    print("Billing Agreement Not Found")
