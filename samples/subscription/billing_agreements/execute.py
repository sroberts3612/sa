# Execute an approved PayPal Billing Agreement
# Use this call to execute (complete) a PayPal BillingAgreement that has
# been approved by the payer.
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

# After creating the agreement, redirect user to the url provided in links array
# entry designated as "approval_url"
if billing_agreement.create():
    print("Billing Agreement created successfully")
    for link in billing_agreement.links:
        if link.rel == "approval_url":
            approval_url = link.href
            print(
                "For approving billing agreement, redirect user to\n [%s]" % (approval_url))
else:
    print(billing_agreement.error)

# After user approves the agreement, call execute with the payment token appended to
# the redirect url to execute the billing agreement.
# https://github.paypal.com/pages/lkutch/paypal-developer-docs/api/#execute-an-agreement
billing_agreement_response = BillingAgreement.execute(payment_token)
print("BillingAgreement[%s] executed successfully" %
      (billing_agreement_response.id))
