from paypalrestsdk import BillingAgreement
import logging

BILLING_AGREEMENT_ID = "I-HT38K76XPMGJ"

try:
    billing_agreement = BillingAgreement.find(BILLING_AGREEMENT_ID)
    print("Billing Agreement [%s] has state %s" %
          (billing_agreement.id, billing_agreement.state))

    suspend_note = {
        "note": "Suspending the agreement"
    }

    if billing_agreement.suspend(suspend_note):
        # Would expect state has changed to Suspended
        billing_agreement = BillingAgreement.find(BILLING_AGREEMENT_ID)
        print("Billing Agreement [%s] has state %s" %
              (billing_agreement.id, billing_agreement.state))

        reactivate_note = {
            "note": "Reactivating the agreement"
        }

        if billing_agreement.reactivate(reactivate_note):
            # Would expect state has changed to Active
            billing_agreement = BillingAgreement.find(BILLING_AGREEMENT_ID)
            print("Billing Agreement [%s] has state %s" % (
                billing_agreement.id, billing_agreement.state))

        else:
            print(billing_agreement.error)

    else:
        print(billing_agreement.error)

except ResourceNotFound as error:
    print("Billing Agreement Not Found")
