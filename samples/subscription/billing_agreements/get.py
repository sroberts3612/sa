from paypalrestsdk import BillingAgreement, ResourceNotFound
import logging
logging.basicConfig(level=logging.INFO)

try:
    billing_agreement = BillingAgreement.find("I-HT38K76XPMGJ")
    print("Got Billing Agreement Details for Billing Agreement[%s]" % (
        billing_agreement.id))

except ResourceNotFound as error:
    print("Billing Agreement Not Found")
