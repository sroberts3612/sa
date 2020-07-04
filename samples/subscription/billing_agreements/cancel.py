from paypalrestsdk import BillingAgreement
import logging

BILLING_AGREEMENT_ID = "I-HT38K76XPMGJ"

try:
    billing_agreement = BillingAgreement.find(BILLING_AGREEMENT_ID)
    print("Billing Agreement [%s] has state %s" %
          (billing_agreement.id, billing_agreement.state))

    cancel_note = {"note": "Canceling the agreement"}

    if billing_agreement.cancel(cancel_note):
        # Would expect status has changed to Cancelled
        billing_agreement = BillingAgreement.find(BILLING_AGREEMENT_ID)
        print("Billing Agreement [%s] has state %s" %
              (billing_agreement.id, billing_agreement.state))

    else:
        print(billing_agreement.error)

except ResourceNotFound as error:
    print("Billing Agreement Not Found")
