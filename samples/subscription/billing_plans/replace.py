from paypalrestsdk import BillingPlan, ResourceNotFound
import logging

logging.basicConfig(level=logging.INFO)

try:
    billing_plan = BillingPlan.find("P-0NJ10521L3680291SOAQIVT")
    print("Got Billing Plan Details for Billing Plan[%s]" % (billing_plan.id))

    billing_plan_update_attributes = [
        {
            "op": "replace",
            "path": "/",
            "value": {
                "state": "ACTIVE"
            }
        }
    ]

    if billing_plan.replace(billing_plan_update_attributes):
        billing_plan = BillingPlan.find("P-0NJ10521L3680291SOAQIVT")
        print("Billing Plan [%s] state changed to [%s]" %
              (billing_plan.id, billing_plan.state))
    else:
        print(billing_plan.error)

except ResourceNotFound as error:
    print("Billing Plan Not Found")
